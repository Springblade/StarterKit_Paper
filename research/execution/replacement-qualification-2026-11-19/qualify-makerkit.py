"""Browser qualification for the Makerkit Lite account workload on local Supabase."""

from contextlib import contextmanager
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen
from urllib.parse import urlencode, urlparse
from uuid import uuid4

from playwright.sync_api import expect, sync_playwright
import study_basic
import study_preservation

BASE = "http://localhost:3000"
MAIL = "http://127.0.0.1:54324"
REVISION = "9ff430df9c58516add0136bd01ed800ce551675e"
AUTH = "packages/features/auth/src"
SIGN_OUT = "apps/web/components/personal-account-dropdown-container.tsx"
SIGN_IN = f"{AUTH}/components/password-sign-in-form.tsx"
SIGN_UP = f"{AUTH}/components/password-sign-up-form.tsx"
ACCOUNTS = "packages/features/accounts/src"
PROFILE_FORM = f"{ACCOUNTS}/components/update-account-details-form.tsx"
PROFILE_HOOK = f"{ACCOUNTS}/hooks/use-update-account.ts"
SIGN_OUT_MENU = f"{ACCOUNTS}/components/personal-account-dropdown.tsx"
CONTAINER = "paper-makerkit-node"
DATABASE = "supabase_db_next-supabase-saas-kit-turbo-lite"
PROFILE = runpy.run_path(str(Path(__file__).with_name("profile-checks.py")))
DEPLOYED = {}
MOVES = {
    SIGN_OUT: "apps/web/app/features/auth/personal-account-dropdown-container.tsx",
    SIGN_IN: f"{AUTH}/account/password-sign-in-form.tsx",
    SIGN_UP: f"{AUTH}/account/password-sign-up-form.tsx",
    f"{AUTH}/schemas/password-sign-up.schema.ts": f"{AUTH}/account/password-sign-up.schema.ts",
    PROFILE_FORM: f"{ACCOUNTS}/profile/update-account-details-form.tsx",
}
IMPORTS = {
    "apps/web/app/home/_components/home-menu-navigation.tsx": ("~/components/personal-account-dropdown-container", "~/features/auth/personal-account-dropdown-container"),
    "apps/web/app/home/_components/home-sidebar.tsx": ("~/components/personal-account-dropdown-container", "~/features/auth/personal-account-dropdown-container"),
    f"{AUTH}/components/password-sign-in-container.tsx": ("./password-sign-in-form", "../account/password-sign-in-form"),
    f"{AUTH}/components/password-sign-up-container.tsx": ("./password-sign-up-form", "../account/password-sign-up-form"),
    f"{AUTH}/sign-up.ts": ("./schemas/password-sign-up.schema", "./account/password-sign-up.schema"),
    f"{ACCOUNTS}/components/update-account-details-form-container.tsx": ("./update-account-details-form", "../profile/update-account-details-form"),
}


