"""Run the registration or sign-out prototype against disposable local databases."""

import json
from contextlib import nullcontext
import os
from pathlib import Path
import re
import runpy
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

TMP = Path(tempfile.gettempdir())
WORK = TMP / "paper-paired-registration"
SMART = WORK / "smartkit"
EXTERNAL = TMP / "paper-external-kit-6e33e58"
DB = "paper-paired-registration-pg"
OUT = Path(__file__).with_name("registration-probe.json")
PUBLIC_CHECK = runpy.run_path(str(Path(__file__).with_name("public-preservation.py")))["check"]
BASIC_CHECK = runpy.run_path(str(Path(__file__).with_name("public-basic.py")))["check"]


def cmd(*args, **options):
    return subprocess.run(args, check=True, text=True, capture_output=True, timeout=120, **options).stdout.strip()


def sql(db, query):
    return cmd("docker", "exec", DB, "psql", "-U", "postgres", "-d", db, "-XAt", "-v", "ON_ERROR_STOP=1", "-c", query)


def wait_http(url):
    for _ in range(100):
        try:
            with urlopen(url, timeout=3) as r:
                assert r.status == 200
                return
        except OSError:
            time.sleep(.3)
    raise RuntimeError(f"Readiness failed for {url}")


def revised(source, smart, variant):
    if variant == "baseline":
        return source
    if smart:
        clause = 'ctx.path === "/sign-up/email"'
        if variant == "fault":
            clause += ' || ctx.path === "/sign-in/email"'
        changed = 'import { APIError, createAuthMiddleware } from "better-auth/api";\n' + source
        block = '''  hooks: {
    before: createAuthMiddleware(async (ctx) => {
      if ((PATHS) && typeof ctx.body?.password === "string" && ctx.body.password.length < 12) {
        throw new APIError("BAD_REQUEST", { message: "Password must be at least 12 characters." });
      }
    }),
  },
'''
        anchor = "  emailAndPassword: {"
        assert changed.count(anchor) == 1
        return changed.replace(anchor, block.replace("PATHS", clause) + anchor)
    signup = "password: z.string().min(8),"
    signin = "password: z.string().min(8).max(100)\n});\n\nexport const signIn"
    assert source.count(signup) == source.count(signin) == 1
    changed = source.replace(signup, signup.replace("min(8)", "min(12)"))
    return changed.replace(signin, signin.replace("min(8)", "min(12)")) if variant == "fault" else changed


def signout_variant(source, smart, variant):
    if variant == "baseline":
        return source
    if smart:
        anchor = "        await signOut();"
        prompt = '        if (!window.confirm("Sign out?")) ' + ("{}" if variant == "fault" else "return;")
    else:
        anchor = '<form action={handleSignOut} className="w-full">'
        prompt = ('<form action={handleSignOut} className="w-full" onSubmit={(event) => { '
                  'if (!window.confirm("Sign out?")) '
                  + ('{}' if variant == "fault" else 'event.preventDefault();') + ' }}>')
    assert source.count(anchor) == 1
    changed = source.replace(anchor, prompt + "\n" + anchor if smart else prompt)
    if variant == "legacy-fault":
        assert changed.count("await signOut();") == 1
        changed = changed.replace("await signOut();", "")
    return changed


def visibility_variant(source, smart, variant):
    if variant == "baseline":
        return source
    start = "  const [error, setError]" if smart else "  const [state, formAction, pending]"
    assert source.count(start) == 1
    initial = "true" if variant == "fault" else "false"
    changed = source.replace(start, f"  const [visible, setVisible] = useState({initial});\n" + start)
    toggle = '''<button type="button" onClick={() => setVisible(!visible)}>
                {visible ? "Hide password" : "Show password"}
              </button>'''
    marker = 'type="password"'
    assert changed.count(marker) == 1
    password_end = changed.index("/>", changed.index(marker)) + 2
    if not smart:
        old_import = "import { useActionState } from 'react';"
        assert changed.count(old_import) == 1
        changed = changed.replace(old_import, "import { useActionState, useState } from 'react';")
        password_end = changed.index("/>", changed.index(marker)) + 2
        toggle = "{mode === 'signin' && (" + toggle + ")}"
    changed = changed[:password_end] + "\n              " + toggle + changed[password_end:]
    condition = "visible" if smart else "mode === 'signin' && visible"
    return changed.replace(marker, 'type={' + condition + ' ? "text" : "password"}')


