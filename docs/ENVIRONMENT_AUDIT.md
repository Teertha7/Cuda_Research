# Environment audit

## Resumed audit: 2026-10-26

The initial audit below is retained as historical evidence. Its installation blockers have since been resolved. On resumption, the workspace contained source, tests, 3,780 raw observations, a literature review, analysis artifacts and a paper PDF; it still has no Git metadata. No AGENTS.md was found outside the dependency directories. Existing work was preserved.

Current verified configuration:

| Item | Verified value / evidence |
|---|---|
| OS | Windows 11, build 26200 (`platform.platform`) |
| CPU | Intel Core i7-13700HX; 24 logical processors; MSVC runtime probe |
| RAM | 16,886,128,640 bytes, fresh CIM query |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU, 8188 MiB, compute capability 8.9 |
| Driver | 576.02; nvidia-smi driver compatibility CUDA 12.9 |
| Toolkit | Local `tools/cuda/bin/nvcc.exe`, CUDA 12.9.41 |
| Compiler | Visual Studio 2022 Build Tools, MSVC 1944 / toolset 14.44 |
| OpenMP | MSVC OpenMP macro 200203; observed team sizes 1/2/4/8/16 |
| Python | Explicit Python 3.14.2; PATH `python` is Python 2.7 |
| Analysis | pandas 3.1.0, NumPy 2.5.4, Matplotlib 3.11.2 in project dependency directory |
| CUDA execution | TESTED: fresh rebuilt suite passed 984 equivalence and three analytical checks |
| Independent oracle | TESTED: 36 fresh NumPy-oracle/RGB fixture checks |
| LaTeX | Local Tectonic with IEEEtran V1.8b |

Evidence: `results/validation/build_resume.txt`, `correctness_resume.txt`, `independent_oracle_resume.txt`, `openmp_runtime.txt`, and the frozen raw manifest. The GPU also drives the desktop; power, thermal state and affinity were not controlled. No sanitizer/profiler executable was present in the minimal local CUDA bin directory.

Sandbox restrictions prevent ordinary agent reads of some pre-existing Python package directories and CIM metadata. Authorized execution outside that sandbox successfully imported packages and queried RAM. The first resumed LaTeX compilation lacked cached font metrics; an authorized rerun downloaded the missing metrics and compiled successfully. These were tooling failures, not benchmark exclusions.

## Historical initial audit

Audit date: 2026-10-26 (Asia/Calcutta). Initial directory was empty, including hidden entries. `git status --short` reported that this is not a Git repository. No existing source, datasets, results, or AGENTS.md were found.

| Item | Observed value |
|---|---|
| Platform | Windows, PowerShell |
| CPU | Intel Core i7-13700HX, 16 cores, 24 logical processors (CIM) |
| RAM | Pending reliable query |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU |
| Device memory | 8188 MiB reported by nvidia-smi |
| Compute capability | 8.9 reported by nvidia-smi |
| Driver | 576.02 |
| Driver CUDA compatibility | 12.9; this is NOT an installed toolkit version |
| CUDA toolkit | nvcc absent from PATH; standard toolkit directory absent |
| C++ compiler | cl, g++, clang absent from PATH; standard Visual Studio directories absent |
| Python | PATH resolves Python 2.7; Python 3.14 and bundled Python also available |
| OpenMP runtime | Pending compiler installation and runtime probe |
| CUDA execution | BLOCKED pending toolkit/compiler installation and executable probe |

GPU is also driving the Windows desktop (WDDM). Background graphics applications were active. Measurements must disclose this source of interference. Initial sandbox CIM access failed; the authorized elevated read succeeded for the CPU. No CUDA measurements exist at this stage.

Requested Microsoft Visual Studio 2022 C++ Build Tools installation. Installation outcome is pending. CUDA 12.x is preferred to avoid requiring a driver upgrade. Installation and dependency changes must be recorded below when known.
