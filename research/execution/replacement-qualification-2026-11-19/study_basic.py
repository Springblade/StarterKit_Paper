"""Run the shared account smoke checks on an isolated study runtime."""

import argparse
import shutil
import subprocess
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

KITS = {
    "nextjs-saas-starter": ("/sign-in", "/sign-up", "/dashboard"),
    "makerkit-lite": ("/auth/sign-in", "/auth/sign-up", "/home"),
}


def sign_in(page, kit, base, email, password):
    signin, _, protected = KITS[kit]
    page.goto(base + signin, wait_until="networkidle")
    page.locator("input[name=email]").fill(email)
    page.locator("input[name=password]").fill(password)
    page.locator("form button[type=submit]").click()
    page.wait_for_url(base + protected)


def check(browser, kit, base, email, password):
    assert urlsplit(base).hostname in ("localhost", "127.0.0.1")
    signin, signup, protected = KITS[kit]
    with browser.new_context() as context:
        assert context.request.get(base + signup).ok
        response = context.request.get(base + protected)
        assert response.ok and urlsplit(response.url).path == signin
        sign_in(context.new_page(), kit, base, email, password)
        response = context.request.get(base + protected)
        assert response.ok and urlsplit(response.url).path == protected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kit", choices=KITS)
    parser.add_argument("base")
    parser.add_argument("email")
    parser.add_argument("password")
    args = parser.parse_args()
    if args.kit == "makerkit-lite":
        pnpm = shutil.which("pnpm.cmd") or shutil.which("pnpm")
        assert pnpm
        command = [pnpm, "--filter", "web", "typecheck"]
    else:
        command = ["node", "node_modules/typescript/bin/tsc", "--noEmit", "--incremental", "false"]
    subprocess.run(command, check=True)
    with sync_playwright() as p, p.chromium.launch() as browser:
        check(browser, args.kit, args.base, args.email, args.password)
    print("Common account checks passed.")


if __name__ == "__main__":
    main()
