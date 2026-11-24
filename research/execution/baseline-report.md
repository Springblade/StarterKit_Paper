# SmartKit feasibility check — 2026-11-10

Status: preliminary; migration and local development authentication blockers repaired in the follow-up below. SmartKit remains a candidate, not a fully qualified experimental baseline. Earlier observations are retained as history.

## Snapshot and environment

- Repository: `research/SmartKit`, revision `2c92d3920d967b9ebf0960ba7890754baa3c90d7`; initially clean working tree.
- Windows host; Node 24.15.0; project-selected pnpm 11.7.0; Docker server 29.6.2.
- Isolated PostgreSQL 16 container: `smartkit-feasibility-pg`, localhost port 55433, database `smartkit_feasibility`. Existing containers/databases were not used.
- Installed with `pnpm install --frozen-lockfile`.
- Created ignored local `.env` from `.env.example`, pointing to the isolated database. Removed empty optional Resend API key and supplied a local development cron secret so production configuration validation could run. No real payment/email credentials used.

## Observed checks

| Check | Result | Evidence |
|---|---|---|
| Dependency installation | Passed | `logs/baseline-install.log` |
| `pnpm test:run` | Passed: 4 files, 14 tests; exit 0 | `logs/baseline-test-run.log` |
| `pnpm check-types` | Passed; exit 0 | `logs/baseline-check-types.log` |
| `pnpm build` | Passed; exit 0 | `logs/baseline-build.log` |
| `pnpm db:migrate` on empty database | Failed; exit 1 | `logs/baseline-migrate.log`, `logs/baseline-postgres.log` |
| Production server on port 3107 | Public home/sign-in returned HTTP 200 | `logs/baseline-http.json`, `logs/baseline-runtime.log` |
| Unauthenticated history request | Redirected to sign-in | `logs/baseline-http.json` |

Build warned about missing optional Google credentials. Existing unit/component tests do not establish database behavior. HTTP checks did not exercise authenticated behavior or browser interaction.

## Blocking observation

PostgreSQL rejected migration `src/database/migrations/0005_drop_github_provider.sql`, specifically `ALTER TYPE "public"."provider" DROP VALUE IF EXISTS 'github'`, with `syntax error at or near "VALUE"`. Direct invocation of the migration CLI also exited 1. The CLI output alone omitted the cause; the database log records it. No public tables remained after the failed migration transaction.

No application source or migrations were patched. Do not silently replace migrations with schema push and report the documented migration path as passing.

## Decision and next gate

Continue considering SmartKit, but do not freeze it or run main agent trials yet. Installation, compilation, tests and unauthenticated HTTP checks provide initial feasibility evidence; they do not qualify it as an experimental baseline.

Next: create a separately recorded baseline migration repair, rerun it on a fresh isolated database, then validate authenticated user/admin access and ownership/state behavior with test fixtures. After that, qualify one development task with a reference solution and independent acceptance/preservation checks, including deliberately incorrect patches. Port it to equivalent layouts before deciding whether to retain SmartKit for the main study.

Task qualification, evaluator validation, reset reproducibility and layout equivalence remain untested. This report supports no comparative claim about SmartKit versus other starter kits.

## Cleanup

The isolated database container was stopped and retained for inspection. The local environment and installed dependencies remain available for the next check. Logs contain only local test setup; no production credentials were used.

## Follow-up repair and verification — 2026-11-10

Authorized repair of baseline blockers; changes are recorded in `baseline-migration-repair.patch` (includes seed repair).

- `0005`: retain journal entry as a no-op; migration 0009 already rebuilds the provider enum without GitHub. No account rows are deleted.
- `0008`: drop the text default before converting role to enum, then restore the typed user default.
- `0010`: retain journal entry as a no-op because its SQL duplicated 0009, including ADD COLUMN statements.
- `scripts/seed.ts`: use Better Auth's own `hashPassword` instead of bcrypt; close the database pool after seeding; document migrations as the setup path. Existing seeded users are still skipped, so this change does not repair old bcrypt hashes in an existing database. Verification used a new test database.

Created another empty isolated database, `smartkit_feasibility_repaired`, and updated the ignored local environment to use it. Full migration chain passed (11 journal records); seed passed (2 users, 3 plans). Repeating migration and seed also exited 0. See `logs/baseline-migrate-fresh.log`, `baseline-seed-fresh.log`, `baseline-migrate-repeat.log`, `baseline-seed-repeat.log`, and `baseline-schema-repaired.log`.

Local development HTTP verification passed for both seeded roles: email/password login, non-null authenticated session, and history-page access. Normal user access to admin users ended at dashboard; admin access stayed on the admin users page. See `logs/baseline-auth-repaired.json` and `baseline-dev-repaired.log`. These were HTTP checks, not browser interaction or a complete authorization audit.

After changes, all 14 existing tests and TypeScript checks passed; `git diff --check` passed. Source revision remains the original commit plus the recorded patch; it must not be described as an unchanged upstream snapshot.

### Remaining limits

- Production-mode authentication against the local non-TLS PostgreSQL container failed because the pool enables SSL in production (`src/database/db.ts`). Runtime verification above used development mode, where this connection works. Production build success from the initial check does not establish production database connectivity.
- Better Auth warns that `nextCookies` should be last in the plugin list. Login/session checks passed; this warning was not repaired as part of the migration/seed fix.
- No cross-user order fixtures, order-state checks, qualified development task, evaluator validation or layout-equivalence demonstration yet.
- Historical migration edits are for qualifying this research baseline. This was not a rollout to an existing deployed database.

Next gate: define and exercise ownership/state contracts with multi-user order fixtures, then qualify the first development task. The repaired baseline has passed initial setup/authentication checks only.

## Order baseline follow-up

Ownership/status/cancellation checks are now implemented and executed; see `order-baseline-verification.md` for fixtures, boundaries, observations and reproduction. They identified a missing session/owner restriction in direct `listOrders` calls, repaired separately in `baseline-order-repair.patch`. After repair, 10/10 integration tests and the existing 14/14 tests passed, along with TypeScript checks. This supersedes the earlier statement that no cross-user order fixtures exist; task qualification and layout equivalence remain outstanding.

## Development-task follow-up

The history status-filter development task now has a contract, reference patch, a tested valid alternative and deliberately faulty variants. See `history-filter-qualification.md` for 15/15 passing integration checks, mutation results and limits. The working tree currently includes the reference solution: exclude its feature patch when assembling an unsolved experimental baseline. Development qualification is local and has not received independent review; layout equivalence and main-task qualification remain outstanding.

## Paired layout follow-up

Two unsolved qualification snapshots now exist under `layouts/feature` and `layouts/layered`. They pass TypeScript, 14 existing tests, production compilation, 10 baseline integration checks, and 15 checks with the temporary reference task. Both were restored to unsolved state and passed the 10 baseline checks again. See `layout-qualification.md` for the module mapping, hashes, evidence and limitations. This provides local equivalence evidence for the exercised contracts; four-condition test visibility, agent isolation and main-task qualification remain outstanding.

## Development smoke-pilot follow-up — 2026-11-11

Four isolated development packages have now been assembled and exercised with
one GPT-6 Luna High session per cell, using a 15-minute cap. All four patches
passed the frozen 29-check development final evaluator. See
`pilot-2026-11-11/report.md` for the visibility inventory, container isolation,
attempt/usage records, one pre-model setup failure, evaluator boundaries and
limits. This supersedes the earlier pending four-condition/isolation status for
this smoke task only. Main-task qualification and the main protocol remain open;
no comparative effect estimate is supported by these four development sessions.
