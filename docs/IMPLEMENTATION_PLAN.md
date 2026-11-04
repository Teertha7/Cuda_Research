# Implementation plan

## Resumed execution and remaining work

The original sequence below has been carried through for a bounded Sobel characterization and CPU Canny comparison. Resumed work rebuilds correctness tests, regenerates derived artifacts, repairs the audit and font warnings, preserves future benchmark snapshots automatically, inspects the six-page PDF, and supplies missing reproduction/final-status documents. Evidence is in `FINAL_STATUS.md`.

Remaining research extensions: independent full measurement sessions; licensed natural images; profiler timeline and Compute Sanitizer; CUDA Canny with global connectivity validation; fuller method/hardware extraction from abstract-only sources. A live venue and real author information are needed before submission preparation can be finalized. Adding these features alone would not establish novelty.

## Original phased plan

1. Establish C++/OpenMP and CUDA build tools; execute a device probe.
2. Implement deterministic grayscale inputs, explicit Sobel semantics, and a custom Canny reference. Validate analytical cases as well as implementation equivalence.
3. Build and validate OpenMP stages, then baseline CUDA Sobel. Only after its tests pass, add a shared-memory candidate.
4. Implement row-partitioned Sobel with a halo and host/device timing; do not infer concurrency solely from asynchronous API use.
5. Benchmark several independent synthetic image families at 512, 1024, 2048 and 4096 square pixels, with randomized configuration order, warm-ups and retained individual observations. Synthetic inputs are openly reproducible but do not establish natural-image generality.
6. Analyze medians, quartiles and paired configuration speedups; keep allocation policy training and evaluation separate where sufficient data exist.
7. Verify primary literature and position this as characterization unless evidence supports a stronger contribution.
8. Generate figures/tables from measurements; write and compile IEEEtran conference manuscript with author placeholders, then audit claims and PDF layout.

Priorities: correctness and measured Sobel comparison first; CPU Canny second; distributed Canny only if dependency handling and validation can be completed. Seven days is a target, not a basis for unsupported completion claims.
