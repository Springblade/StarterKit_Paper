# Scientific evidence and design review

Review date: 10 November 2026. This review supersedes the earlier presentation-only readiness assessment. It covers every section and the scientific claims attached to all references. Retrieval, claim-scoped reading, and experimental validation are distinguished below.

## Assessment

The question is scientifically testable as a controlled SmartKit case study. The manuscript does not yet establish a new empirical finding, a validated task dataset, or a distinct contribution relative to all existing artifacts. Citation count is not evidence of those achievements.

The revised draft has a defensible chain: repository context can influence agent decisions; tests have incomplete and setting-dependent detection ability; therefore concrete layout and verification interventions can be compared using qualified behavioral criteria. None of the cited studies demonstrates that SmartKit's feature layout improves correctness. That proposition remains a hypothesis. The existing inventory is real planning data, not experimental evidence of agent reliability.

## Major concerns and corrections

| Concern | Evidence and consequence | Disposition |
|---|---|---|
| Overcompressed account of context files | Gloaguen v3 §4.2 distinguishes generated files from developer files; the latter have a small positive average difference from no context, without statistical significance in that comparison. “No general improvement” hid this distinction. | Rewrote the literature paragraph and pinned v3. No claim that all instructions are ineffective. |
| Proximity mechanism overinterpretation | Zhu §3.3 and §5 jointly vary location and task relatedness. Their outcome includes implementation choice, not proof of superior maintainability. | Added this limitation and restricted our intervention to the actual combined changes in exposure, paths, and grouping. |
| Task specification did not reflect source | `list-orders.ts` already accepts a status filter; the history page directly queries ownership-scoped orders without exposing a filter control. These are distinct data paths. | Refined the candidate to history-page UI/data-path filtering. Did not label it a wholly absent backend feature, qualified benchmark task, or demonstrated runtime vulnerability. |
| Missing component outcome made the endpoint ambiguous | A numeric product is not defined when acceptance/preservation cannot be assessed. Dropping such cases biases apparent success upward. | Defined categorical component status and a joint-success indicator. Agent-caused unassessable cases are joint failures; infrastructure missingness has separate adjudication and sensitivity bounds. Updated the outcome figure. |
| Fixed-task estimand mixed with task-population resampling | A mean over a frozen convenience set differs from an average over a sampled population. Task bootstrap cannot establish representativeness. | Added the empirical estimator; separated repeat-execution uncertainty from task sensitivity/generalization; grouped related variants into families. Exact interval procedure remains a required freeze decision. |
| Multiplicity and analysis flexibility | Four simple effects plus interaction, multiple models, and several outcomes were insufficiently ranked. | Defined two primary marginal effects, secondary simple effects/interaction, a prespecified primary configuration, and Holm control if confirmatory tests are used. Interval method and valid test construction must be fixed before main outcomes. |
| Verification package was too vaguely specified | More tests may duplicate basic checks, leak hidden cases, or add unsupported requirements. | Required a check-to-contract map, detection rationale, separate visible/final cases, and a treatment manifest. The effect remains access to a package, not pure execution feedback. |
| Reproducibility controls were incomplete | Randomizing run order alone does not handle drift, reachable reference history, or uncontrolled environments. | Added repetition-block scheduling, provider/batch logs, model-change separation, solution-history isolation, and common token/time termination rules. |
| Novelty remains unestablished | SWE-bench already distinguishes new and retained tests; FeatureArc explicitly evaluates new/existing behavior; Mehta controls verification tools; Constraint Decay evaluates feature tasks with behavioral and structural checks. | Kept explicit extension/replication positioning. No first-study or novel-metric claim. Need artifact-level comparison against implemented tasks and interventions. |

## Reading coverage and source limits

The retrieval script archived 16 of the 20 original external full texts as HTML/PDF and extracted text. For these, the review inspected the passages relevant to the manuscript's claims, prioritizing methods, endpoints, results, and validity sections of the closest studies. This is not a line-by-line review of every appendix. Raw retrieval status is in `sources/retrieval-ledger.json`; a successful download alone is not counted as substantive reading.

Four direct downloads failed or returned insufficient content: Borg, Parnas, Inozemtseva, and Arcuri. Their available publisher/institutional versions were consulted with the web reader. Borg's Phase 2 design and scope, Parnas's decomposition criteria, and Inozemtseva's methods/results were inspected there. Arcuri remains publisher-summary/methods-rationale support; full-text access was not established. A newly added Holm citation has its bibliographic record checked against the journal/JSTOR record; the attempted full-text PDF was blocked. It is used only for the named standard multiplicity procedure, not for an extracted empirical result. The local thesis was checked for the specific SmartKit/convention-evaluation claims. No claim that all 22 references received an exhaustive full-text review is made.

## Claim-to-source audit

