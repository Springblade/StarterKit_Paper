"""Audit the two-kit task packages and generate the balanced candidate schedule."""

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import runpy
import subprocess
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "starter-kit-selection-2026-11-16"
KITS = {
    "nextjs-saas-starter": "6e33e58b1e553a41fe22e6b941a7229a002de361",
    "makerkit-lite": "9ff430df9c58516add0136bd01ed800ce551675e",
}
TASKS = ("profile", "signout", "visibility")
SEED = 20261119


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def sources(root, added):
    names = git(root, "ls-files", "-z").decode("utf-8").rstrip("\0").split("\0")
    names = (set(names) | set(added)) - {""}
    return {
        name: (root / name).read_bytes()
        for name in sorted(names)
        if (root / name).is_file() and not any(p.startswith(".env") and p != ".env.example" for p in Path(name).parts)
    }


def packages(root, kit, s, added, cards):
    files = sources(root, added)
    assert {"package.json", "pnpm-lock.yaml", "README.md"} <= files.keys()
    basic = (HERE / "study_basic.py").read_bytes()
    extra = (HERE / "study_preservation.py").read_bytes()
    doc = ("# Available checks\n\nRun these commands from the workspace while the local study runtime is available. "
           "The runtime provides the base URL and synthetic fixture details.\n\n"
           f"\x60python study_basic.py {kit} BASE_URL SMOKE_EMAIL SMOKE_PASSWORD\x60\n")
    rows = []
    for task, spec in cards.items():
        v0 = {**files, "TASK.md": spec.encode(), "study_basic.py": basic, "CHECKS.md": doc.encode()}
        option = ' --saved-name "  Hoa   Nguyen  "' if task == "profile" else ""
        command = f"\n\x60python study_preservation.py {kit} {task} BASE_URL PRESERVATION_EMAIL PRESERVATION_PASSWORD{option}\x60\n"
        v1 = {**v0, "study_preservation.py": extra, "CHECKS.md": v0["CHECKS.md"] + command.encode()}
        assert v1.keys() - v0.keys() == {"study_preservation.py"}
        assert [name for name in v0 if v0[name] != v1[name]] == ["CHECKS.md"]
        for v, package in enumerate((v0, v1)):
            assert all(not name.endswith(("-cases.json", "-profile.json", "profile-checks.py")) for name in package)
            rows.append(dict(kit=kit, task=task, S=s, V=v,
                             files={name: sha(content) for name, content in package.items()}))
    return rows


def audit_packages(inputs):
    intro, *scopes = re.split(r"(?m)^## ", (HERE / "task-cards.md").read_text(encoding="utf-8"))
    cards = {key: intro + "## " + body for key, body in zip(TASKS, scopes, strict=True)}
    makerkit = runpy.run_path(str(HERE / "qualify-makerkit.py"))
    nextjs = runpy.run_path(str(OLD / "prepare-external-layout.py"))
    relocate_nextjs = nextjs["main"]
    rows = []
    with TemporaryDirectory(prefix="paper-audit-replacement-") as temp:
        for kit, layout in itertools.product(KITS, (0, 1)):
            root = Path(temp) / f"{kit}-{layout}"
            subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout",
                            str(inputs[kit]), str(root)], check=True)
            git(root, "checkout", "--quiet", "--detach", KITS[kit])
            if kit == "makerkit-lite":
                with makerkit["repaired_baseline"](root), makerkit["layout"](root, bool(layout)):
                    rows.extend(packages(root, kit, layout, makerkit["MOVES"].values() if layout else (), cards))
            else:
                if layout:
                    relocate_nextjs.__globals__["ROOT"] = root
                    relocate_nextjs()
                rows.extend(packages(root, kit, layout, nextjs["MOVES"].values() if layout else (), cards))
    assert len(rows) == 24
    assert all(len({r["files"]["TASK.md"] for r in rows if r["task"] == task}) == 1 for task in TASKS)
    out = HERE / "package-audit.json"
    out.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return out


