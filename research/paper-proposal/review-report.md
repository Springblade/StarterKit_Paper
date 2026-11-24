# Review and corrections, 10 November 2026

Scope: all 12 pages of the submitted PDF, eight main sections, abstract, bibliography, and five original figures. The revision adds two data figures. Applied pre-submission-reviewer, scientific-visualization, and the previously loaded figure-designer/humanizer guidance. This is a technical proposal for supervisor discussion, with no specified submission venue.

## Summary

Original review: 0 critical, 4 major, 5 minor findings. All presentation findings below have been addressed. Baseline/task qualification and artifact-level novelty assessment remain scientific work, explicitly disclosed in the proposal. Ready for supervisor discussion; not a completed empirical paper ready for submission.

The previous compilation check was insufficient: a clean LaTeX log did not establish visual quality. This review inspected rendered pages and figure details as well as the log.

| Dimension | Evidence in submitted PDF | Severity | Correction |
|---|---|---|---|
| Data/figures | Figure 5: “The matrix defines outcome categories and contains no measured frequencies.” All five figures were conceptual. | Major | Added quantitative candidate counts from the actual audit CSV and a separate planned collection schema. Captions distinguish planning data from experimental outcomes. |
| Layout | Original p. 5 contained Figures 2 and 3 with a large blank region and no explanatory prose. | Major | Adjusted float thresholds and float-page glue, enabled ragged page bottoms. The figures now share their page with method text. |
| Pagination | RQ1 ended p. 3; RQ2 began p. 4. A later conclusion line also spilled to the references page as content shifted. | Major | Kept RQs together, set widow/orphan penalties, removed meeting narration, and gave references a deliberate page boundary. |
| Positioning | “CodeThread compares subsequent agent performance” omitted two directly relevant recent works. | Major | Retrieved primary records and added FeatureArc (2610.37434v1) and the controlled verification-surface study (2608.28795v2), with explicit scope differences. Artifact-level novelty remains unresolved. |
| Figure references | “This is a hypothetical example” and “We will construct a layer-based variant” did not reference the corresponding figures. | Minor | Added explicit in-text references before Figures 1 and 2. |
| Equations | Five numbered equations had no labels or equation references. | Minor | Added labels/prose references; combined the two simple effects into one equation. All four equations are referenced. |
| Table readability | “Filter order history by status” and “Cancel several pending orders” wrapped awkwardly in narrow, tightly packed rows. | Minor | Shortened labels to “Order status filter” and “Batch cancellation”; increased row spacing. Requirements unchanged. |
| Citation format | Breakable citation spaces; long full-author entries; bibliography ended with two items on a sparse page. | Minor | Added nonbreaking citation spaces, standard abbreviated-name bibliography style, consistent bibliography spacing/type, and a clear section boundary. Two reference pages remain appropriate. |
| Writing | “For supervisor discussion, the immediate scientific decisions concern...” narrated the meeting in the paper. | Minor | Removed from manuscript; decisions remain in project notes. |

## Data figures

Figure 4 summarizes `../smartkit-task-audit-v0.csv`: 5 billing candidates and 1 user-administration candidate. All six are author-constructed and unvalidated. Domain classification follows the recorded source surfaces. Source JSON and the reusable Matplotlib script accompany the vector PDF/SVG. These are planning-inventory counts, not agent performance or the main sample allocation.

Figure 7 specifies planned task, attempt, observation, artifact, and analysis records. It is a schema, not a populated dataset. Short labels and arrow spacing were checked after rendering and revised where crowded.

The outcomes section now specifies future figures: success estimates with uncertainty, paired task differences, outcome frequencies, and cost distributions including failures. They cannot be populated before fresh trial data exist. Unavailable thesis pilot artifacts are not reconstructed as new evidence.

## Logic and language

The intervention definitions and equations remain consistent. Layout changes locality and paths; verification supplies examples and feedback. Mechanisms are not claimed to be isolated beyond those interventions. No positive outcome or universal architectural superiority is asserted.

No material article, subject–verb, restrictive-clause, or comma-splice error was identified under grammar rules G1–G5. Planned methods appropriately retain future tense. The full manuscript vocabulary/dash scan found no em-dash connectors or repeated inflated-language pattern. The sole watchlist match, “yet” in “not yet fixed,” states an unresolved choice and was retained. Bibliographic titles are not edited as prose.

## Validation and readiness

- Rebuilt using pdfLaTeX, BibTeX, and repeated pdfLaTeX passes.
- 21 reference keys, all cited; none missing or unused.
- Seven captioned vector figures and one captioned table, with prose references.
- Four labeled equations, each referenced.
- No final unresolved-reference or box-overflow warnings.
- All pages rendered for overview review; data and diagram pages also inspected at readable resolution. A clean log alone is not treated as a visual audit.
- No venue/page-limit compliance is certified because none was specified.

Editorial readiness: 7/10 for supervisor discussion (qualitative reviewer judgement). Before an empirical submission, qualify the baseline/evaluators, settle novelty or replication scope, freeze the protocol, and collect the main trial data.
