"""Assemble and review the source/control materials for the prospective conditions."""

from hashlib import sha256
import itertools
import json
from pathlib import Path
import re
import tempfile

HERE = Path(__file__).resolve().parent
TMP = Path(tempfile.gettempdir())
WORK = TMP / "paper-paired-registration"
QUAD = {
    ("smartkit", 0): WORK / "smartkit-layered",
    ("smartkit", 1): WORK / "smartkit",
    ("nextjs-saas-starter", 0): TMP / "paper-external-kit-6e33e58",
    ("nextjs-saas-starter", 1): WORK / "nextjs-feature",
}
SOURCE_DIRS = {"app", "components", "features", "lib", "public", "scripts", "src"}
FIXED_FILES = {
    ".gitignore", ".env.example", "biome.json", "components.json", "docker-compose.yml",
    "drizzle.config.ts", "middleware.ts", "next-env.d.ts", "next.config.ts", "package.json",
    "pnpm-lock.yaml", "pnpm-workspace.yaml", "postcss.config.mjs", "README.md", "LICENSE",
    "tsconfig.json", "vercel.json", "vitest.config.ts",
}


def source_files(root):
    out = {p.name: p.read_bytes() for p in root.iterdir() if p.name in FIXED_FILES}
    for folder in SOURCE_DIRS:
        for p in (root / folder).rglob("*"):
            if p.is_file() and not any(part.startswith(".env") for part in p.relative_to(root).parts):
                out[p.relative_to(root).as_posix()] = p.read_bytes()
    assert {"package.json", "pnpm-lock.yaml", "next.config.ts"} <= out.keys()
    assert all("node_modules" not in Path(name).parts for name in out)
    return out


def overlay(src, task, specification, kit, v):
    command = f"python study-basic.py {kit} http://localhost:3107"
    config = src["next.config.ts"]
    anchor = b"const nextConfig: NextConfig = {"
    assert config.count(anchor) == 1 and b"devIndicators" not in config
    out = {
        **src,
        "next.config.ts": config.replace(anchor, anchor + b"\n  devIndicators: false,"),
        "TASK.md": specification.encode(),
        "AGENTS.md": b"Keep the supplied source layout, dependencies, and public routes. Read TASK.md and CHECKS.md.\n",
        "CHECKS.md": f"# Available checks\n\n`{command}`\n".encode(),
        "study-basic.py": (HERE / "public-basic.py").read_bytes(),
    }
    if v:
        out["study-preservation.py"] = (HERE / "public-preservation.py").read_bytes()
        extra = f"\n`python study-preservation.py {kit} {task} http://localhost:3107`\n"
        out["CHECKS.md"] += extra.encode()
    return out


def main():
    spec = (HERE / "matched-task-cards.md").read_text(encoding="utf-8")
    intro, *sections = re.split(r"(?m)^## ", spec)
    tasks = dict(zip(("registration", "signout", "visibility"), sections, strict=True))
    rows = []
    for (kit, s), root in QUAD.items():
        files = source_files(root)
        for task, specification in tasks.items():
            statement = intro + "## " + specification
            v0, v1 = (overlay(files, task, statement, kit, v) for v in (0, 1))
            assert v1.keys() - v0.keys() == {"study-preservation.py"}
            assert [p for p in v0 if v0[p] != v1[p]] == ["CHECKS.md"]
            assert all(not Path(name).name.endswith("-qualification.json") for name in v1)
            for v, package in enumerate((v0, v1)):
                with tempfile.TemporaryDirectory(prefix="paper-account-package-") as scratch:
                    dest = Path(scratch)
                    for name, content in package.items():
                        path = dest / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(content)
                    manifest = {name: sha256((dest / name).read_bytes()).hexdigest() for name in sorted(package)}
                    assert len(manifest) == sum(p.is_file() for p in dest.rglob("*"))
                rows.append({"kit": kit, "task": task, "S": s, "V": v, "files": manifest})
    assert len(rows) == 24
    assert {r["task"] for r in rows} == tasks.keys()
    assert all(len({r["files"]["TASK.md"] for r in rows if r["task"] == task}) == 1 for task in tasks)
    (HERE / "two-kit-package-audit.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print("Assembled and checked all 24 account task packages.")


if __name__ == "__main__":
    main()
