"""Runnable public behavior check for the selected task on an isolated study app."""

import argparse
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def check(browser, kit, task, base, email, password):
    smart = kit == "smartkit"
    assert urlsplit(base).hostname in ("localhost", "127.0.0.1")
    prefix = "/auth" if smart else ""
    session_path = "/api/auth/get-session" if smart else "/api/user"
    with browser.new_context() as ctx:
        page = ctx.new_page()
        sign_in = base + prefix + "/sign-in"
        page.goto(sign_in, wait_until="networkidle")
        if task == "visibility":
            return page.locator("#password").get_attribute("type") == "password"
        page.locator("#email").fill(email)
        page.locator("#password").fill(password)
        post = base + ("/api/auth/sign-in/email" if smart else "/sign-in")
        with page.expect_response(lambda r: r.url == post and r.request.method == "POST") as signin:
            page.get_by_role("button", name="Sign in", exact=False).click()
        assert signin.value.status < 500

        def session_email():
            response = ctx.request.get(base + session_path)
            assert response.ok
            body = response.json()
            user = (body or {}).get("user") if smart else body
            return (user or {}).get("email")

        authenticated = session_email() == email
        if task == "registration":
            return authenticated
        assert authenticated, "Sign-out fixture must be signed in at entry"
        page.goto(base + "/dashboard", wait_until="networkidle")
        if not smart:
            page.locator('header button[aria-haspopup="menu"]').click()
        page.on("dialog", lambda dialog: dialog.accept())
        target = (page.get_by_role("button", name="Sign out", exact=True) if smart
                  else page.locator('button[type="submit"]').filter(has_text="Sign out"))
        target.click()
        page.wait_for_url(base + (prefix + "/sign-in" if smart else "/"))
        return session_email() is None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kit", choices=["smartkit", "nextjs-saas-starter"])
    parser.add_argument("task", choices=["registration", "signout", "visibility"])
    parser.add_argument("base")
    parser.add_argument("--fixture-email", default="legacy10@example.test")
    parser.add_argument("--fixture-password", default="Probe!xxxx")
    args = parser.parse_args()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        passed = check(browser, args.kit, args.task, args.base, args.fixture_email, args.fixture_password)
        browser.close()
    print("Specified existing behavior passed" if passed else "Specified existing behavior failed")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
