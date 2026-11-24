"""Planning sensitivity analysis, not a frozen main-study analysis or pilot data.

N is total agent trials; balanced allocation requires N = 4*T*R.
Cells are 00, 01, 10, 11. Primary contrasts are equally task-weighted S and V.
Independent binomial trials conditional on task probabilities are assumed.
Uniform task variation is bounded, with effect SD given in probability units.
No clipping, missingness, batch correlation, or fitted pilot variance is used.

Fixed-task inference uses conservative, finite-sample Hoeffding bounds.
Hypothetical task-population inference uses an approximate task-level t test;
its null rejection rate and coverage must be inspected, especially for small T.
Neither target makes a constructed convenience pool representative.
"""

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import norm, t


CONTRASTS = np.array([[-0.5, -0.5, 0.5, 0.5], [-0.5, 0.5, -0.5, 0.5]])


def holm(pvalues, alpha):
    """Two-hypothesis step-down family, one row per simulated study."""
    order = np.argsort(pvalues, axis=1)
    ordered = np.take_along_axis(pvalues, order, axis=1)
    rejected = np.logical_and.accumulate(ordered <= [alpha / 2, alpha], axis=1)
    return np.take_along_axis(rejected, np.argsort(order, axis=1), axis=1)


def wilson(events):
    n = events.size
    rate = float(events.mean())
    z = norm.ppf(0.975)
    den = 1 + z * z / n
    mid = (rate + z * z / (2 * n)) / den
    half = z * np.sqrt(rate * (1 - rate) / n + z * z / (4 * n * n)) / den
    return {"rate": rate, "mc95": [float(mid - half), float(mid + half)]}


def task_probabilities(rng, studies, tasks, base, base_sd, effects, effect_sd, interaction):
    # Centered coding gives exactly the specified marginal S and V per task.
    b = base + rng.uniform(-1, 1, (studies, tasks)) * np.sqrt(3) * base_sd
    d = np.asarray(effects) + rng.uniform(-1, 1, (studies, tasks, 2)) * np.sqrt(3) * effect_sd
    s, v = d[..., 0], d[..., 1]
    return np.stack([b - s / 2 - v / 2 + interaction / 4,
                     b - s / 2 + v / 2 - interaction / 4,
                     b + s / 2 - v / 2 - interaction / 4,
                     b + s / 2 + v / 2 + interaction / 4], axis=-1)


def validate_scenario(tasks, runs, base, base_sd, effects, effect_sd, interaction):
    if tasks < 2 or runs < 4 * tasks or runs % (4 * tasks):
        raise ValueError("Require T >= 2 and total N divisible by 4*T, with R >= 1.")
    if not 0 < base < 1 or base_sd < 0 or effect_sd < 0:
        raise ValueError("Require 0 < base < 1 and nonnegative SDs.")
    radius = (np.sqrt(3) * base_sd + np.abs(effects).sum() / 2
              + np.sqrt(3) * effect_sd + abs(interaction) / 4)
    if radius > min(base, 1 - base):
        raise ValueError("Scenario admits probabilities outside [0,1]; reduce SD/effects or change base. No clipping is allowed.")


def infer(contrasts, runs, alpha, target):
    estimates = contrasts.mean(axis=1)
    if target == "fixed-tasks":
        # Each observation has weight +/-2/N: sum(weights**2) = 4/N.
        half = np.full_like(estimates, np.sqrt(2 * np.log(2 / alpha) / runs))
        family_half = np.full_like(estimates, np.sqrt(2 * np.log(4 / alpha) / runs))
        pvalues = np.minimum(1, 2 * np.exp(-runs * estimates**2 / 2))
    else:
        tasks = contrasts.shape[1]
        se = contrasts.std(axis=1, ddof=1) / np.sqrt(tasks)
        half = t.ppf(1 - alpha / 2, tasks - 1) * se
        family_half = t.ppf(1 - alpha / 4, tasks - 1) * se
        statistic = np.divide(np.abs(estimates), se, out=np.zeros_like(se), where=se > 0)
        pvalues = 2 * t.sf(statistic, tasks - 1)
        # A degenerate task sample gives no defensible variance estimate.
        # Keep these studies in the denominator, as non-rejections with full CIs.
        pvalues = np.where(se == 0, 1, pvalues)
        half = np.where(se == 0, 2, half)
        family_half = np.where(se == 0, 2, family_half)
    return estimates, half, family_half, pvalues


