# SmartKit qualification snapshot

Next.js App Router paths remain under src/app. Keep existing authentication,
ownership predicates, billing state semantics, and server/client boundaries.
Client components use 'use client'; server-only modules retain server-only imports.
Share validation schemas between callers. Revalidate affected routes after writes.
Keep the supplied layout when extending code. Resolve imports through @/.
Tests remain centralized under src/tests with the same test cases in both layouts.
Run pnpm check-types, pnpm test:run and pnpm build for relevant changes.

## Layout
Application domain modules live under src/features/{domain}. Within each domain, use components, hooks, actions, types, lib and emails as appropriate. Domain entry points and processing modules remain at the domain root.