def verify_evidence():
    def read(name):
        return json.loads((HERE / name).read_text(encoding="utf-8"))

    nextjs = [row for row in read("nextjs-cases.json") if row["task"] in TASKS]
    nextjs += read("nextjs-profile.json")
    makerkit = read("makerkit-cases.json")
    types = read("makerkit-type-audit.json")
    assert len(types) == 6
    assert {(r["layout"], r["bundled_variant"]) for r in types if r["typecheck"]} == set(
        itertools.product((0, 1), ("baseline", "reference", "regression")))
    assert len(nextjs) == len(makerkit) == 36
    expect = set(itertools.product(TASKS, (0, 1), (1, 2), ("baseline", "reference", "regression")))
    aliases = {"legacy-fault": "regression", "fault": "regression"}
    for kit, rows in zip(KITS, (nextjs, makerkit), strict=True):
        seen = set()
        for row in rows:
            kind = aliases.get(row["variant"], row["variant"])
            task = row["task"]
            if kit == "makerkit-lite":
                layout, basic, result = row["layout"], row["basic"], row["observed"]
            else:
                layout, basic, result = int(row["alternate_layout"]), row["common_basic"], row
            seen.add((task, layout, row["repeat"], kind))
            assert basic
            if task == "profile":
                assert result["stored_normalized"] == (kind != "baseline")
                assert result["visible_legacy_name_preserved"] == (kind != "regression")
                assert result["heldout_legacy_name_preserved"] == (kind != "regression")
            elif task == "visibility":
                mask = result["masked" if kit == "makerkit-lite" else "mask"]
                assert mask == (kind != "regression") and result["toggle"] == (kind != "baseline")
            else:
                retained = "retained" if kit == "makerkit-lite" else "session_retained"
                assert result["confirm"][retained] == (kind == "regression")
                for key in ("confirm", "cancel", "keyboard" if kit == "makerkit-lite" else "cancel-keyboard"):
                    prompt = "prompt" if kit == "makerkit-lite" else "confirm_prompt"
                    assert result[key][prompt] == (kind != "baseline")
                    assert result[key][retained] == (kind == "regression" or (kind == "reference" and key != "confirm"))
        assert seen == expect
    for file, field in (("nextjs-rehearsal.json", None), ("makerkit-rehearsal.json", "observed")):
        baseline, replay = read(file)
        assert baseline["variant"] == "baseline" and replay["variant"] == "reference"
        initial, final = (row[field] if field else row for row in (baseline, replay))
        assert initial["public_package_checks"] and final["public_package_checks"]
        assert final["alternative"] and len(final["patch_sha256"]) == 3
        assert not initial["stored_normalized"] and final["stored_normalized"]
        assert initial["heldout_legacy_name_preserved"] and final["heldout_legacy_name_preserved"]


def allocation():
    rng = random.Random(SEED)
    blocks = list(itertools.product(KITS, TASKS, (1, 2)))
    rng.shuffle(blocks)
    slots = []
    for kit, task, r in blocks:
        arms = list(itertools.product((0, 1), repeat=2))
        rng.shuffle(arms)
        slots.extend(dict(kit=kit, task=task, repetition=r, S=s, V=v) for s, v in arms)
    assert len(slots) == 48
    assert Counter(Counter((s["kit"], s["task"], s["S"], s["V"]) for s in slots).values()) == {2: 24}
    return slots


def main():
    inputs = dict(zip(KITS, map(Path, sys.argv[1:]), strict=True))
    package_audit = audit_packages(inputs)
    verify_evidence()
    docs = ["nextjs-cases.json", "nextjs-profile.json", "makerkit-cases.json",
            "nextjs-rehearsal.json", "makerkit-rehearsal.json", "makerkit-type-audit.json",
            "task-cards.md", "study_basic.py", "study_preservation.py", package_audit.name]
    record = dict(status="candidate_schedule", model_calls=0, qualified_cases=72,
                  revisions=KITS, seed=SEED,
                  evidence={name: sha((HERE / name).read_bytes()) for name in docs},
                  slots=allocation())
    (HERE / "allocation-candidate.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Audit passed for 72 instrument cases, 24 package configurations, and 48 prospective slots.")


if __name__ == "__main__":
    main()
