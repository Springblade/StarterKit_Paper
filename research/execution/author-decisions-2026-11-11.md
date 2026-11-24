# Author decisions recorded during the grill-me discussion

Date 2026-11-11. These are author-confirmed planning decisions, not a frozen main-study protocol or preregistration.

| Decision | Author confirmation |
|---|---|
| Research scope | One controlled SmartKit case study of repository organization and supplied behavioral-verification package access; null/adverse outcomes are acceptable. |
| Baseline | Use the current repaired SmartKit baseline. Exact correspondence with the defended thesis version remains unverified; approval did not select the earlier A/B/C historical-version alternatives. |
| User-order contracts | Ordinary users see only their own orders/status; cancel only their own pending orders; completed/cancelled/expired orders cannot be cancelled; search/filter preserves these restrictions. Admin-wide order powers remain unspecified. |
| Organization intervention | Relocate/group modules and update imports, while preserving business logic, dependencies, UI behavior and Next.js-required paths. |
| Main-task scope | Extend existing starter-kit functionality in authentication/authorization, billing and user administration. Individual main tasks and their provenance are not yet approved. |
| Available execution resource | The author's existing Codex usage allowance under their Plus plan. Work may span multiple days when the allowance is exhausted. No separate paid API budget has been authorized. |
| Pilot configuration | Author approved GPT-6 Luna (`gpt-6-luna`), High reasoning, Standard speed as the first development-pilot configuration, shared across the four cells. Actual account access and resolved runtime metadata still need verification. Final main-study configuration is not yet frozen. |
| Constructed tasks | Author agrees that explicitly labelled author-constructed tasks may be used when suitable historical issues/PRs are unavailable. Each requires a practical rationale and author-confirmed contract; task provenance must not be presented as historical evidence without a source. |
| First smoke-pilot scope | Author approved four fresh sessions, one per layout/verification cell, using the already development-qualified history-filter task. Each has a maximum of 15 minutes wall time; this is not a main-study sample size or resource limit. |
| Intended contribution | Author approved a controlled empirical assessment of repository organization and supplied behavioral checks for SmartKit extension, including new behavior, preservation and execution cost. Extension/replication positioning remains subject to prior-art comparison; no novelty priority claim is approved. |
| Main-task variety | Author approved including both localized changes and changes spanning multiple modules/workflows across authentication/authorization, billing and user administration. This does not prescribe file counts, a final task count, domain quotas or a particular implementation. |
| Research-question flexibility (Q14) | Author agrees to adjust the research question or narrow the contribution if prior-art comparison shows that the current comparison adds insufficient understanding, retaining SmartKit where appropriate. Specific changes will be explained before implementation. |
| Paper priority (Q15) | Author selected A: prioritize a complete study that can be clearly explained and reproduced, then choose a submission venue according to the results. Venue selection can be revisited once the contribution and evidence are clearer. |
| Insufficient precision fallback (Q16) | Author agrees to an exploratory study with explicit uncertainty and limitations if development-pilot planning shows that feasible resources cannot support sufficiently precise effect estimates. This positioning decision must precede main collection; an unclear or small observed difference does not establish equivalence. |
| Independent review availability (Q17) | Author is currently working alone and finds it difficult to arrange an external checker. Independent task/evaluator review is currently unavailable and must not be recorded as completed. Self-checks or assistant checks must not be described as independent review; document this limitation in the study. |
| Research artifact sharing (Q18) | Author agrees to target public release of task specifications, evaluator code, configuration, analysis scripts and results with sensitive information removed. SmartKit source-sharing rights must be checked. Author will review the concrete release package before publication; this decision does not authorize publication now. |
| Conditional task-reuse option | The author's follow-up retains the option of fresh main-study runs on DP-03, with DP-04 additionally conditional on a feasible spike without changing the current repaired baseline. This is a planning direction, not confirmation of detailed contracts, qualification, evaluation-ready status or a frozen main sample. Before pilot, author-confirmed cards/matrices, snapshots, visible/final suites, fixtures, reference hashes, execution cap and inclusion rules must be frozen. Tasks completing pilot unchanged remain eligible regardless of pilot pass/fail/time; substantive post-exposure task/instrument/cap revisions make them development-only. Pilot outcomes stay separate, prior exposure is disclosed, and the main task-discovery target must not depend on these two tasks surviving pilot. |

