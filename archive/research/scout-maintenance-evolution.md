# Scout: maintenance, change propagation, and scaffold evolution

Research cutoff and retrieval: 2026-11-09. Primary-source scout for SmartKit thesis reframing. This is a research working note, not manuscript prose. Verification followed deep-research/SKILL.md and references/citation-protocol.md: existence/title/authors checked against primary records; findings checked against abstracts and, for closest collisions, full text. No experiment was run and no fresh empirical result is claimed.

## Frozen questions

1. What has already been established about agents carrying their own code through successive changes, including regressions and maintainability?
2. Which observed failure mechanisms could support a narrower controlled question using real repository history rather than a conventions score on one boilerplate?
3. Which findings contradict an unconditional claim that agent-generated code necessarily becomes less maintainable?

## Search record and limits

Queries included `SlopCodeBench code erosion iterative development benchmark`; `benchmark coding agents long horizon software evolution cross file consistency maintenance SWE evolution`; `"Do AI Agents Write Less Maintainable Code Than Human Developers?"`; `"FeatureLoop" "Benchmarking Coding Agents"`; `"Multi-step SWE" agents paper`; `"RoadmapBench" arxiv`; `coding agents cross file consistency change propagation benchmark 2026 arxiv`; and `"agent" "maintainability" "no" "human" code study 2026 arxiv`. Followed primary references and checked arXiv/publisher/project records. Search-engine discovery was used, but third-party summaries were not used as evidence. This is one bounded perspective, not a systematic field-complete search. Absence in this scout does not establish novelty.

## Verified corpus: nine works

### 1. SlopCodeBench — the direct collision with generic code-erosion work

