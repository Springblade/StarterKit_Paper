# Assigned development task

Add a labelled native dropdown status filter to the authenticated payment history page. Offer All statuses, Pending, Paid (stored as completed), Cancelled and Expired. Apply the chosen filter through a GET submission using the `status` query parameter. Reloading or opening that URL must preserve the selected option and displayed results. Selecting All statuses must restore the complete history for the current user.

Accept exactly pending/completed/cancelled/expired. Missing, empty, invalid or repeated status parameters fall back to All statuses. If a valid filter has no matches, show a clear empty-result message while retaining the filter and an accessible way to return to all orders.

Preserve authentication, ownership restrictions, descending creation-time ordering, and existing order information. Viewing/filtering must not alter stored orders or change the status API or cancellation behavior. Multiple correct implementations are allowed; no required file list, query method, component structure or patch is part of the task contract.


## Local environment
Dependencies are installed. A fresh local test database is migrated and seeded. A Next development server is running at http://localhost:3107. Test accounts are listed by scripts/seed.ts. No real payment or email service is configured.

Available supplied checks: pnpm check-types; pnpm test:run; pnpm build. You may write and run your own checks. Keep changes in this workspace and do not commit them. The same 15-minute wall-time limit applies to every condition. Finish with a short account of your changes and checks.
