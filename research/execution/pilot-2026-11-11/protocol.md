# Development smoke pilot, 11 November 2026

Purpose is to exercise the four-cell runner and identify practical failures. One
session per cell on DEV-HISTORY-STATUS-01 is not a sample for estimating layout or
verification effects and will not enter main-study outcomes.

Author-approved choices are existing Codex Plus allowance with ChatGPT login,
GPT-6 Luna High at Standard speed, four fresh sessions and 15 minutes maximum per
session. No paid API credentials or additional credits are requested. The model
configuration is fixed across the four cells. Exact backend weights may change
behind an alias; the requested identifier, CLI version, times and available usage
events are recorded rather than claiming an immutable model snapshot.

## Treatment inventory

| Cell | Organization | Supplied verification |
|---|---|---|
| S0V0 | Role-first | Existing upstream unit/component tests, TypeScript/build and ordinary project scripts |
| S1V0 | Feature-first | Same basic tests and tools |
| S0V1 | Role-first | Same baseline plus 10 behavioral preservation checks |
| S1V1 | Feature-first | Same baseline plus the corresponding 10 preservation checks |

V1 adds `pnpm test:behavior`, its Vitest config, and a preservation-only test file.
These tests exercise own/foreign history, status access, anonymous access and
cancel/state restrictions using real PostgreSQL/HTTP or action calls with session
and cache stubs. The development feature-acceptance describe block is removed
from every visible package. V0 retains upstream scripts and may create tests.
Existing basic checks are not weakened. Both V levels receive identical public
requirements, including dropdown, query-input policy and required ownership.

The final evaluator is independently authored for this development pilot, using
sparse histories, two plans, different order dates, duplicate-status counts,
owner-specific empty subsets and separate query-input probes. Its 29 checks are
not included in agent packages. It checks HTTP/DOM behavior and persisted orders,
not browser hydration or full application correctness. It does not certify every
entry point or real payment integration. Final scores are not fed back to agents.

## Isolation and fixed environment

Agents run inside new, unprivileged Docker containers with no host bind mounts,
Docker socket, host PID namespace, research folder, gold solutions, final tests,
user configuration, user rules, or previous repository history. The common image
has Node 24, pnpm 11.7.0, Codex CLI 0.166.0 and dependencies from the same lockfile.
Model commands are executed without the inner CLI sandbox only inside this
external container boundary. Code and local fixture database are copied into
fresh environments per cell. The CLI is initialized with the author's existing
ChatGPT credential file, stored outside the application workspace and never added
to source artifacts. No credential value is printed or included in a manifest.

The public application is started before model time begins. Identical development
users/plans are seeded; test credentials are local-only. A private network gives
each trial access to its own PostgreSQL container. No host research path is
mounted. All actual model sessions get the same task prompt and environment
description, with only layout descriptions and visible test inventories varying.

Per-cell file hashes, image IDs and isolation audits are archived. The root
research checkout and qualification snapshots are not edited by the trial.
Final patch and code archive are captured before scoring in a fresh container
without ChatGPT credentials. Agent-visible tests do not determine final scoring.

## Allocation and attempt rules

Seed 20261111 produces S0V0, S1V0, S0V1, S1V1. Runs are serial, one per cell.
Allocation is recorded before any model outcome is seen. Wall clock starts at
CLI invocation and ends at completion or 900 seconds. No per-trial token cap is
claimed for this smoke test; emitted token usage is archived. Limits for the main
study remain to be selected.

Timeouts within an otherwise functioning environment retain the partial patch
for scoring and are reported explicitly. Quota, authentication, transport or
model-availability interruptions are infrastructure events and stop the batch;
they are not joint failures and are not silently retried. Every attempt remains
in the ledger. No unattended reset time or next-day restart is assumed. An
incomplete record requires adjudication before the runner may retry that cell.

Qualification before model execution requires preservation to pass on both
unsolved baselines, acceptance to fail on those baselines, the reference to pass
on both, and the V1 package to run successfully without the solution. The hidden
evaluator hash is recorded before the pilot. This smoke protocol is not a
preregistration or a finalized confirmatory protocol.

Commands are `python pilot.py prepare`, `python pilot.py qualify`, then
`python pilot.py run` from this directory. The first command refuses overwrites;
the final command skips completed cells and refuses silent reruns of incomplete
attempts. It consumes the available subscription allowance.
