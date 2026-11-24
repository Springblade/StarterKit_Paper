# Assigned task: DP03

Add a labelled display-name field and Save name control on Settings. Trim leading
and trailing whitespace, then accept 1–80 Unicode code points; support Vietnamese
and supplementary-plane characters. Empty/whitespace-only and 81-code-point names
are rejected server-side without changing business records. Do not conflate UTF-16
code units or grapheme clusters with code points. A successful submission must
persist the name and show it in Settings in the same browser session and after
reload. Another fresh sign-in still works. API/server-action implementation is free.

The caller may update only their own name. Tampered user IDs, email, role and
verification fields cannot modify another account or protected fields. Rejecting
the tampered request or ignoring unauthorized fields are both acceptable. Anonymous
writes are denied. Existing Settings display treats the stored name as text, and
existing sign-in, order access and persisted order records remain intact. The
task does not require new length rules on unrelated existing auth endpoints.

Preserve the supplied layout and behavior outside this task. Do not change dependencies, globally disable cookie caching, or modify auth-library internals. You may add appropriate source files and use any correct implementation. No fixed file list is required.

## Local environment and tools

Dependencies are installed. A fresh PostgreSQL database is migrated/seeded and a Next.js development server is running at http://localhost:3107. Synthetic test accounts are listed in scripts/seed.ts; no real payment/email credentials are configured. Playwright 1.58.2 and Chromium are available in every condition. A Node check can load require('/opt/behavior/node_modules/playwright') and launch chromium with args: ['--no-sandbox']. You may write/run your own checks and use the browser.

Supplied checks: pnpm check-types; pnpm test:run; pnpm build; existing project scripts. Additional preservation command: pnpm test:preservation.

The wall-time limit is 900 seconds from CLI invocation, including check execution. Keep all work in this workspace and do not commit it. Finish with a brief account of changes and checks.
