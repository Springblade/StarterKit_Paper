"""Check one existing behavior with synthetic fixtures on the local runtime."""

import argparse
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

from study_basic import KITS, sign_in


def check(browser, kit, task, base, email, password, saved_name=None):
    signin, _, protected = KITS[kit]
    makerkit = kit == "makerkit-lite"
    assert urlsplit(base).hostname in ("localhost", "127.0.0.1")
    with browser.new_context() as context:
        page = context.new_page()
        if task == "visibility":
            page.goto(base + signin, wait_until="networkidle")
            return page.locator("input[name=password]").get_attribute("type") == "password"
        sign_in(page, kit, base, email, password)
        if task == "profile":
            assert saved_name is not None
            settings = "/home/settings" if makerkit else "/dashboard/general"
            field = "displayName" if makerkit else "name"
            page.goto(base + settings, wait_until="networkidle")
            return page.locator(f"input[name={field}]:visible").input_value() == saved_name
        if makerkit:
            page.add_style_tag(content="nextjs-portal { display: none !important; }")
            page.locator('[data-test="account-dropdown-trigger"]').click()
            action = page.locator('[data-test="account-dropdown-sign-out"]')
            destination = "/"
        else:
            page.locator('header button[aria-haspopup="menu"]').click()
            action = page.get_by_role("button", name="Sign out", exact=True)
            destination = "/"
        page.on("dialog", lambda dialog: dialog.accept())
        action.click()
        page.wait_for_url(base + destination)
        response = context.request.get(base + protected)
        return response.ok and urlsplit(response.url).path == signin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kit", choices=KITS)
    parser.add_argument("task", choices=("profile", "signout", "visibility"))
    parser.add_argument("base")
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument("--saved-name")
    args = parser.parse_args()
    with sync_playwright() as p, p.chromium.launch() as browser:
        passed = check(browser, args.kit, args.task, args.base, args.email, args.password, args.saved_name)
    print("Specified existing behavior passed." if passed else "Specified existing behavior failed.")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