def check_visibility(browser, base, smart, email, test):
    prefix = "/auth" if smart else ""
    path = base + prefix + "/sign-in"
    with browser.new_context() as ctx:
        page = ctx.new_page()
        page.goto(path, wait_until="networkidle")
        password = page.locator("#password")
        masked = password.get_attribute("type") == "password"
        if test == "mask":
            assert password.get_attribute("autocomplete") == "current-password"
            signup = ctx.new_page()
            signup.goto(base + prefix + "/sign-up", wait_until="networkidle")
            assert signup.locator("#password").get_attribute("type") == "password"
            assert signup.locator("#password").get_attribute("autocomplete") == "new-password"
            return masked
        secret = "Probe!xxxxxx"
        password.fill(secret)
        initial = password.get_attribute("type")
        toggle = page.get_by_role("button", name=re.compile("^(Show|Hide) password$"))
        if not toggle.count():
            return False
        posts = []
        page.on("request", lambda req: posts.append(req) if req.method == "POST" else None)
        assert initial in ("text", "password")
        for expected_type in ("text" if initial == "password" else "password", initial):
            toggle.press("Enter")
            assert password.get_attribute("type") == expected_type
            assert password.input_value() == secret
        return not posts and active_user(ctx, base, smart) != email


def active_user(context, base, smart):
    endpoint = "/api/auth/get-session" if smart else "/api/user"
    response = context.request.get(base + endpoint)
    assert response.ok, (endpoint, response.status)
    body = response.json()
    user = (body or {}).get("user") if smart else body
    return (user or {}).get("email")


def browser_check(browser, base, smart, signup, email, length, decision=None, variant=None):
    prefix = "/auth" if smart else ""
    path = "/sign-up" if signup else "/sign-in"
    context = browser.new_context()
    try:
        page = context.new_page()
        page.goto(base + prefix + path, wait_until="networkidle")
        if smart and signup:
            page.locator("#name").fill("Synthetic study account")
        page.locator("#email").fill(email)
        page.locator("#password").fill("Probe!" + "x" * (length - 6))
        endpoint = "/api/auth" + path + "/email" if smart else path
        with page.expect_response(lambda response: response.request.method == "POST" and response.url == base + endpoint) as pending:
            page.get_by_role("button", name=re.compile("^Sign " + ("up" if signup else "in") + "$", re.I)).click()
        assert pending.value.status < 500, (endpoint, pending.value.status)
        if not signup:
            if decision is None:
                return active_user(context, base, smart) == email
            assert active_user(context, base, smart) == email, "Account must be signed in before testing sign-out"
            page.goto(base + "/dashboard", wait_until="networkidle")
            if not smart:
                page.locator('header button[aria-haspopup="menu"]').click()
            prompts = []

            def handle_dialog(dialog):
                prompts.append(dialog.type)
                dialog.accept() if decision == "confirm" else dialog.dismiss()

            page.on("dialog", handle_dialog)
            target = (page.get_by_role("button", name="Sign out", exact=True) if smart
                      else page.locator('button[type="submit"]').filter(has_text="Sign out"))
            posts = []
            logout_url = base + ("/api/auth/sign-out" if smart else "/dashboard")
            page.on("request", lambda req: posts.append(req) if req.method == "POST" else None)
            should_navigate = variant in ("baseline", "fault") or decision == "confirm"
            should_post = should_navigate and variant != "legacy-fault"
            observed = (page.expect_response(lambda r: r.url == logout_url and r.request.method == "POST")
                        if should_post else nullcontext())
            with observed as pending_logout:
                (target.press("Enter") if decision == "cancel-keyboard" else target.click())
            if should_post:
                assert pending_logout.value.status < 500
            if should_navigate:
                page.wait_for_url(base + ("/auth/sign-in" if smart else "/"))
            assert bool(posts) == should_post
            dashboard_response = context.request.get(base + "/dashboard")
            assert dashboard_response.ok
            dashboard = dashboard_response.url.split("?")[0] == base + "/dashboard"
            session_alive = active_user(context, base, smart) == email
            assert session_alive == dashboard, (session_alive, dashboard_response.url)
            assert prompts in ([], ["confirm"]), prompts
            return {"confirm_prompt": bool(prompts), "signed_out_destination": should_navigate,
                    "session_retained": session_alive}
    finally:
        context.close()


