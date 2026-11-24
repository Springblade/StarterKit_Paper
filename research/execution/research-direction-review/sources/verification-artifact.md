Source: https://doi.org/10.5281/zenodo.21961590

[Skip to main](https://zenodo.org/records/23197787#main)

Published October 6, 2026
\| Version 1.3.2

[Dataset](https://zenodo.org/search?q=&f=resource_type%3Adataset)
Open


# Verification-Surface Dataset: 1,116 Controlled Web-Application Builds by Six LLMs under Eight Tool Configurations

### Authors/Creators

- [Mehta, Achint](https://zenodo.org/search?q=metadata.creators.person_or_org.name:%22Mehta,+Achint%22) [![ORCID icon](https://zenodo.org/static/images/orcid.svg)](https://orcid.org/0009-0004-4192-8750 "Mehta, Achint's ORCID profile")

## Description

Companion dataset to the article "The reach of a verification tool decides its value: A controlled study of verification surface, artifact quality, and cost in AI coding agents" (A. Mehta, under review, 2026).

1,116 web applications built by six frontier language models (claude-4.6-sonnet, claude-4.6-opus, claude-4.8-opus, gpt-5.5, gemini-3.1-pro, grok-4.3) under eight verification-tool configurations, from no checking tools to full shell plus screenshots, with byte-identical prompts proven by cryptographic fingerprints in every run manifest.

Contents: every artifact as shipped, complete per-run tool-call logs, machine grades from adversarial behavioral probes, condition-blind human rubric scores for all 1,116 runs, hand-audited launch-failure classifications, three SHA256-sealed dataset snapshots (freeze-20260720 is the dataset of record), the pre-specified statistical analysis plan with its committed code and complete output, and the grading instrument needed to re-grade every artifact. See README.md for reproduction recipes; the analysis table and all statistics regenerate from the published inputs.

The complete per-run request-response traces (1,116 `trace.jsonl` files, one per run) are published in this record as the supplementary archive `traces-batch-20260613.tar.gz` (sha256 `2c47fa647a7e55218a0ffd42dda04e0bc13a216fd1561235dfab3ad1f6f5c4df`). Unpacking it from the root of a repository clone restores the per-run paths that `verify_paper_claims.py --with-traces` verifies.

Code is MIT-licensed; data and documentation are CC BY 4.0 (see LICENSE).

## Files

### Files (3.3 GB)

| Name | Size |  |
| --- | --- | --- |
| [traces-batch-20260613.tar.gz](https://zenodo.org/records/23197787/files/traces-batch-20260613.tar.gz?download=1)<br>md5:5b537395132adc636e2f2cd8fe5f7f19 | 3.2 GB | [Download](https://zenodo.org/records/23197787/files/traces-batch-20260613.tar.gz?download=1) |
| [verification-surface-dataset-1.3.2.tar.gz](https://zenodo.org/records/23197787/files/verification-surface-dataset-1.3.2.tar.gz?download=1)<br>md5:21a1160d3443e24c253a7173f80a112b | 100.9 MB | [Download](https://zenodo.org/records/23197787/files/verification-surface-dataset-1.3.2.tar.gz?download=1) |

## Additional details


Dataset:





[https://github.com/achintmehta/verification-surface-dataset](https://github.com/achintmehta/verification-surface-dataset "Opens in new tab")



(URL)



Citations [Citations help page](https://support.zenodo.org/help/en-gb/25-citations)

literature (0)

dataset (0)

software (0)

unknown (0)

Citations to this version

Search citations

Search

|
|

_No citations found_

Jump up


This site uses cookies. Find out more on [how we use cookies](https://about.zenodo.org/cookie-policy)

Accept all cookiesAccept only essential cookies
