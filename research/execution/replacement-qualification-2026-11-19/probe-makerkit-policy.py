"""Measure the local Supabase service's signup and password-update contract.

Use only synthetic users and Mailpit, and restore the upstream settings afterward.
"""

from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.error import HTTPError
from urllib.parse import parse_qs, quote, urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4

ROOT = Path(sys.argv[1]).resolve()
WEB = ROOT / "apps/web"
CONFIG = WEB / "supabase/config.toml"
API = "http://127.0.0.1:54321/auth/v1"
MAIL = "http://127.0.0.1:54324/api/v1"
SERVICE = "supabase_auth_next-supabase-saas-kit-turbo-lite"
PNPM = shutil.which("pnpm.cmd")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


def http(url, data=None, headers=None, method=None):
    headers = headers or {}
    if data is not None:
        headers = dict(headers, **{"Content-Type": "application/json"})
    req = Request(url, data=json.dumps(data).encode() if data is not None else None,
                  headers=headers, method=method)
    try:
        response = build_opener(NoRedirect()).open(req, timeout=20)
    except HTTPError as exc:
        response = exc
    with response:
        body = response.read()
        payload = json.loads(body) if "application/json" in response.headers.get("Content-Type", "") else {}
        return response.status, payload


def command(*args):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=240)
    if proc.returncode:
        raise RuntimeError(f"{args[-1]} failed with status {proc.returncode}")
    return proc.stdout.strip()


def password_setup(api_headers, email, password):
    status, data = http(API + "/signup", dict(email=email, password=password), api_headers)
    return dict(status=status, code=data.get("error_code"), user_returned=bool(data.get("id")))


def verify_email(email, headers):
    for _ in range(35):
        status, body = http(MAIL + "/search?" + urlencode({"query": f"to:{email}"}))
        assert status == 200
        if body["messages"]:
            break
        time.sleep(.3)
    else:
        raise AssertionError("Synthetic confirmation email not found")
    status, body = http(MAIL + "/message/" + quote(body["messages"][0]["ID"], safe=""))
    assert status == 200
    parser = Links()
    parser.feed(body["HTML"])
    link, = {href for href in parser.links if "/auth/confirm?" in href}
    parsed = urlparse(link)
    assert parsed.hostname in ("127.0.0.1", "localhost")
    fields = parse_qs(parsed.query)
    status, _ = http(API + "/verify",
                     dict(token_hash=fields["token_hash"][0], type=fields["type"][0]), headers)
    assert status == 200


def assess(headers, phase, email, password):
    sign_up = {length: password_setup(headers, f"case-{uuid4().hex[:12]}@example.com",
                                     f"Study!{'x' * (length - 6)}")
               for length in (11, 12)}
    status, user = http(API + "/token?grant_type=password",
                        dict(email=email, password=password), headers)
    assert status == 200 and user["user"]["email"] == email
    authorized = dict(headers, Authorization=f"Bearer {user['access_token']}")
    update_status, update = http(API + "/user", dict(password="New!xxxxxxx"),
                                 authorized, method="PUT")
    return dict(phase=phase, minimum=command("docker", "exec", SERVICE, "printenv", "GOTRUE_PASSWORD_MIN_LENGTH"),
                registration=sign_up, old_account_login=status,
                change_to_11=dict(status=update_status, code=update.get("error_code")))


def main():
    assert PNPM and command("git", "rev-parse", "HEAD") == "9ff430df9c58516add0136bd01ed800ce551675e"
    env = dict(line.split("=", 1) for line in (WEB / ".env.development").read_text().splitlines()
               if "=" in line and not line.startswith("#"))
    headers = {"apikey": env["NEXT_PUBLIC_SUPABASE_ANON_KEY"]}
    saved = CONFIG.read_bytes()
    assert b"minimum_password_length" not in saved
    p10 = "Study!xxxx"
    initial, legacy = (f"legacy-{uuid4().hex[:12]}@example.com" for _ in range(2))
    for email in (initial, legacy):
        assert password_setup(headers, email, p10)["status"] == 200
        verify_email(email, headers)
    output = Path(__file__).with_name("makerkit-password-policy.json")
    results = [assess(headers, "upstream", initial, p10)]
    assert results[0]["registration"][11]["status"] == 200
    assert results[0]["change_to_11"]["status"] == 200
    output.write_text(json.dumps(results, indent=2) + "\n")
    try:
        command(PNPM, "--filter", "web", "exec", "supabase", "stop")
        CONFIG.write_bytes(saved.replace(b"[auth]", b"[auth]\nminimum_password_length = 12", 1))
        command(PNPM, "--filter", "web", "exec", "supabase", "start")
        results.append(assess(headers, "minimum_12", legacy, p10))
        assert results[-1]["registration"][11]["status"] >= 400
        assert results[-1]["registration"][12]["status"] == 200
        assert results[-1]["change_to_11"]["status"] >= 400
        output.write_text(json.dumps(results, indent=2) + "\n")
        print(json.dumps(results, indent=2))
    finally:
        if CONFIG.read_bytes() != saved:
            try:
                command(PNPM, "--filter", "web", "exec", "supabase", "stop")
            finally:
                CONFIG.write_bytes(saved)
            command(PNPM, "--filter", "web", "exec", "supabase", "start")


if __name__ == "__main__":
    main()