Read-only local verification found codex-cli 0.166.0 and `Logged in using ChatGPT`. `codex exec --help` exposes non-interactive execution, explicit model selection and JSONL output. No trial or model request was run for this verification. Login status alone does not establish remaining allowance or which model identifiers are currently available to this account.

Allowance exhaustion is a scheduling/infrastructure event. It does not set the scientific sample size or justify outcome-dependent stopping. A per-trial budget, total main sample/precision target and a consistent interrupted-attempt policy still require a protocol decision. Work can continue when allowance is available; no reset time or unattended next-day restart is assumed.

Pending decisions include remaining harness settings, individual task provenance and inclusion, V0/V1 visibility, isolated trial packages, per-trial limits, main sample/precision, and author confirmation of the final contribution statement. These must be resolved before main collection; development work and a deliberately separate pilot can inform them.

## Approved first pilot model

The author approved GPT-6 Luna with High reasoning and Standard speed as the first development-pilot candidate, replacing the earlier provisional GPT-6.1 Sol Medium suggestion. This is not a frozen main-study setting or a measured quality claim for SmartKit. Official model guidance describes Luna as efficient for focused high-volume coding and suggests starting Luna at High. GPT-6.1 Sol remains a candidate for longer, more demanding tasks. Pilot can inform a final fixed configuration before main outcomes; results from different model configurations must remain separate.

Official pages checked 2026-11-11: https://learn.chatgpt.com/docs/models?surface=cli and https://learn.chatgpt.com/docs/pricing. Subscription allowance depends on workload, and additional weekly limits may apply. Credit prices do not directly determine included subscription allowance. No model trial was run in making this recommendation.

## First smoke pilot completed

The subsequent authorized four-cell smoke pilot completed on 2026-11-11 using
GPT-6 Luna High, Standard default, CLI 0.166.0 and a 900-second cap. All four
patches passed the frozen 29-check final development evaluator. Agent wall times
were 141.27 seconds (S0V0), 101.61 (S1V0), 99.66 (S0V1), and 100.11 (S1V1).
One database setup failure occurred before S1V0 model invocation and was archived
and adjudicated separately. No unsuccessful agent outcome was selectively rerun.

See `pilot-2026-11-11/report.md`, protocol, manifests and raw attempt records.
This is one development task with one session per cell, not main-study evidence
of a layout or package effect. The main-task frame, main configuration, sample,
precision and resource plan remain unfrozen.

## Task-discussion steering

The author subsequently asked the assistant to propose suitable pilot tasks
rather than continue asking the author to decide each task's business rules.
`pilot-task-plan-v2.md` therefore contains assistant-proposed constructed
specifications for an expanded development pilot. Earlier MT candidate IDs are
not approved main tasks, and the author's direction is not retroactive approval
of every detailed rule. No new model run is implied by this proposal document.

## Follow-up grilling decisions confirmed on 2026-11-12

These decisions were explicitly confirmed in the subsequent discussion and its
closing shared-understanding summary. They update planning priorities, not task
qualification status or main-study protocol freeze.

