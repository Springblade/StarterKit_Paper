# Order baseline verification — 2026-11-10

Scope: local development baseline ownership and cancellation checks. These are instrument-development observations, not main-study agent outcomes.

## Contract exercised

- History and order-status reads are scoped to the signed-in owner.
- Unauthenticated callers cannot list, inspect or cancel orders.
- An owner may cancel a pending order once. Completed, cancelled, expired, missing and foreign orders must not be changed by cancellation.
- Status filtering in `listOrders` must preserve ownership restrictions.

This adopts an owner-scoped contract for `listOrders`, consistent with history/status/cancellation behavior. No application callers of `listOrders` were found before the repair; no admin-wide order listing contract was implemented. This decision should be retained in the study baseline specification.

## Fixtures and boundaries

`scripts/check-order-baseline.integration.ts` creates two ordinary users with real Better Auth password hashes, credential accounts, one plan, and four orders per user: pending/completed/cancelled/expired. Each execution uses UUID-scoped IDs and deletes only its own fixtures afterward. Expired orders have past expiry timestamps. The script refuses non-local databases and any database name other than `smartkit_orders_test`.

History and status API checks use real HTTP login cookies, server rendering and the actual PostgreSQL database. Server-action checks invoke the actual action implementations and SQL with only session lookup and Next cache invalidation stubbed. They do not prove the browser-to-server action transport or cache refresh behavior.

## Observations and repair

Before repair: **8/10 tests passed**. The two failures demonstrated that direct invocation of `listOrders` did not require a session and returned both users' orders. This was not reproduced as an unauthenticated network exploit; no application call site was found, and the history page uses a separate owner-scoped query.

Repair: `src/features/billing/actions/list-orders.ts` now requires a session and combines the owner predicate with the optional status predicate.

After repair: **10/10 integration tests passed**, and the existing **14/14 tests** and TypeScript check passed. The tests also verified unchanged rows following rejected cancellation and rejection of a repeated cancellation.

Production build after the action repair also passed (`logs/orders-build.log`). This confirms compilation only, not production database TLS connectivity. A post-test SQL check found zero remaining users, orders and plans in the dedicated database (`logs/orders-cleanup.log`).

Evidence:

- `logs/orders-before-fix.log`: original failures.
- `logs/orders-check-0.log`: integration checks after repair.
- `logs/orders-check-1.log`: TypeScript check.
- `logs/orders-check-2.log`: existing tests.
- `logs/orders-server.log`: development server requests.
- `logs/orders-migrate.log`: isolated database setup.
- `baseline-order-repair.patch`: action repair; reusable verification files are in the SmartKit working tree. Earlier baseline repair is recorded separately.

## Reproduce

From `research/SmartKit`, point the ignored `.env` to a dedicated local database named `smartkit_orders_test`. The verification used PostgreSQL 16 on port 55433 in container `smartkit-feasibility-pg`. Set `BETTER_AUTH_URL`, `NEXT_PUBLIC_BETTER_AUTH_URL`, and `NEXT_PUBLIC_APP_URL` to `http://localhost:3107` for the local server.

1. Start the dedicated PostgreSQL container and create the empty database if absent.
2. Run `pnpm db:migrate`.
3. In a separate terminal, run `pnpm exec next dev -p 3107`.
4. Run `pnpm exec vitest run --config vitest.orders.config.ts`.

No seed run is needed for this test: it creates its own fixtures. Existing unrelated rows are not deleted. The database and test server were stopped after verification.

## Interpretation and remaining work

The repaired baseline passes the specified ownership/status/cancellation checks. This is initial evidence that SmartKit contains meaningful behavior suitable for preservation testing, not proof of overall correctness or representativeness of starter kits.

Not covered: browser interaction, browser-triggered cancellation, payment/webhook/cron races, full security audit, production TLS setup, independent oracle review, or equivalent layouts. Next: qualify the history status-filter development task, with reference solution, acceptance checks and preservation checks; validate that the evaluator distinguishes deliberately incorrect patches. Do not count this fixture work as a qualified main-study task.
