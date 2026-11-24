Source: https://arxiv.org/html/2606.21804v2
Retrieved for research-direction appraisal on 2026-11-10.

[Skip to main content](https://arxiv.org/html/2606.21804v2#infobox)

Title:

Content selection saved. Describe the issue below:

Description:

[License: CC BY 4.0](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2606.21804v2 \[cs.SE\] 29 Sep 2026

# Is Agent Code Less Maintainable Than Human Code?

Shaswat Patel
††thanks: Equal contribution.

Code and data available at: [https://github.com/shaswatpatel123/CodeThread](https://github.com/shaswatpatel123/CodeThread "")Affiliation: New York University
Email: [spp9399@nyu.edu](mailto:)Betty Li Hou11footnotemark: 1Affiliation: New York University
Email: [betty.li.hou@nyu.edu](mailto:)Arun Purohit
Affiliation: New York University
Kai Xu
Affiliation: New York University
Jane Pan
Affiliation: New York University
He He
Affiliation: New York University
Valerie Chen
Affiliation: Carnegie Mellon University

###### Abstract

Maintainability is a core dimension of software engineering, shaping how code is written, reviewed, and developed over time. While coding agents have demonstrated strong performance on single-issue tasks, it remains unclear how maintainable their code is when future agents build on top of it, potentially leading to compounding downstream effects. We investigate how agent code compares to human code in these maintenance settings, presenting CodeThread, a framework to construct controlled experiments from repository-level coding benchmarks. Applying CodeThread to four frontier coding agents and four benchmarks, we find that agents are less effective at resolving tasks when building on agent code compared to human code, with task resolve rate drops of up to 13.1%. Regression analysis reveals that many traditional software engineering maintainability metrics do not explain this difference. Instead, the clearest signals are subtler behavioral differences in agent code, such as changes to input validation and error handling, along with differences in downstream code size and task difficulty. These findings highlight the need to evaluate coding agents not only by immediate task resolution but also by maintainability, and point to potential sources of downstream errors introduced by agent code.

## 1 Introduction

Coding agents are increasingly integrated into software engineering workflows, with promises of “completing weeks of work in days” ( [OpenAI, 2026a](https://arxiv.org/html/2606.21804v2#bib.bib1 "")). Model capabilities on coding tasks have also improved rapidly, with state-of-the-art agents solving a growing share of repository-level benchmarks ( [OpenAI, 2026b](https://arxiv.org/html/2606.21804v2#bib.bib40 "")).
However, a patch that passes tests and is functionally correct may introduce structural complexity, brittle abstractions, or confusing implementation choices that only surface as failures when the code is extended or modified in downstream tasks (Figure [1](https://arxiv.org/html/2606.21804v2#S1.F1 "Figure 1 ‣ 1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?")).

![Refer to caption](https://arxiv.org/html/2606.21804v2/images/figure_1.png)Figure 1: Two pieces of code both being functionally correct does not mean they are equally maintainable. An example instance where both the human and agent code pass the initial implementation task’s tests, yet when an agent makes a subsequent change to both, the version built on human code passes while the version built on agent code fails.

This dimension of code quality is captured by maintainability, or how well the code can be modified and extended over time. Maintainability has been studied across many software development contexts, and static metrics have emerged to provide quantitative evaluations of maintainability. In particular, structural and size-based
metrics, such as cyclomatic complexity ( [Ebert et al., 2016](https://arxiv.org/html/2606.21804v2#bib.bib4 "")),
Halstead volume ( [Halstead, 1977](https://arxiv.org/html/2606.21804v2#bib.bib19 "")), and cognitive
complexity ( [Campbell, 2018](https://arxiv.org/html/2606.21804v2#bib.bib3 "")), have been used widely as proxies
for the maintenance cost of a project ( [Riaz et al., 2009](https://arxiv.org/html/2606.21804v2#bib.bib21 ""); [Ardito et al., 2020](https://arxiv.org/html/2606.21804v2#bib.bib22 "")). The adoption of coding agents raises questions about whether code authored by agents is as maintainable as human-authored code. Recent work has measured agent code maintainability using these static metrics ( [Wang et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib14 ""); [Orlanski et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib11 "")), but does not compare it with human code. Moreover, static metrics can often be confounded by codebase conventions and context ( [Zhang et al., 2013](https://arxiv.org/html/2606.21804v2#bib.bib39 "")).

To this end, we present CodeThread, a framework for controlled experiments to compare the maintainability of agent- and human-written code based on how well an agent can build on each. CodeThread transforms single-step, repository-level coding tasks (e.g., instances from SWE-Bench [Jimenez et al. (2024)](https://arxiv.org/html/2606.21804v2#bib.bib2 "")) into two-step tasks comprising an initial implementation task and a dependent downstream task. CodeThread then constructs comparable agent and human code on the initial task while holding the downstream task author and test-based evaluation fixed, allowing us to isolate how authorship of the initial task affects downstream agent performance.

We use CodeThread to evaluate four frontier models—Claude 4.5 Sonnet [Anthropic ()](https://arxiv.org/html/2606.21804v2#bib.bib18 ""), GPT-5 [OpenAI ()](https://arxiv.org/html/2606.21804v2#bib.bib17 ""), GLM 4.7 [Zeng et al. (2025)](https://arxiv.org/html/2606.21804v2#bib.bib34 ""); [Z.ai ()](https://arxiv.org/html/2606.21804v2#bib.bib36 ""), and MiniMax 2.5 [MiniMax ()](https://arxiv.org/html/2606.21804v2#bib.bib35 "")—on four software engineering benchmarks spanning a range of programming languages and task types. We find that building on agent code leads to drops in downstream task resolve rates more often than building on human code, with gaps in resolve rate of up to 13.1%. Using code instances from CodeThread, we identify sources of differences in downstream task performance on agent and human code, performing a logistic regression analysis on cases where the two conditions produce different outcomes. We find that traditional static maintainability metrics generally do not explain these differences. Instead, the clearest predictors of cases where the downstream task fails on agent code but succeeds on human code are subtle differences in input validation and error handling. Larger downstream edits and task difficulty also help characterize where the two conditions diverge.

Our contributions are as follows:

1. 1.


We introduce CodeThread, a framework for studying the maintainability of agent code through two-step pull-request chains. CodeThread applies to any SWE benchmark, making it scalable across task types and languages, and provides controlled comparisons of agent to human code.

2. 2.


Applying CodeThread to multiple frontier models and benchmarks, we show that agent code is overall less maintainable than human code, leading to worse downstream task performance.

3. 3.


We analyze the sources of maintainability differences between agent and human code, showing that traditional proxies such as structural complexity and verbosity do not fully capture these differences, which instead often arise from subtler behavioral effects.


Together, CodeThread and our findings suggest that coding agents introduce maintainability costs that compound as their code is reused or extended in ways that current benchmarks and metrics fail to capture. We suggest directions for future work on the maintainability of agent code.

## 2 Related Work

![Refer to caption](https://arxiv.org/html/2606.21804v2/images/CodeThread_framework.png)Figure 2: CodeThread framework. From the original benchmark instance, we construct a two-step task—an Implementation Task followed by a Follow-On Issue—producing three code states (PR0\\text{PR}\_{0}, PR1\\text{PR}\_{1}, and PR2\\text{PR}\_{2}) and three conditions: AA (agent performs both steps), HA (human performs the Implementation Task, agent performs the Follow-On Issue on human code), and HH (human performs both steps). Comparing AA and HA isolates the effect of agent authorship on maintainability, holding the follow-on author fixed.

#### Evaluating Agents on Sequential Tasks.

Several recent benchmarks evaluate coding agents on sequences of dependent tasks rather than individual issues.
CodeFlowBench decomposes Codeforces problems along their function-level dependency tree and requires the agent to implement each subfunction by reusing those it built in earlier turns ( [Wang et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib12 "")).
SWE-Bench-CL orders GitHub issues chronologically within each repository to evaluate whether experience from earlier issues transfers to later ones ( [Joshi et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib13 "")).
SlopCodeBench measures behavioral drift as agents repeatedly modify a codebase across long-horizon iterative trajectories ( [Orlanski et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib11 "")).
In contrast, our work grounds measurements in real GitHub pull requests rather than fully synthetic problems or hand-authored projects. Additionally, by varying the authorship of an intermediate patch while holding the downstream task fixed, we isolate the maintainability cost of agent-written code from the inherent difficulty of sequential development.

#### Maintainability of LLM-Generated Code.

Large-scale GitHub analyses report rising code churn and duplication coinciding with AI-assistant adoption ( [Harding and Kloster, 2025](https://arxiv.org/html/2606.21804v2#bib.bib24 ""); [Cynthia et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib28 ""); [Huang et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib29 ""); [Liu et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib25 "")), static analyses find that LLM-generated code exhibits more code smells than human-written code ( [Paul et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib23 "")), and recent work shows that non-functional quality and design-constraint compliance degrade even when agent-generated patches pass tests ( [Sun et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib26 ""); [Yu et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib27 "")).
Prior work has also measured code-quality degradation in sequential tasks.
MaintainCoder applies synthetic requirement changes to competitive-coding tasks and measures post-modification correctness alongside static metrics such as Cyclomatic Complexity and AST similarity ( [Wang et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib14 "")). SWE-CI uses test pass rates over iterative edit trajectories as a maintainability proxy, treating later-stage pass rate as evidence of how well early decisions support subsequent maintenance ( [Chen et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib15 "")).

Our study instead measures maintainability directly through downstream issue-resolution performance. Rather than relying primarily on static proxies or synthetic requirement changes, we ask whether an agent can successfully complete a dependent follow-on task when the intermediate code it inherits is written by an agent versus a human, creating controlled experiments to measure the effect of authorship. The resulting code can also be analyzed using static metrics and failure-mode annotations, as performed in Section [5](https://arxiv.org/html/2606.21804v2#S5 "5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

## 3 CodeThread

We introduce CodeThread, a framework for measuring the downstream effects of building on agent code in comparison to human code (Figure [2](https://arxiv.org/html/2606.21804v2#S2.F2 "Figure 2 ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?")). CodeThread transforms standard single-issue software engineering benchmark instances into dependent two-step pull-request chains (Section [3.1](https://arxiv.org/html/2606.21804v2#S3.SS1 "3.1 Step 1: Create a Two-Step Task ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?")), allowing for controlled comparisons of downstream outcomes across authorship conditions (Section [3.2](https://arxiv.org/html/2606.21804v2#S3.SS2 "3.2 Step 2: Set-up Authorship Scenarios ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?")) with evaluation built in (Section [3.3](https://arxiv.org/html/2606.21804v2#S3.SS3 "3.3 Step 3: Evaluate agent vs human code ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?")).

CodeThread starts from an existing issue-resolution coding benchmark where instances consist of a written issue, a base commit, a human-authored ground-truth patch, and a test suite to determine whether the patch resolved the task.
Example benchmarks that follow this format include SWE-Bench Verified ( [Chowdhury et al., 2024](https://arxiv.org/html/2606.21804v2#bib.bib5 "")), SWE-Bench
Multilingual ( [Khandpur, 2025](https://arxiv.org/html/2606.21804v2#bib.bib6 "")), SWE-Bench
Pro ( [Deng et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib7 "")), and FeatBench ( [Chen et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib8 "")).

### 3.1 Step 1: Create a Two-Step Task

From each benchmark instance, we construct a two-step chain consisting of two dependent tasks and three code states: the Implementation Task and Follow-On Issue, and code states PR0\\text{PR}\_{0}, PR1\\text{PR}\_{1}, and PR2\\text{PR}\_{2}. To create the first state, PR0\\text{PR}\_{0}, we remove the target function bodies while preserving their signatures, leaving a skeleton version of the benchmark’s initial code state. This provides a starting point from which different authors can implement the intended functionality, similar to the use of skeleton code in prototyping, where an initial code structure is later fleshed out with implementation details [Ryoo et al. (2008)](https://arxiv.org/html/2606.21804v2#bib.bib32 ""); [Queirós (2013)](https://arxiv.org/html/2606.21804v2#bib.bib31 "").

The Implementation Task (PR0→PR1{\\text{PR}\_{0}}\\rightarrow{\\text{PR}\_{1}}) produces human and agent implementations of the same task. Using an LLM, we create an issue asking the author to restore the missing functionality in the skeletonized code. This issue is provided to the agent, which implements the requested functionality to produce the agent PR1\\text{PR}\_{1}. We filter out PR1\\text{PR}\_{1} solutions that have already solved the benchmark issue by requiring them to pass all Pass-to-Pass tests, confirming that the original functionality is restored, while still failing all Fail-to-Pass tests, confirming that the downstream issue is not yet resolved. This ensures that the agent PR1\\text{PR}\_{1} reflects the benchmark’s initial code state rather than a partial or complete solution to the Follow-On Issue; accordingly, the target methods are functionally equivalent across the two PR1\\text{PR}\_{1} versions. Although agents sometimes incidentally satisfy Fail-to-Pass tests while restoring functionality, the filter retains a large majority of instances. Appendix [A](https://arxiv.org/html/2606.21804v2#A1 "Appendix A Synthetic Problem Statement Construction for \"PR\"_1 ‣ Is Agent Code Less Maintainable Than Human Code?") shows the prompt used to generate Implementation Task statements, as well as the prompt given to models when solving it.

The Follow-On Issue (PR1→PR2\\text{PR}\_{1}\\rightarrow\\text{PR}\_{2}) is the original benchmark issue applied on top of the PR1 implementation. The problem statement and testing criteria for the Follow-On Issue are unchanged from the original benchmark, making it a downstream task whose difficulty may depend on the maintainability of the PR1 implementation. We evaluate whether the Follow-On Issue is resolved using the original benchmark test suite: a PR2\\text{PR}\_{2} solution is considered correct if it passes both the Pass-to-Pass tests, confirming that existing functionality is preserved, and the Fail-to-Pass tests, confirming that the original benchmark issue has been fixed.

### 3.2 Step 2: Set-up Authorship Scenarios

Using the two-step issue resolution pipeline, we vary authorship on PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}, creating a total of three comparable authorship scenarios: human PR1\\text{PR}\_{1} followed by human PR2\\text{PR}\_{2} (HH), human PR1\\text{PR}\_{1} followed by agent PR2\\text{PR}\_{2} (HA), and agent PR1\\text{PR}\_{1} followed by agent PR2\\text{PR}\_{2} (AA).
The HH condition consists of the original developer’s PRs provided by each benchmark, acting as the human baseline against which the other conditions are compared. Comparing AA to HA isolates the downstream effect of PR1\\text{PR}\_{1} authorship on PR2\\text{PR}\_{2} success, allowing us to directly evaluate whether agent code imposes a maintainability burden on subsequent agent work in comparison to human code.

We focus on the maintainability costs that agents incur when building on prior code, comparing the outputs from the AA versus HA scenarios, as a growing fraction of developers use AI agents to extend existing codebases ( [Li et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib20 "")). The AH setting of a human performing the follow-on task on top of agent code would offer a complementary human-centric view (by comparing AH versus AA), but would require recruiting a substantial number of developers and is out of scope for this study. By keeping the PR2\\text{PR}\_{2} author fixed, CodeThread is scalable and can be applied to many existing issue-resolution benchmarks without additional data collection from humans.

| Benchmark | \# Instances | Filtered Subset | PR1 (Avg.) | PR2 (Avg.) | Task Types |
| --- | --- | --- | --- | --- | --- |
|  | Total | Filtered. | #Repos | #Lang | Files | Funcs | Files | Funcs |  |
| SWE-Bench Verified | 500 | 441 | 12 | 1 | 1.12 | 1.60 | 1.18 | 1.71 | BF |
| SWE-Bench Multilingual | 300 | 171 | 34 | 7 | 1.29 | 1.90 | 1.84 | 3.28 | BF |
| SWE-Bench Pro | 731 | 641 | 11 | 4 | 2.43 | 5.51 | 5.22 | 10.70 | BF, FI & RF |
| FeatBench | 156 | 124 | 22 | 1 | 1.52 | 2.54 | 2.35 | 4.03 | FI |
| Total | 1,687 | 1,377 | 78 | 10 | 1.79 | 3.54 | 3.25 | 6.30 |  |

Table 1: Benchmarks used in our CodeThread evaluation. We list each benchmark’s full and filtered instance counts, retaining only instances requiring function-level edits. For the filtered subset, we report repository and language coverage (#Repos, #Lang), the mean files and functions modified per PR stage (PR1\\text{PR}\_{1}, PR2\\text{PR}\_{2}), and a breakdown of task types: bug fixes (BF), feature implementation (FI), and refactoring (RF).

### 3.3 Step 3: Evaluate agent vs human code

We assess the final HA and AA outputs, PR2\\text{PR}\_{2}, using resolve rate: the percentage of instances in which the code successfully resolves the original benchmark issue after both editing steps. Differences in resolve rate indicate whether the authorship of PR1\\text{PR}\_{1} affects downstream issue-resolution success, providing a task-based measure of maintainability. The resulting code samples can also be compared along other dimensions of code quality since the task setup is controlled and the downstream issue is held fixed across authorship conditions. We show this in Section [5](https://arxiv.org/html/2606.21804v2#S5 "5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

## 4 CodeThread on SWE Problems

### 4.1 Experimental Set-up

#### Task Types.

We source a total of 1,377 instances from SWE-Bench Verified ( [Chowdhury et al., 2024](https://arxiv.org/html/2606.21804v2#bib.bib5 "")), SWE-Bench Multilingual ( [Khandpur, 2025](https://arxiv.org/html/2606.21804v2#bib.bib6 "")), SWE-Bench Pro ( [Deng et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib7 "")), and FeatBench ( [Chen et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib8 "")).
The four benchmarks were selected to cover a range of software engineering tasks: bug fixing (BF), feature implementation (FI), and refactoring (RF), as shown in Table [1](https://arxiv.org/html/2606.21804v2#S3.T1 "Table 1 ‣ 3.2 Step 2: Set-up Authorship Scenarios ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?").
Following [Xu et al. (2025)](https://arxiv.org/html/2606.21804v2#bib.bib10 ""), we treat SWE-Bench Verified and SWE-Bench Multilingual as bug fix benchmarks. We use the native labels of each SWE-Bench Pro instance, and treat FeatBench as a feature-implementation benchmark.

#### Models and Agent Configuration.

In order to cover a breadth of model types, we evaluate four frontier models: Claude 4.5 Sonnet, GPT-5, GLM 4.7 and MiniMax M2.5, two proprietary frontier models and two publicly available open-weight models. We use SWE-Agent [Yang et al. (2024)](https://arxiv.org/html/2606.21804v2#bib.bib16 "") as the scaffolding framework for all models. We follow the standard evaluation protocol of the underlying benchmarks and run each pair (model, authorship condition) once per instance in order to maintain tractable computational costs while providing coverage across all benchmark categories. We provide further details in Appendix [C](https://arxiv.org/html/2606.21804v2#A3 "Appendix C Agent Execution and Model Details ‣ Is Agent Code Less Maintainable Than Human Code?").

### 4.2 Results

Overall findings. Table [2](https://arxiv.org/html/2606.21804v2#S4.T2 "Table 2 ‣ Per-model patterns. ‣ 4.2 Results ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?") shows the PR2\\text{PR}\_{2} resolve rates under HA and AA conditions. The number of instances that pass the PR1\\text{PR}\_{1} filtering differs by model, so we compare models using the subset of instances shared across all models within each benchmark. Across these instances, we find that agents more often perform worse when building on agent code than on human code: AA generally underperforms HA, with drops in downstream resolve rate of up to 13.1%. Full scores for each model and benchmark are provided in Appendix [B](https://arxiv.org/html/2606.21804v2#A2 "Appendix B Resolve Rate and Maintainability Metric Comparison on the Full Dataset ‣ Is Agent Code Less Maintainable Than Human Code?"); we observe a similar pattern in both the shared-instance analysis and the full per-model benchmark results. The largest drops occur for GLM 4.7 on SWE-Bench Pro, which contains longer, multi-file edits drawn from professional codebases, and with GPT-5 on FeatBench, a set of feature implementation tasks. We trace the source of the gap between HA and AA in Section [5](https://arxiv.org/html/2606.21804v2#S5 "5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

We also observe four cases where AA matches or exceeds HA performance. These should be considered in light of benchmark-specific baseline performance and sample size. GPT-5 shows small positive gaps on SWE-Bench Multilingual (+3.1) and SWE-Bench Pro (+0.8), but these coincide with lower HA baseline performance on the benchmarks, suggesting that the gap may reflect a weaker ceiling rather than greater robustness to agent code. The clearest positive result, Claude 4.5 Sonnet on FeatBench (+6.2), occurs on our smallest overlap set of 16 instances, where a small number of cases can substantially shift the observed gap.

#### Per-model patterns.

Table [2](https://arxiv.org/html/2606.21804v2#S4.T2 "Table 2 ‣ Per-model patterns. ‣ 4.2 Results ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?") shows the HA-vs-AA gap across models. GLM shows the largest and most consistent effect of PR1\\text{PR}\_{1} authorship, with AA underperforming HA on all benchmarks and dropping by 13.1% on SWE-Bench Pro. Claude and MiniMax also drop by around 33-88% across SWE-Bench variants, though FeatBench shows mixed results. GPT-5 has the smallest gaps on SWE-Bench variants, however, we see a 12.5% drop on FeatBench, suggesting that maintainability costs may be more visible on feature implementation tasks.

|  | Resolve Rate % (↑\\uparrow) |
|  | Claude | GPT | GLM | MiniMax |
| Benchmark | HA | AA | Δ\\Delta | HA | AA | Δ\\Delta | HA | AA | Δ\\Delta | HA | AA | Δ\\Delta |
| SWE-Bench Verified | 71.7 | 66.7 | −-5.1 | 62.6 | 61.6 | −-1.0 | 65.7 | 62.6 | −-3.0 | 74.7 | 68.7 | −-6.1 |
| SWE-Bench Multilingual | 53.1 | 50.0 | −-3.1 | 46.9 | 50.0 | ++3.1 | 62.5 | 59.4 | −-3.1 | 65.6 | 62.5 | −-3.1 |
| SWE-Bench Pro | 46.3 | 38.6 | −-7.7 | 39.0 | 39.8 | ++0.8 | 45.2 | 32.0 | −-13.1 | 43.6 | 36.7 | −-6.9 |
| FeatBench | 50.0 | 56.2 | ++6.2 | 56.2 | 43.8 | −-12.5 | 62.5 | 56.2 | −-6.2 | 56.2 | 56.2 | 0.0 |

Table 2: Comparing HA and AA PR2 resolve rate. We observe a consistent lower resolution rate under the AA condition than HA across nearly all model–benchmark pairs. Bolded values indicate the higher resolve rate within
each HA/AA pair.

|  |  | Resolve Rate % (↑\\uparrow) |  |
|  |  | Claude | GPT | GLM | MiniMax |  |
| Task | N | HA | AA | Δ\\Delta | HA | AA | Δ\\Delta | HA | AA | Δ\\Delta | HA | AA | Δ\\Delta | Avg. Δ\\Delta |
| BF | 210 | 59.05 | 51.43 | −-7.62 | 49.52 | 50.00 | ++0.48 | 56.19 | 52.38 | −-3.81 | 61.43 | 56.19 | −-5.24 | −-4.05 |
| FI | 104 | 44.23 | 41.35 | −-2.88 | 41.35 | 38.46 | −-2.88 | 46.15 | 30.77 | −-15.38 | 42.31 | 38.46 | −-3.85 | −-6.25 |
| RF | 70 | 57.14 | 50.00 | −-7.14 | 48.57 | 51.43 | ++2.86 | 55.71 | 40.00 | −-15.71 | 54.29 | 41.43 | −-12.86 | −-8.21 |
| FI + RF | 22 | 27.27 | 22.73 | −-4.55 | 27.27 | 27.27 | 0.00 | 31.82 | 13.64 | −-18.18 | 27.27 | 22.73 | −-4.55 | −-6.82 |

Table 3: Task-type stratified resolved rate results by model on overlapping instances. The dataset is stratified by task type into bug fixes (BF), feature implementation (FI), refactoring (RF), and feature implementation &
refactoring (FI + RF). PR2 resolve rates under HA and AA; Δ\\Delta denotes the percentage-point change from HA to AA within each task type and model. Avg. Δ\\Delta denotes the average % change across models for each task type.

#### Stratifying by task type.

Table [3](https://arxiv.org/html/2606.21804v2#S4.T3 "Table 3 ‣ Per-model patterns. ‣ 4.2 Results ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?") shows that refactoring tasks have the largest average drop across models of 8.21%.
Feature implementation and combined FI+RF tasks also show notable average drops of 6.25 and 6.82%, respectively.
Bug-fix tasks show the smallest average drop, with an average 4.05%.
These observations are consistent with prior work, which show that refactoring and multi-file edits are harder for coding agents than localized fixes [Xu et al. (2025)](https://arxiv.org/html/2606.21804v2#bib.bib10 ""); [Gautam et al. (2025)](https://arxiv.org/html/2606.21804v2#bib.bib9 "").

## 5 Why does AA underperform HA?

We observe that agents building on agent code generally perform worse than on human code. To investigate the drivers of this gap, we focus on discordant instances—i.e., those where HA and AA yield different outcomes on the task.
Across all four models and benchmarks, there are 454 discordant instances. 64.3% of these are HA wins (HA passes while AA fails), while 35.7% are AA wins (AA passes while HA fails). After excluding instances with incomplete features, our analysis includes 405 instances (64.7% HA wins, 35.3% AA wins). We extract features from PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}, detailed in Section [5.1](https://arxiv.org/html/2606.21804v2#S5.SS1 "5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?"), and fit a logistic regression model to identify which features most strongly predict whether HA or AA won in a discordant instance.

### 5.1 Features

We use four feature categories to identify the root causes of the gap: static maintainability metrics to test traditional code-quality signals, patch localization features to compare the files and functions edited, behavioral drift labels to capture differences missed by static metrics, and an instance difficulty score to control for task-level variation. We describe each below and provide implementation details in Appendix [D](https://arxiv.org/html/2606.21804v2#A4 "Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?").

#### Static maintainability metrics on PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}.

Our first feature set comprises four static proxies for maintenance cost based on software engineering literature ( [Riaz et al., 2009](https://arxiv.org/html/2606.21804v2#bib.bib21 ""); [Ardito et al., 2020](https://arxiv.org/html/2606.21804v2#bib.bib22 "")), spanning two dimensions of code quality.
The first dimension is structural complexity, for which we use Cyclomatic Complexity (CC) ( [Ebert et al., 2016](https://arxiv.org/html/2606.21804v2#bib.bib4 "")), which counts linearly independent paths through a function, and Cognitive Complexity (CogC) ( [Campbell, 2018](https://arxiv.org/html/2606.21804v2#bib.bib3 "")), which penalizes nested control structures.
The second dimension is verbosity, for which we use Halstead Volume (HV) ( [Halstead, 1977](https://arxiv.org/html/2606.21804v2#bib.bib19 "")), based on operator and operand counts, and Logical Lines of Code (LLOC), which counts executable statements. For each metric, we compute two features per discordant instance: the AA–HA delta at PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}.

![Refer to caption](https://arxiv.org/html/2606.21804v2/images/disagreement_distributions.png)Figure 3: HA vs AA-only wins are differentiated by behavioral drift, instance difficulty, and downstream code-size change. Panels compare instances resolved only in HA (teal) versus in AA (lavender); whiskers show the 5th/95th percentiles. Most static maintainability metrics have similar distributions, except Δ\\DeltaLLOC at PR2\\text{PR}\_{2}; input error contract and instance resolve rate also separate the two groups.

#### Patch localization features on PR2\\text{PR}\_{2}.

Our second feature set measures files and functions that the agent edits.
Prior work has shown that localization is one of the leading failure modes for coding agents ( [He and Roy, 2026](https://arxiv.org/html/2606.21804v2#bib.bib30 ""); [Liu et al., 2025](https://arxiv.org/html/2606.21804v2#bib.bib33 "")). We focus on PR2\\text{PR}\_{2} because the PR1\\text{PR}\_{1} prompt explicitly lists the files and functions each chain must edit. The PR2\\text{PR}\_{2} problem statement does not, and the agent can freely choose which files and functions to edit.
We measure this with two Jaccard overlaps: one over the set of edited files, and one over the set of edited functions. Higher values indicate that the HA and AA patches modify more similar parts of the codebase.

#### Behavioral drift labels on PR1\\text{PR}\_{1}.

The third feature set captures differences between agent and human PR1\\text{PR}\_{1}s not reflected in aggregate static metrics. We develop a ten-category taxonomy for forms of behavioral drift, detailed in Appendix [D.3](https://arxiv.org/html/2606.21804v2#A4.SS3 "D.3 \"PR\"_1 Behavioral Drift ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?"), and use Deepseek-V4 Pro ( [DeepSeek-AI et al., 2026](https://arxiv.org/html/2606.21804v2#bib.bib37 "")) as an LLM-judge to label instances by category.
We are particularly interested in cases where the agent’s PR1\\text{PR}\_{1} alters input-validation or error-handling behavior, which we define as input/error contract (IEC). From our observations, differences in exception types or swapped defaults can silently creep into the codebase. Agents may add an extra input-gating check that raises ValueError or use getattr with None as the default, while the human PR1\\text{PR}\_{1} would raise an error. In both cases, neither static metrics nor patch location features would distinguish the agent from the human code. Appendix [D.7](https://arxiv.org/html/2606.21804v2#A4.SS7 "D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") shows five such cases contrasting the human and agent implementations of PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}.
As such, we look at whether or not the behavioral drift was labeled as one of three IEC categories—Input Gating, Silent Fallback, and Error Handling—setting the feature to 1 if so, and 0 otherwise. To verify LLM-judge accuracy, we manually check a subset of 50 LLM-judge labels (Appendix [D.5](https://arxiv.org/html/2606.21804v2#A4.SS5 "D.5 Human Audit of the \"PR\"_1 Fidelity Judge ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?")).

#### Instance difficulty control.

We add a difficulty control to ensure that HA is not winning simply because it is evaluated on easier tasks. We use a leave-one-out (LOO) instance difficulty score, defined as the mean resolution rate of the other three models on the same instance.

### 5.2 Modeling

Given these twelve features, together with benchmark and model fixed effects, we fit a logistic regression (LR) to identify which features push the outcome toward HA or AA winning.
We define Yi=1Y\_{i}=1 when HA resolves and AA fails on instance ii and Yi=0Y\_{i}=0 otherwise.
The model is defined as:

|     |     |     |     |
| --- | --- | --- | --- |
|  | logit⁡Pr⁡(Yi=1∣Xi)\\displaystyle\\operatorname{logit}\\,\\Pr(Y\_{i}=1\\mid X\_{i}) | =β0+βIEC​IECi+𝜷J⊤​𝐉i\\displaystyle=\\beta\_{0}\\,+\\,\\beta\_{\\text{IEC}}\\,\\text{IEC}\_{i}+\\,\\boldsymbol{\\beta}\_{J}^{\\!\\top}\\,\\mathbf{J}\_{i} |  |
|  |  | +𝜷1⊤​𝚫iPR1+𝜷2⊤​𝚫iPR2\\displaystyle+\\,\\boldsymbol{\\beta}\_{1}^{\\!\\top}\\,\\boldsymbol{\\Delta}^{\\text{PR}\_{1}}\_{i}\\,+\\,\\boldsymbol{\\beta}\_{2}^{\\!\\top}\\,\\boldsymbol{\\Delta}^{\\text{PR}\_{2}}\_{i} |  |
|  |  | +𝜷D⊤​𝐃i+βLOO​LOOi\\displaystyle+\\,\\boldsymbol{\\beta}\_{D}^{\\!\\top}\\,\\mathbf{D}\_{i}\\,+\\,\\beta\_{\\text{LOO}}\\,\\text{LOO}\_{i} |  |

Static maintainability metrics are denoted with 𝚫iPR1\\boldsymbol{\\Delta}^{\\text{PR}\_{1}}\_{i} and 𝚫iPR2\\boldsymbol{\\Delta}^{\\text{PR}\_{2}}\_{i} for each of four AA−-HA metric deltas (CC, CogC, HV, LLOC) at PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2}. For fault localization, the HA-vs-AA file and function Jaccards on the PR2\\text{PR}\_{2} patches are denoted by 𝐉i=(Jifile,Jifunc)\\mathbf{J}\_{i}=(J^{\\text{file}}\_{i},J^{\\text{func}}\_{i}). PR1\\text{PR}\_{1} behavioral drift is denoted by IECi∈{0,1}\\text{IEC}\_{i}\\in\\{0,1\\}, an input/error-contract indicator on the agent’s PR1\\text{PR}\_{1}. LOOi\\text{LOO}\_{i} denotes the leave-one-out instance difficulty score, and 𝐃i\\mathbf{D}\_{i} is a fixed-effect for benchmark and model. We interpret coefficients as Odds Ratios (ORs), each of which captures how a feature shifts the outcome: a one-unit increase in feature kk multiplies the odds of HA winning by ORk\\text{OR}\_{k}. Coefficients with OR >1>1 therefore tilt the outcome toward HA, and OR <1<1 toward AA. In Figure [3](https://arxiv.org/html/2606.21804v2#S5.F3 "Figure 3 ‣ Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?"), we similarly observe the effects of each feature on the direction of discordance by visualizing the distribution of each feature across HA wins and AA wins.

### 5.3 Findings

|     |     |     |
| --- | --- | --- |
| Feature | OR (95% CI) | 𝒑\\boldsymbol{p} |
| Δ​CCPR1\\Delta\\text{CC}\_{\\text{PR}\_{1}} | 0.920.92 (0.530.53, 1.611.61) | 0.7790.779 |
| Δ​CogCPR1\\Delta\\text{CogC}\_{\\text{PR}\_{1}} | 1.001.00 (0.670.67, 1.481.48) | 0.9810.981 |
| Δ​HVPR1\\Delta\\text{HV}\_{\\text{PR}\_{1}} | 1.031.03 (0.690.69, 1.531.53) | 0.8850.885 |
| Δ​LLOCPR1\\Delta\\text{LLOC}\_{\\text{PR}\_{1}} | 0.920.92 (0.530.53, 1.611.61) | 0.7800.780 |
| Δ​CCPR2\\Delta\\text{CC}\_{\\text{PR}\_{2}} | 0.710.71 (0.380.38, 1.311.31) | 0.2710.271 |
| Δ​CogCPR2\\Delta\\text{CogC}\_{\\text{PR}\_{2}} | 0.970.97 (0.690.69, 1.371.37) | 0.8660.866 |
| Δ​HVPR2\\Delta\\text{HV}\_{\\text{PR}\_{2}} | 0.930.93 (0.690.69, 1.251.25) | 0.6150.615 |
| Δ​LLOCPR2\\Delta\\text{LLOC}\_{\\text{PR}\_{2}} | 1.88\\mathbf{1.88} (1.021.02, 3.463.46) | 0.042\\mathbf{0.042} |
| File Jaccard | 0.770.77 (0.580.58, 1.011.01) | 0.0610.061 |
| Func. Jaccard | 1.221.22 (0.930.93, 1.601.60) | 0.1440.144 |
| IEC | 1.83\\mathbf{1.83} (1.151.15, 2.922.92) | 0.011\\mathbf{0.011} |
| Inst. resolve rate | 1.42\\mathbf{1.42} (1.121.12, 1.781.78) | 0.003\\mathbf{0.003} |

Table 4: Effect of PR1\\text{PR}\_{1} and PR2\\text{PR}\_{2} features on HA-to-AA Odds Ratio (OR). The three significant predictors of whether HA or AA will resolve in the discordant pair are: Δ​LLOCPR2\\Delta\\text{LLOC}\_{\\text{PR}\_{2}}, IEC, and instance difficulty. All three tilt the outcome toward HA: IEC drift in agent PR1\\text{PR}\_{1}, AA over-editing at PR2\\text{PR}\_{2} relative to HA, and easier instances each raise the odds that only HA resolves.

#### Which features predict HA and AA disagreement?

Table [4](https://arxiv.org/html/2606.21804v2#S5.T4 "Table 4 ‣ 5.3 Findings ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?") reports the fitted logistic regression on the discordant instances. Three features emerge as statistically significant predictors of the discordance direction, with all three tilting the outcome toward HA winning: IEC, Δ​LLOCPR2\\Delta\\text{LLOC}\_{\\text{PR}\_{2}}, and Instance resolve rate.
When agent PR1\\text{PR}\_{1} alters input-validation or error-handling behavior, the odds of HA winning are 1.83×1.83\\times that of AA, and when AA’s PR2\\text{PR}\_{2} adds more lines than HA’s, HA is 1.88×1.88\\times more likely to win over AA.
The difficulty control feature signifies that instances where HA wins tend to be easier.
The model recovers a modest but reliable signal (McFadden R2=0.069R^{2}=0.069, LR χ2​(18)=36.1\\chi^{2}(18)=36.1, p=0.007p=0.007) suggesting that these features are informative signals of downstream success, but do not fully explain or predict it.

Figure [3](https://arxiv.org/html/2606.21804v2#S5.F3 "Figure 3 ‣ Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?") corroborates these results as static maintainability metrics show near-identical distributions on HA wins and AA wins, while IEC drift, Δ​LLOCPR2\\Delta\\text{LLOC}\_{\\text{PR}\_{2}}, and instance resolve rate show the clearest visual separation between the two groups. To verify the LLM-judge labels and assess robustness to the choice of judge, we re-ran the PR1\\text{PR}\_{1} behavioral drift judge with Kimi K2.6 ( [Kimi,](https://arxiv.org/html/2606.21804v2#bib.bib38 "")) and re-fit the same model. This yielded the same three significant features with comparable odds ratios (IEC: OR =1.70=1.70, p=0.039p=0.039; see Appendix [D.6](https://arxiv.org/html/2606.21804v2#A4.SS6 "D.6 Robustness to Choice of LLM Judge ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") for further details).

#### Does PR1\\text{PR}\_{1} drift cause the unresolved outcome in PR2\\text{PR}\_{2}?

The IEC coefficient in Table [4](https://arxiv.org/html/2606.21804v2#S5.T4 "Table 4 ‣ 5.3 Findings ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?") establishes the population-level signal, but population-level evidence does not tell us whether the drift was actually the cause of failing to resolve a given instance. We further investigate the cause of failures in the AA scenario, focusing on IEC for per-instance attribution as the only significant predictor in our model that identifies a specific, code-level mechanism. Δ​LLOCPR2\\Delta\\text{LLOC}\_{\\text{PR}\_{2}} is a summary statistic and instance difficulty is a control variable, neither of which corresponds to a verifiable property of the agent’s PR1\\text{PR}\_{1}.

We consider two scenarios that could decouple IEC drift from the downstream failure. First, the agent may rewrite the function containing the PR1\\text{PR}\_{1} input/error-contract divergence in PR2\\text{PR}\_{2}, removing the drift before evaluation. Second, the drift may persist into PR2\\text{PR}\_{2}, but the failing test may be evaluating a different part of the code. We use an LLM-judge (DeepSeek-V4 Pro) to attribute whether the failing test falls under either of these scenarios. The LLM-judge is given the PR1\\text{PR}\_{1} behavioral drift label with the generated rationale, the AA PR2\\text{PR}\_{2} patch, and the AA test outcome. It judges whether the divergence persisted into PR2\\text{PR}\_{2}, and whether the failing test can be traced back to the divergence.

Table [A4](https://arxiv.org/html/2606.21804v2#A4.T4 "Table A4 ‣ D.4 \"PR\"_1 Error Compounding into \"PR\"_2 ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") reports the breakdown. The first scenario is rare: PR2\\text{PR}\_{2} rewrites the divergent function on only 6.9% of instances, while the drift is unchanged in 85.9% of instances. On 20.6% of instances, the drift is judged to both persist and directly relate to the failing test case. The remaining 74.4% fail for reasons we have not isolated, and we leave this analysis to future work. The high persistence rate also suggests that on long-horizon tasks (i.e., chains longer than our two-PR setup), this drift could compound across PRs and degrade downstream resolve rates further. Our setup cannot test this directly, and future work should assess the effects of these drifts over long-horizon tasks. The full prompt and output schema are provided in Appendix [D.4](https://arxiv.org/html/2606.21804v2#A4.SS4 "D.4 \"PR\"_1 Error Compounding into \"PR\"_2 ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?").

## 6 Conclusion

Across four benchmarks and four frontier models, building on agent code more often lowers downstream resolve rates than building on human code, with effects varying by model and task type. These differences are not well explained by static maintainability metrics alone; the clearest code-level signal is subtle behavioral drift in agent code, while larger downstream edits and task difficulty also indicate where the conditions diverge. Thus, building on agent code often introduces maintainability costs, which appear even on two-step chains and are likely to compound over many edits of a software project. As agent contributions become a larger share of working codebases, evaluation must shift from isolated task completion toward long-term maintainability.

## Limitations

We present limitations of our study. First, we consider only two-step pull request chains (PR1→\\rightarrowPR2). Although this setup is sufficient to study whether the quality of an intermediate patch affects a downstream modification, it does not capture longer-horizon development trajectories, where technical debt may compound over multiple successive edits. Future work should explore constructing longer PR chains with function-level overlap across successive tasks.

Second, we filter PR1\\text{PR}\_{1} by instances where the agent PR1\\text{PR}\_{1} did not already address the Follow-On Issue. This filtering is necessary for the two-step chain to be well-defined, maintaining the separation between the two tasks so that the effect of authorship can be evaluated in isolation from functionality. However, it may introduce selection bias, since restricting the analyzed instances to where the agent did not solve the Follow-On Issue at PR1\\text{PR}\_{1} may not represent the agent’s natural behavior across the full benchmark. Nonetheless, the filter retains a large majority of instances, and we verify that cases where the model satisfies Fail-to-Pass tests in the Implementation Task are often incidental.

Third, as discussed in Section [3.2](https://arxiv.org/html/2606.21804v2#S3.SS2 "3.2 Step 2: Set-up Authorship Scenarios ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?"), our work does not study the effect of human-authored PR2\\text{PR}\_{2} on top of agent-authored PR1\\text{PR}\_{1} (AH) setting. Doing so would allow for a comparison of how difficult it is for human developers to build on agent code versus human code, and provide a more human-centric analysis of code maintainability. However, constructing this condition at scale would require recruiting developers to author PR2\\text{PR}\_{2} across all instances, which is infeasible in our current setting and difficult to control due to factors such as familiarity with the codebase. Future work could examine the AH setting on a smaller curated subset.

## Ethical Considerations

This work aims to support more reliable evaluation and deployment of coding agents by studying the maintainability of code produced by these systems. Our findings show that agent code can affect downstream maintenance, underscoring the need for benchmarks, review practices, and safeguards that evaluate coding agents beyond immediate task completion and support informed decisions about when and how to rely on agent code. These findings should not be interpreted as evidence against the use of coding agents broadly, but as a call for evaluations that better reflect the long-term effects on software development.

## Acknowledgments

We thank Carlos Jimenez, Nicholas Lourie, Varun Yerram, Shashwat Singh, Rico Angell, and Yueh-Han Chen for insightful feedback and discussion. This work was supported by NSF IIS-2340345, NSF CAREER Award 2145542, and Coefficient Giving (formerly Open Philanthropy), and in part by the NYU IT High Performance Computing resources, services, and staff expertise.

## References

- \[1\]AnthropicClaude sonnet 4.5.
External Links: [Link](https://www.anthropic.com/news/claude-sonnet-4-5 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p4.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- Ardito et al. (2020)L. Ardito, R. Coppola, L. Barbato, and D. VergaA tool-based perspective on software code maintainability metrics: a systematic literature review.
Scientific Programming2020 (1), pp. 8840389.
External Links: [Document](https://dx.doi.org/https%3A//doi.org/10.1155/2020/8840389 ""),
[Link](https://onlinelibrary.wiley.com/doi/abs/10.1155/2020/8840389 ""),
https://onlinelibrary.wiley.com/doi/pdf/10.1155/2020/8840389Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px1.p1.1 "Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Campbell (2018)G. A. CampbellCognitive complexity: an overview and evaluation.
In 2018 IEEE/ACM International Conference on Technical Debt (TechDebt),
Vol. , pp. 57–58.
External Links: [Document](https://dx.doi.org/ "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px1.p1.1 "Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Chen et al. (2025)H. Chen, C. Li, and J. LiFeatBench: evaluating coding agents on feature implementation for vibe coding.
arXiv preprint arXiv:2509.22237.
Cited by: [§3](https://arxiv.org/html/2606.21804v2#S3.p2.1 "3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§4.1](https://arxiv.org/html/2606.21804v2#S4.SS1.SSS0.Px1.p1.1 "Task Types. ‣ 4.1 Experimental Set-up ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- Chen et al. (2026)J. Chen, X. Xu, H. Wei, C. Chen, and B. ZhaoSWE-ci: evaluating agent capabilities in maintaining codebases via continuous integration.
External Links: 2603.03823,
[Link](https://arxiv.org/abs/2603.03823 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Chowdhury et al. (2024)N. Chowdhury, J. Aung, C. J. Shern, O. Jaffe, D. Sherburn, G. Starace, E. Mays, R. Dias, M. Aljubeh, M. Glaese, C. E. Jimenez, J. Yang, L. Ho, T. Patwardhan, K. Liu, and A. MadrySWE-bench verified.
External Links: [Link](https://openai.com/index/introducing-swe-bench-verified "")Cited by: [§3](https://arxiv.org/html/2606.21804v2#S3.p2.1 "3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§4.1](https://arxiv.org/html/2606.21804v2#S4.SS1.SSS0.Px1.p1.1 "Task Types. ‣ 4.1 Experimental Set-up ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- Cynthia et al. (2026)S. T. Cynthia, A. Muttakin, and B. RoyBeyond bug fixes: an empirical investigation of post-merge code quality issues in agent-generated pull requests.
arXiv preprint arXiv:2601.20109.
Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- DeepSeek-AI et al. (2026)DeepSeek-AI, A. Xu, B. Lin, B. Xue, B. Wang, B. Xu, B. Wu, B. Zhang, C. Lin, C. Dong, C. Ling, C. Lu, C. Zhao, C. Deng, C. Hou, C. Xu, C. Shao, C. Ruan, C. Sun, D. Dai, D. Guo, D. Yang, D. Chen, D. Li, D. Ji, E. Li, F. Wei, F. Lin, F. Yuan, F. Xia, F. Dai, G. Hao, G. Chen, G. Cao, G. Meng, G. Li, H. Yu, H. Zhang, H. Xu, H. Li, H. Liang, H. Zhang, H. Luo, H. Wei, H. Yuan, H. Zhang, H. Luo, H. Chen, H. Ji, H. Zhang, H. Ding, H. Tang, H. Cao, H. Gao, H. Qu, H. Zeng, J. Yang, J. Zhu, J. Luo, J. Song, J. Yu, J. Huang, J. Cai, J. Liang, J. Zhou, J. Ye, J. Li, J. Xu, J. Hu, J. Yang, J. Chen, J. Yan, J. Chen, J. Zhou, J. Xiang, J. Yuan, J. Cheng, J. Zhou, J. Zhu, J. Yu, J. Sun, J. Ran, J. Jiang, J. Qiu, J. Li, J. Zheng, J. Song, K. Dong, K. Gao, K. Guan, K. Zhou, K. Huang, K. Yu, L. Wang, L. Zhang, L. Wang, L. Xia, L. Zhang, L. Zhao, L. Guo, L. Luo, L. Ma, L. Zhu, L. Wang, L. Cai, L. Zhang, L. Chen, M. Di, M. Xu, M. Mei, M. Wang, M. Zhang, M. Zhang, M. Tang, M. Li, M. Zhou, M. Han, N. Wang, P. Huang, P. Wang, P. Cong, P. Wang, P. Zhang, Q. Wang, Q. Zhu, Q. Li, Q. Chen, Q. Du, Q. Jiang, R. Tian, R. Xu, R. Lu, R. Xu, R. Ge, R. Zhang, R. Pan, R. Wang, R. Chen, R. Yin, R. Xu, R. Shen, R. Zhang, R. Chen, S. Liu, S. Lu, S. Sun, S. Zhou, S. Chen, S. Cai, S. Nie, S. Wu, S. Chen, S. Hu, S. Liu, S. Hu, S. Ma, S. Wang, S. Yu, S. Zhou, S. Pan, S. Yu, S. Zhou, T. Ni, T. Yun, T. Jin, T. Pei, T. Ye, T. Lin, T. Ji, T. Cui, T. Yue, T. Yu, T. Wang, W. Zhang, W. Xiao, W. Zeng, W. An, W. Zhao, W. Liu, W. Liang, W. Pang, W. Luo, W. Yao, W. Gao, W. Yang, W. Huang, W. Hou, W. Zhang, W. Ma, X. Gao, X. He, X. Wang, X. Wang, X. Bi, X. Liu, X. Wang, X. Chen, X. Zhang, X. Nie, X. Sun, X. Wang, X. Cheng, X. Liu, X. Xie, X. Liu, X. Liu, X. Yu, X. Li, X. Yang, X. Zhang, X. Chen, X. Wang, X. Su, X. Chen, X. Lin, X. Fu, Y. Yan, Y. Wang, Y. Ma, Y. Luo, Y. Zhang, Y. Xu, Y. Ma, Y. Huang, Y. Li, Y. Li, Y. Xu, Y. Zhao, Y. Sun, Y. Wang, Y. Qian, Y. Shao, Y. Yu, Y. Zhang, Y. Ding, Y. Shi, Y. Wu, Y. Xiong, Y. Ma, Y. He, Y. Tang, Y. Zhou, Y. Luo, Y. Zhong, Y. Piao, Y. Wang, Y. Zhang, Y. Chen, Y. Tan, Y. Wei, Y. Ma, Y. Liu, Y. Yang, Y. Guo, Y. Wu, Y. Wu, Y. Li, Y. Cheng, Y. Ou, Y. Xu, Y. Li, Y. Wang, Y. Yang, Y. Xu, Y. Wu, Y. Meng, Y. Zou, Y. Zha, Y. Xiong, Y. Chen, Y. Lin, Y. Cao, Y. Wang, Y. Zhang, Y. Yan, Y. Lin, Y. Gu, Y. Luo, Y. You, Y. Liu, Y. Zhou, Y. Zhou, Y. Huang, Z. Wu, Z. Wang, Z. Zhao, Z. Ren, Z. Zhang, Z. Sha, Z. Fu, Z. Ju, Z. Xu, Z. Xie, Z. Zhang, Z. Gao, Z. Hao, Z. Gou, Z. Ma, Z. Yan, Z. Shao, Z. Huang, Z. Chen, Z. Wu, Z. Ren, Z. Wu, Z. Li, Z. Zhang, Z. Xu, Z. Wang, Z. Qu, Z. Gu, Z. Zhu, Z. Li, Z. Zhang, Z. Xie, Z. Gao, Z. Wan, Z. Pan, and Z. YaoDeepSeek-v4: towards highly efficient million-token context intelligence.
External Links: 2606.19348,
[Link](https://arxiv.org/abs/2606.19348 "")Cited by: [§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px3.p1.1 "Behavioral drift labels on \"PR\"_1. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Deng et al. (2025)X. Deng, J. Da, E. Pan, Y. Y. He, C. Ide, K. Garg, N. Lauffer, A. Park, N. Pasari, C. Rane, K. Sampath, M. Krishnan, S. Kundurthy, S. Hendryx, Z. Wang, V. Bharadwaj, J. Holm, R. Aluri, C. B. C. Zhang, N. Jacobson, B. Liu, and B. KenstlerSWE-bench pro: can ai agents solve long-horizon software engineering tasks?.
External Links: 2509.16941,
[Link](https://arxiv.org/abs/2509.16941 "")Cited by: [§D.3](https://arxiv.org/html/2606.21804v2#A4.SS3.p1.1 "D.3 \"PR\"_1 Behavioral Drift ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§3](https://arxiv.org/html/2606.21804v2#S3.p2.1 "3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§4.1](https://arxiv.org/html/2606.21804v2#S4.SS1.SSS0.Px1.p1.1 "Task Types. ‣ 4.1 Experimental Set-up ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- Ebert et al. (2016)C. Ebert, J. Cain, G. Antoniol, S. Counsell, and P. LaplanteCyclomatic complexity.
IEEE Software33 (6), pp. 27–29.
External Links: [Document](https://dx.doi.org/10.1109/MS.2016.147 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px1.p1.1 "Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Gautam et al. (2025)D. Gautam, S. Garg, J. Jang, N. Sundaresan, and R. Z. MoghaddamRefactorBench: evaluating stateful reasoning in language agents through code.
External Links: 2503.07832,
[Link](https://arxiv.org/abs/2503.07832 "")Cited by: [§4.2](https://arxiv.org/html/2606.21804v2#S4.SS2.SSS0.Px2.p1.1 "Stratifying by task type. ‣ 4.2 Results ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- Halstead (1977)M. H. HalsteadElements of software science.
External Links: [Link](https://api.semanticscholar.org/CorpusID:61365155 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px1.p1.1 "Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Harding and Kloster (2025)W. Harding and M. KlosterAI Copilot code quality: 2025 look at long-term effects.
Technical ReportGitClear.
External Links: [Link](https://www.gitclear.com/ai_assistant_code_quality_2025_research "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- He and Roy (2026)K. He and K. RoySWE-adept: an llm-based agentic framework for deep codebase analysis and structured issue resolution.
External Links: 2603.01327,
[Link](https://arxiv.org/abs/2603.01327 "")Cited by: [§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px2.p1.1 "Patch localization features on \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Huang et al. (2026)H. Huang, P. Jaisri, S. Shimizu, L. Chen, S. Nakashima, and G. Rodríguez-PérezMore code, less reuse: investigating code quality and reviewer sentiment towards ai-generated pull requests.
External Links: 2601.21276,
[Link](https://arxiv.org/abs/2601.21276 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Jimenez et al. (2024)C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. R. NarasimhanSWE-bench: can language models resolve real-world github issues?.
In The Twelfth International Conference on Learning Representations,
External Links: [Link](https://openreview.net/forum?id=VTF8yNQM66 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p3.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- Joshi et al. (2025)T. Joshi, S. Chowdhury, and F. UysalSWE-bench-cl: continual learning for coding agents.
External Links: 2507.00014,
[Link](https://arxiv.org/abs/2507.00014 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px1.p1.1 "Evaluating Agents on Sequential Tasks. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Khandpur (2025)K. KhandpurSWE-bench multilingual.
External Links: [Link](https://kabirk.com/multilingual "")Cited by: [§3](https://arxiv.org/html/2606.21804v2#S3.p2.1 "3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§4.1](https://arxiv.org/html/2606.21804v2#S4.SS1.SSS0.Px1.p1.1 "Task Types. ‣ 4.1 Experimental Set-up ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- \[19\]KimiKimi k2.6.
External Links: [Link](https://www.kimi.ai/blog/kimi-k2-6 "")Cited by: [§5.3](https://arxiv.org/html/2606.21804v2#S5.SS3.SSS0.Px1.p2.1 "Which features predict HA and AA disagreement? ‣ 5.3 Findings ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Li et al. (2025)H. Li, H. Zhang, and A. E. HassanThe rise of ai teammates in software engineering (se) 3.0: how autonomous coding agents are reshaping software engineering.
External Links: 2507.15003,
[Link](https://arxiv.org/abs/2507.15003 "")Cited by: [§3.2](https://arxiv.org/html/2606.21804v2#S3.SS2.p2.1 "3.2 Step 2: Set-up Authorship Scenarios ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?").

- Liu et al. (2025)S. Liu, F. Liu, L. Li, X. Tan, Y. Zhu, X. Lian, and L. ZhangAn empirical study on failures in automated issue solving.
External Links: 2509.13941,
[Link](https://arxiv.org/abs/2509.13941 "")Cited by: [§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px2.p1.1 "Patch localization features on \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Liu et al. (2026)Y. Liu, R. Widyasari, Y. Zhao, I. C. Irsan, J. Chen, and D. LoDebt behind the ai boom: a large-scale empirical study of ai-generated code in the wild.
External Links: 2603.28592,
[Link](https://arxiv.org/abs/2603.28592 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- \[23\]MiniMaxMiniMax m2.5.
External Links: [Link](https://www.minimax.io/news/minimax-m25 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p4.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- \[24\]OpenAIGPT 5.
External Links: [Link](https://openai.com/index/introducing-gpt-5 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p4.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- OpenAI (2026a)OpenAICodex: AI Coding Agent.
Note: [https://chatgpt.com/codex/](https://chatgpt.com/codex/ "") Accessed: 2026-04-25Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p1.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- OpenAI (2026b)OpenAIWhy swe-bench verified no longer measures frontier coding capabilities.
Note: [https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p1.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- Orlanski et al. (2026)G. Orlanski, D. Roy, A. Yun, C. Shin, A. Gu, A. Ge, D. Adila, F. Sala, and A. AlbarghouthiSlopCodeBench: benchmarking how coding agents degrade over long-horizon iterative tasks.
arXiv preprint arXiv:2603.24755.
Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px1.p1.1 "Evaluating Agents on Sequential Tasks. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Paul et al. (2025)D. G. Paul, H. Zhu, and I. BayleyInvestigating the smells of llm generated code.
External Links: 2510.03029,
[Link](https://arxiv.org/abs/2510.03029 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Queirós (2013)R. QueirósCodeSkelGen-a program skeleton generator.
Cited by: [§3.1](https://arxiv.org/html/2606.21804v2#S3.SS1.p1.1 "3.1 Step 1: Create a Two-Step Task ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?").

- Riaz et al. (2009)M. Riaz, E. Mendes, and E. TemperoA systematic review of software maintainability prediction and metrics.
In Proceedings of the 2009 3rd International Symposium on Empirical Software Engineering and Measurement,
ESEM ’09, USA, pp. 367–377.
External Links: ISBN 9781424448425,
[Link](https://doi.org/10.1109/ESEM.2009.5314233 ""),
[Document](https://dx.doi.org/10.1109/ESEM.2009.5314233 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§5.1](https://arxiv.org/html/2606.21804v2#S5.SS1.SSS0.Px1.p1.1 "Static maintainability metrics on \"PR\"_1 and \"PR\"_2. ‣ 5.1 Features ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?").

- Ryoo et al. (2008)J. Ryoo, F. Fonseca, and D. S. JanzenTeaching object-oriented software engineering through problem-based learning in the context of game design.
In 2008 21st Conference on Software Engineering Education and Training,
pp. 137–144.
Cited by: [§3.1](https://arxiv.org/html/2606.21804v2#S3.SS1.p1.1 "3.1 Step 1: Create a Two-Step Task ‣ 3 CodeThread ‣ Is Agent Code Less Maintainable Than Human Code?").

- Sun et al. (2026)X. Sun, D. Ståhl, K. Sandahl, and C. KesslerQuality assurance of llm-generated code: addressing non-functional quality characteristics.
Journal of Systems and Software, pp. 112885.
Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Wang et al. (2026)S. Wang, Z. Wang, D. Ma, Y. Yu, R. Ling, Z. Li, F. Xiong, and W. ZhangCodeFlowBench: a multi-turn, iterative benchmark for complex code generation.
External Links: 2504.21751,
[Link](https://arxiv.org/abs/2504.21751 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px1.p1.1 "Evaluating Agents on Sequential Tasks. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Wang et al. (2025)Z. Wang, R. Ling, C. Wang, Y. Yu, S. Wang, Z. Li, F. Xiong, and W. ZhangMaintainCoder: maintainable code generation under dynamic requirements.
External Links: 2503.24260,
[Link](https://arxiv.org/abs/2503.24260 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- Xu et al. (2025)J. Xu, K. Deng, W. Li, S. Yu, H. Tang, H. Huang, Z. Lai, Z. Zhan, Y. Wu, C. Zhang, K. Lei, Y. Yao, X. Lei, W. Zhu, Z. Feng, H. Li, J. Xiong, D. Li, Z. Gao, K. Wu, W. Xiang, Z. Zhan, Y. Zhang, W. Gong, Z. Gao, G. Wang, Y. Xue, M. Li, M. Xie, X. Zhang, J. Wang, W. Zhuang, Z. Lin, H. Wang, Z. Zhang, Y. Zhang, H. Zhang, B. Chen, and J. LiuSWE-compass: towards unified evaluation of agentic coding abilities for large language models.
External Links: 2511.05459,
[Link](https://arxiv.org/abs/2511.05459 "")Cited by: [§D.3](https://arxiv.org/html/2606.21804v2#A4.SS3.p1.1 "D.3 \"PR\"_1 Behavioral Drift ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§4.1](https://arxiv.org/html/2606.21804v2#S4.SS1.SSS0.Px1.p1.1 "Task Types. ‣ 4.1 Experimental Set-up ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?"),
[§4.2](https://arxiv.org/html/2606.21804v2#S4.SS2.SSS0.Px2.p1.1 "Stratifying by task type. ‣ 4.2 Results ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- Yang et al. (2024)J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. R. Narasimhan, and O. PressSWE-agent: agent-computer interfaces enable automated software engineering.
In The Thirty-eighth Annual Conference on Neural Information Processing Systems,
External Links: [Link](https://arxiv.org/abs/2405.15793 "")Cited by: [§4.1](https://arxiv.org/html/2606.21804v2#S4.SS1.SSS0.Px2.p1.1 "Models and Agent Configuration. ‣ 4.1 Experimental Set-up ‣ 4 CodeThread on SWE Problems ‣ Is Agent Code Less Maintainable Than Human Code?").

- Yu et al. (2026)K. Yu, Z. Zhou, J. Zeng, Y. Wang, X. Du, Z. Yuan, J. Liu, Z. Zhou, Y. Wang, C. Wang, and X. PengDoes pass rate tell the whole story? evaluating design constraint compliance in llm-based issue resolution.
External Links: 2604.05955,
[Link](https://arxiv.org/abs/2604.05955 "")Cited by: [§2](https://arxiv.org/html/2606.21804v2#S2.SS0.SSS0.Px2.p1.1 "Maintainability of LLM-Generated Code. ‣ 2 Related Work ‣ Is Agent Code Less Maintainable Than Human Code?").

- \[38\]Z.aiGLM 4.7.
External Links: [Link](https://z.ai/blog/glm-4.7 "")Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p4.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- Zeng et al. (2025)A. Zeng, X. Lv, Q. Zheng, Z. Hou, B. Chen, C. Xie, C. Wang, D. Yin, H. Zeng, J. Zhang, et al.Glm-4.5: agentic, reasoning, and coding (arc) foundation models.
arXiv preprint arXiv:2508.06471.
Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p4.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").

- Zhang et al. (2013)F. Zhang, A. Mockus, Y. Zou, F. Khomh, and A. E. HassanHow does context affect the distribution of software maintainability metrics?.
In 2013 IEEE International Conference on Software Maintenance,
pp. 350–359.
Cited by: [§1](https://arxiv.org/html/2606.21804v2#S1.p2.1 "1 Introduction ‣ Is Agent Code Less Maintainable Than Human Code?").


## Appendix A Synthetic Problem Statement Construction for PR1\\text{PR}\_{1}

Figure [A1](https://arxiv.org/html/2606.21804v2#A1.F1 "Figure A1 ‣ Appendix A Synthetic Problem Statement Construction for \"PR\"_1 ‣ Is Agent Code Less Maintainable Than Human Code?") shows the prompt used to generate synthetic PR1\\text{PR}\_{1} problem statements. Figure [A2](https://arxiv.org/html/2606.21804v2#A1.F2 "Figure A2 ‣ Appendix A Synthetic Problem Statement Construction for \"PR\"_1 ‣ Is Agent Code Less Maintainable Than Human Code?") shows the prompt template used for solving PR1\\text{PR}\_{1}.

![Refer to caption](https://arxiv.org/html/2606.21804v2/images/synthetic_PR1.png)Figure A1: Prompt used to generate synthetic PR1\\text{PR}\_{1} problem statements. Given the full file context, target function code, and function name, the model is instructed to produce a standalone docstring that enables implementation without revealing the original function body. The prompt specifies the required sections: summary, arguments, returns, exceptions, implementation notes, and edge cases. ![Refer to caption](https://arxiv.org/html/2606.21804v2/images/maintain_PR_1_example_ps.png)Figure A2: Prompt template used for solving PR1\\text{PR}\_{1}. The prompt is formatted in markdown and includes multiple components: a task overview, function summary, arguments, returns, raised exceptions, edge cases, and step-by-step implementation guidance.

## Appendix B Resolve Rate and Maintainability Metric Comparison on the Full Dataset

Table [A1](https://arxiv.org/html/2606.21804v2#A2.T1 "Table A1 ‣ Appendix B Resolve Rate and Maintainability Metric Comparison on the Full Dataset ‣ Is Agent Code Less Maintainable Than Human Code?") shows the comparison of PR2 resolution rates under HA and AA conditions.

| Benchmark | Model | #Instances | 𝐏𝐑𝟐H​A\\mathbf{PR\_{2}}^{HA}Resolve | 𝐏𝐑𝟐A​A\\mathbf{PR\_{2}}^{AA}Resolve | Δ\\Delta |
| --- | --- | --- | --- | --- | --- |
| SWE-Bench Verified | Claude | 215 | 152 (70.7%) | 149 (69.3%) | -1.4 |
|  | GPT | 186 | 114 (61.3%) | 108 (58.1%) | -3.2 |
|  | GLM | 207 | 137 (66.2%) | 131 (63.3%) | -2.9 |
|  | MiniMax | 233 | 173 (74.25%) | 162 (69.53%) | -4.72 |
| SWE-Bench Multilingual | Claude | 38 | 21 (55.3%) | 21 (55.3%) | 0.0 |
|  | GPT | 36 | 17 (47.2%) | 18 (50.0%) | 2.8 |
|  | GLM | 58 | 40 (69.0%) | 32 (55.2%) | -13.8 |
|  | MiniMax | 86 | 54 (65.9%) | 52 (63.4%) | -2.5 |
| SWE-Bench Pro | Claude | 313 | 141 (45.1%) | 116 (37.1%) | -8.0 |
|  | GPT | 280 | 109 (38.9%) | 111 (39.6%) | 1.0 |
|  | GLM | 397 | 179 (45.1%) | 135 (34.0%) | -11.1 |
|  | MiniMax | 395 | 171 (42.3%) | 150 (38.0%) | -4.3 |
| FeatBench | Claude | 17 | 8 (47.1%) | 9 (52.9%) | 5.8 |
|  | GPT | 17 | 9 (52.9%) | 7 (41.2%) | -11.7 |
|  | GLM | 42 | 18 (42.9%) | 14 (33.3%) | -9.5 |
|  | MiniMax | 40 | 19 (47.5%) | 16 (40.0%) | -7.5 |

Table A1: PR2 resolution rates under HA and AA conditions. Across most model-benchmark pairs, building on agent code drops the resolve rate relative to building on human code. To save cost, the Claude and GPT-5 runs on SWE-bench Pro, Multilingual, and FeatBench are restricted to instances where the PR1 gate passed for both MiniMax and GLM-4.7.

## Appendix C Agent Execution and Model Details

### C.1 Agent Execution

All experiments use SWE-Agent under a single shared configuration: a step\_limit of 250 steps, a cost\_limit of $3 USD per instance, and high reasoning effort across all models. For each agent-authored patch, we run the harness once to produce a patch. We adopt each benchmark’s official evaluation harness, and for FeatBench we follow the harbor framework’s open pull request ( [#1218](https://github.com/harbor-framework/harbor/pull/1218 "")).

### C.2 Model link list

Table [A2](https://arxiv.org/html/2606.21804v2#A3.T2 "Table A2 ‣ C.2 Model link list ‣ Appendix C Agent Execution and Model Details ‣ Is Agent Code Less Maintainable Than Human Code?") presents the closed- and open-source models included in our benchmark.

|     |     |     |
| --- | --- | --- |
| Model | Provider | Reference |
| Closed-source models |
| Claude 4.5 Sonnet | Anthropic | [https://www.anthropic.com/claude](https://www.anthropic.com/claude "") |
| GPT-5 | OpenAI | [https://openai.com/index/introducing-gpt-5/](https://openai.com/index/introducing-gpt-5/ "") |
| Open-source models |
| GLM 4.7 FP8 | Z.ai | [https://huggingface.co/zai-org/GLM-4.7-FP8](https://huggingface.co/zai-org/GLM-4.7-FP8 "") |
| MiniMax M2.5 | MiniMax | [https://huggingface.co/MiniMaxAI/MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5 "") |

Table A2: Models evaluated in this work, grouped by access type. Closed-source models are accessed via provider APIs; open-source models are run via self-hosted vLLM.

## Appendix D LR Feature Details and LLM-Judge Details

### D.1 Maintainability Metric Computation

We compute four maintainability metrics—cyclomatic complexity (CC), cognitive
complexity (CogC), Halstead volume (HV), and logical lines of code (LLOC)—across
all supported languages in our corpus. No single tool covers every metric across
every language, so we combine multiple open-source libraries and one custom tool,
selected to maximize per-language consistency. Table [A3](https://arxiv.org/html/2606.21804v2#A4.T3 "Table A3 ‣ D.1 Maintainability Metric Computation ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?")
lists each library’s metric coverage. To fill a gap in Go tooling, we extend Maintidx, an existing Go library, into a custom go-halstead package that computes Halstead volume.

| Library | Languages | CC | CogC | HV | LLOC |
| --- | --- | --- | --- | --- | --- |
| [radon](https://pypi.org/project/radon/ "") | Python | ✓ | — | ✓ | ✓ |
| [complexipy](https://pypi.org/project/complexipy/0.3.1/ "") | Python | — | ✓ | — | — |
| [rust-code-analysis-cli](https://github.com/mozilla/rust-code-analysis "") | Rust, C, Java, JS, TS | ✓ | ✓ | ✓ | ✓ |
| go-halstead (custom) | Go | — | — | ✓ | ✓ |
| [gocognit](https://github.com/uudashr/gocognit "") | Go | — | ✓ | — | — |
| [lizard](https://pypi.org/project/lizard/ "") | Go, Ruby | ✓ | — | — | ✓ |

Table A3: Metric coverage of the libraries used to compute maintainability
metrics. ✓indicates supported, — indicates unsupported.

### D.2 Patch Localization Features

The patch localization features measure where each chain’s PR2\\text{PR}\_{2} patch edits. For each instance and each condition (HA, AA), we extract the set of files and the set of (file, function) pairs touched by the PR2\\text{PR}\_{2} patch. We parse each post-patch source file with an AST parser (Python’s built-in ast module111 [https://docs.python.org/3/library/ast.html](https://docs.python.org/3/library/ast.html "") for Python and lizard222 [https://github.com/terryyin/lizard](https://github.com/terryyin/lizard "") for all other supported languages) and compare against the pre-patch state to identify which files and functions the agent added, edited, or removed. We then compute the Jaccard overlap between the HA and AA edit sets on the same instance. Given two sets AA and BB, the Jaccard overlap is:

|     |     |     |
| --- | --- | --- |
|  | J⁡(A,B)=\|A∩B\|\|A∪B\|.J(A,B)=\\frac{\|A\\cap B\|}{\|A\\cup B\|}. |  |

For each discordant instance we compute two Jaccards: JifileJ^{\\text{file}}\_{i} over the file sets and JifuncJ^{\\text{func}}\_{i} over the (file, function) sets, comparing HA’s PR2\\text{PR}\_{2} patch with AA’s PR2\\text{PR}\_{2} patch on the same instance. A Jaccard of 1.0 means the two chains edited exactly the same set; a Jaccard of 0 means the two sets are disjoint.

### D.3 PR1\\text{PR}\_{1} Behavioral Drift

Prior work on agent failure analysis typically looks at the trajectory and the final agent-produced patch to classify failures into various categories [Xu et al. (2025)](https://arxiv.org/html/2606.21804v2#bib.bib10 ""); [Deng et al. (2025)](https://arxiv.org/html/2606.21804v2#bib.bib7 ""). Given our two-stage setup, we adapt this taxonomy to capture how Agent PR1\\text{PR}\_{1} diverges from Human PR1\\text{PR}\_{1}. These divergences can silently propagate and cause failure during PR2\\text{PR}\_{2}, as observed in Section [5](https://arxiv.org/html/2606.21804v2#S5 "5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?"). We develop a ten-category taxonomy that captures changes to the function’s input contract, changes to its observable outputs and side effects, and edits that go beyond the stubbed target functions. Any of these can leave the downstream PR2\\text{PR}\_{2} task unresolved. Figure [A3](https://arxiv.org/html/2606.21804v2#A4.F3 "Figure A3 ‣ D.4 \"PR\"_1 Error Compounding into \"PR\"_2 ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") shows the full system prompt. The prompt contains the definition of each category. We also reproduce the full definitions in Table [A5](https://arxiv.org/html/2606.21804v2#A4.T5 "Table A5 ‣ D.4 \"PR\"_1 Error Compounding into \"PR\"_2 ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?"). Figure [A4](https://arxiv.org/html/2606.21804v2#A4.F4 "Figure A4 ‣ D.4 \"PR\"_1 Error Compounding into \"PR\"_2 ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") shows the user prompt and the output schema. We use DeepSeek V4 Pro as our LLM judge. We run it on 2,517 records, one for every instance in our four-model by four-benchmark grid.

### D.4 PR1\\text{PR}\_{1} Error Compounding into PR2\\text{PR}\_{2}

The PR1\\text{PR}\_{1} behavioral drift judge in Appendix [D.3](https://arxiv.org/html/2606.21804v2#A4.SS3 "D.3 \"PR\"_1 Behavioral Drift ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") identifies instances where Agent PR1\\text{PR}\_{1} diverges from Human PR1\\text{PR}\_{1}. A PR1\\text{PR}\_{1} divergence does not automatically mean the chain fails. Two scenarios can decouple it from the dwonstream failure. First, the agent’s PR2\\text{PR}\_{2} may rewrite the divergent function, replacing the drift with a different code block. Second, even when the drift survives, the benchmark’s unit tests may not exercise it. The question is therefore: did a PR1\\text{PR}\_{1} divergence persist into PR2\\text{PR}\_{2}’s final state, and did it directly relate to the failing test case? We use DeepSeek-V4 Pro to judge AA instances. Figure [A5](https://arxiv.org/html/2606.21804v2#A4.F5 "Figure A5 ‣ D.4 \"PR\"_1 Error Compounding into \"PR\"_2 ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") and Figure [A8](https://arxiv.org/html/2606.21804v2#A4.F8 "Figure A8 ‣ D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") show the full system and user prompt with the output schema. We exclude instances labeled EQUIVALENT or STYLE by the PR1\\text{PR}\_{1} behavioral drift judge because they have no divergence to compound, which leaves 2,153 instances.

| Outcome | n | % |
| --- | --- | --- |
| Drift survived | 225 | 85.9 |
| Partially corrected | 19 | 7.3 |
| Rewrote / corrected | 18 | 6.9 |

Did the PR1\\text{PR}\_{1} drift survive PR2\\text{PR}\_{2}?PR2\\text{PR}\_{2} leaves the agent’s PR1\\text{PR}\_{1} drift unchanged on 85.9% of the 262 discordant instances, suggesting that the drift almost always persists into PR2\\text{PR}\_{2}.

| Outcome | n | % |
| --- | --- | --- |
| Yes (compounding-confirmed) | 54 | 20.6 |
| No (unrelated failure) | 195 | 74.4 |
| Unclear | 12 | 4.6 |
| Not applicable (passed) | 1 | 0.4 |

Did the failure trace back to the drift? The surviving PR1 drift directly causes the failing test on 20.6% of the 262 discordant instances. The remaining instances fail for undetermined reasons.

Table A4: LLM-judge attribution on the HA-wins discordant cohort (n=262 instances with a divergent agent PR1; 30 PR1-equivalent/style cases excluded). Drift survives PR2 in 86%86\\% of cases; on 20.6%20.6\\% of the
cohort the surviving drift directly traces to the failing test.

| Category | Definition |
| Group A: functionally compatible |
| EQUIVALENT | Same logic, control flow, and observable contract. Only cosmetic differences such as whitespace, comments, docstrings, or local-variable renames. |
| STYLE | Same observable contract and the same operations in the same order, expressed in a different surface syntactic form (e.g., list comprehension vs. loop, ternary vs. if/else, early return vs. nested). |
| ALGORITHM | Same observable contract, but the operations themselves differ in identity, count, or resource regime (e.g., iterative vs. recursive, added memoization, different short-circuit ordering). |
| Group B: behavioral divergence |
| INPUT GATING | Agent added or removed an explicit input check that prevents the main body from executing on some inputs. The function exits early via a raise, an early return, or an assert. |
| SILENT FALLBACK | Agent silently substituted or coerced an input so that the main body still runs but on different data (e.g., dict.get(k, default), int(x), x or default). |
| ERROR HANDLING | Agent raises, catches, or wraps exceptions differently on a structurally equivalent code path (e.g., different exception type at the same raise site, propagating vs. catching). |
| RETURN SHAPE | Return value’s type, structure, or layout differs (e.g., None vs. \[\], scalar vs. tuple, different dict keys or layout). |
| EXTERNAL EFFECTS | Observable mutations or I/O differ (e.g., stdout or log calls added or removed, mutation of arguments, writes to instance or module state). |
| Group C: scope |
| EXTRA EDITS | Target functions are behaviorally compatible, but the agent also modified non-target files or functions that were not mechanically required. Imports and helpers called from the target body do not count. |
| Group D: agent failure |
| INCOMPLETE | Agent left at least one target stub in a non-functional or placeholder state (e.g., empty body, raise NotImplementedError, return paired with a TODO comment). |

Table A5: The ten PR1\\text{PR}\_{1} behavioral drift categories. The judge picks exactly one primary category per instance.![[Uncaptioned image]](https://arxiv.org/html/2606.21804v2/images/LLM_as_a_judge_PR1_fidelity_1.png)![Refer to caption](https://arxiv.org/html/2606.21804v2/images/LLM_as_a_judge_PR1_fidelity_2.png)Figure A3: System prompt for the PR1\\text{PR}\_{1} behavioral drift judge. Defines the ten-category taxonomy.![Refer to caption](https://arxiv.org/html/2606.21804v2/images/LLM_as_a_judge_PR1_fidelity_user_prompt.png)Figure A4: User prompt for the PR1\\text{PR}\_{1} behavioral drift judge. Defines the output schema.![Refer to caption](https://arxiv.org/html/2606.21804v2/images/LLM_as_a_judge_PR2_system.png)Figure A5: System prompt for the PR1\\text{PR}\_{1}/PR2\\text{PR}\_{2} compounding judge.![Refer to caption](https://arxiv.org/html/2606.21804v2/images/LLM_as_a_judge_PR2_user_prompt.png)Figure A6: User prompt for the PR1\\text{PR}\_{1}/PR2\\text{PR}\_{2} compounding judge Defines the output schema.

### D.5 Human Audit of the PR1\\text{PR}\_{1} Fidelity Judge

We verify a stratified sample of the DeepSeek-V4 Pro judge’s outputs against the underlying code to assess the reliability of its IEC labels. We sampled 50 instances, with 56% labeled IEC and the remainder assigned non-IEC labels. Instances used as examples or illustrations elsewhere in the paper were excluded from the sample. Rare labels were over-sampled so that every label is represented. The sample spans all four models and all four benchmarks used in our evaluation. Samples range from 28 to 376 combined patch lines (median 109).

For each instance, the auditor was shown the judge’s label and reasoning together with the human and agent PR1\\text{PR}\_{1} implementations of the same stubbed target functions. The auditor then determined whether the assigned label was correct using the same criteria specified in the judge prompt. We audit the judge’s labels rather than obtain independent blind annotations given the difficulty of the task—assigning a label from scratch often requires repository-specific knowledge beyond the patch itself, such as whether an attribute may take a false value, and the sample of 50 instances covers 29 distinct repositories.
As such, this procedure is a verification audit rather than an independent re-annotation, and we report confirmation rates.

The IEC/non-IEC classification underlying our analysis was confirmed in 48 of 50 instances (96.0%). Seven of these moved an item between two labels on the same side of the boundary, leaving its IEC classification unchanged. The remaining two were reclassified from IEC to non-IEC, and no item was reclassified from non-IEC to IEC.

### D.6 Robustness to Choice of LLM Judge

IEC is the only feature in our model that comes from an LLM judge. To check that the result does not depend on a judge model, we re-ran the PR1\\text{PR}\_{1} behavioral drift judge with Kimi K2.6 on the 405405 discordant instances used to fit the model in Section [5](https://arxiv.org/html/2606.21804v2#S5 "5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?"). We rebuilt the IEC indicator from its labels and re-fit the same LR model by keeping everything constant. Table [A6](https://arxiv.org/html/2606.21804v2#A4.T6 "Table A6 ‣ D.6 Robustness to Choice of LLM Judge ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") compares the significant coefficients against Table [4](https://arxiv.org/html/2606.21804v2#S5.T4 "Table 4 ‣ 5.3 Findings ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?"); all three keep their sign, their significance, and their approximate magnitude.

|  | DeepSeek V4 Pro | Kimi K2.6 |
| --- | --- | --- |
| Feature | OR | 𝒑\\boldsymbol{p} | OR | 𝒑\\boldsymbol{p} |
| --- | --- | --- | --- | --- |
| Δ​LLOCPR2\\Delta\\text{LLOC}\_{\\text{PR}\_{2}} | 1.881.88 | 0.0420.042 | 1.831.83 | 0.0420.042 |
| IEC | 1.831.83 | 0.0110.011 | 1.701.70 | 0.0390.039 |
| Inst. resolve rate | 1.421.42 | 0.0030.003 | 1.421.42 | 0.0030.003 |

Table A6: Swapping the LLM judge does not change our findings. We re-fit the model in Table [4](https://arxiv.org/html/2606.21804v2#S5.T4 "Table 4 ‣ 5.3 Findings ‣ 5 Why does AA underperform HA? ‣ Is Agent Code Less Maintainable Than Human Code?") using IEC labels from a second judge, Kimi K2.6. The same three features stay significant, with similar odds ratios.

### D.7 Examples of IEC Divergence

Each figure below shows an instance with the human and agent implementations of the same function after PR1 on the left, and what each becomes after the same follow-on issue is addressed on the right. Shaded lines mark the code identified as divergent. The five span all three divergence types and four languages: Figures [A7](https://arxiv.org/html/2606.21804v2#A4.F7 "Figure A7 ‣ D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") and [A10](https://arxiv.org/html/2606.21804v2#A4.F10 "Figure A10 ‣ D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") in C and Go, Figures [A8](https://arxiv.org/html/2606.21804v2#A4.F8 "Figure A8 ‣ D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") and [A9](https://arxiv.org/html/2606.21804v2#A4.F9 "Figure A9 ‣ D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") in Python, and Figure [A11](https://arxiv.org/html/2606.21804v2#A4.F11 "Figure A11 ‣ D.7 Examples of IEC Divergence ‣ Appendix D LR Feature Details and LLM-Judge Details ‣ Is Agent Code Less Maintainable Than Human Code?") in TypeScript.

![Refer to caption](https://arxiv.org/html/2606.21804v2/images/iec_examples/S1_valkey_928.png)Figure A7: Example of a silent fallback. In human PR1\\text{PR}\_{1}, clusterManagerMoveSlot returns zero on failure (line 4), propagating the failure to its caller. In agent PR1\\text{PR}\_{1} (lines 2–13), a failed call is handled differently: the code checks whether the error message contains certain keywords and, if so, prints the error and continues execution instead of returning zero. This behavior persists into agent PR2\\text{PR}\_{2} and causes the follow-up test to failure.![Refer to caption](https://arxiv.org/html/2606.21804v2/images/iec_examples/S2_django_14311.png)Figure A8: Example of added input gating. In Agent PR1\\text{PR}\_{1}, the condition on line 5 introduces an additional input check. This condition is carried over into Agent PR2\\text{PR}\_{2}, where it causes the follow-up test to fail.
![Refer to caption](https://arxiv.org/html/2606.21804v2/images/iec_examples/S3_sympy_12481.png)Figure A9: Example of removed input gating. The human authored PR1\\text{PR}\_{1} rejects a call made with two list arguments. The agent’s PR1\\text{PR}\_{1} accepts them and builds a result instead (highlighted). PR2\\text{PR}\_{2} edits another function, leaving this behaviour exactly as PR2\\text{PR}\_{2} left it, so the test that expects the call to be rejected fails.![Refer to caption](https://arxiv.org/html/2606.21804v2/images/iec_examples/S4_teleport_6a14edcf.png)Figure A10: Example of changed error handling. When err is nil, human PR1\\text{PR}\_{1} records and stores the latest heartbeat. In agent PR1\\text{PR}\_{1}, the heartbeat is not stored; instead, the function returns to its caller. This behavior is preserved in Agent PR2\\text{PR}\_{2}, which returns an empty heartbeat date and causes the follow-up test to fail.![Refer to caption](https://arxiv.org/html/2606.21804v2/images/iec_examples/S5_element_web_9a31cd0.png)Figure A11: Example of added input gating. Human PR1\\text{PR}\_{1} does not include a disabled property, while Agent PR1\\text{PR}\_{1} adds one. This changes the frontend behavior: clicking the option no longer opens the dialog box. The same behavior persists in Agent PR2\\text{PR}\_{2} and is also applied to a newly added option. As a result, all nine follow-up tests fail because the expected dialog never appears.