| Decision | Author confirmation and boundary |
|---|---|
| Research question and study object | Investigate how repository organization and access to a supplied behavioral-verification package affect agent feature extension, preservation and execution cost. SmartKit is the experimental object. Empirical conclusions remain bounded by the evaluated tasks, system, model/harness and budget. |
| Intended use of contribution | Produce evidence supporting repository grouping and supplied regression-check decisions for agent-driven extension. Extension/replication positioning still requires comparison with closest artifacts; no novelty priority or superiority is established. |
| Initial planning difference | Use an absolute 10-percentage-point difference in joint-success probability as an initial discussion anchor for main-study scenarios. It is not a frozen practically meaningful threshold, expected effect, equivalence margin or uncertainty-width target. Main precision and interval choices remain open. |
| Review milestone | Review contribution, qualified workload/instruments and actual allocation/resource totals after DP-02/DP-03 preparation and resolution of DP-04 status, before expanded-pilot model invocation. Existing pre-allocation reserve rules apply if priority tasks are ineligible. |
| Task diversity | After pilot, prioritize discovering and qualifying meaningfully different task types before increasing repetitions on a few tasks. Include localized and cross-workflow changes without prescribing file counts or selecting tasks by winning condition. |
| Time constraint | Do not use the author's deadline or weekly hours as planning constraints; do not continue asking for them. This does not remove per-trial limits, spike effort boundaries, attempt caps, account allowance constraints or the absence of authorization for paid APIs/credits. |
| Technical responsibility and review | Assistant proposes tasks, prompts, detailed rules, reference/alternative solutions, requirement-to-check matrices and evaluators, and verifies technical facts. Author reviews the concrete package as a whole for research purpose, task rationale, requirements/evaluation scope and resources. Do not interview the author about every business rule. Q4/Q5 task specifications were not individually approved; final card/matrix confirmation remains pending. |
| Primary and secondary effects | The two equally weighted marginal intervention effects are primary. Conditional effects and interaction are supplementary; strong interaction claims require separately adequate precision. Joint success still requires acceptance and preservation; cost and failure patterns complement interpretation. |
| Scope of the closing confirmation | Author confirmed this shared understanding and updating the existing plan/decision log. No new model trials were authorized by that confirmation. The 16/28 expanded-pilot counts remain conditional planning scenarios; main sample size is unset. |

The next handoff is the updated plan plus concrete contribution, task/instrument
qualification and resource/precision evidence as those are produced. Recording
these decisions does not establish that the corresponding artifacts have already
been completed. DP-04 remains blocked pending reference/scope resolution, and
DP-02/DP-03 remain unqualified under the currently recorded evidence.

## Cost-first screening decisions confirmed on 2026-11-12

The author explicitly selected C for DP-04 and accepted the assistant's recommended
V1 and reuse policies in response to three concrete questions.

| Decision | Confirmed policy |
|---|---|
| DP-04 | Hold/development-only for this round. Retain the existing repaired baseline and its cookie-cache behavior. Neither an auth-cache repair nor DP-04 v2 is authorized by this choice. |
| V1 utilities | Permit path-independent behavioral checking utilities exercising real auth/DB on the unsolved baseline. They must exclude acceptance of new features, solution hints, module-path assertions and hidden evaluator cases. Runtime and parity still require qualification. |
| Reuse | DP-02 is development-only. DP-03 targets evaluation-ready only after all qualification gates and pre-pilot freeze. Main eligibility is independent of pilot pass/fail/time; substantive post-exposure revision makes the exposed task/version development-only. This confirms the policy, not current readiness or the detailed task contract. |
| Work order | Paper V-gate analysis and workload registry/discovery precede oracle construction and P0–P3 qualification. No model invocation when no non-lookup task clears the required gates. Stopping for lack of eligible workload is a valid feasibility result; apply Q16's exploratory positioning with explicit limits. |

Current evidence: no newly proposed non-lookup task has passed runtime V-gate
qualification. Paper feasibility is recorded separately from observed pass/fail.


## Autonomous technical preparation through pilot-start gate

The author requested autonomous skill-assisted verification of all preparation steps, returning only at the start-of-pilot gate. This authorized technical implementation, qualification and self-review, without intermediate business-rule interviews. It did not authorize new model trials. The concrete DP-02/DP-03 release and its limitations are now presented in prepilot-2026-11-12/report.md; author pilot release remains pending.


## Author-confirmed paper framing