def replace(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def command(*args, **kwargs):
    return subprocess.check_output(args, text=True, timeout=240, **kwargs).strip()


def reset_database(pnpm, root):
    for attempt in range(3):
        try:
            command(pnpm, "--filter", "web", "exec", "supabase", "db", "reset", "--local", cwd=root)
            return
        except subprocess.CalledProcessError as error:
            print(f"Local Supabase reset attempt {attempt + 1} failed", flush=True)
            if error.stdout:
                print("\n".join(error.stdout.splitlines()[-6:]), flush=True)
            if attempt == 2:
                raise
            time.sleep(3)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.urls.append(dict(attrs).get("href", ""))


@contextmanager
def repaired_baseline(root):
    form = root / PROFILE_FORM
    source = form.read_bytes()
    marker = b"<Button disabled={updateAccountMutation.isPending}>"
    assert source.count(marker) == 1
    form.write_bytes(source.replace(marker, b'<Button type="submit" disabled={updateAccountMutation.isPending}>'))
    try:
        yield
    finally:
        form.write_bytes(source)


@contextmanager
def layout(root, feature):
    if not feature:
        yield {name: root / name for name in MOVES}
        return
    edits = {}
    targets = {}
    try:
        for old, new in MOVES.items():
            src, dest = root / old, root / new
            assert not dest.exists()
            targets[old] = dest
            edits[src] = src.read_bytes()
            text = edits[src].decode("utf-8")
            if old.endswith("/password-sign-up-form.tsx"):
                text = replace(text, "../schemas/password-sign-up.schema", "./password-sign-up.schema")
                text = replace(text, "./terms-and-conditions-form-field", "../components/terms-and-conditions-form-field")
            if old.endswith("/password-sign-up.schema.ts"):
                text = replace(text, "./password.schema", "../schemas/password.schema")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(text.encode("utf-8"))
            src.unlink()
        for rel, (before, after) in IMPORTS.items():
            path = root / rel
            edits[path] = path.read_bytes()
            path.write_bytes(replace(edits[path].decode("utf-8"), before, after).encode("utf-8"))
        yield targets
    finally:
        for path, data in edits.items():
            path.write_bytes(data)
        for path in targets.values():
            path.unlink(missing_ok=True)


def variant(source, task, kind):
    if task == "profile":
        source = replace(source, "const data = { name: displayName };", "const data = { name: displayName.trim() };")
        if kind == "reference":
            return source
        return replace(source, "      displayName,\n    },", "      displayName: displayName.trim(),\n    },")
    if task == "signout":
        handler = "signOutRequested={() => signOut.mutateAsync()}"
        body = 'if (window.confirm("Sign out?")) void signOut.mutateAsync();'
        if kind == "reference":
            return replace(source, handler, f"signOutRequested={{() => {{ {body} }}}}")
        if kind == "regression":
            return replace(source, handler, 'signOutRequested={() => { if (window.confirm("Sign out?")) window.location.assign("/"); }}')
    if task == "visibility":
        source = replace(source, "import Link from 'next/link';", "import Link from 'next/link';\nimport { useState } from 'react';")
        start = "false" if kind == "reference" else "true"
        source = replace(source, "  const t = useTranslations", f"  const [revealed, setRevealed] = useState({start});\n  const t = useTranslations")
        source = replace(source, 'type="password"', 'type={revealed ? "text" : "password"}')
        marker = """              <div>
                <Button"""
        return replace(source, marker, """              <button type="button" onClick={() => setRevealed((previous) => !previous)}>
                {revealed ? "Hide password" : "Show password"}
              </button>
              <div>
                <Button""")
    raise ValueError((task, kind))


def sync_sources(root):
    for rel in sorted(MOVES.keys() | set(MOVES.values()) | IMPORTS.keys() | {PROFILE_HOOK, SIGN_OUT_MENU}):
        src = root / rel
        dest = "/work/" + rel
        content = src.read_bytes() if src.is_file() else None
        if rel in DEPLOYED and content == DEPLOYED[rel]:
            continue
        if content is not None:
            command("docker", "exec", CONTAINER, "mkdir", "-p", dest.rsplit("/", 1)[0])
            command("docker", "cp", str(src), CONTAINER + ":" + dest)
        else:
            command("docker", "exec", CONTAINER, "rm", "-f", dest)
        DEPLOYED[rel] = content


def typecheck():
    subprocess.run(["docker", "exec", "-w", "/work", CONTAINER, "npm", "exec", "--yes",
                    "--package=pnpm@11.18.0", "--", "pnpm", "--filter", "web", "typecheck"],
                   check=True, timeout=240)


@contextmanager
def app(root, log):
    sync_sources(root)
    args = ["docker", "exec", "-w", "/work/apps/web", "-e", "NEXT_TELEMETRY_DISABLED=1", CONTAINER,
            "sh", "-c", "echo $$ >/tmp/study-next.pid; exec node node_modules/next/dist/bin/next dev --hostname localhost --port 3000"]
    with log.open("wb") as stream:
        proc = subprocess.Popen(args, stdout=stream, stderr=subprocess.STDOUT)
        try:
            for _ in range(90):
                if proc.poll() is not None:
                    raise RuntimeError(f"Makerkit app exited, see {log}")
                try:
                    with urlopen(BASE + "/auth/sign-in", timeout=3) as response:
                        assert response.status == 200
                    break
                except OSError:
                    time.sleep(.5)
            else:
                raise RuntimeError(f"Makerkit app did not become ready, see {log}")
            yield proc
        finally:
            subprocess.run(["docker", "exec", CONTAINER, "sh", "-c",
                            "kill -TERM $(cat /tmp/study-next.pid)"], capture_output=True, timeout=15)
            proc.wait(timeout=20)


def path(page):
    return urlparse(page.url).path


def sign_in(page, email, password):
    page.goto(BASE + "/auth/sign-in", timeout=90000)
    page.wait_for_load_state("networkidle")
    page.locator('input[name=email]').fill(email)
    page.locator('input[name=password]').fill(password)
    page.get_by_test_id("auth-submit-button").click()
    page.wait_for_url("**/home")


def register(page, email, password):
    page.goto(BASE + "/auth/sign-up", timeout=90000)
    page.wait_for_load_state("networkidle")
    for field, value in (("email", email), ("password", password), ("repeatPassword", password)):
        page.locator(f"input[name={field}]").fill(value)
    page.get_by_test_id("auth-submit-button").click()
    expect(page.get_by_test_id("email-confirmation-alert")).to_be_visible(timeout=15000)
    page.goto(BASE + "/home", timeout=90000)
    assert path(page) == "/auth/sign-in"
    for _ in range(30):
        response = page.request.get(f"{MAIL}/api/v1/search?" + urlencode({"query": f"to:{email}"}))
        assert response.ok
        messages = response.json()["messages"]
        if messages:
            break
        time.sleep(.3)
    else:
        raise AssertionError("No confirmation email in local mailbox")
    response = page.request.get(f"{MAIL}/api/v1/message/{messages[0]['ID']}")
    assert response.ok
    links = Links()
    links.feed(response.json()["HTML"])
    link, = {url for url in links.urls if "/auth/confirm?" in url}
    assert urlparse(link).hostname in ("localhost", "127.0.0.1")
    try:
        page.goto(link, timeout=90000)
    except Exception:
        raise RuntimeError("Local browser could not follow the confirmation link") from None
    page.wait_for_url("**/home")


def stored_name(email):
    assert re.fullmatch(r"study-[a-f0-9]+@example\.com", email)
    query = f"SELECT to_json(a.name) FROM public.accounts a JOIN auth.users u ON a.id = u.id WHERE u.email = '{email}'"
    return json.loads(command("docker", "exec", DATABASE, "psql", "-U", "postgres", "-d", "postgres",
                              "-XAt", "-v", "ON_ERROR_STOP=1", "-c", query))


def basic(browser, email, password):
    with browser.new_context() as context:
        page = context.new_page()
        page.goto(BASE + "/auth/sign-up", timeout=90000)
        expect(page.get_by_test_id("auth-submit-button")).to_be_visible()
        page.goto(BASE + "/home", timeout=90000)
        assert path(page) == "/auth/sign-in"
        sign_in(page, email, password)


def visibility(browser):
    with browser.new_context() as context:
        page = context.new_page()
        page.goto(BASE + "/auth/sign-in", wait_until="networkidle")
        password = page.locator('input[name=password]')
        masked = password.get_attribute("type") == "password"
        button = page.get_by_role("button", name=re.compile("^(Show|Hide) password$"))
        if not button.count():
            return dict(masked=masked, toggle=False)
        before = password.get_attribute("autocomplete")
        password.fill("Study!xxxx")
        expect(password).to_have_value("Study!xxxx")
        original = page.url
        page.evaluate("""document.querySelector('form').addEventListener('submit', () => {
          document.documentElement.dataset.submitted = 'yes';
        }, { capture:true })""")
        for next_type in (("text", "password") if masked else ("password", "text")):
            button.focus()
            button.press("Enter")
            expect(password).to_have_attribute("type", next_type)
            expect(password).to_have_value("Study!xxxx")
        assert page.url == original and page.locator("html").get_attribute("data-submitted") is None
        assert password.get_attribute("autocomplete") == before
        assert password.get_attribute("type") == ("password" if masked else "text")
        return dict(masked=masked, toggle=True)


def signout(browser, email, password, decision):
    with browser.new_context() as context:
        page = context.new_page()
        sign_in(page, email, password)
        page.wait_for_load_state("networkidle")
        page.add_style_tag(content="nextjs-portal { display: none !important; }")
        page.get_by_test_id("account-dropdown-trigger").click()
        action = page.get_by_test_id("account-dropdown-sign-out")
        prompts = []
        def on_dialog(dialog):
            prompts.append(dialog.type)
            dialog.accept() if decision == "confirm" else dialog.dismiss()
        page.on("dialog", on_dialog)
        if decision == "keyboard":
            action.focus()
            action.press("Enter")
        else:
            action.click()
        if decision == "confirm" or not prompts:
            expect(page.get_by_test_id("account-dropdown-trigger")).not_to_be_visible(timeout=10000)
        page.goto(BASE + "/home/settings")
        return dict(prompt=prompts == ["confirm"], retained=path(page).startswith("/home"))


def audit_types(root):
    rows = []
    for feature in (False, True):
        with repaired_baseline(root), layout(root, feature) as sources:
            targets = {task: sources[key] for task, key in (("signout", SIGN_OUT), ("profile", PROFILE_FORM), ("visibility", SIGN_IN))}
            baseline = {task: target.read_bytes() for task, target in targets.items()}
            try:
                for kind in ("baseline", "reference", "regression"):
                    for task, target in targets.items():
                        data = baseline[task]
                        if kind != "baseline":
                            data = variant(data.decode("utf-8").replace("\r\n", "\n"), task, kind).encode("utf-8")
                        target.write_bytes(data)
                    sync_sources(root)
                    typecheck()
                    rows.append(dict(layout=int(feature), bundled_variant=kind, typecheck=True))
            finally:
                for task, target in targets.items():
                    target.write_bytes(baseline[task])
    assert len(rows) == 6
    Path(__file__).with_name("makerkit-type-audit.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def run(root, mode):
    pnpm = shutil.which("pnpm.cmd")
    assert pnpm and command("git", "rev-parse", "HEAD", cwd=root) == REVISION
    assert not command("git", "status", "--porcelain", cwd=root)
    if mode == "types":
        audit_types(root)
        return
    assert mode in ("matrix", "matrix-resume", "rehearsal")
    rehearsal = mode == "rehearsal"
    marker = Path(tempfile.gettempdir()) / "paper-makerkit-qualification-app.log"
    output = Path(__file__).with_name("makerkit-rehearsal.json" if rehearsal else "makerkit-cases.json")
    with sync_playwright() as p:
        p.selectors.set_test_id_attribute("data-test")
        browser = p.chromium.launch()
        rows = json.loads(output.read_text(encoding="utf-8")) if mode == "matrix-resume" else []
        for feature in (True,) if rehearsal else (False, True):
            with repaired_baseline(root), layout(root, feature) as sources:
                for repeat in (1,) if rehearsal else (1, 2):
                    previous = [r for r in rows if r["layout"] == int(feature) and r["repeat"] == repeat]
                    if len(previous) == 9:
                        assert len({(r["task"], r["variant"]) for r in previous}) == 9
                        continue
                    if previous:
                        rows = [r for r in rows if r not in previous]
                    reset_database(pnpm, root)
                    password = "Study!xxxxxx"
                    accounts = {key: f"study-{uuid4().hex[:10]}@example.com" for key in ("edit", "visible", "heldout")}
                    email = accounts["edit"]
                    with app(root, marker):
                        for key, address in accounts.items():
                            with browser.new_context() as context:
                                page = context.new_page()
                                register(page, address, password)
                                if key in PROFILE["LEGACY_NAMES"]:
                                    legacy_name = PROFILE["LEGACY_NAMES"][key]
                                    PROFILE["save_name"](page, BASE, True, legacy_name)
                                    assert stored_name(address) == legacy_name
                    for task, loc in (("signout", SIGN_OUT), ("profile", PROFILE_FORM), ("visibility", SIGN_IN)):
                        if rehearsal and task != "profile":
                            continue
                        target = sources[loc]
                        original = target.read_bytes()
                        extras = {root / PROFILE_HOOK: None, root / SIGN_OUT_MENU: None, sources[SIGN_IN]: None}
                        for kind in ("baseline", "reference") if rehearsal else ("baseline", "reference", "regression"):
                            try:
                                digest = None
                                if kind != "baseline":
                                    source = original.decode("utf-8").replace("\r\n", "\n")
                                    if rehearsal:
                                        extras = {path: path.read_bytes() for path in extras}
                                        different = {path: data.decode("utf-8").replace("\r\n", "\n") for path, data in extras.items()}
                                        hook, menu, form = different
                                        different[hook] = replace(different[hook], ".update(data)",
                                                                  '.update(typeof data.name === "string" ? { ...data, name: data.name.trim() } : data)')
                                        different[menu] = replace(different[menu], "onClick={signOutRequested}",
                                                                  'onClick={() => { if (window.confirm("Sign out?")) signOutRequested(); }}')
                                        shown = variant(different[form], "visibility", "reference")
                                        shown = shown.replace("useState", "useReducer")
                                        shown = shown.replace("const [revealed, setRevealed] = useReducer(false)",
                                                              "const [revealed, toggle] = useReducer((value: boolean) => !value, false)")
                                        different[form] = shown.replace("onClick={() => setRevealed((previous) => !previous)}", "onClick={toggle}")
                                        digest = {file.relative_to(root).as_posix(): PROFILE["replay"](root, file, content.encode(), marker.with_suffix(f".{index}.patch"))
                                                  for index, (file, content) in enumerate(different.items())}
                                    else:
                                        target.write_bytes(variant(source, task, kind).encode("utf-8"))
                                with app(root, marker):
                                    basic(browser, email, password)
                                    if task == "visibility":
                                        result = visibility(browser)
                                        expected = dict(masked=kind != "regression", toggle=kind != "baseline")
                                    elif task == "signout":
                                        result = {key: signout(browser, email, password, key) for key in ("confirm", "cancel", "keyboard")}
                                        expected = {key: dict(prompt=kind != "baseline",
                                                              retained=kind == "regression" or (kind == "reference" and key != "confirm"))
                                                    for key in result}
                                    else:
                                        result = PROFILE["checks"](browser, BASE, True,
                                                                  lambda page, address: sign_in(page, address, password),
                                                                  stored_name, accounts, kind)
                                        expected = result
                                    assert result == expected, (task, kind, result, expected)
                                    if rehearsal:
                                        typecheck()
                                        study_basic.check(browser, "makerkit-lite", BASE, email, password)
                                        for public_task in ("profile", "visibility", "signout"):
                                            assert study_preservation.check(browser, "makerkit-lite", public_task, BASE,
                                                                            accounts["visible"], password, PROFILE["LEGACY_NAMES"]["visible"])
                                        if kind == "reference":
                                            assert visibility(browser) == dict(masked=True, toggle=True)
                                            for decision, retained in (("confirm", False), ("cancel", True), ("keyboard", True)):
                                                assert signout(browser, email, password, decision) == dict(prompt=True, retained=retained)
                                        result.update(patch_sha256=digest, public_package_checks=True, alternative=(kind == "reference"))
                                rows.append(dict(layout=int(feature), repeat=repeat, task=task,
                                                 variant=kind, basic=True, observed=result))
                                output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
                                print(json.dumps(rows[-1]), flush=True)
                            finally:
                                target.write_bytes(original)
                                for path, data in extras.items():
                                    if data is not None:
                                        path.write_bytes(data)
        assert len(rows) == (2 if rehearsal else 36)


if __name__ == "__main__":
    run(Path(sys.argv[1]).resolve(), sys.argv[2])
