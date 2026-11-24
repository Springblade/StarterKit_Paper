# Assigned task: DP02

Add a labelled native GET dropdown All/User/Admin to `/dashboard/admin/users`.
Values are empty/user/admin. Missing, empty, invalid, case-mismatched or repeated
`role` parameters mean All. Submit/reload retain the effective choice. Rows and
total reflect the selected set, including zero matches with controls still present.
Keep per-account session-record counts, displayed metadata and descending created
date order. Ties do not prescribe a new tie-break rule. Counts remain counts of
all session records, not only unexpired sessions. Only admin may see the directory,
including direct requests. Reads must not change users/orders or expose session tokens.

Preserve the supplied layout and behavior outside this task. Do not change dependencies, globally disable cookie caching, or modify auth-library internals. You may add appropriate source files and use any correct implementation. No fixed file list is required.

## Local environment and tools

Dependencies are installed. A fresh PostgreSQL database is migrated/seeded and a Next.js development server is running at http://localhost:3107. Synthetic test accounts are listed in scripts/seed.ts; no real payment/email credentials are configured. Playwright 1.58.2 and Chromium are available in every condition. A Node check can load require('/opt/behavior/node_modules/playwright') and launch chromium with args: ['--no-sandbox']. You may write/run your own checks and use the browser.

Supplied checks: pnpm check-types; pnpm test:run; pnpm build; existing project scripts. Additional preservation command: pnpm test:preservation.

The wall-time limit is 900 seconds from CLI invocation, including check execution. Keep all work in this workspace and do not commit it. Finish with a brief account of changes and checks.
