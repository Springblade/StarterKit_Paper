# Expanded pilot task contracts and requirement-to-check matrix

Version 1, prepared 12 November 2026 before any new model trial. Provenance:
assistant-proposed constructed tasks, not historical issues or production incidents.
The author delegated technical preparation and verification through the pilot-start
gate in the latest instruction. Final research release is presented at that gate;
this document does not invent an earlier author confirmation of each rule.

## Common contract

Start independently from the recorded unsolved feature/layered snapshots. Preserve
the supplied layout, dependencies, authentication cache policy, existing routes,
account identity/permissions and order behavior outside the requested extension.
Implementations may add appropriate files/routes/actions; no required gold file list.
Use current framework conventions. Both verification levels receive all requirements,
the same ordinary tools and a pinned real Chromium browser. V0 may write/run tests.
V1 adds preservation checks only. Final cases, references, faults and prior logs are
excluded from agent packages and reachable history. Never modify auth dependencies
or globally disable cookie caching to satisfy a task.

Services are synthetic/local; no email/payment credentials or real transactions.
Independent cases use isolated cookies and real auth/DB. A pass means passing this
scope; it does not prove correctness of every untested application behavior.

## DP-02 — Role filter in the admin account directory

Rationale (hypothetical use case): an admin wants to inspect accounts of one role.
This is a localized lookup/filter calibration task, permanently development-only.

Add a labelled native GET dropdown All/User/Admin to `/dashboard/admin/users`.
Values are empty/user/admin. Missing, empty, invalid, case-mismatched or repeated
`role` parameters mean All. Submit/reload retain the effective choice. Rows and
total reflect the selected set, including zero matches with controls still present.
Keep per-account session-record counts, displayed metadata and descending created
date order. Ties do not prescribe a new tie-break rule. Counts remain counts of
all session records, not only unexpired sessions. Only admin may see the directory,
including direct requests. Reads must not change users/orders or expose session tokens.

| Requirement | Final check IDs | Visible preservation | Oracle / fixture boundary |
|---|---|---|---|
| Role subsets and correct selected total | U-A-role-all/user/admin | None for new subsets | DB membership/count; different role distribution from visible fixtures |
| Labelled native GET control; actual submit/reload | U-A-native-get-control-submit-and-reload | None | Chromium interaction and resulting URL; no source-path assertions |
| Invalid/repeated fallback | U-A-invalid-or-repeated-* | None | Five distinct query policies, public above |
| Empty subset keeps control and total 0 | U-A-empty-selection-keeps-controls-and-zero-total | None | Temporarily make disposable accounts admin, then restore roles |
| Existing admin-only access | U-P1-direct-route-non-admin-and-anonymous | VP-U1 | Real non-admin/anonymous browser contexts, direct URL |
| Existing counts/order | U-P2-unfiltered-session-aggregates-and-date-order | VP-U2 | Hidden 0/1/3 session counts; distinct fixture dates; visible distribution differs |
| No raw tokens | U-P3-no-token-in-admin-output | VP-U3 | Compare response DOM/HTML with local DB tokens without logging token values |
| Read-only identity and orders | U-P4-read-only-directory; P-orders-unchanged | VP-identity-and-order-preservation | DB before/after; legitimate session touches excluded |

Public V0 commands: `pnpm check-types`, `pnpm test:run`, `pnpm build`, existing
scripts. V1 adds `pnpm test:preservation`. The latter exercises the unfiltered
directory on the unsolved baseline; it does not test the new dropdown/filter.

## DP-03 — Edit the signed-in user's display name

Rationale (hypothetical use case): the user wants to correct a display name without
changing login identity. Settings currently displays profile fields. Better Auth
already exposes update-user; the feature is a usable Settings form and its rules.

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

| Requirement | Final check IDs | Visible preservation | Oracle / fixture boundary |
|---|---|---|---|
| Actual form submit, trim, persistence, same-session display/reload | A-A1-labelled-form-submission-trim-and-refresh | VP-A3 checks only the existing API/display path | Chromium plus DB; no required endpoint/file path for the new form |
| Valid 1/80 code points | A-A2-boundary-one/eighty-unicode | None | One CJK character; 80 supplementary-plane emoji |
| Server rejects invalid length/whitespace | A-A3-server-rejects-* | None | Intercept the real form's POST to replace a valid marker after client validation; reject unsupported transport rather than silently skip |
| New write cannot target foreign identity/protected fields | A-A4-own-target-and-protected-fields-through-actual-write | VP-A1/A2 check only existing update-user | Tamper actual JSON/multipart request; independent users and DB before/after |
| Anonymous new write denied | A-A5-anonymous-new-write-denied | VP-A2 checks existing API only | Replay actual captured write without cookies/authorization; no synthetic gold endpoint |
| Existing safe stored-name rendering | A-P3-stored-name-safe-on-existing-settings | VP-A4 | Existing API sets markup-shaped text; independent visible img vs hidden svg payload; real Chromium execution/DOM checks |
| Existing identity/sign-in | A-P4-identity-and-sign-in-preserved | VP-identity-and-order-preservation | DB protected fields plus fresh cookie context and sign-in |
| Existing anonymous Settings access denied | A-P5-existing-settings-anonymous-denied | VP-A5 | Actual protected browser request |
| Existing order ownership/status/history | A-P6-existing-order-status-and-history-ownership; P-orders-unchanged | Only persisted-order invariant visible | Existing status route and history; own completed vs foreign expired order |

The two security checks of the **new** write transport are acceptance/feature-security
checks. They cannot run on the unsolved baseline and are not supplied as V1 preservation.
Baseline preservation is tested through existing APIs/pages. This classification
keeps the baseline expectation meaningful without skipping new-path security tests
after a solution exists. Acceptance and preservation are scored separately; joint
success requires both. Setup/cleanup completion is an additional instrument gate.

## Fault plausibility and qualification policy

DP-02 probes omit/filter the wrong role, miscount total/sessions, or replace the
admin guard with authentication only. The last two regress existing behavior.
DP-03 probes omit server validation, persistence or trim; count UTF-16 incorrectly;
or change the existing profile-name display from escaped text to raw HTML while
working on name presentation. The unsafe-display probe is the V-gate candidate:
it affects baseline display behavior, runs without the new form, and needs no
artificial auth-cache/configuration change. It does not assert that real agents
will commonly make this mistake. Frequency is not estimated by constructed probes.

For retained tasks: qualify baseline, reference and a structurally different valid
alternative in both layouts; every named fault must fail the corresponding semantic
check, with build/type failures distinguished. Run baseline/reference visible suites
20 times each per layout, full reference browser scorer 20 times, and baseline/
alternative final scorer initially 3 times. Preserve every discrepant attempt and
repeat qualification after instrument changes; never remove failed rounds from logs.
Report per-suite counts, runtime/overhead and limitations. These checks are author/
assistant self-checks, not independent external review.