The author confirmed that the study investigates whether two starter-kit design choices affect coding agents. It does not start from a demonstrated SmartKit obstacle for which an intervention is proposed as a remedy. The manuscript was reframed accordingly; hypothetical scenarios and injected faults are evaluation illustrations/instrument checks, not observed agent problems. No pilot authorization or change to frozen task artifacts follows from this editorial revision.


## Task-frame revision agreed in the current session — 2026-11-14

The author agreed to the recommended direction: retain the 2 × 2 SmartKit question, revise task selection and the path to main evidence, then decide the role of the prepared 16-session development pilot. A single-factor study was discussed as a fallback, not selected.

- Each candidate needs rationale/provenance, new behavior, preservation, family/shared surface and a descriptive relation to organization and check conditions.
- Retain localized and cross-workflow tasks; do not impose changed-file/module thresholds or select by a winning condition.
- DP-02 remains development-only; DP-03 retains the prior conditional reuse option. Pilot records stay separate from fresh main outcomes.
- The 16-session allocation is a retained option pending task-frame/pilot-purpose review. Do not replace it with another arbitrary number or invoke a model from this agreement.
- Update existing plans/registry while preserving evidence. A03/B03/U03 is the assistant's proposed discovery sequence; individual contracts and main sample size are still unapproved.

This authorizes the planning revision and changes the work order. It does not authorize new model trials or certify detailed task contracts. Pilot only requires qualification of its selected tasks; the whole main set must qualify before main collection. A small number of candidates is a scope limitation, not an automatic ban on a narrowly defined feasibility pilot.

### Technical observation during the planning edit

A read-only comparison on 14 November found `local-runtime.py` different from the prepilot freeze manifest before these edits began. Cause and runtime impact are unverified. The planning edit preserves technical artifacts; inspect the discrepancy and requalify affected parts before future execution. This finding is not an author decision or proof that every earlier qualification result is invalid.

## Request for one collection schedule — 2026-11-15

The author requested an understandable rewritten plan with explicit task and run totals, completed in one collection rather than successive pilot/main reruns. This authorizes rewriting planning documents; it is not authorization to invoke model trials.

The assistant's concrete proposal is six named tasks (MT-A01, MT-A03, MT-B03, MT-B04, MT-U02, MT-B01), four conditions, 17 repetitions per task-condition, 408 scheduled slots, one model/harness configuration, no new pilot and no replacement model attempts. The proposed precision target is a simultaneous 95% halfwidth at most 15 percentage points for both equally weighted marginal effects conditional on this fixed task set. The existing independent-run Hoeffding calculation needs at least 390 runs; balanced rounding gives 408 and a 14.656-point halfwidth. This target, roster, scope and resource total are assistant recommendations awaiting review, not author-confirmed numbers or a claim of 80% power at a 10-point difference.

The six tasks are selected for preparation, not certified main-ready. DP-03 retains its qualification/exposure record; five other tasks need full qualification. All must be ready before any collection begins. Task contracts, 24 packages, a new 408-slot allocation, analysis and the 102-hour maximum agent time must be concrete for one review before execution. Keeping one collection cannot guarantee no technical interruption; starts resume at uninvoked slots, while interrupted invoked slots remain documented missing unless assessable.

History-filter and DP-02 remain development-only with no new model runs. DP-04 remains held under the previous baseline decision. MT-B02, MT-U03 and MT-U04 are outside this proposed collection. The registry still has eleven candidates; adding the separately stored history task gives twelve recorded tasks. The 4 completed development sessions remain separate from the proposed 408 main slots. Existing 16-session allocation, freeze, qualification records and raw outcomes are preserved unchanged; they are not repurposed as the new execution schedule.

Current summaries are in paper-completion-plan.md and pilot-task-plan-v2.md. Older plan/registry text is retained in collapsed historical sections. This entry does not approve detailed contracts, certify new qualification, alter the application or freeze manifests, or authorize model execution.

## Resource revision after the 408-run proposal — 2026-11-15

The author said the number of runs was too high to execute. The assistant withdrew its 408-run recommendation and asked for a total run cap. The author's next instruction was to continue, without providing a numerical cap. This supports continuing the planning revision, not treating a new run count as approved or invoking models.

