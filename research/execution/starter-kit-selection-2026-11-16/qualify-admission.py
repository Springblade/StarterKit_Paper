"""Verify the two-kit account-task evidence and generate a prospective schedule."""

from hashlib import sha256
import itertools
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
KITS = ("smartkit", "nextjs-saas-starter")
TASKS = ("registration", "signout", "visibility")
SEED = 20261118


def verify_treatment(row, task):
    baseline = row["variant"] == "baseline"
    reference = row["variant"] == "reference"
    assert row["common_basic"] is True
    assert row["public_preservation"] == (baseline or reference)
    if task == "registration":
        assert row["new11"] == baseline and row["new12"] is True
        assert row["heldout_old11_login"] == (baseline or reference)
    elif task == "signout":
        assert row["confirm"] == {
            "confirm_prompt": not baseline,
            "signed_out_destination": True,
            "session_retained": not (baseline or reference),
        }
        for decision in ("cancel", "cancel-keyboard"):
            assert row[decision]["confirm_prompt"] == (not baseline)
            assert row[decision]["session_retained"] == (not baseline)
    else:
        assert row["toggle"] == (not baseline) and row["mask"] == (baseline or reference)


def allocation():
    rng = random.Random(SEED)
    blocks = list(itertools.product(KITS, TASKS, (1, 2)))
    rng.shuffle(blocks)
    slots = []
    for kit, task, repetition in blocks:
        conditions = list(itertools.product((0, 1), repeat=2))
        rng.shuffle(conditions)
        for s, v in conditions:
            slots.append(dict(kit=kit, task=task, repetition=repetition, S=s, V=v))
    assert len(slots) == 48
    assert len({tuple(slot.values()) for slot in slots}) == 48
    return slots


def main():
    evidence = {}
    for task, alternate in itertools.product(TASKS, (False, True)):
        suffix = "-alternate" if alternate else ""
        path = HERE / f"{task}-qualification{suffix}.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        fault = "legacy-fault" if task == "signout" else "fault"
        expected = set(itertools.product(KITS, (1, 2), ("baseline", "reference", fault)))
        assert len(rows) == len(expected)
        assert {(r["kit"], r["repeat"], r["variant"]) for r in rows} == expected
        for row in rows:
            assert row["alternate_layout"] is alternate
            verify_treatment(row, task)
        evidence[path.name] = sha256(path.read_bytes()).hexdigest()
    result = {
        "scope": "Fixed exploratory account workload, no agent outcomes or start release",
        "qualified_cases": 72,
        "evidence": evidence,
        "factor_mapping": {
            "S0": "SmartKit layered / Next.js SaaS Starter native",
            "S1": "SmartKit feature grouping / Next.js SaaS Starter relocated auth modules",
            "V0": "Common basic checks",
            "V1": "Common basic checks plus runnable task-specific preservation check",
        },
        "seed": SEED,
        "model_calls": 0,
        "slots": allocation(),
    }
    path = HERE / "two-kit-allocation-candidate.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Verified {result['qualified_cases']} instrument cases and {len(result['slots'])} prospective slots.")


if __name__ == "__main__":
    main()
