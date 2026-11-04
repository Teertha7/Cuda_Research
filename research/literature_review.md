# Literature review

Status: NEEDS REVIEW for submission-level completeness; 21 research publications selected, plus technical documentation. Search date: 2026-10-26. This is a focused narrative review, not a systematic-review claim. Primary publisher pages, author-hosted papers, official proceedings, and Crossref deposits were checked. Full-text depth differs by record; absent hardware fields mean not extracted, never invented. Bibliographic existence is distinct from replicating or endorsing a paper's conclusions.

## Search and selection

Queries covered CUDA/OpenMP Sobel, CUDA Canny, cooperative image processing, adaptive mapping, transfer-aware scheduling, stencil tiling and measurement bias. Qilin, SKMD, StarPU and the 2026 stage-aware Canny paper are especially consequential to novelty. Citation chaining from the 2024 PLOS paper identified earlier hybrid and CUDA Canny work. Excluded unverified promotional claims, unrelated edge-device DNN papers, and unrelated conferences sharing acronyms. No claimed literature speedup is used as our experimental data.

## Synthesis

GPU Canny is established, including complete hysteresis handling in Luo and Duraiswami and alternatives to BFS in Emrani et al. Song et al. directly compare CPU, OpenMP, CUDA and OpenCL. Their described local-neighbor threshold step should not be assumed equivalent to unrestricted global edge tracking. Chang et al. study a different, four-direction 5x5 Sobel operator; their optimized kernel cannot be treated as an apples-to-apples baseline for our 3x3 L1 operator.

CPU/GPU cooperation and transfer-aware partitioning have long precedents in Qilin, SKMD, StarPU, FluidiCL, and performance-aware image-analysis scheduling. Huang et al. (2026) further provide stage-aware Canny allocation with transfer-aware prediction. A generic rate-ratio formula or row split is therefore not novel. Our defensible contribution is a transparent, bounded replication/characterization on a particular laptop, with raw observations and identical Sobel outputs.

Datta et al. and Halide motivate separating algorithm semantics from schedule choices. Roofline offers explanatory concepts, but absent hardware-counter measurements we cannot establish a bandwidth-bound diagnosis. Rodinia motivates workload diversity; our synthetic corpus and two algorithms remain much narrower. Measurement-bias and repeated-evaluation literature justify reporting spread and avoiding significance claims from a single session.

## Reading records

### canny1986: A Computational Approach to Edge Detection