The revised assistant proposal retains MT-A01, MT-A03, MT-B03, MT-B04, MT-U02 and MT-B01, with four conditions and two repetitions per task-condition: 48 scheduled slots, 8 per task, 12 per condition, and a 12-agent-hour maximum at 900 seconds per run. It is a pragmatic resource proposal, not a statistically powered sample or a verified affordable budget. Both repetitions are within one collection. There is no new pilot, no replacement model attempts and no outcome-dependent extension.

The previous 15-percentage-point simultaneous halfwidth target is withdrawn. Report task-condition counts, observed failures and resource use; descriptive contrasts may be accompanied by the existing conservative fixed-task intervals under their stated assumptions. At N=48, that method has a simultaneous halfwidth of approximately 42.7 percentage points before domain clipping. This illustrates uncertainty, not precision adequacy. Two observations per task-condition do not establish a stable success probability, equivalence or a general layout advantage. Missingness and task/shared-surface restrictions remain explicit.

Task qualification requirements, isolated fresh sessions and preservation evidence are unchanged. Five tasks still lack full qualification; DP-03's existing evidence requires the recorded checks before a new freeze. The total cannot silently change if a task fails qualification. Preparation cost is separate from model-run count. Historical development outcomes, technical artifacts, allocation and freeze files remain unchanged. The live plans, registry, tracker and reading-entry notes now state 48 as the proposed collection; actual model execution still requires the completed reviewed package.

## Evidence-based revision of the 48-run proposal — 2026-11-15

The author requested research and a rewritten plan addressing thin comparative evidence, narrow task coverage and a contribution beyond pass rates. The existing 48-run resource proposal is retained: six tasks, four conditions, two fresh sessions per cell, one collection, no new pilot and no replacement model attempts. This request authorizes research and planning revisions, not model execution or an automatic increase in resources.

The assistant proposes replacing MT-B01 (order-code lookup, close to the history development task) with MT-U03 (admin role assignment). The proposed roster is MT-A01, MT-A03, MT-B03, MT-B04, MT-U02 and MT-U03, with eight slots each. The rationale is adding a permission-sensitive write operation, not satisfying a 2/2/2 domain quota. The number of repositories and the limited comparative precision are unchanged. U03 and the new roster are proposals awaiting contract/qualification review, not new author-confirmed task details.

U03's public contract is to change another account's persisted user/admin role, reject self-demotion through the new feature, authorize writes from the caller's current server-side role (including a demoted caller holding cached cookies), preserve unrelated identity/orders, and verify the target's permissions after fresh authentication. Existing cached read-session behavior is documented and tested separately; no immediate whole-application revocation is promised. Static installed Better Auth1.6.25 source supports an authoritative-session middleware on setRole, while SmartKit's route guard uses cached getSession. Runtime qualification is not complete. No baseline/auth-cache repair, dependency change, DP-04 reopening or automatic fallback to B01 is authorized by this plan edit.

The plan retains both equally weighted marginal S/V summaries and adds prespecified evidence: an all-patch frozen V0/V1/hidden-evaluator audit; separate labels for previously passing behavior broken versus new-feature/new-path defects; actual transport and assertion links; observable trace labels with author review; all cases retained and at most one illustration per task selected by a published rule. Offline testing does not invoke agents or measure counterfactual agent behavior. Estimates, missingness, leave-one-task/domain-out sensitivity and reporting limits are specified before outcomes.

Primary-source research was appended to paper-proposal/citation-evidence.md under '48-run study evidence review — 15 November 2026'. It finds prior feature+regression endpoints, repository interventions and trace/live-path analyses. The proposed contribution is therefore a conditional empirical extension or purposeful replication linking the matched S/V experiment to contract-detection evidence, not an established novelty claim. Experimental sample size remains48; richer trace or suite data does not increase independent N or guarantee publication.

