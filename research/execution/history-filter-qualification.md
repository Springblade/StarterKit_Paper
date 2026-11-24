# Development task qualification — history status filter

Date: 2026-11-10. Status: locally development-qualified for the exercised contracts; not an independently reviewed main-study task and not yet ported to both layouts.

## Deliverables

- `history-filter-task-card.md`: implementer-facing behavior contract and provenance.
- `history-filter-reference.patch`: reference feature patch relative to the baseline history page.
- `history-page-before-filter.tsx.txt`: exact pre-feature page saved before implementation.
- `SmartKit/scripts/check-order-baseline.integration.ts`: 10 existing baseline checks plus 5 filter-task checks.
- `SmartKit/vitest.orders.config.ts`: explicit integration configuration; no extra packages installed.
- `verify-history-filter-mutations.py`: development evaluator probes with page restoration in a finally block.

The working tree currently contains the reference implementation. The task starting snapshot must exclude `history-filter-reference.patch`; retain migration/seed and ownership repairs. These repairs, reference solution and evaluator are distinct artifacts. No baseline/task set has been frozen or committed by this work.

## Reference behavior

The history page offers a labelled native select and GET form, backed by a status query parameter. It accepts pending/completed/cancelled/expired, with completed labelled Paid. All statuses is represented by the empty value. Invalid or repeated parameters fall back to All statuses. Valid filters with no matches have a clear message and a View all orders link. The SQL combines owner and optional status predicates; descending creation time and existing row data remain intact.

## Evaluator and evidence

The isolated local `smartkit_orders_test` PostgreSQL database is shared with a local development server on port 3107. Each run creates three ordinary users: two with one order in each of four states, one without orders. The evaluator performs real HTTP login, parses server-rendered HTML and checks exact fixture order codes. It checks every status for both owners, URL/selection agreement, controls/reset, invalid inputs, ordering, empty results, unchanged order rows and unauthenticated redirects. Existing action checks still use stubbed session/cache boundaries with real SQL.

The initial HTML parser, Happy DOM, misreported the selected value in a minimal native select example. A standalone comparison with installed JSDOM showed the correct value. The evaluator now uses JSDOM without executing page scripts. Selection checks were retained rather than removed.

| Implementation | Observed result | Evidence |
|---|---|---|
| Unsolved baseline | 4 failures, 11 passes | `logs/history-filter-unsolved.log` |
| SQL-filter reference | 15/15 pass | `logs/history-filter-reference-final.log` |
| Ignore status filter | 1 assertion failure | `logs/history-filter-ignore-filter.log` |
| Remove ownership predicate | 6 assertion failures, including foreign codes in history | `logs/history-filter-remove-owner.log` |
| Always query pending | 1 assertion failure on completed subset | `logs/history-filter-wrong-status.log` |
| Correct in-memory filtering after owner-scoped query | 15/15 pass | `logs/history-filter-correct-in-memory-filter.log` |

Mutation outcomes and individual variant patches are retained in `logs/history-filter-mutation-results.json` and `logs/history-filter-*.patch`. The deliberately incorrect variants failed behavioral assertions, not merely compilation or infrastructure checks. The alternative correct implementation passed, providing limited evidence that the evaluator accepts more than the SQL reference approach. The reference was restored and passed again afterward.

Existing 14 unit/component tests and TypeScript passed after the feature; see `logs/history-filter-check-1.log` and `history-filter-check-0.log` respectively. Production build passed (`logs/history-filter-build.log`); this does not establish production TLS connectivity. Post-test SQL confirmed zero remaining users/orders/plans (`logs/history-filter-cleanup.log`); test server and container were stopped.

## Reproduce

Follow the database/server setup in `order-baseline-verification.md`. With the server running and local environment pointing to `smartkit_orders_test`, run:

```powershell
pnpm exec vitest run --config vitest.orders.config.ts
python ../execution/verify-history-filter-mutations.py
```

Run mutation probes alone while nobody else edits the page; they temporarily replace the reference page and restore its exact bytes. The integration command needs the history-filter reference applied to pass all 15 cases. To exercise only baseline behavior on an unsolved task, use `pnpm exec vitest run --config vitest.orders.config.ts -t "real HTTP ownership checks|actual server actions"`, rather than reporting task acceptance failures as baseline defects.

## Interpretation and next gate

This supplies a concrete development example of extending SmartKit while checking preservation. It does not show that one layout improves agent performance, that these checks detect every defect, or that the task represents typical SaaS requirements.

Browser interaction/hydration, independent review, performance, and error/loading UX are not qualified by these HTTP/DOM checks. Test fixtures and gold patches have been seen during instrument development; keep this task outside held-out main-study outcomes.

Next gate: construct equivalent layered/feature baseline variants and port this development task, reference solution and evaluator to both. Preserve identical logic, domain information, dependencies, instructions appropriate to each layout, and check visibility. Freeze task contracts and review limits separately before main trials.
