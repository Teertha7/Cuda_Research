# CPU-GPU edge-detection performance study

CSE 3129 project: **A Performance Characterization of CPU-GPU Edge Detection using OpenMP and CUDA**.

The measured study implements sequential/OpenMP Sobel and Canny, global-memory and shared-memory CUDA Sobel, and CPU-GPU row-partitioned Sobel. CUDA Canny is not implemented. The six-page IEEE paper is a research draft with author placeholders, not a submitted paper.

## Deliverables

- `paper/main.pdf`: compiled IEEE conference draft; `paper/main.tex` and `paper/references.bib`: editable source.
- `src/`: implementation; `tests/`: independent NumPy oracle and overlap/runtime probes.
- `results/raw/20261026T153339790016Z/`: immutable paper dataset, executable/source snapshots, manifests, 252 case outputs, and 3,780 observations.
- `results/processed/20261026T153339790016Z/`: summaries, speedups, partition policy and held-out predictions.
- `paper/figures/` and `paper/tables/`: generated figures and tables.
- `research/`: 21-publication review, overlap matrix, bibliography and 19 DOI metadata records.
- `docs/FINAL_STATUS.md`: verified completion boundaries and remaining work.
- `paper/SUBMISSION_CHECKLIST.md` and `paper/CONFERENCE_SHORTLIST.md`: venue preparation; no submission authorized.

## Build and test on this Windows machine

Run PowerShell from the project root. Visual Studio 2022 C++ Build Tools, CUDA 12.9, and an NVIDIA compute-capability 8.9 GPU are the tested configuration. The scripts discover Visual Studio using `vswhere`; CUDA is available at `tools/cuda/bin/nvcc.exe` even though it is absent from PATH. The build targets `sm_89`; change the architecture only when porting to a different compatible GPU. This is not yet a cross-platform build system.

```powershell
./scripts/build.ps1
./scripts/build_image.ps1
./scripts/build_probes.ps1
./build/edge.exe --probe
./build/edge.exe --test
./build/runtime_probe.exe
$py = 'C:/Users/12p20/AppData/Local/Programs/Python/Python314/python.exe'
& $py tests/reference.py
```

The current machine's `python` command resolves to Python 2.7: use the explicit Python 3 path above. On another machine, use a Python 3 environment with `python -m pip install -r requirements.txt`. Scripts prefer project-local `tools/python` packages if present. This machine's pre-existing package directories require access outside the agent sandbox; ordinary authorized execution succeeded. No benchmark timings depend on Python's numerical libraries: the C++ executable emits those timings directly.

## Run an image

```powershell
./build/edge_image.exe data/test_images/vertical_step.pgm build/edges.pgm sobel cuda 8
./build/edge_image.exe data/test_images/weak_connected.pgm build/canny.pgm canny omp 8
```

Input is binary 8-bit PGM (P5) or PPM (P6). RGB is converted with `(77R+150G+29B+128)>>8`. Sobel output is a big-endian 16-bit PGM with header maximum 2040, preserving L1 gradient magnitude; some image viewers require contrast adjustment. Canny output is 8-bit binary 0/255. Hybrid CLI uses a half-row split and eight CPU threads. See `docs/ALGORITHMS.md` for numeric and boundary contracts.

## Reproduce analysis and paper

```powershell
& $py scripts/analyze.py results/raw/20261026T153339790016Z
./scripts/build_paper.ps1
& $py scripts/inspect_pdf.py
& $py scripts/audit.py
```

Analysis regenerates eight PDF/PNG figures, tables and claim macros from the named raw run. It overwrites derived outputs, never raw observations. `audit.py` deliberately audits the frozen paper dataset; it is not a generic audit of arbitrary future runs. `inspect_pdf.py` renders pages into `paper/qa/`; inspect them visually in addition to checking bounds. Tectonic is in `tools/tectonic`; its first run may download fonts/TeX packages. Standard LaTeX alternatives are `pdflatex main`, `bibtex main`, and two further `pdflatex main` passes from `paper/`, with IEEEtran installed or the included class/style files.

## Collect a new benchmark session

```powershell
& $py scripts/benchmark.py --repeats 15 --warmups 3 --sizes 512 1024 2048 4096
```

Every invocation creates a new timestamped directory. It preserves source, executable, runner, per-case stdout/stderr, manifest and observations. Do not replace the paper dataset with a fresh run without rechecking every claim. The full protocol uses three procedural image families, sequential and OpenMP 1/2/4/8/16, CUDA baseline, three tiled shapes, and five hybrid fractions. Each case is a separate process; order is shuffled with seed 3129. All retained timings and warm-ups are correctness-checked. No slow samples are excluded.

Timing is steady-workspace host-to-host processing: Sobel includes staging, H2D, kernels, D2H, CPU work, synchronization and merge, but excludes workspace allocation, input generation, file I/O and validation. Canny includes its temporary allocations. CUDA events and host wall time describe different intervals and must not be conflated.

## Interpretation

The paper dataset is a single session on an i7-13700HX / RTX 4060 laptop. At 4096 square pixels, pooled Sobel medians were 37.318 ms sequential, 5.996 ms OpenMP 8, and 9.839 ms CUDA baseline. Tiling increased kernel time in every measured shape/size. These are hardware- and protocol-specific findings. No novel scheduler, universal speedup, statistical significance, or submission readiness is claimed.
# Cuda_Research
