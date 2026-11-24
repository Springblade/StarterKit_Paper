# Scout: application invariants during agentic feature development

Search date/cutoff: 2026-11-09. Independent scout under the deep-research skill and its two-step citation protocol. All eight papers below passed existence and claim checks against primary sources. This is a bounded scout, not proof that no additional work exists. No experiments or paid APIs were run.

## Brief

RQ1: What direct evidence shows coding agents implementing a requested feature while violating application correctness or security requirements?

RQ2: Does prior evaluation distinguish setup failure from failure to preserve existing domain rules, especially across requests, tenants, retries, and persistent state?

RQ3: What narrow empirical question remains credible after the closest competing benchmarks are considered?

The intended outcome is a defensible paper direction independent of SmartKit, framework conventions, and server/client boundary checks. A business invariant means a property of allowed state or state transitions (for example, an operation cannot debit twice for one logical event), rather than stylistic compliance. Examples in this document are proposed study targets, not observed failures.

## Verified papers, organized by what their evidence actually establishes

### 1. Closest direct competitor: SusVibes

Songwen Zhao, Danqing Wang, Kexun Zhang, Jiaxuan Luo, Zhuo Li, and Lei Li. **Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks.** First posted 2025-12-02; inspected arXiv v4, 2026-09-21. ICML 2026 status supported by the authors' repository citation, not inferred from arXiv keywords. [Full text](https://arxiv.org/html/2512.03262v4), [metadata](https://arxiv.org/abs/2512.03262), [author repository and venue citation](https://github.com/LeiLiLab/susvibes).

**Evidence:** 186 security-sensitive feature requests reconstructed from real open-source vulnerability histories, evaluated with functional and security tests. For SWE-agent with Claude 4 Sonnet, 57% are functionally correct and 11.8% secure. These are task-set-specific results, not population prevalence. Prompts primarily specify functionality; the agent must recover implicit security requirements. Full-text construction and mitigation sections inspected.

**Implication:** “Feature tests pass but code is insecure” and “repository feature additions need hidden security tests” are already central contributions here. Real repositories do not make its task distribution representative of ordinary feature requests: sampling starts with known vulnerability history. A new study needs a different sampling frame or different properties, not merely Next.js tasks.

### 2. Important adversarial comparator: SecureVibeBench

