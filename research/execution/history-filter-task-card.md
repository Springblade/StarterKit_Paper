# DEV-HISTORY-STATUS-01 — development task, not a main-study task

Origin: constructed from the SmartKit history workflow; no historical issue or user-demand evidence is claimed. The existing listOrders action already supports status filtering, but the history page has a separate query and no filter control.

Starting point: upstream revision `2c92d3920d967b9ebf0960ba7890754baa3c90d7` plus separately recorded migration/seed and listOrders ownership repairs. History-filter reference code must not be included in the task's starting snapshot.

## Requirement supplied to the implementer

Add a labelled status filter to the authenticated payment history page. Offer All statuses, Pending, Paid (stored as completed), Cancelled and Expired. Apply the chosen filter through a GET submission using the `status` query parameter. Reloading or opening that URL must preserve the selected option and displayed results. Selecting All statuses must restore the complete history for the current user.

Accept exactly pending/completed/cancelled/expired. Missing, empty, invalid or repeated status parameters fall back to All statuses. If a valid filter has no matches, show a clear empty-result message while retaining the filter and an accessible way to return to all orders.

Preserve authentication, ownership restrictions, descending creation-time ordering, and existing order information. Viewing/filtering must not alter stored orders or change the status API or cancellation behavior. Multiple correct implementations are allowed; no required file list, query method, component structure or patch is part of the task contract.

## Qualification evidence to collect

Acceptance: correct subsets for all four states, URL/selection agreement, functional GET form and reset, invalid input policy and empty results.

Preservation: cross-user exclusion for every filter, unfiltered history/order fields/order, unauthenticated redirect, unchanged database rows, and existing status/cancel checks.

Evaluator uses a real local development server, real login cookies, PostgreSQL and rendered HTML parsed as a DOM. Server action preservation tests stub only session/cache boundaries. This is not a browser interaction test or an independent human review.

Development fixtures: two ordinary users with four states each plus one user without orders. Fixture IDs are generated per run and removed afterward. Development fixtures and outcomes must not be reused as held-out main-study tasks or observations.

Only call this task development-qualified after the reference passes and deliberately incorrect implementations fail for the intended assertions. Layout portability and independent review remain separate gates.
