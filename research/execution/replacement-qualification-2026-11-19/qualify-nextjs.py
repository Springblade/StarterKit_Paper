"""Re-run Next.js account qualification on clean, disposable upstream worktrees."""

import itertools
import json
import os
from pathlib import Path
import runpy
import secrets
import shutil
import subprocess
import sys
import tempfile
import time

from playwright.sync_api import sync_playwright
import study_basic
import study_preservation

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "starter-kit-selection-2026-11-16"
REVISION = "6e33e58b1e553a41fe22e6b941a7229a002de361"
TASKS = ("registration", "signout", "visibility")
PROFILE = runpy.run_path(str(HERE / "profile-checks.py"))


def run_profile(browser, root, db_port, run_kit, work, alternate, rows, rehearsal=False):
    env = run_kit.__globals__
    cmd, sql, wait_http = (env[k] for k in ("cmd", "sql", "wait_http"))
    pnpm = shutil.which("pnpm.cmd")
    actions = root / ("features/auth/actions.ts" if alternate else "app/(login)/actions.ts")
    form = root / "app/(dashboard)/dashboard/general/page.tsx"
    original_actions, original_form = actions.read_bytes(), form.read_bytes()
    before = b"const updateAccountSchema = z.object({\n  name: z.string()"
    updated = original_actions.replace(b"\r\n", b"\n")
    assert updated.count(before) == 1
    updated = updated.replace(before, before + b".trim()")
    assert original_form.count(b"nameValue={user?.name ?? ''}") == 1
    fault = original_form.replace(b"nameValue={user?.name ?? ''}", b"nameValue={user?.name?.trim() ?? ''}")
    port = 43192
    base = f"http://localhost:{port}"
    visibility = root / ("features/auth/login.tsx" if alternate else "app/(login)/login.tsx")
    signout = root / "app/(dashboard)/layout.tsx"
    original_visibility, original_signout = visibility.read_bytes(), signout.read_bytes()
    for repeat in (1,) if rehearsal else (1, 2):
        db = f"profile_{int(alternate)}_{repeat}"
        sql("postgres", f"CREATE DATABASE {db}")
        conn = f"postgresql://postgres:local_probe_only@127.0.0.1:{db_port}/{db}"
        app_env = dict(os.environ, DATABASE_URL=conn, POSTGRES_URL=conn, BASE_URL=base,
                       AUTH_SECRET=secrets.token_hex(24), STRIPE_SECRET_KEY="local-placeholder",
                       NEXT_TELEMETRY_DISABLED="1", NODE_ENV="development")
        cmd(pnpm, "db:migrate", cwd=root, env=app_env)
        accounts = {fixture: f"{fixture}@example.test" for fixture in ("edit", "visible", "heldout")}

        def login(page, email):
            page.goto(base + "/sign-in")
            page.locator("input[name=email]").fill(email)
            page.locator("input[name=password]").fill("Probe!xxxxxx")
            page.locator("button[type=submit]").click()
            page.wait_for_url("**/dashboard")

        def stored(email):
            assert email in accounts.values()
            return json.loads(sql(db, f"SELECT to_json(name) FROM users WHERE email='{email}'"))

        try:
            for kind in ("baseline", "reference") if rehearsal else ("baseline", "reference", "regression"):
                actions.write_bytes(original_actions if kind == "baseline" else updated)
                digest = None
                if rehearsal and kind == "reference":
                    actions.write_bytes(original_actions)
                    different = original_actions.replace(b"\r\n", b"\n")
                    block = different.index(b"export const updateAccount =")
                    head, tail = different[:block], different[block:]
                    assert tail.count(b"const { name, email } = data;") == 1
                    different = head + tail.replace(b"const { name, email } = data;",
                                                    b"const { email } = data;\n    const name = data.name.trim();")
                    shown = env["visibility_variant"](original_visibility.decode().replace("\r\n", "\n"), False, "reference")
                    shown = shown.replace("useState", "useReducer")
                    shown = shown.replace("const [visible, setVisible] = useReducer(false)",
                                          "const [visible, toggle] = useReducer((value: boolean) => !value, false)")
                    shown = shown.replace("onClick={() => setVisible(!visible)}", "onClick={toggle}").encode()
                    old_button = b'<button type="submit" className="flex w-full">'
                    assert original_signout.count(old_button) == 1
                    signed = original_signout.replace(old_button, b'<button type="submit" className="flex w-full" onClick={(e) => { if (!window.confirm("Sign out?")) e.preventDefault(); }}>')
                    digest = {file.relative_to(root).as_posix(): PROFILE["replay"](root, file, content, work / f"candidate-{index}.patch")
                              for index, (file, content) in enumerate(((actions, different), (visibility, shown), (signout, signed)))}
                form.write_bytes(fault if kind == "regression" else original_form)
                with (work / f"profile-{alternate}-{repeat}-{kind}.log").open("wb") as log:
                    app = subprocess.Popen(["node", "node_modules/next/dist/bin/next", "dev", "--turbopack",
                                            "--hostname", "127.0.0.1", "--port", str(port)],
                                           cwd=root, env=app_env, stdout=log, stderr=subprocess.STDOUT)
                    try:
                        wait_http(base + "/sign-up")
                        if kind == "baseline":
                            for fixture, address in accounts.items():
                                env["browser_check"](browser, base, False, True, address, 12)
                                if fixture in PROFILE["LEGACY_NAMES"]:
                                    with browser.new_context() as context:
                                        page = context.new_page()
                                        login(page, address)
                                        legacy = PROFILE["LEGACY_NAMES"][fixture]
                                        PROFILE["save_name"](page, base, False, legacy)
                                        assert stored(address) == legacy
                        cmd("node", "node_modules/typescript/bin/tsc", "--noEmit", "--incremental", "false",
                            cwd=root, env=app_env)
                        env["BASIC_CHECK"](browser, "nextjs-saas-starter", base, accounts["edit"], "Probe!xxxxxx")
                        observed = PROFILE["checks"](browser, base, False, login, stored, accounts, kind)
                        if rehearsal:
                            study_basic.check(browser, "nextjs-saas-starter", base, accounts["edit"], "Probe!xxxxxx")
                            for task in ("profile", "visibility", "signout"):
                                assert study_preservation.check(browser, "nextjs-saas-starter", task, base,
                                                                accounts["visible"], "Probe!xxxxxx", PROFILE["LEGACY_NAMES"]["visible"])
                            if kind == "reference":
                                assert env["check_visibility"](browser, base, False, accounts["edit"], "toggle")
                                for decision, retained in (("confirm", False), ("cancel", True), ("cancel-keyboard", True)):
                                    result = env["browser_check"](browser, base, False, False, accounts["edit"], 12, decision, "reference")
                                    assert result["confirm_prompt"] and result["session_retained"] == retained
                            observed.update(patch_sha256=digest, public_package_checks=True, alternative=(kind == "reference"))
                        rows.append(dict(kit="nextjs-saas-starter", task="profile", repeat=repeat,
                                         alternate_layout=alternate, variant=kind, common_basic=True, **observed))
                        print(json.dumps(rows[-1]), flush=True)
                    finally:
                        subprocess.run(["taskkill", "/PID", str(app.pid), "/T", "/F"], capture_output=True)
                        app.wait(timeout=15)
        finally:
            actions.write_bytes(original_actions)
            form.write_bytes(original_form)
            visibility.write_bytes(original_visibility)
            signout.write_bytes(original_signout)
            sql("postgres", f"DROP DATABASE {db} WITH (FORCE)")