Junkai Chen, Huihui Huang, Yunbo Lyu, Junwen An, Jieke Shi, Chengran Yang, Ting Zhang, Haoye Tian, Yikun Li, Zhenhao Li, Xin Zhou, Xing Hu, and David Lo. **SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios.** First posted 2025-09-26 under the older title *SecureAgentBench*; inspected v5, 2026-06-06. Publication venue not independently confirmed; treat as preprint. [Full text](https://arxiv.org/html/2509.22097v5), [metadata](https://arxiv.org/abs/2509.22097).

**Evidence:** 105 C/C++ memory-safety coding tasks from 41 OSS-Fuzz/ARVO projects, reconstructing contexts at vulnerability introduction; functional and security oracles include static and dynamic checking. Latest abstract reports 23.8% correct-and-secure for the best evaluated configuration. Do not combine the old title's 15.2% result with the revised evaluation. Full-text formulation and overview inspected.

**Implication:** Historical-context fidelity is a contribution already made here. Its memory-safety focus leaves application state semantics distinct, but calling a dataset “realistic vulnerability-introducing scenarios” is insufficient differentiation.

### 3. Application generation with executable attacks: BaxBench

Mark Vero, Niels Mündler, Victor Chibotaru, Veselin Raychev, Maximilian Baader, Nikola Jovanović, Jingxuan He, and Martin Vechev. **BaxBench: Can LLMs Generate Correct and Secure Backends?** 2025; ICML 2025 Spotlight confirmed by the authors' institutional publication page. [Full text inspected](https://arxiv.org/html/2502.11844v2), [project](https://baxbench.com/), [venue confirmation](https://www.sri.inf.ethz.ch/publications/vero2025baxbench).

**Evidence:** 392 tasks combine 28 scenarios and 14 backend frameworks across six languages. Generated backend services face functionality tests and expert-designed end-to-end exploits. These are constructed application tasks from specifications, not naturally occurring historical feature additions. Full-text construction and evaluation sections inspected; avoid quoting early-version correctness numbers because the abstract changed between versions.

**Implication:** An executable backend, more files, more frameworks, or exploit tests do not by themselves supply novelty. Its security/functionality split is a suitable baseline measurement design; brownfield preservation of previously correct stateful behavior is a different unit of analysis.

### 4. Direct setup-versus-logic overlap: ABC-Bench

Jie Yang, Honglin Guo, Li Ji, Jiazheng Zhou, Rui Zheng, Zhikai Lei, Shuo Zhang, Zhiheng Xi, Shichun Liu, Yuxin Wang, Bo Wang, Yining Zheng, Tao Gui, and Xipeng Qiu. **ABC-Bench: Benchmarking Agentic Backend Coding in Real-World Development.** Findings of ACL 2026, pp. 22765–22787. DOI: 10.18653/v1/2026.findings-acl.1142. [Venue metadata](https://aclanthology.org/2026.findings-acl.1142/), [primary full text](https://arxiv.org/pdf/2601.11077).

**Evidence:** 224 repository-derived tasks; 132 use pre-provisioned runtimes and 92 additionally require environment configuration. Section 4.1 removes synthesized setup files for the latter; section 5.2 and Figure 4 distinguish build success S1 from functional success conditional on building S2. Tasks mask endpoint implementations, rather than necessarily following actual feature-request histories. Full-text construction, verification, and setup analysis inspected.

**Implication:** It already demonstrates that setup can mask coding competence. I found no same-task randomized paired setup toggle or dedicated preservation outcome. Comparing its two different task subsets would not identify a setup effect. Any stronger claim of absence needs artifact inspection.

### 5. Closest SaaS overlap: SaaSBench

Qingnan Ren, Shun Zou, Shiting Huang, Ziao Zhang, Kou Shi, Zhen Fang, Yiming Zhao, Yu Zeng, Qisheng Su, Lin Chen, Yong Wang, Zehui Chen, Xiangxiang Chu, and Feng Zhao. **SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering.** arXiv:2605.17526v1, 2026-05-17; preprint status in inspected record. [Full text](https://arxiv.org/html/2605.17526v1), [metadata](https://arxiv.org/abs/2605.17526).

**Evidence:** 30 from-scratch enterprise SaaS reconstruction tasks; 5,370 dependency-linked validation nodes; evaluation includes Logic and AuthZ. The source repositories validate the reference oracles; agents receive PRD and knowledge-base artifacts. The 95.6% early-failure result refers to T4/T5 among 480 analyzed capability units, not 95.6% of independent tasks. Deterministic and rubric-judge evaluation are combined. Full-text construction, scoring, and failure taxonomy inspected.

**Implication:** “Full-stack SaaS evaluation,” dependencies among checks, and setup diagnosis are occupied. I found no warm-start or setup ablation; absence of those terms alone is not conclusive. It evaluates reconstruction, not preserving a functioning brownfield application's existing rules.

### 6. Repository feature additions: FEA-Bench

Wei Li, Xin Zhang, Zhongxin Guo, Shaoguang Mao, Wen Luo, Guangyue Peng, Yangyu Huang, Houfeng Wang, and Scarlett Li. **FEA-Bench: A Benchmark for Evaluating Repository-Level Code Generation for Feature Implementation.** ACL 2025, pp. 17160–17176. DOI: 10.18653/v1/2025.acl-long.839. [Venue metadata](https://aclanthology.org/2025.acl-long.839/), [full PDF](https://aclanthology.org/2025.acl-long.839.pdf).

**Evidence:** Feature-focused tasks drawn from pull requests in 83 GitHub repositories and paired with relevant unit-test files. It explicitly requires both introducing new components and editing existing connected code. Abstract and full PDF introduction inspected; no claim here that all tasks receive domain-specific invariant tests.

**Implication:** Cross-file integration in feature implementation is already evaluated with real repository evidence. A proposed feature-addition benchmark must explain what its independent preservation oracle reveals beyond ordinary PR tests.

### 7. Features spanning development history: FeatureBench

Qixing Zhou, Jiacheng Zhang, Haiyang Wang, Rui Hao, Jiahe Wang, Minghao Han, Yuxue Yang, Shuzhe Wu, Feiyang Pan, Lue Fan, Dandan Tu, and Zhaoxiang Zhang. **FeatureBench: Benchmarking Agentic Coding for Complex Feature Development.** arXiv:2602.10975, 2026-02-11; ICLR 2026 publication banner confirmed in primary conference PDF. [Full text](https://arxiv.org/html/2602.10975v1), [conference PDF](https://openreview.net/pdf/5a73d3028cb1df0955fd6a1e37f104849abdc762.pdf).

**Evidence:** Dependency-graph tracing from tests constructs feature-level tasks spanning multiple commits/PRs, with 200 evaluation tasks and 3,825 executable environments from 24 repositories in the first version. Construction aims to preserve other features after removal. Full-text abstract and construction overview inspected.

**Implication:** “A feature spans more than one PR” and preserving other functionality during task construction are not open contributions. Domain invariants that require sequences or perturbations remain a possible narrower measurement target, subject to task-by-task comparison.

### 8. Temporal side effects, but agent execution rather than coding: LIMBO

Jiapeng Li. **Where Does Exactly-Once Live? Model, Harness, and Tool-Contract Effects on Duplicate Side Effects in LLM Agents.** arXiv:2609.29095v1, 2026-09-24; preprint. [Metadata and abstract](https://arxiv.org/abs/2609.29095), [full text](https://arxiv.org/html/2609.29095v1).

**Evidence:** A deterministic sandbox with six services and twelve service-boundary fault modes; committed-effect ledgers score tool-agent behavior under ambiguity, late commits, and duplicate delivery. The paper varies model, harness, and contract. Abstract and full-text outline inspected; theoretical result not independently checked.

**Implication:** Retry ambiguity and idempotency are already studied empirically for tool use. A coding study should test whether generated application code implements the required guarantees under those faults. It must not relabel a runtime-agent result as evidence that coding agents generate broken payment handlers.

## Additional deployment-facing evidence, outside the eight-paper corpus

Stripe's primary engineering report, [Can AI agents build real Stripe integrations? We built a benchmark to find out](https://stripe.com/blog/can-ai-agents-build-real-stripe-integrations), provides an adversarial check against assuming all full-stack integration is uniformly poor: it reports high task scores for some tested configurations and describes browser-verified purchases. This is a vendor benchmark report, not a peer-reviewed paper or production incident prevalence study. It strengthens the need to specify failure conditions precisely. Do not use a secondary InfoQ comment about missing idempotency tests as proof of Stripe's actual test coverage.

## Synthesis and dataset implications

The strongest evidence for functional/security divergence in brownfield feature implementation is SusVibes, while BaxBench establishes divergence for constructed backend generation. SecureVibeBench adds faithful vulnerability-introduction context, but in memory safety. FEA-Bench and FeatureBench defeat a broad claim that multi-file feature additions are unstudied. ABC-Bench and SaaSBench defeat a broad claim that setup and integration are absent from evaluations. LIMBO defeats a broad claim that retry and duplicate-side-effect failures have not been measured at all. These distinctions limit the remaining contribution rather than eliminate it.

No source in this scout establishes prevalence of billing-idempotency violations in ordinary agent-authored production PRs. A historical vulnerability-selected sample cannot estimate that prevalence. Likewise, a deployment failure makes a downstream property unobserved; treating it as direct evidence that an agent misunderstood a domain rule would overstate the result.

For actual public bug tasks, the defensible immediate sources are SusVibes' linked vulnerability histories, FEA-Bench's PR histories, and FeatureBench's repository/commit task manifests. They require manual screening for persistent-state and temporal properties; their existence does not guarantee a sufficient billing subset. ABC-Bench's endpoint masks are a useful harness starting point but weaker evidence of naturally occurring bugs. SaaSBench seed applications are potential domains and oracle references, not historical feature tasks. No individual billing bug is claimed verified in this scout.

## At most two candidate questions

### Candidate A: Does supplying a verified runnable starting state improve safe feature completion on the same tasks?

Pair each public, historical feature task with two starts: identical source and requirement, either with a verified environment supplied or with its deployment setup withheld. Keep task budget, tools, model, domain facts, and hidden tests fixed; repeat runs and analyze paired task outcomes. Primary outcome: all requested behavior plus preservation of pre-existing executable domain rules. Also report build success and each outcome on all attempts; conditional results alone induce survivor selection. Register whether supplied setup changes time available for implementation, since that mechanism is part of the treatment rather than a nuisance to conceal.

Closest overlap is ABC-Bench's setup split and conditional-stage evaluation; the distinction would be a same-task intervention and preservation-specific outcome. SaaSBench is a motivation for isolating setup, not sufficient evidence that domain competence is low. This is credible only if a hand audit confirms no equivalent matched intervention and if task curation produces real nontrivial domain properties.

**Falsifiers:** supplied setup does not improve joint success; agents already preserve almost every rule after building; ordinary regression tests capture essentially all violations; effects disappear under equally informative setup documentation; or benefits are explained entirely by benchmark packaging defects. A null finding remains useful only with adequate task diversity and uncertainty estimates.

### Candidate B: What does a happy-path feature acceptance test miss about persistent application behavior?

First conduct an empirical audit, not a mitigation proposal. Sample ordinary historical feature requests without conditioning on known security bugs. Recover pre-existing rules from explicit contracts, tests, maintainer discussions, and verified historical fixes. Independently author hidden state-transition and perturbation tests: duplicate delivery, out-of-order events, role changes between steps, partial transaction failure. Require expert validation and a passing reference implementation. Compare acceptance-test success with joint feature-and-preservation success, stratified by rule class and provenance.

The differentiation from SusVibes would be ordinary-request sampling, preservation of existing behavior, and temporal/nonsecurity rules, rather than known vulnerability reimplementation. The differentiation from LIMBO is editing application code rather than operating tools. A new generic “security-aware prompt” is not a contribution earned by this question.

**Falsifiers:** few tasks admit independently verifiable rules; hidden tests encode preferences absent from the actual contract; normal regression tests already detect nearly every issue; effects are dominated by API misunderstandings unrelated to persistence; or the corpus collapses to one application family. Stop before large model runs if those occur.

## Search log and verification limits

Broad queries: `coding agents business logic vulnerabilities benchmark authorization application invariants`; `SWE-bench feature development benchmark integration tests regression agent real repositories`; `LLM billing idempotency benchmark coding agents`; `coding agents business logic paper arxiv invariant`.

Narrow/adversarial queries: `SusVibes benchmark paper security functional feature tasks arxiv`; `BaxBench executable benchmark backend applications security arxiv`; `SecureAgentBench paper arxiv`; `SaaSBench authorization`; `ABC-Bench pre-provisioned environment`; `ABC-Bench ablation`; `ABC-Bench 132 92`; `SaaSBench scaffold OR warm-start OR ablation`; `site:stripe.com/blog agent benchmark`; venue confirmation queries for BaxBench, SusVibes, FeatureBench.

Primary sources were opened after discovery. Important version corrections: SusVibes is 186 tasks in v4 (older reports say 200); SecureAgentBench is renamed SecureVibeBench in v5 and its evaluated systems/results changed; BaxBench early abstract statistics changed. ABC-Bench venue metadata was confirmed against ACL Anthology. Searches with no result are not claims of absence. Full-text access means the relevant sections were inspected, not that every appendix or released test was audited. The remaining work before claiming novelty is artifact-level overlap analysis and verification of individual public feature/bug tasks.
