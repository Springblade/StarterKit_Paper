# Static source check supporting task refinement

All paths below are relative to `research/SmartKit/`. These observations are not runtime validation.

- `src/features/billing/actions/list-orders.ts`: the input schema has an optional status parameter; `whereClause` uses order status. The inspected function does not itself add the signed-in-user predicate used by the history page. Intended caller/access policy remains to be confirmed; no live exploit or runtime security verdict is claimed.
- `src/app/dashboard/billing/history/page.tsx`: calls `requireAuth`, obtains the session user ID, queries orders with `eq(orders.userId, userId)`, and renders the history table. No filter control is present in the inspected page. The status-filter candidate therefore concerns the history interaction and safe query path.
- `src/app/dashboard/admin/users/page.tsx`: calls `requireAdmin` and renders users/roles. No role filter is present in the inspected page. Admission of an admin-filter task still requires a complete contract and executable qualification.
- `src/features/billing/actions/cancel-order.ts`: the update predicate combines order ID, session user ID, and pending state. It supports a source-level preservation candidate for batch cancellation. Atomic versus partial batch semantics remain unspecified.
- `src/tests/features/billing/process-sepay-payload.test.ts`: mocks payment persistence and order completion. Passing that suite cannot independently establish real database transaction/uniqueness behavior.

The original six-row audit CSV is preserved as historical planning data. The inventory count figure is not relabeled as a validated benchmark after this inspection.
