# Expanded-pilot preparation and qualification

Status: **technical qualification and pipeline rehearsal completed; awaiting author pilot release**. No new model invocation occurred. Current evidence is summarized in `qualification-summary.json`; `pilot.py audit` validates the technical freeze. The
author asked the assistant to complete technical preparation autonomously and
return at the pilot-start gate. That instruction does not authorize starting pilot.

## Scope and unchanged baseline

- DP-02: admin role-filter calibration, development-only.
- DP-03: display-name editing; main reuse targets evaluation-ready after gates,
  technical freeze and author pilot release; eligibility remains independent of
  pilot pass/fail/time. Main outcomes require fresh sessions.
- DP-04: hold/development-only. No auth-cache repair or contract v2 was introduced.
- Replacement discovery remains in the registry; no replacement was selected from
  agent outcomes, because no new agent trial has occurred.

Task cards and the requirement-to-check matrix are in [task-cards.md](task-cards.md).
These are explicitly constructed tasks and assistant-authored artifacts, not
historical issues or independently reviewed specifications.

All application source comes from the previously recorded unsolved feature/layered
snapshots. Snapshot digests are checked during packaging. The SmartKit clone's
development history-filter reference is not used as a starting implementation.
No shared authentication/cache logic, dependency version or schema was repaired.

## Runtime and authoritative sources

The common image adds Playwright 1.58.2 and Chromium 145.0.7632.6 to the existing
Node v24.22.2 image. Installed application versions are Next.js 16.2.12, Better Auth
1.6.25 and React 18.3.1. PostgreSQL is the same local 16-alpine service family.
Auth is real HTTP authentication with separate browser-cookie contexts and real
PostgreSQL records. No production email/payment service or provider credentials
are supplied during preparation.

The expanded harness uses `next dev --webpack`, consistently in all conditions.
This is a recorded harness change from the earlier Turbopack smoke-pilot runner,
made before any expanded-pilot outcome. It does not establish a unique root cause
for earlier stalls; final-version repeated qualification must demonstrate its
operational suitability.

Sources consulted and checked against the installed implementation/runtime:

- [Better Auth user/update APIs](https://www.better-auth.com/docs/concepts/users-accounts).
- [Better Auth Next integration](https://www.better-auth.com/docs/integrations/next),
  including nextCookies and propagation of update-user response cookies. The
  existing plugin order produces a warning; it was retained rather than silently
  repairing the shared auth configuration. Qualification concerns the tested flows.
- [Next dev CLI option](https://nextjs.org/docs/app/api-reference/cli/next#next-dev-options)
  and [versioned Server Action/redirect guidance](https://github.com/vercel/next.js/blob/v16.2.9/docs/01-app/03-api-reference/04-functions/redirect.mdx).
- [Playwright API/browser cookie sharing](https://playwright.dev/docs/api-testing)
  and [request interception](https://playwright.dev/docs/api/class-route#route-continue).
- Installed Codex 0.166.0 CLI help confirms the existing flags. `--ignore-rules`
  concerns execpolicy `.rules` files; it does not mean that repository AGENTS.md
  is removed. The model itself has not been invoked in this preparation.

## Initial findings and instrument revisions

1. DP-03's existing update-user API and Settings display can be exercised on the
   unsolved baseline. New 1–80-code-point validation remains acceptance, never V1.
2. An unsafe-name-display fault on the feature reference passed V0 type/unit/build
   and billing checks, while visible and withheld browser checks detected the
   rendering regression. Final-version qualification repeats this on both layouts.
   The fault is explicitly constructed; no frequency of real agent errors is claimed.
3. The initial fixture omitted SQL fields normally supplied by Drizzle application
   defaults. This caused setup failure; code/expiry fields were added to synthetic
   fixtures, with the failed attempt retained.
4. The initial admin denial assertion required the final URL to be sign-in.
   The real baseline may redirect an authenticated non-admin onward to dashboard.
   The checker was corrected to require denial of directory access/data.
5. Expected absence of new controls on baseline originally consumed locator
   timeouts. Existence is now asserted before interaction; acceptance still fails.
6. The withheld evaluator recognizes labelled controls without requiring the
   reference's exact display-name/role label wording. New-write tampering handles
   JSON-object, JSON-array Server Action and multipart transports, while rejecting
   unsupported transports rather than silently skipping the check.
7. Two development runs encountered a long Next dev compilation stall, including
   an auth request logged at about 4.8 minutes of compilation and tens of milliseconds
   of application execution. Watchdog/progress records retain incomplete invocations.
   Webpack was selected as a common pre-pilot harness adjustment. Browser/resource
   pressure and host/VM interruption are alternatives; the root cause is not asserted.

All earlier files remain under `qualification/`, including intentionally interrupted
instrument-development rounds. They are not agent outcomes and are not combined
with final-version reliability denominators. The final report must retain a separate
history count and include any mismatch under the final checker/harness version.

## Qualification and exposure gates

The required evidence is baseline preservation pass/acceptance fail, reference and
structurally different alternative pass, semantic fault detection with V0 results,
repeated visible/final checks, package equality and source mapping, and complete
patch/archive/fresh-scorer rehearsal without a model. Machine ledgers record actual
counts and timing; their existence alone does not imply passing qualification.

Static auditing has established that all eight packages retain baseline source and
equivalent requirements. Within each layout, V0/V1 differences are exactly the
declared command/package entry, TASK command inventory and preservation script.
References and active fault probes have equal canonical module bodies across layouts.
Reference source metrics are descriptive in [reference-metrics.json](reference-metrics.json):
DP-02 changes one route file; DP-03 reference changes three source files, including
two new modules placed according to each layout. Existing relocated-module count
and newly created layout-specific modules are reported separately.

No final/gold/probe files enter agent packages. Rehearsal will check fresh single-
commit history, no host mounts/Docker socket, and no provider-auth material. Final
scoring occurs in a fresh container without agent credentials. Modified visible
checks cannot change the withheld evaluator.

## Pilot-start boundary

The intended allocation remains DP-02 one session/cell and DP-03 three sessions/cell:
16 scheduled trials at 900 seconds each, a four-hour scheduled wall-time cap. At
most six infrastructure-only replacements, one per slot, would raise the attempt
cap to 22 and wall-time cap to 5.5 hours. No token cap is implied. Setup/scoring and
qualification time are separate from model wall time.

The runner requires a separate author-release record tied to the technical freeze.
Completed agent outcomes are not selectively rerun. Model replacements require
explicit infrastructure adjudication; scoring problems require retrying the same
patch. The author's existing ChatGPT allowance is the only approved model resource.
The main study's task set, precision target, model configuration and sample size
remain unfrozen.


## Final handoff

The completed reliability ledger contains 12 task/layout/implementation cases,
212 visible runs and 124 final-evaluator runs. DP-02 uses 20 visible baseline and
reference rounds per layout and 20 final reference rounds. DP-03 uses 30 of each;
baseline and alternative final checks have three rounds per layout. All selected
qualification rounds have their expected outcomes. These counts exclude deliberately
faulty implementations and do not count as agent trials.

All 26 fault/layout cases completed all five applicable V0 commands successfully.
Each failed its named semantic final assertion. V1 additionally detected existing
admin-access/session-count regressions for DP-02 and unsafe stored-name rendering
for DP-03 on both layouts. Both tasks therefore meet the operational V-gate in the
checked scope. Eight no-model rehearsals successfully captured source patches and
archives and scored them in fresh containers without provider credentials. The
package audit, paired-source audit, runner self-check and technical-freeze audit passed.

A prior DP-03 baseline rendering check returned a transient browser Error under
Webpack. Its precise cause could not be recovered from the original limited error
record; a diagnostic rerun passed. Subsequent 30-round baseline/reference visible
qualification passed on both layouts. This history is retained and must not be
summarized as zero unexpected results across all preparation attempts. Thirty
successful rounds do not establish a low flake-rate bound. This unresolved transient
and the lack of independent review are explicit limitations for author release.

DP-02 remains development-only. DP-03 is technically qualified and awaits author
approval of this concrete task contract, evaluation scope and pilot allocation;
it is not retroactively labelled author-confirmed or admitted main workload.
DP-04 remains on hold. The proposed release has 16 scheduled fresh model sessions:
DP-02 four, DP-03 twelve, GPT-6 Luna High/Standard default, 900 seconds per session.
The author-release file is absent; the runner is gated and no pilot has started.
