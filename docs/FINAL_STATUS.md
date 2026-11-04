# Final status of the resumed audit

Date: 2026-10-26, Asia/Calcutta. Overall: **NEEDS REVIEW** for the complete master prompt and conference submission; **MEASURED** for the bounded characterization study. No paper has been submitted or accepted.

## What already existed

The workspace already contained all five Sobel execution paths, sequential/OpenMP Canny, correctness fixtures, 252 benchmark configurations with 15 observations each, generated figures/tables, a 21-publication review, and a six-page IEEE manuscript/PDF. Initial status documents had never been updated past installation blockers. There is no Git repository, so no commit history can establish when individual changes were made. The frozen benchmark manifest and archived source provide experimental provenance.

## Work completed on resumption

- **BUILT / TESTED:** rebuilt the main program, image CLI, OpenMP runtime probe and overlap probe using local CUDA 12.9.41 and Visual Studio 2022 toolset 14.44.
- **TESTED:** executed 984 equivalence checks plus three analytical checks on the real RTX 4060; separately passed 36 independent NumPy-oracle/RGB fixture checks.
- **TESTED:** regenerated all eight figure pairs and paper tables from the original 3,780 observations; raw files were preserved.
- **IMPLEMENTED / TESTED:** benchmark runner now archives its executable, source and runner before measurement. A new 64-square Sobel smoke session contains 45 configurations and 90 correct observations, with no failures. This session validates the runner, not the paper's performance conclusions.
- **IMPLEMENTED / TESTED:** strengthened the audit to verify archived executable/source hashes, every per-case CSV against the consolidated dataset, finite positive timings, fresh tests, and actual LaTeX warnings. All **313/313** checks passed.
- **BUILT:** fixed font-encoding initialization before IEEEtran, added a paper-build script, recompiled the PDF, rendered all six pages and visually inspected them.
- **IMPLEMENTED:** added root/paper reproduction instructions, updated stale environment/status/plan documents, and created this report and the paper audit.
- **NEEDS REVIEW:** rechecked the official IPDPS workshop, HiPC SRS and Euro-Par pages and key overlapping research sources. The characterization title remains appropriate; no novelty claim is supported.

## Build and execution evidence

| Evidence | Result |
|---|---|
| `results/validation/build_resume.txt` | Main source rebuilt successfully |
| `results/validation/build_image_resume.txt` | Image CLI rebuilt successfully |
| `results/validation/build_probes_resume.txt` | Runtime and isolated overlap probes rebuilt |
| `results/validation/correctness_resume.txt` | RTX 4060 CC 8.9; PASS 984 plus three analytical checks |
| `results/validation/independent_oracle_resume.txt` | PASS 36 |
| `results/validation/openmp_runtime_resume.txt` | Actual team sizes match requested 1/2/4/8/16 |
| `results/validation/overlap_resume.csv` | Fresh isolated compute-window measurements; separate from end-to-end dataset |
| `results/validation/runner_smoke_resume.txt` | All 45 smoke configurations executed |
| `results/validation/paper_build_resume.txt` | Tectonic successful; no unresolved citations/fonts or overflow |
| `results/validation/audit.json` | 313 checks passed |

## Actual measured study and supported findings

Paper dataset: `results/raw/20261026T153339790016Z`, SHA-256 of `observations.csv`: `1a3bce5fba669bc3103f4bb3bfdfa54932706d59e26a26dde9be9f3bd856f2f7`. Three deterministic synthetic families, widths 512/1024/2048/4096, three warm-ups and 15 retained samples per configuration. All 3,780 observations have correct output; failures.json is empty. No observations were removed.

At 4096 square pixels, pooled Sobel medians are 37.318 ms sequential, 5.996 ms OpenMP 8 and 9.839 ms CUDA baseline. Baseline kernel median is 0.531 ms; tiled 16x16 is 0.767 ms. All tested tiled shapes have higher pooled kernel medians at every resolution. Half-CPU hybrid median is 6.528 ms, which does not establish an advantage over standalone OpenMP 8. Canny medians are 1083.075 ms sequential and 203.268 ms with 16 threads. The four-coefficient model has 6.13% MAPE on 15 largest-resolution medians excluded from fitting. These figures are generated from data, not estimates.

Five original hybrid observations have a conservative CPU-region/kernel interval overlap lower bound above 0.01 ms. This is limited evidence of temporal overlap, not a profiler trace or utilization measurement. Separate isolated overlap probes are retained but not conflated with host-to-host latency. Neither small runner timings nor validation-probe timings are pooled into the paper dataset.

## Platform and timing scope

Windows 11 build 26200; Intel Core i7-13700HX (16 cores, 24 logical processors); 16,886,128,640 bytes physical RAM; RTX 4060 Laptop GPU (8188 MiB, CC 8.9); driver 576.02; CUDA 12.9.41; MSVC 1944 / toolset 14.44; Python 3.14.2. OpenMP runtime reports macro 200203. See `ENVIRONMENT_AUDIT.md` for observations and tooling restrictions.

Sobel timing is steady-workspace processing including staging, transfers, CPU/GPU work, synchronization and merge. It excludes process/context startup, reusable allocation, input generation and correctness checking. Canny includes temporary allocation. The GPU also drives the desktop; clocks, power and affinity are uncontrolled. This is a single-session descriptive study with pooled medians/IQRs, not a statistically significant multi-session comparison.

## Literature, scope and paper readiness

**NEEDS REVIEW:** 21 publications plus two technical references, 19 cached DOI records and two additional primary-source publications. Existing Qilin, SKMD, cooperative image processing and recent stage-aware Canny work invalidate broad novelty claims for rate-based splitting. Several review entries transparently lack full hardware/method extraction. Existence checks do not substitute for a full critical reading.

**BUILT:** six-page letter-size IEEEtran conference PDF, five embedded figures and two tables; all eight analysis figures supplied separately. All citations resolve, figures are present, text stays on-page, and visual inspection found no clipping or overlap. Two underfull-box notices concern spacing, not missing content. Real author information and venue-specific review remain outstanding.

**NOT STARTED:** CUDA/hybrid Canny, natural-image performance corpus, independent full benchmark sessions, GPU sanitizer run and profiler timeline. These are scope limitations, not hardware impossibilities. GPU Canny would need its own staged correctness work, especially global hysteresis, before being included. No scheduled seven-day background task was created.

**NEEDS REVIEW:** current conference fit and live CFP. Shortlist includes future watch-list options and explicitly closed calls. Author identity, order, affiliation, email, eligibility, advisor declarations and approval cannot be fabricated. No fees, submission, agreement or declaration has been made.

## Reproduction commands

From `C:/Ekansh/academics/PCAP_project` in PowerShell:

```powershell
$py = 'C:/Users/12p20/AppData/Local/Programs/Python/Python314/python.exe'
./scripts/build.ps1
./scripts/build_image.ps1
./scripts/build_probes.ps1
./build/edge.exe --test
& $py tests/reference.py
& $py scripts/analyze.py results/raw/20261026T153339790016Z
./scripts/build_paper.ps1
& $py scripts/inspect_pdf.py
& $py scripts/audit.py
# Optional new full session; creates a fresh raw directory:
& $py scripts/benchmark.py --repeats 15 --warmups 3 --sizes 512 1024 2048 4096
```

The audit checks the frozen paper run and recorded fresh-validation logs. Full build/test logging and dependency notes are in the root README. Do not run the generic PATH Python 2.7. The smoke session is `results/raw/20261026T164511897570Z` and is excluded from the manuscript.
