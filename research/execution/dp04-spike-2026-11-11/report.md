# DP-04 feasibility spike, 11 November 2026

Status: real HTTP/PostgreSQL spike completed on both existing pilot layouts. Immediate next-protected-request invalidation failed with the victim's valid cached cookies. DP-04 is blocked pending a defensible reference solution and scope decision; it is not evaluation-ready. This is instrument-development evidence, not an agent outcome or proof that every possible task implementation is infeasible.

## Observations

Each layout used a new application container and PostgreSQL database, the existing `smartkit-pilot:20261111` image, and its unchanged S1V0/S0V0 starting package. There was no coding-agent invocation, auth/cache mock, source repair, or existing user-data mutation. Two verified local fixture users were inserted, with two real login sessions for one user and one for the other. HTTP cookie jars retained all server cookies, including `session_data`.

| Check | Feature | Layered |
|---|---|---|
| Listing sessions returns only caller's sessions | Pass | Pass |
| Attempt to revoke foreign token leaves foreign session in DB | Pass (API returns 200) | Pass (API returns 200) |
| Revoke own other-session token removes its DB record | Pass | Pass |
| First Settings request using victim's full cached cookie jar | 200, profile rendered | 200, profile rendered |
| Default cached get-session after revoke | Still authenticated | Still authenticated |
| get-session with disableCookieCache=true | null | null |
| Settings without session_data cookie after revoke | 307 to sign-in | 307 to sign-in |
| Current and foreign sessions retain protected access | Pass | Pass |

The first victim protected request after revoke used a copy of its captured real cookie jar. Authoritative checks came afterwards, so clearing cookies in that control could not explain the observed cached access. Secrets/tokens were used only in memory and omitted from result JSON and console output. Test users were deleted in finally, followed by disposable application/DB/network cleanup. Runtime logs and isolation evidence are retained per layout.

## Interpretation and readiness

`session.cookieCache.enabled=true` and `maxAge=300` in the shared auth configuration allow valid cached session data. The dashboard's `requireAuth` calls the shared `getSession`, which invokes `auth.api.getSession` without `disableCookieCache`. The installed session route can return cookie data before `findSession`; revoke deletes the server record but cannot clear cookies held by a different client. The authoritative-read control rejected the deleted session, isolating the difference to cached versus server-store validation under the exercised conditions.

Simply adding session-list/revoke controls around the existing APIs does not satisfy the proposed immediate-invalidation contract. Satisfying it may require a changed validation path or another reference approach. No such patch has been constructed or qualified here. Changing the starting baseline would require the separate release/scope process already in the plan; a permissible task patch, if proposed, must be assessed against allowed changes and full preservation before claiming feasibility. Neither a weaker delayed-invalidation requirement nor a disabled-cache baseline has been silently substituted.

Plan verification therefore supports beginning preparation, not running DP-04 factorial trials. DP-02/DP-03 still need author-confirmed cards/matrices, references, browser qualification, V0/V1 detection evidence and manifests. The conditional reuse option for DP-04 remains unresolved; do not count it toward the minimum main task target.

## Reproduction and limits

`../dp04-session-spike.cjs` contains the in-container assert-based probe. `../verify-dp04-spike.py` reuses the existing container harness and refuses to overwrite this archive. Reproduction requires Docker running with the recorded pilot image/packages; preserve or choose a new output archive rather than overwriting observations. `summary.json` records the probe hash and layout results; per-layout `isolation.json`, `result.json`, `spike.log` and setup/runtime logs retain execution evidence. The initial run used the same orchestration as the saved reproduction script.

The test exercised real HTTP endpoints and server-rendered Settings, not browser interaction/hydration, a new task UI, a full alternative reference implementation, cache-expiry timing, concurrent revocation, browser/session flakiness loops, or production deployment. Each layout was probed once; matching results demonstrate this reproduced case, not a measured failure probability or a complete security audit. The cache max age is configuration evidence; no five-minute expiry experiment was performed.