| Source | Relevant inspected location | Permitted use and boundary |
|---|---|---|
| Gloaguen, arXiv:2602.11988v3 | §4.2, §4.4, §5 | Mixed context-file effects; Python/task-resolution scope. No universal claim about documentation. |
| Zhu, arXiv:2610.38244v1 | §3.3–3.6; §5 | Precedents, placement, and instructions affect choices; location and relatedness are not isolated. |
| Dente, arXiv:2605.06445v2 | §3.3; Appendix C.4; G.1 | Separate behavioral/static evaluation and codebase-ablation feature tasks. Prior art, not proof for our architecture. |
| Patel, arXiv:2606.21804v2 | §3.1–3.3; §5.1–5.3 | Two-step downstream evaluation; static metrics do not fully explain observed differences. Does not causally identify feature locality. |
| FeatureArc, arXiv:2610.37434v1 | §II-A/B; III-D; IV-D; VI-B | Persistent same-feature chains and F2P/P2P validation. Fresh-session factorial is the proposed difference, not preservation alone. |
| Mehta, arXiv:2608.28795v2 | Introduction/design, methods and limitations passages | Controlled verification-tool access during application building. Different workload/package and a custom harness; results do not certify our tests. |
| SWE-bench, arXiv:2310.06770v3 | Evaluation and Appendix task fields | Existing repository issue tasks, FAIL_TO_PASS/PASS_TO_PASS. Our joint endpoint is not itself new. |
| SWE-agent, arXiv:2405.15793v3 | Interface design and case-study analysis | Interface affects navigation/editing/testing; supports harness control, not a layout benefit. |
| Agentless, arXiv:2407.01489v2 | Workflow and issue-quality analysis | Localization/repair/validation and ambiguous or answer-leaking task descriptions. Version-specific preprint citation retained. |
| SWE-Bench Pro, arXiv:2509.16941v2 | Scaffold, evaluation settings, issue ambiguity | Longer multi-file workload and explicit task contracts; benchmark scores not transplanted to SmartKit. |
| EvalPlus, arXiv:2305.01210v3 | Test augmentation and evaluation/results | Inadequate tests miss incorrect synthesized functions and can affect ranking. Function-level setting differs. |
| Zhao, arXiv:2607.22880v1 | §3.6–3.7; §5.4; §7–8 | Metric usefulness depends on bug-free/buggy input and aggregation; Java/Defects4J scope. |
| Just et al., FSE 2014 | Experiment design, real-fault/mutation comparison | Association in evaluated Java systems; mutants support diagnostics, not oracle completeness. |
| Barr et al., TSE 2015 | Oracle definitions; specified/derived oracles | Basis for requirement-grounded checks and limits of soundness/completeness. |
| Lost in the Middle, TACL 2024 | §2 experimental setup and positional analysis | QA/retrieval sensitivity; explicitly not a repository-editing experiment. |
| Reflexion, arXiv:2303.11366v4 | Feedback/memory mechanism and trial analysis | Reflection with retained experience; not the same as our within-session checks. |
| Borg et al., EMSE 2026 | Publisher methods/Phase 2 design and interpretation | Human downstream evolution; observed null does not prove equivalence or transfer to agents. |
| Parnas, CACM 1972 | Reprinted decomposition comparison and criteria | Information hiding/change locality; not synonymous with feature directories. |
| Inozemtseva and Holmes, ICSE 2014 | §3 and §4.3 | Coverage relationship controlling suite size; effectiveness measured using mutation in this study. |
| Arcuri and Briand, STVR 2014 | Publisher summary, journal metadata | Need to account for stochastic executions; not a justification for a particular unselected interval model. |
| Holm, SJS 1979 | Journal/JSTOR bibliographic record | Named familywise procedure only; assumes valid individual tests, which must be fixed in the protocol. |
| Local thesis | SmartKit definition, pilot convention rubric, bundle-confound discussion | Supports artifact and prior evaluation description. Does not supply fresh trial observations. |

## Data verification

The audit CSV has six unique task IDs, all `constructed_candidate` and `unvalidated`. The figure's 5/1 split follows recorded source surfaces; it describes this inventory only. The code-source observations above refine one candidate without changing those historical counts. No task has been run end to end or admitted to a main dataset in this review. No API trials, build qualification, production transactions, or reconstructed pilot scores were generated.

The test file for payment-payload processing mocks persistence and order completion. It therefore cannot establish database-transaction or concurrent-delivery correctness by itself. This confirms the proposal's need for suitable integration checks, without asserting that production behavior is defective.

## Required author decisions and next evidence

1. Confirm intended business/access behavior where UI paths and actions differ, then qualify at least one task and both baseline variants.
2. Approve a traceable task set with sufficient domain/family diversity; six constructed candidates are not evidence of representativeness.
3. Fix interval/test construction, primary model, sample/precision targets, budgets, and infrastructure policies before main data.
4. Compare the actual tasks and package with closest public artifacts; choose an extension claim only if the differences are substantively useful, otherwise state replication.
5. Retain source notes, drafts, and research decisions, and disclose AI assistance according to university/venue requirements.

No numeric scientific-quality score is assigned. The proposal's rationale is supported; novelty, evaluator validity, and intervention effectiveness remain different propositions requiring their own evidence.
