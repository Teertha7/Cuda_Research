# Novelty assessment

Status: NEEDS REVIEW by the student and supervisor before submission.

The original broad novelty proposition is not supported. CPU/GPU edge detection, tiling, adaptive partitioning, transfer-aware models and heterogeneous image pipelines have substantial prior art. Especially close: Qilin (2009), SKMD (2015), Song et al. (2024), and Huang et al. (2026; DOI 10.1109/ACCESS.2026.3721457). The latter explicitly models stage-level CPU/GPU Canny allocations and transfers.

Use the characterization title. Research question: under a fully specified 3x3 Sobel contract and a documented CPU Canny variant, how do thread count, image size, staging/transfers and row allocation affect steady-workspace latency on this laptop?

Permissible contribution: reproducible, hardware-specific performance characterization, including unfavorable hybrid/tiled outcomes; exact Sobel output comparisons; a modest held-out diagnostic model. Not claimed: a new edge detector, optimal scheduler, general speedup, first CPU/GPU comparison, or publication-ready novelty. A single-machine synthetic-input study is most naturally a course project or student/workshop artifact until broadened.

The initial `P_CPU/(P_CPU+P_GPU)` estimate balances ideal rates. Endpoint throughput that includes fixed transfer/staging costs is not perfectly divisible with rows. Evaluate its nearest tested fraction retrospectively and disclose this limitation; do not call it a proven optimum.
