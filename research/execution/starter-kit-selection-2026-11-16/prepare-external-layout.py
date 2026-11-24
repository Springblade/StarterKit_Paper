"""Relocate auth modules in a disposable checkout while preserving public routes."""

from pathlib import Path
import subprocess
import tempfile

ROOT = Path(tempfile.gettempdir()) / "paper-paired-registration" / "nextjs-feature"
REVISION = "6e33e58b1e553a41fe22e6b941a7229a002de361"
MOVES = {
    "app/(login)/actions.ts": "features/auth/actions.ts",
    "app/(login)/login.tsx": "features/auth/login.tsx",
    "lib/auth/session.ts": "features/auth/session.ts",
    "lib/auth/middleware.ts": "features/auth/middleware.ts",
}
IMPORTS = {
    "from '@/app/(login)/actions'": "from '@/features/auth/actions'",
    "from '../login'": "from '@/features/auth/login'",
    "from '@/lib/auth/session'": "from '@/features/auth/session'",
    "from '@/lib/auth/middleware'": "from '@/features/auth/middleware'",
}


def main():
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert revision == REVISION
    assert all((ROOT / src).is_file() and not (ROOT / dst).exists() for src, dst in MOVES.items())
    sources = [ROOT / "middleware.ts"]
    for directory in ("app", "lib", "components"):
        sources += [p for p in (ROOT / directory).rglob("*") if p.suffix in (".ts", ".tsx")]
    changed = {}
    for path in sources:
        original = path.read_bytes()
        revised = original
        for old, new in IMPORTS.items():
            revised = revised.replace(old.encode(), new.encode())
        relative = path.relative_to(ROOT).as_posix()
        target = ROOT / MOVES.get(relative, relative)
        if target != path or original != revised:
            changed[relative] = target.relative_to(ROOT).as_posix()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(revised)
            if target != path:
                path.unlink()
    assert set(MOVES) <= set(changed)
    assert all((ROOT / target).is_file() for target in changed.values())
    print(changed)


if __name__ == "__main__":
    main()