Gabriel Orlanski, Devjeet Roy, Alexander Yun, Changho Shin, Alex Gu, Albert Ge, Dyah Adila, Frederic Sala, Aws Albarghouthi (2026), *SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks*. VERIFIED. [arXiv v1 full text](https://arxiv.org/html/2603.24755v1); [author repository](https://github.com/SprocketLab/slop-code-bench); [updated primary research page](https://snorkel.ai/research-paper/slopcodebench-benchmarking-how-coding-agents-degrade-over-long-horizon-iterative-tasks/).

Constructed CLI/API behavioral problems let agents repeatedly extend their own architecture. V1 reports 20 problems/93 checkpoints; the updated primary page reports 36/196. Do not mix their result denominators. V1 measures complexity concentration and verbosity and finds deterioration; its quality prompts improve initial quality without stopping accumulation. Native provider harnesses differ between model families. Only the workspace survives checkpoints; conversations, installed packages, and session state reset. Human repositories calibrate static metrics rather than supply matched solutions to identical tasks. Full-text §§2–4 and Appendix C inspected. This already covers evolving specifications, self-authored code, structural erosion, and prompt interventions; static proxy deterioration alone cannot establish later maintenance cost.

### 2. SWE-EVO — release-scale coordinated changes

Minh V. T. Thai, Tue Le, Dung Nguyen Manh, Huy N. Phan, Nghi D. Q. Bui (2025), *SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios*. VERIFIED. [Full text](https://arxiv.org/html/2512.18470v1).

Historical release notes and snapshots from seven Python projects support 48 evolution tasks, averaging 21 modified files and 874 tests. GPT-5/OpenHands resolves 21% under its setup. These are broad changes to real repositories, reconstructed as evaluation tasks, not a direct observation of months of autonomous production maintenance. The comparison with SWE-bench changes both task distribution and scale, so it does not isolate horizon causally. Full-text introduction, construction headings, and experimental findings inspected. A proposal merely asking whether agents can modify many related files is already occupied.

### 3. SWE-Milestone — continuous evolution and error accumulation

Gangda Deng, Zhaoling Chen, Zhongming Yu, Haoyang Fan, Yuhong Liu, Yuxin Yang, Dhruv Parikh, Rajgopal Kannan, Le Cong, Mengdi Wang, Qian Zhang, Viktor Prasanna, Xiangru Tang, Xingyao Wang (2026), *SWE-Milestone: Evaluating AI Agents on Continuous Software Evolution*. ICML, PMLR 306:23853–23890. VERIFIED. [Publisher record](https://proceedings.mlr.press/v306/deng26d.html); [project](https://swe-milestone.com/).

DeepCommit reconstructs executable milestone DAGs from real commit histories. Evaluation spans 12 models/four agent frameworks and reports a drop from over 80% isolated-task performance to at most 38% continuous performance. The measured system includes agent, framework, sequencing, and reconstruction pipeline. This directly collides with “earlier mistakes accumulate during continuous maintenance.” Evidence here is publisher abstract and project material; publisher-linked PDF fetch failed, so finer construction claims are intentionally omitted.

### 4. RoadmapBench — large version upgrades

Xinbo Xu, Ruihan Yang, Haiyang Shen, Wendong Xu, Bofei Gao, Ruoyu Wu, Kean Shi, Weichu Xie, Xuanzhong Chen, Ming Wu, Jason Zeng, Michael Heinrich, Elvis Zhang, Liang Chen, Kuan Li, Baobao Chang (2026), *RoadmapBench: Evaluating Long-Horizon Agentic Software Development Across Version Upgrades*. VERIFIED. [Primary record](https://arxiv.org/abs/2605.15846); [full text](https://arxiv.org/html/2605.15846v1).

115 tasks reconstruct real upgrades in 17 repositories/five languages; median reference change is 3,700 lines over 51 files. Thirteen models are evaluated, with highest task resolution 39.1%. The task starts from a source version and requests a target roadmap; the historical patch is evidence of feasible evolution, not a unique required implementation. Its broad scope already covers upgrade-scale change coordination. Full text retrieved; abstract-level claims used here.

### 5. FeatureLoop — staged feedback, cumulative requirements, regressions

Jia Feng, Alyssa Wu, Cuiyun Gao, Yunlong Wang, Songyuanyi Lu, Zhichao Hu (2026), *FeatureLoop: Benchmarking Coding Agents under Evolving Requirements*. VERIFIED. [Primary record](https://arxiv.org/abs/2610.35488); [full text v1](https://arxiv.org/html/2610.35488v1).

61 reviewed tasks from 34 repositories span 2–8 stages. Real public issues ground goals, but staged specifications, extensions, checks, and reference checkpoints are constructed with agents and human review; they are not literal replayed issue histories. Later public history is screened to exclude already-complete solutions. In a shared Claude Code harness, pooled strict completion rises from 40.3% upfront to 51.6% progressive to 64.1% progressive plus correction. It therefore provides counterevidence to “more iterations necessarily worsen final success.” Full-text §§2.2–2.4, §4.1, and appendix setup inspected. Any new evaluation of staged feature requests plus regression checks must distinguish itself explicitly from this work.

### 6. Multi-step SWE — very recent collision, with a useful admitted limitation

Xiangkai Zeng, Zheng Liu, Zihao Lin (2026), *Multi-step SWE: Can Coding Agents Keep Building on Their Own Code Over Long Horizons?* Posted Nov 4. VERIFIED. [Primary record](https://arxiv.org/abs/2611.07166); [full text](https://arxiv.org/html/2611.07166v1); [authors' report](https://www.klavis.ai/blog/multi-step-swe).

69 tasks comprise 5–15 dependent steps, 574 steps total, across nine languages and both new and existing codebases. Public sources of truth ground verifiers. Highest complete-task solve rate is 18.5%, despite considerably higher step success. Crucially, authors explicitly leave reference-initialized isolated-step baselines for future work: present results cannot separate accumulating errors from intrinsic later-step difficulty. C/C++ accounts for 38/69 tasks. Full-text limitations inspected. This is a methodological opportunity, but merely adding an isolated-step control is already an acknowledged extension rather than a broad new research premise.

### 7. CrossSWE — change propagation and interface consistency are already explicit

Silin Chen, Yuling Shi, Heng Lian, Zihan Zhang, Xiaodong Gu, Haotian Lin, Zhensu Sun (2026), *CrossSWE: Benchmarking Cross-Repository Joint Development for Coding Agents*. Posted Nov 1. VERIFIED. [Full text](https://arxiv.org/html/2611.01484v1).

171 historical instances span 165 repositories, 20 domains, and 13 languages. Executable partial-change checks establish that coordinated changes are necessary. Cross-repository inconsistency accounts for 44.2% of analyzed failures, not 44.2% of all tasks. All models share mini-SWE-agent, 300 interactions, and $10/instance. Repositories are provided rather than discovered; 165 instances involve two repositories. Full-text §§5.4 and limitations inspected. This supplies a strong necessity-test design for a smaller web-app study, while preventing a generic “change propagation is hard” novelty claim.

### 8. CodeThread — the closest controlled maintainability experiment

Shaswat Patel, Betty Li Hou, Arun Purohit, Kai Xu, Jane Pan, He He, Valerie Chen (2026), *Is Agent Code Less Maintainable Than Human Code?* arXiv:2606.21804, v2 Sep 29. VERIFIED. [Record](https://arxiv.org/abs/2606.21804); [v2 full text](https://arxiv.org/html/2606.21804v2).

Constructs two-step chains by deleting target function bodies, asking agents to reconstruct functionality, and comparing a dependent task on agent versus original human implementations. Passing baseline tests and failing downstream tests filter reconstructed intermediates; equivalence is test-relative. Four models/four benchmarks show generally lower downstream resolution on agent code, with exceptions; the largest shared-instance gap is 13.1 percentage points. Traditional static metrics generally do not explain the gap; input-validation/error-handling drift is more informative. Those drift labels and regression associations do not establish a causal mediator. Full-text §§3, 4.2, 5, and limitations inspected. This rules out simply proposing “human versus AI starting code plus downstream change” as new.

### 9. Echoes of AI — direct counterevidence with a different unit of analysis

Markus Borg, Dave Hewett, Nadim Hagatulah, Noric Couderc, Emma Söderberg, Donald Graham, Uttam Kini, Dave Farley (2026), *Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability*. Empirical Software Engineering 31, 161. DOI 10.1007/s10664-026-10889-1. VERIFIED. [Publisher full text](https://link.springer.com/article/10.1007/s10664-026-10889-1).

A preregistered two-phase study has 151 completing participants, mostly professionals: humans implement a Java-web feature with/without AI; new humans evolve those implementations without AI in phase-two random assignment. No systematic downstream completion-time or code-quality disadvantage is detected. First-phase tool use follows preferences and models adjust for Java proficiency; this is not random assignment of autonomous-agent code generation. Data collection ended Jan 2025 and no whole-task fully autonomous agents were observed. Full-text abstract, §§3.1, 4.1, and tool-use details inspected. This does not negate CodeThread: human supervision, downstream author, task size, and model era differ.

## Synthesis and proposed questions

The broad phenomenon is well occupied: longitudinal code erosion, continuous repository evolution, large upgrades, staged feedback, and consistency across repositories each have direct precedents. Changing the stack to Next.js or replacing function tasks with SaaS features is domain coverage, not by itself a scientific contribution. The more promising move is to manipulate a precise failure mechanism and measure observable user behavior, while separating representation effects from accumulated semantic errors. These are candidate directions, not established novel contributions.

### Candidate RQ1: Does inherited contract drift cause downstream change failures even when current acceptance tests pass?

Operational question: among equivalent-for-current-tests implementations of real web-application changes, does preserving versus restoring an explicit input/error/state contract change the success of a later historically motivated request?

Decisive experiment: mine successive, semantically dependent issue/PR pairs from multiple public applications, retaining exact base/merge SHAs and contemporaneous discussions. Select pairs using executable dependency evidence: later behavior must require a coordinated change, and reverting a required component must fail an appropriate check. Reproduce baseline and later behavior in pinned containers before evaluating agents. For each intermediate that passes current tests, construct a minimal contract-restored variant, validated against an independent oracle, and a sham-edit control of comparable size. The same downstream request, agent version, harness, budget, and clean context are paired across original, restored, and sham conditions. Primary outcome is cumulative behavioral success; secondary outcomes distinguish new-feature failure, regression, and invalid setup. Hold out contract tests from the agent. Report all candidate exclusions and treat each issue chain/repository as a cluster.

This extends an association into an intervention: an improvement only after targeted contract restoration would support a mechanism. If sham edits perform equally well, restoration adds no benefit, or fuller baseline tests eliminate all disagreement, the causal claim fails or reduces to inadequate test coverage. CodeThread is the mandatory comparator; new tasks alone are insufficient. SmartKit can be one feasibility fixture, but one repository cannot establish cross-project generality.

### Candidate RQ2: Does revealing a dependency map improve complete change propagation beyond extra context and extra verification?

Operational question: with identical behavioral requirements and compute budget, does an executable map linking a changed concept to its consumers reduce omission and regression relative to a length-matched repository summary and ordinary test feedback?

Decisive experiment: use real issue/PR pairs whose joint necessity is independently demonstrated by partial-change/revert tests. Include changes to persistence, validation, API behavior, tests, and documentation only when each artifact is actually required. Derive the map from information available before the target fix; never expose the historical gold patch or its file list. Compare no map, length-matched generic summary, map alone, and equivalent extra verification budget. Freeze total tokens/time and include a held-out repository evaluation. Evaluate semantic consistency at public observation points and human-adjudicated omission categories, not conformity with the human patch. A map that succeeds only by revealing gold locations or consuming extra budget does not answer the question.

This question is more speculative and needs a targeted follow-up against repository localization, impact-analysis, and specification-compilation methods before commitment. It becomes redundant if a prior method already tests the same information intervention with matched context/compute on jointly necessary changes. It also fails substantively if failures are almost entirely implementation mistakes after all affected consumers are already found.

## Concrete next decision

Do a free data-feasibility audit before any paid runs: identify a small set of runnable dependent change pairs across at least several public web applications, with provenance and executable acceptance/regression checks. Retain negative cases and failed setup attempts. Then choose one mechanism and compare directly with the nearest prior study. The deleted one-feature pilot cannot serve as fresh empirical evidence; a new, reproducible collection must distinguish historical artifacts, researcher-constructed tasks, and agent-generated trajectories.

No claim of novelty is justified by this search alone. Before finalizing RQ1, inspect all CodeThread related-work citations on behavioral drift/design constraints. Before finalizing RQ2, inspect change-localization and repository specification methods. Neither direction should be sold as the first long-horizon or consistency benchmark.