def run_kit(browser, smart, pg_port, results, task, output, variants, alternate):
    kit = "smartkit" if smart else "nextjs-saas-starter"
    root = ((WORK / ("smartkit-layered" if smart else "nextjs-feature"))
            if alternate else (SMART if smart else EXTERNAL))
    if task == "signout":
        relative = "src/app/dashboard/sign-out-button.tsx" if smart else "app/(dashboard)/layout.tsx"
    elif task == "visibility":
        relative = ("src/app/(auth)/auth/sign-in/page.tsx" if smart else
                    ("features/auth/login.tsx" if alternate else "app/(login)/login.tsx"))
    else:
        relative = (("src/services/auth/auth.config.ts" if alternate else "src/features/auth/auth.config.ts") if smart else
                    ("features/auth/actions.ts" if alternate else "app/(login)/actions.ts"))
    patch = {"signout": signout_variant, "visibility": visibility_variant, "registration": revised}[task]
    path = root / relative
    original = path.read_bytes()
    source = original.decode("utf-8").replace("\r\n", "\n")
    table = '"user"' if smart else "users"
    pnpm = shutil.which("pnpm.cmd")
    for repeat in (1, 2):
        db = f"probe_{'s' if smart else 'n'}_{repeat}"
        sql("postgres", f"CREATE DATABASE {db}")
        env = dict(os.environ)
        for key in ("RESEND_API_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"):
            env.pop(key, None)
        port = 43190 if smart else 43191
        base = f"http://localhost:{port}"
        conn = f"postgresql://postgres:local_probe_only@127.0.0.1:{pg_port}/{db}"
        env.update(DATABASE_URL=conn, POSTGRES_URL=conn, BASE_URL=base,
                   BETTER_AUTH_URL=base, NEXT_PUBLIC_BETTER_AUTH_URL=base,
                   NEXT_PUBLIC_APP_URL=base, BETTER_AUTH_SECRET=secrets.token_hex(24),
                   AUTH_SECRET=secrets.token_hex(24), STRIPE_SECRET_KEY="local-placeholder",
                   NEXT_TELEMETRY_DISABLED="1", NODE_ENV="development")
        cmd(pnpm, "db:migrate", cwd=root, env=env)
        old = {n: f"legacy{n}@example.test" for n in (10, 11)}

        def register(email, length):
            browser_check(browser, base, smart, True, email, length)
            return sql(db, f"SELECT count(*) FROM {table} WHERE email = '{email}'") == "1"

        try:
            for variant in variants:
                path.write_bytes(patch(source, smart, variant).encode("utf-8"))
                log = WORK / f"{task}-{kit}-{repeat}-{variant}.log"
                with log.open("wb") as stream:
                    app = subprocess.Popen(["node", "node_modules/next/dist/bin/next", "dev", "--turbopack",
                                            "--hostname", "127.0.0.1", "--port", str(port)],
                                           cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT)
                    try:
                        wait_http(base + ("/auth" if smart else "") + "/sign-up")
                        if variant == "baseline":
                            for length, email in old.items():
                                assert register(email, length)
                            if smart:
                                sql(db, f"UPDATE {table} SET email_verified=true WHERE email LIKE 'legacy%@example.test'")
                        e12 = variant + "-new12@example.test"
                        new12 = register(e12, 12)
                        assert new12
                        if smart:
                            sql(db, f"UPDATE {table} SET email_verified=true WHERE email='{e12}'")
                        cmd("node", "node_modules/typescript/bin/tsc", "--noEmit", "--incremental", "false", cwd=root, env=env)
                        BASIC_CHECK(browser, kit, base, e12, "Probe!xxxxxx")
                        public_pass = PUBLIC_CHECK(browser, kit, task, base, old[10], "Probe!xxxx")
                        assert public_pass == (variant not in ("fault", "legacy-fault")), (task, kit, variant)
                        if task == "signout":
                            check = {decision: browser_check(browser, base, smart, False, old[length], length, decision, variant)
                                     for decision, length in (("confirm", 10), ("cancel", 10), ("cancel-keyboard", 11))}
                            expected = {decision: {"confirm_prompt": variant != "baseline",
                                                   "signed_out_destination": variant in ("baseline", "fault") or decision == "confirm",
                                                   "session_retained": variant == "legacy-fault" or
                                                   (variant == "reference" and decision != "confirm")}
                                        for decision in check}
                        elif task == "visibility":
                            check = {test: check_visibility(browser, base, smart, e12, test)
                                     for test in ("toggle", "mask")}
                            expected = dict(toggle=variant != "baseline", mask=variant != "fault")
                        else:
                            check = {"new11": register(variant + "-new11@example.test", 11),
                                     "new12": new12}
                            check.update(basic_new12_login=True,
                                         visible_old10_login=browser_check(browser, base, smart, False, old[10], 10),
                                         heldout_old11_login=browser_check(browser, base, smart, False, old[11], 11))
                            expected = dict(new11=variant == "baseline", new12=True, basic_new12_login=True,
                                            visible_old10_login=variant != "fault", heldout_old11_login=variant != "fault")
                        result = dict(kit=kit, repeat=repeat, variant=variant, common_basic=True,
                                      public_preservation=public_pass,
                                      alternate_layout=alternate, **check)
                        results.append(result)
                        print(json.dumps(result), flush=True)
                        output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
                        assert check == expected, result
                    finally:
                        subprocess.run(["taskkill", "/PID", str(app.pid), "/T", "/F"], capture_output=True)
                        app.wait(timeout=15)
        finally:
            path.write_bytes(original)
        sql("postgres", f"DROP DATABASE {db} WITH (FORCE)")


