# Paper reproduction

Status: BUILT; NEEDS REVIEW for submission.

`main.pdf` is a six-page, letter-size, two-column IEEEtran conference draft. `main.tex` includes generated tables and figures. Author names, affiliations and contact details are intentionally placeholders.

From the repository root, run the analysis, `scripts/build_paper.ps1`, PDF inspection and audit commands documented in `../README.md`, in that order. Tectonic handles bibliography passes automatically and preserves logs. The local `IEEEtran.cls`, `IEEEtran.bst`, and `template/bare_conf.tex` accompany the downloaded template archives in `../tools/downloads/`; retain their original notices. The class reports IEEEtran V1.8b.

The manuscript uses only the frozen raw run `20261026T153339790016Z`. `tables/numbers.tex` is generated, not a place to manually edit results. Five figures are included for page economy; all eight requested analysis figures are available in `figures/`. No target venue has been selected, so six pages is a draft layout, not a verified venue page limit.

See `FINAL_AUDIT.md`, `SUBMISSION_CHECKLIST.md`, and `CONFERENCE_SHORTLIST.md`. The known limits include synthetic images, one measurement session, no CUDA/hybrid Canny, no GPU profiler timeline or Compute Sanitizer result, and incomplete full-text extraction for some reviewed publications. Do not remove these limitations or convert prospective plans into completed-work claims.
