# Paper quality audit

Date: 2026-10-26. Status: **BUILT / TESTED**, **NEEDS REVIEW** for submission.

- Rebuilt the supported implementations and ran correctness checks on a real RTX 4060: 984 equivalence checks plus three analytical checks, and 36 independent Python-oracle/RGB checks.
- Verified original raw data: 3,780 observations, 252 configurations, 15 repetitions each, all output comparisons correct, no recorded benchmark failures. Verified archived executable/source hashes and all 252 original per-case CSVs against the consolidated file.
- Regenerated eight PDF/PNG figures, latency/variability tables and numerical macros from the named frozen dataset. Confirmed speedup uses corresponding per-image sequential medians. Timings include explicitly documented transfer/staging costs.
- Checked citation keys, matching research/paper bibliographies and 19 saved DOI metadata records. The 21-publication literature review remains incomplete in full-text depth for some sources; that limitation is disclosed.
- Compiled the official IEEEtran conference class with Tectonic after fixing font-encoding initialization. No unresolved citations/references, LaTeX errors, missing font warnings or overfull boxes remain. Two underfull-box spacing notices remain and were visually reviewed.
- Rendered and inspected all six pages. Two-column layout, five figures, two tables and references are legible; all pages are letter size, no detected text lies outside the page, and no visual clipping or overlaps were found.
- Automated evidence checks: **313/313 passed**, recorded in `../results/validation/audit.json`. Automated checks do not establish scientific novelty, universal correctness, publication eligibility or acceptance.

The first resumed audit exposed inaccessible dependency imports and an overly broad warning test. The first resumed compilation needed missing font metrics. Authorized dependency/cache access resolved these issues; no experimental observations were excluded. Fresh smoke timings and isolated overlap probes are preserved separately and are not reported as a new full benchmark study.

Unresolved: author/affiliation details; supervisor and author review; natural-image and independent-session generality; fuller literature extraction; CUDA/hybrid Canny; sanitizer/profiler evidence; target venue, page limit, anonymity, AI policy and fees. The paper explicitly avoids claims of a novel partitioner, beneficial tiling, statistically significant speedups or robust superiority of hybrid execution. Submission remains **NOT STARTED**.