def main():
    alternate = "--alternate" in sys.argv[1:]
    options = [x for x in sys.argv[1:] if x != "--alternate"]
    assert options in ([], ["--signout"], ["--signout-preservation"], ["--visibility"])
    task = {None: "registration", "--signout": "signout", "--signout-preservation": "signout", "--visibility": "visibility"}[
        options[0] if options else None]
    preservation = options == ["--signout-preservation"]
    variants = ("baseline", "reference", "legacy-fault" if preservation else "fault")
    suffix = "-alternate" if alternate else ""
    tag = "signout-acceptance" if options == ["--signout"] else task
    output = OUT.with_name(f"{tag}-qualification{suffix}.json")
    roots = (WORK / "smartkit-layered", WORK / "nextjs-feature") if alternate else (SMART, EXTERNAL)
    assert all((root / "node_modules/next/dist/bin/next").exists() for root in roots)
    cmd("docker", "run", "--rm", "--pull=never", "-d", "--name", DB,
        "--tmpfs", "/var/lib/postgresql:rw,size=256m", "-p", "127.0.0.1::5432",
        "-e", "POSTGRES_PASSWORD=local_probe_only", "postgres:18")
    configs = {}
    try:
        if task in ("signout", "visibility"):
            for root in roots:
                config = root / "next.config.ts"
                original = config.read_bytes()
                anchor = b"const nextConfig: NextConfig = {"
                assert original.count(anchor) == 1
                configs[config] = original
                config.write_bytes(original.replace(anchor, anchor + b"\n  devIndicators: false,"))
        pg_port = cmd("docker", "port", DB, "5432/tcp").rsplit(":", 1)[1]
        for _ in range(60):
            try:
                cmd("docker", "exec", DB, "pg_isready", "-h", "127.0.0.1", "-U", "postgres")
                break
            except subprocess.CalledProcessError:
                time.sleep(.5)
        else:
            raise RuntimeError("PostgreSQL did not become ready")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            results = []
            run_kit(browser, True, pg_port, results, task, output, variants, alternate)
            run_kit(browser, False, pg_port, results, task, output, variants, alternate)
            assert len(results) == 12
            browser.close()
    finally:
        for config, original in configs.items():
            config.write_bytes(original)
        cmd("docker", "stop", DB)


if __name__ == "__main__":
    main()