John Canny. IEEE Transactions on Pattern Analysis and Machine Intelligence, 1986. [Primary/DOI source](https://doi.org/10.1109/tpami.1986.4767851).

- Workload/programming model: Canny; mathematical detector formulation.
- Hardware: Not a CPU/GPU benchmark.
- Strategy: Detection/localization criteria; gradient maxima and hysteresis.
- Evidence and findings: Foundational detector derivation; not a speedup source.
- Limits and overlap: Defines algorithm family; our discrete binomial variant is not the full multiscale formulation.

### luo2008: Canny edge detection on NVIDIA CUDA

Yuancheng Luo; Ramani Duraiswami. 2008 IEEE Computer Society Conference on Computer Vision and Pattern Recognition Workshops, 2008. [Primary/DOI source](https://doi.org/10.1109/cvprw.2008.4563088).

- Workload/programming model: Canny; CUDA; OpenCV/MATLAB CPU baselines.
- Hardware: GeForce 8800 GTX, 768 MB; CPU model not extracted.
- Strategy: Full pipeline including connected-component hysteresis.
- Evidence and findings: Runtime across image resolutions; source full text inspected.
- Limits and overlap: Direct prior GPU Canny; output differences acknowledged by authors; not evidence for our exact variant.

### emrani2017: A New Parallel Approach for Accelerating the GPU-Based Execution of Edge Detection Algorithms

Zahra Emrani; Soroosh Bateni; Hossein Rabbani. Journal of Medical Signals & Sensors, 2017. [Primary/DOI source](https://doi.org/10.4103/2228-7477.199155).

- Workload/programming model: Sobel, Prewitt, Roberts and Canny; CUDA/OpenCV/MATLAB.
- Hardware: Exact GPU model not extracted.
- Strategy: Parallel alternative to BFS for Canny edge tracking.
- Evidence and findings: OCT images; execution-time comparisons.
- Limits and overlap: Direct multi-detector overlap; does not establish our particular row-partition benefit.

### song2024: A parallel Canny edge detection algorithm based on OpenCL acceleration

Yupu Song; Cailin Li; Shiyang Xiao; Qinglei Zhou; Han Xiao. PLOS ONE, 2024. [Primary/DOI source](https://doi.org/10.1371/journal.pone.0292345).

- Workload/programming model: Canny; sequential/OpenMP/CUDA/OpenCL.
- Hardware: Intel i7-8700K and GTX 1050 discussed; multiple platforms.
- Strategy: Task partition, vector access and NDRange tuning.
- Evidence and findings: Images and resolutions; runtime and acceleration metrics.
- Limits and overlap: Direct comparison overlap; local-neighbor threshold description warrants semantic caution versus global hysteresis.

### chang2023: Multi-directional Sobel operator kernel on GPUs

Qiong Chang; Xiang Li; Yun Li; Jun Miyazaki. Journal of Parallel and Distributed Computing, 2023. [Primary/DOI source](https://doi.org/10.1016/j.jpdc.2023.03.004).

- Workload/programming model: Four-direction 5x5 Sobel; GPU.
- Hardware: Jetson AGX Xavier and GTX 1650Ti.
- Strategy: Warp primitives, prefetch and operator transformation.
- Evidence and findings: Kernel comparisons with OpenCV GPU.
- Limits and overlap: Different operator than our two-direction 3x3; hardware-specific gains cannot transfer directly.

### mochurad2022: Canny Edge Detection Analysis Based on Parallel Algorithm, Constructed Complexity Scale and CUDA

Lesia I. Mochurad. Computing and Informatics, 2022. [Primary/DOI source](https://doi.org/10.31577/cai_2022_4_957).

- Workload/programming model: Canny; CUDA.
- Hardware: Not extracted from inspected abstract.
- Strategy: Parallel algorithm; image noise/complexity analysis.
- Evidence and findings: Image-size and kernel-size speedups; noise sensitivity.
- Limits and overlap: Already studies resolution effects; not validation of our implementation or CPU/GPU partitions.

### recent2026: A Decomposition-Based Method for Stage-Aware CPU/GPU Configuration Selection Under Computation-Latency SLOs in Python Image Processing Pipelines

Che Huang; Ayako Iwaki; Tomoya Hatano; Tatsuya Shimada. IEEE Access, 2026. [Primary/DOI source](https://doi.org/10.1109/access.2026.3721457).

- Workload/programming model: Canny pipeline; NumPy/SciPy and CuPy/CuPyX.
- Hardware: Three heterogeneous environments; exact models not extracted.
- Strategy: AppModel, OpModel, TransferModel; stage-aware latency SLO selection.
- Evidence and findings: Publisher abstract: prediction error and configuration selection evaluation.
- Limits and overlap: Strong recent overlap with performance-aware allocation; our study is simpler and not a novel stage-selection method.

### qilin: Qilin: Exploiting Parallelism on Heterogeneous Multiprocessors with Adaptive Mapping

Chi-Keung Luk; Sunpyo Hong; Hyesoon Kim. MICRO, 2009. [Primary/DOI source](https://faculty.cc.gatech.edu/~hyesoon/qilin_luk.pdf).

- Workload/programming model: Eight computational benchmarks including image convolution; CPU/GPU.
- Hardware: Multicore CPU and NVIDIA GPU; exact primary configuration not extracted.
- Strategy: Adaptive runtime mapping from trained performance estimates.
- Evidence and findings: Manual/static/adaptive mappings; latency and energy; varying sizes.
- Limits and overlap: Direct precedent for throughput-informed partitioning; our fixed sweep is narrower.

### skmd: SKMD: Single Kernel on Multiple Devices for Transparent CPU-GPU Collaboration

Janghaeng Lee; Mehrzad Samadi; Yongjun Park; Scott Mahlke. ACM Transactions on Computer Systems, 2015. [Primary/DOI source](https://doi.org/10.1145/2798725).

- Workload/programming model: OpenCL data-parallel kernels.
- Hardware: One multicore CPU and two asymmetric GPUs in reported evaluation.
- Strategy: Automatic partition, partial kernels, output merge; transfer awareness.
- Evidence and findings: Real-hardware comparison against fastest-device strategy.
- Limits and overlap: Direct precedent for collaboration including transfers; our hand-coded row split is not a new runtime.

### starpu: StarPU: a unified platform for task scheduling on heterogeneous multicore architectures

Cédric Augonnet; Samuel Thibault; Raymond Namyst; Pierre‐André Wacrenier. Concurrency and Computation: Practice and Experience, 2011. [Primary/DOI source](https://doi.org/10.1002/cpe.1631).

- Workload/programming model: Numerical tasks; heterogeneous runtime.
- Hardware: Multicore CPU plus GPU; exact models not extracted.
- Strategy: Dynamic task scheduling and data management.
- Evidence and findings: Runtime strategies and MAGMA comparison in publisher abstract.
- Limits and overlap: Task-runtime precedent; our single-image split does not replace StarPU.

### hybrid2014: Boosting CUDA Applications with CPU–GPU Hybrid Computing

Changmin Lee; Won Woo Ro; Jean-Luc Gaudiot. International Journal of Parallel Programming, 2014. [Primary/DOI source](https://doi.org/10.1007/s10766-013-0252-y).

- Workload/programming model: CUDA kernels; CPU/GPU runtime.
- Hardware: Exact models unavailable in inspected publisher abstract.
- Strategy: Runtime distribution queue and transparent memory.
- Evidence and findings: GPU-only comparison reported in abstract.
- Limits and overlap: Automatic hybrid execution predates our project; no numerical comparison across systems.

### survey2018: A survey on techniques for cooperative CPU-GPU computing

Raju K; Niranjan N. Chiplunkar. Sustainable Computing: Informatics and Systems, 2018. [Primary/DOI source](https://doi.org/10.1016/j.suscom.2018.07.010).

- Workload/programming model: Survey of cooperative CPU/GPU computing.
- Hardware: Multiple studies; no single benchmark platform.
- Strategy: Taxonomy of collaboration and allocation approaches.
- Evidence and findings: Publisher abstract and topic overview.
- Limits and overlap: Secondary synthesis for search guidance; not direct evidence for our measured speedup.

### fluidic: Fluidic Kernels: Cooperative Execution of OpenCL Programs on Multiple Heterogeneous Devices

Prasanna Pandit; R. Govindarajan. Proceedings of Annual IEEE/ACM International Symposium on Code Generation and Optimization, 2014. [Primary/DOI source](https://doi.org/10.1145/2544137.2544163).

- Workload/programming model: OpenCL cooperative execution.
- Hardware: Not extracted.
- Strategy: FluidiCL runtime; cooperative execution across devices.
- Evidence and findings: Metadata and author publication list verified; detailed full-text review pending.
- Limits and overlap: Relevant allocation precedent; no quantitative findings asserted.

### rodinia: Rodinia: A benchmark suite for heterogeneous computing

Shuai Che; Michael Boyer; Jiayuan Meng; David Tarjan; Jeremy W. Sheaffer; Sang-Ha Lee; Kevin Skadron. 2009 IEEE International Symposium on Workload Characterization (IISWC), 2009. [Primary/DOI source](https://doi.org/10.1109/iiswc.2009.5306797).

- Workload/programming model: Diverse heterogeneous kernels; OpenMP and CUDA.
- Hardware: GTX 280 and 3.2 GHz quad-core Core 2 Extreme.
- Strategy: Benchmark diversity and data-layout characterization.
- Evidence and findings: Performance, communication and power measurements.
- Limits and overlap: Motivates varied workloads; two edge algorithms cannot represent all heterogeneous programs.

### roofline: Roofline: an insightful visual performance model for multicore architectures

Samuel Williams; Andrew Waterman; David Patterson. Communications of the ACM, 2009. [Primary/DOI source](https://doi.org/10.1145/1498765.1498785).

- Workload/programming model: Multicore performance modeling.
- Hardware: Multiple architectures; not extracted here.
- Strategy: Operational intensity and attainable performance ceilings.
- Evidence and findings: Primary report and publisher-deposited metadata.
- Limits and overlap: Explanatory framework only; no roofline bottleneck claimed without counters/bandwidth measurements.

### teodoro: Accelerating Large Scale Image Analyses on Parallel, CPU-GPU Equipped Systems

George Teodoro; Tahsin M. Kurc; Tony Pan; Lee A.D. Cooper; Jun Kong; Patrick Widener; Joel H. Saltz. 2012 IEEE 26th International Parallel and Distributed Processing Symposium, 2012. [Primary/DOI source](https://doi.org/10.1109/ipdps.2012.101).

- Workload/programming model: Large-scale image feature analyses; CPU/GPU.
- Hardware: Parallel CPU/GPU system; exact devices not extracted.
- Strategy: Performance-aware co-scheduling and pipeline optimizations.
- Evidence and findings: Official proceedings abstract: CPU-only/GPU-only/cooperative evaluation.
- Limits and overlap: Direct image-processing scheduling precedent; our per-image stencil experiment has narrower scope.

### datta: Stencil computation optimization and auto-tuning on state-of-the-art multicore architectures

K. Datta; M. Murphy; V. Volkov; S. Williams; J. Carter; L. Oliker; D. Patterson; J. Shalf; K. Yelick. 2008 SC - International Conference for High Performance Computing, Networking, Storage and Analysis, 2008. [Primary/DOI source](https://doi.org/10.1109/sc.2008.5222004).

- Workload/programming model: Nearest-neighbor stencils.
- Hardware: Intel Clovertown, AMD Barcelona, Sun Victoria Falls, PowerXCell 8i, GTX280.
- Strategy: Blocking, locality, SIMD and auto-tuning.
- Evidence and findings: Cross-architecture stencil measurements.
- Limits and overlap: Tiling is established and architecture-sensitive; this is not our measured roofline.

### nickolls: Scalable Parallel Programming with CUDA: Is CUDA the parallel programming model that application developers have been waiting for?

John Nickolls; Ian Buck; Michael Garland; Kevin Skadron. Queue, 2008. [Primary/DOI source](https://doi.org/10.1145/1365490.1365500).

- Workload/programming model: CUDA programming model.
- Hardware: CUDA-capable manycore GPU architecture.
- Strategy: Thread hierarchy, shared memory and synchronization.
- Evidence and findings: Programming-model exposition on NVIDIA research page.
- Limits and overlap: Foundational programming reference, not proof that our candidate optimization is faster.

### halide: Decoupling Algorithms from Schedules for Easy Optimization of Image Processing Pipelines

Jonathan Ragan-Kelley; Andrew Adams; Sylvain Paris; Marc Levoy; Saman Amarasinghe; Fredo Durand. ACM Transactions on Graphics 31(4), 2012. [Primary/DOI source](https://people.csail.mit.edu/jrk/halide12/).

- Workload/programming model: Feed-forward image pipelines; ARM/x86/GPU.
- Hardware: ARM/x86/GPU; exact models not extracted.
- Strategy: Separate algorithm from schedule; tiling, fusion and recomputation.
- Evidence and findings: Author page describes application comparisons.
- Limits and overlap: Algorithm-preserving scheduling is established; we use handwritten loops rather than Halide.

### measurementbias: Producing wrong data without doing anything obviously wrong!

Todd Mytkowicz; Amer Diwan; Matthias Hauswirth; Peter F. Sweeney. ACM SIGPLAN Notices, 2009. [Primary/DOI source](https://doi.org/10.1145/1508284.1508275).

- Workload/programming model: Systems performance evaluation.
- Hardware: Pentium 4, Core 2 and m5 O3CPU; GCC/Intel compiler.
- Strategy: Causal analysis and setup randomization.
- Evidence and findings: IBM author abstract; SPEC CPU2006 measurement bias.
- Limits and overlap: Random configuration order helps but does not eliminate laptop thermal/system bias.

### georges: Statistically rigorous java performance evaluation

Andy Georges; Dries Buytaert; Lieven Eeckhout. Proceedings of the 22nd annual ACM SIGPLAN conference on Object-oriented programming systems, languages and applications, 2007. [Primary/DOI source](https://doi.org/10.1145/1297027.1297033).

- Workload/programming model: Java performance evaluation methodology.
- Hardware: Java platforms; not a CUDA benchmark.
- Strategy: Repeated measurement and rigorous statistical analysis.
- Evidence and findings: Author paper and institutional bibliographic record.
- Limits and overlap: Methodological context only; our short within-process samples are not independent cross-session replications.

