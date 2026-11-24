"""Common agent-visible browser smoke check for the account workload."""

import argparse
import subprocess
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def check(browser, kit, base, email, password):
    assert urlsplit(base).hostname in ("localhost", "127.0.0.1")
    smart = kit == "smartkit"
    sign_in = base + ("/auth/sign-in" if smart else "/sign-in")
    sign_up = base + ("/auth/sign-up" if smart else "/sign-up")
    session_path = "/api/auth/get-session" if smart else "/api/user"
    with browser.new_context() as ctx:
        blocked = ctx.request.get(base + "/dashboard")
        assert blocked.ok and "/sign-in" in blocked.url
        assert ctx.request.get(sign_up).ok
        page = ctx.new_page()
        page.goto(sign_in, wait_until="networkidle")
        page.locator("#email").fill(email)
        page.locator("#password").fill(password)
        endpoint = base + ("/api/auth/sign-in/email" if smart else "/sign-in")
        with page.expect_response(lambda r: r.url == endpoint and r.request.method == "POST") as result:
            page.get_by_role("button", name="Sign in", exact=False).click()
        assert result.value.status < 500
        response = ctx.request.get(base + session_path)
        assert response.ok
        user = (response.json() or {}).get("user") if smart else response.json()
        assert (user or {}).get("email") == email


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kit", choices=["smartkit", "nextjs-saas-starter"])
    parser.add_argument("base")
    parser.add_argument("--fixture-email", default="baseline-new12@example.test")
    parser.add_argument("--fixture-password", default="Probe!xxxxxx")
    args = parser.parse_args()
    subprocess.run(["node", "node_modules/typescript/bin/tsc", "--noEmit", "--incremental", "false"], check=True)
    with sync_playwright() as p, p.chromium.launch() as browser:
        check(browser, args.kit, args.base, args.fixture_email, args.fixture_password)
    print("Common account smoke check passed")


if __name__ == "__main__":
    main()
