# Paired layout qualification — 2026-11-10

Status: both layouts pass the exercised local development contracts. Not a proof of equivalence for every possible execution. No coding-agent performance trial has been run.

## Snapshots and transformation

- `layouts/feature`: the existing domain-first layout, with the earlier baseline migration/seed and ownership repairs, and without the history-filter solution.
- `layouts/layered`: a role-first counterpart built from exactly the same inputs. Next.js `src/app` routes, database schema/migrations, UI primitives, public assets and test locations stay in place.
- `build-layout-variants.py`: stdlib-only generator that refuses to overwrite an existing snapshot directory.
- `layout-manifest.json`: original revision, source-to-destination mapping, SHA-256 file digests and instruction digests. The source is the recorded working tree, not an unchanged upstream commit.

Each snapshot contains 142 copied/transformed files plus its own AGENTS.md. Forty-seven modules move in the layered layout:

| Original | Role-first location |
|---|---|
| `src/features/{domain}/components/*` | `src/components/{domain}/*` |
| `.../hooks/*` | `src/hooks/{domain}/*` |
| `.../actions/*` | `src/actions/{domain}/*` |
| `.../types/*` | `src/types/{domain}/*` |
| `.../lib/*` | `src/lib/{domain}/*` |
| `.../emails/*` | `src/emails/{domain}/*` |
| Root processing modules/config/entry points | `src/services/{domain}/*` |
| Root `types.ts` | `src/types/{domain}.ts` |
| Auth `client.ts` | `src/lib/auth/client.ts` |

Imports/exports, dynamic imports and mock module paths are mechanically updated. Some relative paths become `@/` aliases. The generator resolves quoted local module paths to original module identities and checks that transformed code/config bodies are otherwise identical. It rejects path collisions. No business logic, dependency, schema, function signature, error handling or server/client directive was intentionally changed. One historical source comment still mentions a former features path; comments were preserved by the mechanical transformation.

Both original AGENTS.md files are replaced with the same common instructions and a layout-specific paragraph. Shared domain facts remain in the same README and code. The original feature-only instructions are not used to steer the layered counterpart. Existing tests stay in the same centralized locations to avoid also changing test placement.

## Behavioral checks

`check-layout-behavior.py` starts one development server at a time on localhost:3107, using the isolated local PostgreSQL `smartkit_orders_test` database. It creates/cleans fixtures through the previously qualified integration evaluator. For each layout it checks the unsolved baseline, temporarily applies the corresponding reference page, tests the development task, then restores and rechecks the unsolved baseline.

| Check | Feature | Layered |
|---|---|---|
| Frozen-lockfile dependency install | Pass | Pass |
| TypeScript | Pass | Pass |
| Existing unit/component suite | 14/14 | 14/14 |
| Production compilation | Pass | Pass |
| Baseline ownership/status/cancel integration | 10/10 | 10/10 |
| Reference history-filter task + preservation | 15/15 | 15/15 |
| Restored unsolved baseline | 10/10 | 10/10 |

The 5 filter-specific checks are intentionally excluded from baseline-only runs; their absence is the task to solve. Read the detailed test boundaries in `history-filter-qualification.md`: history/status use real HTTP and database; direct action checks stub session lookup and cache invalidation.

Evidence: `layout-behavior-results.json`, `logs/layout-{feature,layered}-{install,types,unit,build,baseline,reference,restored-baseline,server}.log`. `layout-snapshot-verification.json` confirms all 284 copied/transformed file hashes match after restoring solutions and the generated next-env declarations. `logs/layout-cleanup.log` confirms zero remaining fixture users/orders/plans. Development servers and the test database container were stopped.

## Reference isolation and reproducibility

Gold pages and patches are stored outside the snapshots:

- `history-reference-feature.tsx.txt` / `history-reference-feature.patch`.
- `history-reference-layered.tsx.txt` / `history-reference-layered.patch`.

The generator excludes `.git`, `.next`, node_modules, real `.env`, local memory and IDE instructions from its input set. For this local qualification only, ignored `.env` files were created from the known local test setup. Each snapshot ran `pnpm install --frozen-lockfile`. Production compilation passing does not resolve the separate production database TLS issue.

To repeat runtime checks, start the existing isolated test container, configure each snapshot with the same localhost:3107 auth/app URLs and the dedicated `smartkit_orders_test` database, and run `python research/execution/check-layout-behavior.py` from the Paper workspace. Fixtures reset on each run. The development-task reference is restored to baseline even on failure. Generation requires a new output location or explicit archival of previous snapshots; it will not silently overwrite them.

## Limits and next gate

These snapshots are qualification workspaces. They contain development evaluator files and are nested under the research workspace; they are not yet isolated agent trial packages. Both gold solutions and parent-workspace instructions/artifacts must be inaccessible in actual agent trials. No V0/V1 test-visibility allocation is claimed here.

Scope is one domain-first layout and one concrete role-first layout of SmartKit. Local structural checks and tested contracts support moving forward; browser interaction, production runtime, all billing integrations, independent review and general equivalence remain outside these observations. There is no evidence here that either layout improves agent outcomes.

Next: specify which checks the agent sees in V0 and V1, keep the final evaluator hidden and identical across all four cells, and build isolated resettable trial packages. Then perform the development pilot before locking main-study tasks and protocol.