All task materials, current affected runtime, classification/audit rules and one execution allocation must qualify and be reviewed before invocation. If U03 cannot satisfy the contract, stop before model collection and present the unresolved task issue; do not force the 48 total by a silent substitution. Main outcome data, task qualification, independent second review and journal/conference acceptance have not been produced in this revision. Manuscript prospective sections remain an explicit pre-collection update; earlier data and technical manifests stay intact.

## Requested pre-run research-value verification — 2026-11-15

The author requested verification that both the research direction and the experimental direction provide practical research value before any pilot begins. The assistant performed a targeted fresh prior-work audit, a read-only local source/qualification review and local numerical information checks. No model trial, application runtime check or task admission was performed.

Current assistant assessment: the scoped decision about source grouping and supplied preservation checks is defensible; the present 48-run proposal is not yet endorsed for immediate execution or for a strong comparative claim. Nearest work already covers repository-location/context interventions and preservation/test information. The exact combination was not found among inspected methods; novelty and paper-level value are not certified. Finite-task exploratory evidence remains a possible contribution after measurement/qualification gaps close.

Local exact enumeration in pre-run-information-check.json illustrates weak sensitivity at10pp under one stated24v24 homogeneous Bernoulli/Fisher scenario; it does not replace the proposed main analysis or prove a universal minimum sample size. Old DP03 constructed faults show both a V1-detected existing-rendering regression and limitations on new write paths. These are instrument evidence, not new agent outcomes. Main roster, 48 slots, no-new-pilot policy, DP04 hold and all baseline/frozen artifacts remain unchanged.

See research-direction-review/assessment.md for current findings and the four evidence conditions before release. The practical threshold, treatment reach and five remaining task qualifications are not marked resolved by this audit. No new author approval, task contract, sample size, deadline, paid resource or execution release is inferred.

## Actual no-model feasibility verification — 2026-11-15

The author explicitly asked the assistant to verify the remaining issues. The assistant built local reference/alternative candidates in task-feasibility-2026-11-15, restored a separate no-model image from the recorded application lockfile, and exercised fresh app/PostgreSQL containers and Chromium. This authorized technical verification; no experimental agent or account credentials were used.

All six tasks have two candidate implementations passing scoped runtime checks in both layouts (24 cases), with typecheck and unit/build evidence. Six seeded fault types were detected in both layouts (12 cases). The 47 technical invocations include four retained development failures; this is not a flakiness-free reliability series or48 main trials. All created DB volumes were removed. The284 layout-manifest records and old frozen technical artifacts remain unchanged. The old image was missing; the rebuilt feasibility image is recorded as a different environment, not silently certified as the old freeze.

U03's current-role write and fresh-login permission behavior was observed. Cached get-session can still report a demoted role as admin, while existing authoritative admin writes return403. Existing API permits self-demotion; the new task guard is restricted to the new feature, with the limitation disclosed. No baseline/cache repair or DP04 reopening occurred.

Source mapping found zero edits to existing relocated modules in all12 task/implementation pairs. Imports still differ across layouts, so this does not prove no S effect. The new fault probes mainly target new-feature acceptance, not an established V1 preservation gate. Assistant recommendation is therefore to hold the proposed48 collection for research-value/treatment-relevance review, rather than treat technical feasibility as proof of a useful comparative study. This is a recommendation, not a user-approved pivot or roster change. Full generic-oracle qualification, five-task V-gate/reliability and actual agent effects remain unverified.

## Hold after feasibility verification — 2026-11-15

Technical feasibility was verified without model calls: six candidate task implementations had scoped passes on both layouts and seeded faults were detected. This does not release model collection. The assistant's revised recommendation is to hold the proposed 48 slots until four gates pass: G1 treatment reach, G2 old/shared-behavior preservation gate, G3 full task/evaluator validity and G4 research value/contribution.

The existing 48 allocation remains a held option. No model invocation, task substitution or extra run is authorized by this status update. If a gate fails, narrow the estimand or stop the design rather than force the roster. Historical artifacts and baseline remain unchanged.
