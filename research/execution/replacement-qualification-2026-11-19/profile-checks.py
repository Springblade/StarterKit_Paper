"""Shared browser checks for write-time profile display-name normalization."""

from difflib import unified_diff
from hashlib import sha256
import subprocess

from playwright.sync_api import expect

NEW_NAME = "  Mai  Linh  "
NORMALIZED = "Mai  Linh"
LEGACY_NAMES = {"visible": "  Hoa   Nguyen  ", "heldout": "  Minh Le  "}


def replay(root, target, replacement, archive):
    """Capture a candidate diff outside the checkout and apply it to the checked baseline."""
    name = target.relative_to(root).as_posix()
    baseline = target.read_bytes().replace(b"\r\n", b"\n")
    replacement = replacement.replace(b"\r\n", b"\n")
    patch = "".join(unified_diff(baseline.decode("utf-8").splitlines(keepends=True),
                                 replacement.decode("utf-8").splitlines(keepends=True),
                                 fromfile=f"a/{name}", tofile=f"b/{name}"))
    assert patch
    archive.write_bytes(patch.encode("utf-8"))
    target.write_bytes(baseline)
    subprocess.run(["git", "apply", "--check", str(archive)], cwd=root, check=True)
    subprocess.run(["git", "apply", str(archive)], cwd=root, check=True)
    assert target.read_bytes().replace(b"\r\n", b"\n") == replacement
    return sha256(archive.read_bytes()).hexdigest()


def settings(page, base, makerkit):
    if makerkit:
        page.goto(base + "/home/settings", wait_until="networkidle", timeout=60000)
        form = page.get_by_test_id("update-account-name-form")
        return form.locator("input[name=displayName]"), form.get_by_role("button")
    page.goto(base + "/dashboard/general", wait_until="networkidle", timeout=60000)
    expect(page.locator("input[name=email]:visible")).not_to_have_value("")
    return page.locator("input[name=name]:visible"), page.get_by_role("button", name="Save Changes")


def save_name(page, base, makerkit, name):
    field, send = settings(page, base, makerkit)
    field.fill(name)
    expect(field).to_have_value(name)
    if makerkit:
        with page.expect_response(lambda resp: "/rest/v1/accounts" in resp.url and resp.request.method == "PATCH") as result:
            send.click()
        assert result.value.ok, result.value.status
    else:
        send.click()
        expect(page.get_by_text("Account updated successfully.", exact=True)).to_be_visible()


def displayed(page, base, makerkit):
    field, _ = settings(page, base, makerkit)
    expect(field).not_to_have_value("")
    return field.input_value()


def checks(browser, base, makerkit, login, read_stored, accounts, kind):
    with browser.new_context() as context:
        page = context.new_page()
        login(page, accounts["edit"])
        save_name(page, base, makerkit, NEW_NAME)
        stored = read_stored(accounts["edit"])
        expected = NEW_NAME if kind == "baseline" else NORMALIZED
        assert stored == expected
        assert displayed(page, base, makerkit) == stored

    row = {"stored_normalized": stored == NORMALIZED}
    for fixture, original in LEGACY_NAMES.items():
        with browser.new_context() as context:
            page = context.new_page()
            login(page, accounts[fixture])
            field = displayed(page, base, makerkit)
            assert read_stored(accounts[fixture]) == original
            row[fixture + "_legacy_name_preserved"] = field == original
            assert field == (original.strip() if kind in ("regression", "fault") else original)
    return row