def simulate(*, tasks, runs, base, base_sd, effects, effect_sd, interaction,
             simulations, alpha, anchor, seed, target):
    validate_scenario(tasks, runs, base, base_sd, effects, effect_sd, interaction)
    rng = np.random.default_rng(seed)
    # Fixed tasks are drawn once, then held across Monte Carlo replications.
    # The hypothetical population target redraws tasks in each replication.
    if target == "fixed-tasks":
        # Symmetric task pairs keep the finite-set marginal truths exactly at
        # the requested effects, including the null calibration scenarios.
        center = task_probabilities(rng, 1, 1, base, 0, effects, 0, interaction)
        first = task_probabilities(rng, 1, tasks // 2, base, base_sd, effects, effect_sd, interaction)
        pieces = [first, 2 * center - first]
        if tasks % 2:
            pieces.append(center)
        p = np.concatenate(pieces, axis=1)
    else:
        p = task_probabilities(rng, simulations, tasks, base, base_sd, effects, effect_sd, interaction)
    r = runs // (4 * tasks)
    counts = rng.binomial(r, p, size=(simulations, tasks, 4))
    contrasts = counts / r @ CONTRASTS.T
    truth = (p @ CONTRASTS.T).mean(axis=1) if target == "fixed-tasks" else np.asarray(effects)
    estimates, half, family_half, pvalues = infer(contrasts, runs, alpha, target)
    rejects = holm(pvalues, alpha)
    result = {"T": tasks, "N": runs, "R_per_cell_task": r, "target": target,
              "base": base, "baseline_task_sd": base_sd, "effects_S_V": list(effects),
              "task_effect_sd": effect_sd, "interaction": interaction, "simulations": simulations,
              "alpha": alpha, "anchor_pp": 100 * anchor, "seed": seed,
              "any_primary_rejected": wilson(rejects.any(axis=1)),
              "both_primary_rejected": wilson(rejects.all(axis=1)),
              "family_interval_coverage": wilson((np.abs(estimates - truth) <= family_half).all(axis=1)),
              "all_pass_or_all_fail_cell_fraction": float(((counts == 0) | (counts == r)).mean())}
    for j, name in enumerate(["S", "V"]):
        result[name] = {"truth_mean": float(np.asarray(truth)[..., j].mean()),
                        "estimate_mean": float(estimates[:, j].mean()),
                        "holm_rejection": wilson(rejects[:, j]),
                        "interval_coverage": wilson(np.abs(estimates[:, j] - np.asarray(truth)[..., j]) <= half[:, j]),
                        "median_interval_width_pp": float(200 * np.median(half[:, j])),
                        "median_family_interval_width_pp": float(200 * np.median(family_half[:, j])),
                        "halfwidth_at_most_anchor": wilson(half[:, j] <= anchor),
                        "family_halfwidth_at_most_anchor": wilson(family_half[:, j] <= anchor),
                        "degenerate_task_variance_fraction": float((contrasts[:, :, j].std(axis=1) == 0).mean())}
    return result


def self_check():
    assert np.array_equal(holm(np.array([[.01, .04], [.03, .04], [.8, .001]]), .05),
                          [[True, True], [False, False], [False, True]])
    p = task_probabilities(np.random.default_rng(1), 1, 8, .5, 0, [.1, .06], 0, .04)
    assert np.allclose(p @ CONTRASTS.T, [.1, .06])
    assert np.allclose(p[..., 3] - p[..., 2] - p[..., 1] + p[..., 0], .04)
    zero = np.zeros((20, 8, 2))
    _, h, _, pv = infer(zero, 96, .05, "hypothetical-task-population")
    assert np.all(pv == 1) and np.all(h == 2)
    _, h, _, _ = infer(zero, 96, .05, "fixed-tasks")
    assert np.allclose(h, np.sqrt(2 * np.log(40) / 96))
    try:
        validate_scenario(8, 95, .5, .05, [.1, .1], .05, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Unbalanced N was accepted")
    kwargs = dict(tasks=8, runs=96, base=.5, base_sd=.05, effects=[0, 0], effect_sd=.05,
                  interaction=0, simulations=100, alpha=.05, anchor=.1, seed=12, target="fixed-tasks")
    assert simulate(**kwargs) == simulate(**kwargs)
    print("self-check passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=int, nargs="+", default=[8, 10, 17, 40, 120, 200])
    parser.add_argument("--repetitions", type=int, nargs="+", default=[3, 10])
    parser.add_argument("--N", type=int, help="Total trials; requires one T and replaces repetitions.")
    parser.add_argument("--effect-sd", type=float, nargs="+", default=[0, .05, .10])
    parser.add_argument("--base", type=float, default=.5)
    parser.add_argument("--base-sd", type=float, default=.05)
    parser.add_argument("--effects", type=float, nargs=2, default=[.10, .10], metavar=("S", "V"))
    parser.add_argument("--interaction", type=float, default=0)
    parser.add_argument("--simulations", type=int, default=5000)
    parser.add_argument("--alpha", type=float, default=.05)
    parser.add_argument("--anchor", type=float, default=.10, help="Planning anchor; not an equivalence margin.")
    parser.add_argument("--seed", type=int, default=20261112)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.simulations < 100 or not 0 < args.alpha < 1 or not 0 < args.anchor < 1:
        parser.error("Require simulations >= 100, 0 < alpha < 1 and 0 < anchor < 1.")
    if args.N is not None and len(args.tasks) != 1:
        parser.error("--N requires exactly one --tasks value.")
    rows = []
    counter = 0
    for tasks in args.tasks:
        totals = [args.N] if args.N is not None else [4 * tasks * r for r in args.repetitions]
        for runs in totals:
            for sd in args.effect_sd:
                # Partial nulls are needed to check strong family-wise control.
                scenarios = {"global-null": [0, 0], "S-only": [args.effects[0], 0],
                             "V-only": [0, args.effects[1]], "both-effects": args.effects}
                for scenario, effects in scenarios.items():
                    for target in ["fixed-tasks", "hypothetical-task-population"]:
                        try:
                            row = simulate(tasks=tasks, runs=runs, base=args.base, base_sd=args.base_sd,
                                           effects=effects, effect_sd=sd, interaction=args.interaction,
                                           simulations=args.simulations, alpha=args.alpha, anchor=args.anchor,
                                           seed=args.seed + counter, target=target)
                        except ValueError as error:
                            parser.error(str(error))
                        row["scenario"] = scenario
                        nulls = np.flatnonzero(np.asarray(effects) == 0)
                        # Holm false rejection for the true null subset, including partial nulls.
                        if len(nulls) == 2:
                            row["null_family_error"] = row["any_primary_rejected"]
                        elif len(nulls) == 1:
                            row["null_family_error"] = row[["S", "V"][nulls[0]]]["holm_rejection"]
                        rows.append(row)
                        counter += 1
    payload = {"kind": "assumption-based-planning-simulation", "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
               "notes": ["No empirical task count or pilot outcomes used.",
                         "Task-population t intervals/tests are approximate; inspect null error and coverage.",
                         "Fixed-task Hoeffding inference is conservative under independent trials.",
                         "Family intervals use Bonferroni; tests use Holm. Neither is an equivalence test.",
                         "The 10pp anchor is not a frozen precision target or expected effect."], "results": rows}
    content = json.dumps(payload, indent=2, allow_nan=False)
    if args.output:
        args.output.write_text(content + "\n", encoding="utf-8")
        print(f"Wrote {len(rows)} scenarios to {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
