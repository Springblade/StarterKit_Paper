# Scout: real-world agent PR evidence and a defensible paper problem

Research date: 2026-11-09. Working research memo, not manuscript prose. Scope: publicly observable coding-agent PR integration, review corrections, and reliability of accompanying tests. SmartKit is an implementation context, not evidence that the wider problem exists. No paid runs or dataset-wide downloads were performed.

## Frozen research questions

1. What failures and human work are actually observed after coding agents submit PRs?
2. Do agent-involved tests provide evidence of fault detection, or mostly evidence of test presence and execution?
3. Which tractable public-artifact study would add information beyond current descriptive comparisons?

Search perspectives were failure/rejection, testing adequacy, collaboration/integration, and contrary or causal productivity evidence. Citation protocol: title/authors verified at primary landing pages; quantitative claims checked in abstract or full text; anonymous preprint identity checked against final ACM metadata. All eight works below are VERIFIED for the specifically stated claims. A non-peer-reviewed working paper is labelled accordingly.

## Verified evidence map (eight distinct works)

**1. Hao Li, Haoxiang Zhang, Ahmed E. Hassan (2026). AIDev: Studying AI Coding Agents on GitHub.** [Primary abstract](https://arxiv.org/abs/2602.09185), [full text](https://arxiv.org/html/2602.09185v1). Dataset paper, MSR 2026. Original snapshot: 932,791 PRs; enriched AIDev-pop: 33,596 PRs in 2,807 repositories above 100 stars. Full text inspected: overview, schema, cutoff, access sections. Useful contribution: review events, discussions, diffs, linked issues and timelines allow studying the submission-to-integration trajectory. The paper describes an August 2025 snapshot; it is not the current dataset release. Dataset version issues are documented separately below.

**2. Ramtin Ehsani, Sakshi Pathak, Shriya Rawal, Abdullah Al Mujahid, Mia Mohammad Imran, Preetha Chatterjee (2026). Where Do AI Coding Agents Fail? An Empirical Study of Failed Agentic Pull Requests in GitHub.** [Primary record](https://arxiv.org/abs/2601.15195), [full text](https://arxiv.org/html/2601.15195v1). January 21 preprint. Quantitative analysis of roughly 33k agent PRs plus qualitative coding of 600 rejected PRs. Non-integration includes reviewer abandonment, duplicates and unwanted work as well as CI failures. Thus closed/unmerged cannot serve as an automatic technical-incorrectness label. Their last-commit check status and review-revision churn are proxies, not a direct measurement of correctness or human labor. Inspected methods and taxonomy. This already occupies the generic failure-taxonomy space.

**3. Sabrina Haque, Sarvesh Ingale, Christoph Csallner (2026). An Empirical Study of Tests in Agentic Pull Requests.** MSR 2026, pp. 929–933, DOI [10.1145/3793302.3793604](https://doi.org/10.1145/3793302.3793604); [author full text](https://c.csallner.org/papers/Haque26Empirical.pdf); preprint title [Do Autonomous Agents Contribute Test Code?](https://arxiv.org/abs/2601.03556). These are one work, not two. Test-containing PRs tend to be larger and have longer turnaround, with broadly similar merge rates. Later test revisions are observed, but longer turnaround is not itself measured human intervention. Tests are identified through touched files, so this establishes test inclusion/evolution rather than fault detection. The five-page full text was inspected, including timestamp augmentation and tables. [Replication](https://doi.org/10.6084/m9.figshare.30944168).

**4. Atish Kumar Dipongkor, Talank Baral, Wing Lam, Kevin Moran (2026). Test Coverage Analysis of Agentic Pull Requests.** [Primary record](https://arxiv.org/abs/2607.18057), [full text](https://arxiv.org/html/2607.18057v1). July 20 preprint; artifact labels it ICSME 2026 accepted. Dataset: 4,882 Java/Python PRs; executable coverage uses a narrower merged, buildable subset. Existing tests cover 61.5% of changed executable lines in Java and 27.0% in Python. Agent-written tests improve coverage in a minority of Code + Tests PRs: 35.9% Java, 22.5% Python. Error handling is a recurring uncovered category. Full-text methods and limitations confirm substantial buildability selection. These results establish uncovered paths, not defect prevalence; a covered line can still lack a meaningful assertion. [Reusable patches and reports](https://doi.org/10.5281/zenodo.21419686), [code](https://github.com/SageSELab/Agentic-Pull-Request-Test-Coverage).

**5. Roberto Milanese, Francesco Salzano, Hovhannes Muradyan, Jingjing Wu, Remo Pareschi, Fausto Fasano, Mattia Fazzini (2026). Testing with Coding Agents: A Large-Scale Comparison of Agent-Supported and Human-Authored Pull Requests.** [Primary record](https://arxiv.org/abs/2610.35297), [full text](https://arxiv.org/pdf/2610.35297). October 26 preprint, 114,134 merged PRs in 391 Java repositories. Within-repository models find agent-supported PRs more likely to touch tests (OR 1.65); no difference detected in production-change coverage in 95 buildable repositories. This challenges a blanket claim of poorer agent testing. Pooled comparisons can hide/reverse within-project patterns. Crucially, final PR artifacts include review corrections; absence of significance does not demonstrate equivalence. Pages 52–54 explicitly propose separating initial output from review corrections and measuring fault detection with mutation analysis. [Replication](https://doi.org/10.5281/zenodo.21914644). Methods, attribution heuristics, discussion and threats inspected.

**6. Anthonia Oluchukwu Njoku, Zohreh Sharafi, Foutse Khomh (2026). When Code Authors Are Agents: A Large-Scale Study of Human–Agent Collaboration in Pull Requests.** AIware 2026, pp.188–196, DOI [10.1145/3805760.3814909](https://doi.org/10.1145/3805760.3814909); [anonymous submission full text](https://openreview.net/pdf?id=ArurxAmCtR). Final publisher metadata verifies authors/title and July 5 publication. Comparison: 33,596 agent and 6,618 human PRs. Agent PRs integrate faster but have lower overall merge rates; task type changes the comparison. More bot-mediated comments and different communication patterns are observed. This does not support a universal claim that agent PR review always takes longer. Final publisher abstract and corresponding submission text inspected; use final DOI for citation.

**7. Joel Becker, Nate Rush, Beth Barnes, David Rein (2025). Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.** [Primary full paper](https://metr.org/Early_2025_AI_Experienced_OS_Devs_Study-paper.pdf). Task-randomized trial: 16 experienced maintainers, 246 real tasks in familiar mature projects; allowing early-2025 tools increased completion time by 19%, despite participants believing they were faster. This supplies causal evidence under a specific historical tool/user/task setting. It is not a trial of all current autonomous PR agents and cannot estimate their November 2026 effect. Full abstract and setting inspected. Best used to motivate measuring completed work and checking subjective impressions, not to predict SmartKit outcomes.

**8. Fiona Chen, James Stratton (2026). Artificial Intelligence in the Firm: Bottlenecks in Software Production.** [Author-hosted primary paper, current November 7 version](https://fion.ac/jellyfish.pdf). Working paper, not a randomized trial. Proprietary events from 655 firms; staggered adoption design. Current estimates: agents associated with +35.7% PRs opened, +13.7% Jira issues resolved (borderline significant), +56.1% review duration. Review queue and active-review measures both rise. Abstract, introduction, review section and conclusion inspected. Older October press coverage saying no software-output gains is stale relative to this revision. Adoption identification requires assumptions; their firm data cannot simply be reproduced from GitHub. Model-based future employment projections are not observations and are unnecessary for this paper.

## Synthesis: what the evidence does and does not establish

Ehsani et al. show that repository coordination can prevent integration even when code correctness is not adjudicated; Njoku et al. show that faster agent integration can coexist with lower acceptance. Chen and Stratton instead find longer firm-level review after agent adoption. These are different populations and estimands: PR-level accepted contributions versus firm production following rollout. They should not be averaged into a universal slowdown claim.

Haque et al. count tests and their timing; Dipongkor et al. execute tests and find substantial uncovered changes; Milanese et al. compare within projects and find no detected production-coverage deficit among accepted contributions. Together they support asking what the tests actually detect and what reviewers repair. They do not establish that all agent tests are weak, that agents introduce more bugs, or that adding a test file causes acceptance.

An evidence-bounded problem statement is: accepted agent-supported changes are products of a review process, while current measurements often inspect the final artifact or count test files; the initial verification gap and the corrections that close it are incompletely measured. This is a research opportunity, not an established finding about SmartKit.

## Dataset choice and hazards

The [official AIDev dataset card](https://huggingface.co/datasets/hao-li/AIDev) currently documents v5: 7,685,281 PRs, six agents, cutoff March 31, 2026. Pin a revision, never mix current counts with v3 paper statistics. v3/v4 subresources were truncated at 30 records per PR by missing API pagination; v5 fixes threads, but some later commit diffs remain incomplete. Re-fetched events can postdate cutoffs. Labels use bot identities, branch prefixes and body signatures, with additional popular-subset validation. They indicate detectable involvement, not autonomous authorship. Conventional-Commit task labels ship only in v3. Large patches may be absent.

My proposed handling: define a fixed observation window and PR cohort first, join corrected threads, validate each sampled PR against Git history, retain explicit missingness flags, and exclude incomplete histories only from analyses requiring them. Compare included/excluded cohorts. Preserve initial submission SHA, every relevant subsequent SHA, actor evidence, timestamp and original URL. For a small sample it may be simpler to reconstruct histories directly from the linked public repositories.

Additional ready-to-reuse artifacts are the three testing replication packages linked above. The coverage package has real executable patches/reports; the October comparison provides a matched ecosystem context. Neither guarantees that its build environment still works. Confirm artifact contents and rerun a small feasibility sample before committing to a large study.

## Two possible studies, in priority order

### Direction A: What verification gaps are repaired between agent submission and integration?

Descriptive longitudinal study; public review threads and versioned patches are the main data. Proposed RQs: Which behavior-changing review requests concern missing/incorrect verification? Which are followed by a production change, an assertion change, both, or no observable correction? What remains unresolved at merge/closure?

Start with a manually tractable stratified sample of agent-involved bug-fix PRs with substantive human review, from a small set of repositories with recoverable histories. Do not pretend the reviewed subset represents all agent PRs: report the complete sampling funnel, including abandoned and unreviewed PRs. A JS/TS web-project scope can connect to SmartKit only if the available sample and real review concerns justify that restriction; do not select server/client boundaries in advance.

Unit: review concern linked to a subsequent change, nested in PR and repository. Independent coding of a subset, explicit codebook, agreement and adjudication. Categories should emerge from authentic artifacts, with security/error-path/state-transition cases retained only when actually present. Require an explicit reviewer concern plus traceable patch/test evidence before calling something a review correction. Record actor uncertainty rather than assigning every post-review commit to a human. Counts of comments and elapsed calendar time remain proxies; do not label them labor hours.

Contribution over the eight works: connect concrete review concerns to versioned verification repairs, rather than another merge-rate comparison or generic rejection taxonomy. Closest prior work already calls for initial-versus-final separation, so novelty requires the traceable concern-to-repair dataset and an empirical finding, not the idea alone. Feasibility gate: inspect about 20 PR histories without executing agents; abandon or change scope if histories or substantive linked concerns are too sparse.

### Direction B: Do tests present at submission detect the reported bug, and what is added during review?

Paired executable study of public bug-fix artifacts; it can complement Direction A if runtime and histories permit. Restrict to PRs with a concrete issue, executable reproducer, recoverable buggy and fixed revisions, and separable tests. Compare pre-existing tests, tests present at submission, and final tests against the same buggy/fixed production snapshots. A valid witness should fail on the buggy state and pass on the fixed state for the intended reason. Classify installation/compilation failures separately from bug detection. Then, if feasible, compare fault detection against the same small, reviewed set of plausible mutants on a fixed implementation.

This is a controlled intervention on test-suite availability for those artifacts, not a causal estimate of using an agent. Holding the program and fault fixed permits measuring the incremental detection contribution of a test set; historical human-versus-agent authorship and general production defect effects remain observational. Do not transplant tests blindly when APIs changed; report inapplicable cases and adaptation rules. Equivalent mutants, flaky tests and build exclusions need explicit handling. Prefer executable behavior oracles grounded in the original issue over self-invented acceptance checklists.

Contribution over coverage papers: actual fault detection at submission versus integration, with reviewer repair provenance. The October study explicitly proposes mutation analysis, so simply adding a mutation tool is insufficient novelty. A useful result would identify which initially green suites miss real reported behavior and whether the review-stage changes repair those misses. Sample size should follow feasibility and precision planning, not an arbitrary promise of dozens of tasks. SmartKit can later serve as a demonstration of a resulting verification practice; one SaaS starter cannot establish ecosystem-wide effectiveness.

## Claims to avoid

- Merged = correct; unmerged = failed code; test file present = adequate verification.
- Agent branch or footer = fully autonomous patch; no visible trace = entirely human work.
- Reviewer comments or elapsed PR days = measured human effort.
- Agent-supported final code = the agent's initial output.
- A within-project adjusted association = causal agent effect; controlling patch size can remove part of a true total effect.
- Higher coverage = stronger bug detection; passing self-written tests = independent acceptance validation.
- A public OSS sample = commercial SaaS workflows; a buildable merged subset = all agent contributions.

## Reproducible search log

Broad discovery searches (web search; primary records then opened):

- `AIDev dataset coding agents pull requests review empirical study`
- `AI coding agents pull requests human review rework tests empirical 2026`
- `"AIDev: Studying AI Coding Agents on GitHub"`
- `"Where Do AI Coding Agents Fail?"`
- `"An Empirical Study of Tests in Agentic Pull Requests"`
- `"Test Coverage Analysis of Agentic Pull Requests"`
- `"When Code Authors Are Agents" "authors"`
- `"Testing with Coding Agents" "Large-Scale" authors`
- `"METR" "experienced" "19%" "2025" randomized`
- `"Fiona Chen" "James Stratton" AI coding review`

Narrowing/verification: primary arXiv landing pages and full texts; author-hosted PDFs; ACM DOI metadata; official dataset card and repository; full-text searches for mutation, validity, attribution, replication, November version, 35.7 and 56.1. Secondary news/reddit surfaced candidate leads but supplied no final evidence. No claim of exhaustive systematic-review coverage: this is a focused scout designed to identify concrete problems and nearest competitors.
