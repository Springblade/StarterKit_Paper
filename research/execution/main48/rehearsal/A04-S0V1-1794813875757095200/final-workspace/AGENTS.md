# SmartKit qualification snapshot

Next.js App Router paths remain under src/app. Keep existing authentication,
ownership predicates, billing state semantics, and server/client boundaries.
Client components use 'use client'; server-only modules retain server-only imports.
Share validation schemas between callers. Revalidate affected routes after writes.
Keep the supplied layout when extending code. Resolve imports through @/.
Tests remain centralized under src/tests with the same test cases in both layouts.
Run pnpm check-types, pnpm test:run and pnpm build for relevant changes.

## Layout
Application modules are grouped by technical role under src/components, src/hooks, src/actions, src/types, src/lib, src/emails and src/services. Within each role, use domain subdirectories; domain entry points and processing modules live under services.