def main():
    source = Path(sys.argv[1]).resolve()
    rehearsal = "--rehearsal" in sys.argv[2:]
    profile_only = rehearsal or "--profile" in sys.argv[2:]
    pnpm = shutil.which("pnpm.cmd")
    assert pnpm is not None
    probe = runpy.run_path(str(OLD / "probe-registration.py"))
    run_kit = probe["run_kit"]
    cmd = probe["cmd"]
    prepare = runpy.run_path(str(OLD / "prepare-external-layout.py"))["main"]
    validate = runpy.run_path(str(OLD / "qualify-admission.py"))["verify_treatment"]
    output = HERE / ("nextjs-rehearsal.json" if rehearsal else "nextjs-profile.json" if profile_only else "nextjs-cases.json")
    with tempfile.TemporaryDirectory(prefix="paper-nextjs-qualification-", ignore_cleanup_errors=True) as scratch:
        work = Path(scratch)
        db = work.name
        roots = [work / "native", work / "nextjs-feature"]
        run_kit.__globals__.update(WORK=work, EXTERNAL=roots[0], DB=db)
        for root in roots:
            cmd("git", "clone", "--shared", "--no-checkout", str(source), str(root))
            cmd("git", "checkout", "--detach", REVISION, cwd=root)
            cmd(pnpm, "install", "--frozen-lockfile", "--ignore-scripts",
                "--config.strict-dep-builds=false", cwd=root)
        prepare.__globals__["ROOT"] = roots[1]
        prepare()
        for root in roots:
            config = root / "next.config.ts"
            anchor = b"const nextConfig: NextConfig = {"
            content = config.read_bytes()
            assert content.count(anchor) == 1
            config.write_bytes(content.replace(anchor, anchor + b"\n  devIndicators: false,"))
        cmd("docker", "run", "--rm", "--pull=never", "-d", "--name", db, "--tmpfs",
            "/var/lib/postgresql:rw,size=256m", "-p", "127.0.0.1::5432",
            "-e", "POSTGRES_PASSWORD=local_probe_only", "postgres:18")
        try:
            port = cmd("docker", "port", db, "5432/tcp").rsplit(":", 1)[1]
            for _ in range(60):
                try:
                    cmd("docker", "exec", db, "pg_isready", "-h", "127.0.0.1", "-U", "postgres")
                    break
                except subprocess.CalledProcessError:
                    time.sleep(.5)
            else:
                raise RuntimeError("PostgreSQL did not become ready")
            rows = []
            with sync_playwright() as p:
                browser = p.chromium.launch()
                if profile_only:
                    for alternate, root in enumerate(roots):
                        if rehearsal and not alternate:
                            continue
                        run_profile(browser, root, port, run_kit, work, bool(alternate), rows, rehearsal)
                        output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
                else:
                    for task, alternate in itertools.product(TASKS, (False, True)):
                        case_rows = []
                        variants = ("baseline", "reference", "legacy-fault" if task == "signout" else "fault")
                        run_kit(browser, False, port, case_rows, task, work / "latest.json", variants, alternate)
                        for row in case_rows:
                            validate(row, task)
                            rows.append(dict(task=task, **row))
                        output.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
            assert len(rows) == (2 if rehearsal else 12 if profile_only else 36)
        finally:
            cmd("docker", "stop", db)


if __name__ == "__main__":
    main()
