# DoraHacks Submission Dossier: Symbolic-Alpha-Synthesizer

## 1. Hackathon Target Profile
* **Active Target:** [MunichTech Innovation Hackathon 2026 – Build Applied Solutions for Industry](https://dorahacks.io/hackathon/2019/tracks)
  * **Tracks:** Applied AI for Real-World Impact & Industrial AI / DeepTech
  * **BUIDL Profile:** [#48962](https://dorahacks.io/buidl/48962)
  * **Eligibility:** Code-only submission with working C++20 engine, tests, and live demo
* **Co-Target:** [The Turing Test Hackathon 2026](https://dorahacks.io/hackathon)
  * **Focus:** Agentic AI, Quant Systems, Financial Computation, Autonomous Decision Making
  * **Prize Pool:** $120,000 USD

---

## 2. BUIDL Profile & Form Fields (Copy-Paste Ready)

### Project Name
`Symbolic-Alpha-Synthesizer: Deterministic C++20 Evolutionary Engine for Mathematical Alpha & Sensor Discovery`

### Tagline (One-Liner)
A high-performance C++20 ARM64 vectorized genetic programming compiler discovering non-linear, human-interpretable mathematical equations for quantitative finance and industrial IoT.

### Repository URL
`https://github.com/Ishant5436/symbolic-alpha-synthesizer`

### Primary Track
`Applied AI for Real-World Impact / Industrial AI / DeepTech`

---

## 3. Project Description (Markdown Form Text)

### Problem Statement
In institutional quantitative finance and tournaments (e.g., Numerai, CrunchDAO), participants predominantly train gradient-boosted decision trees (LightGBM, CatBoost) on tabular market features. Because decision trees make strictly axis-aligned splits, they cannot efficiently represent continuous, non-linear mathematical combinations (such as geometric interactions or tanh-normalized differentials). As a result, thousands of competing models discover collinear signals, reducing Meta-Model Contribution (MMC) and degrading risk-adjusted alpha.

### The Solution: Symbolic Alpha Synthesizer
Symbolic Alpha Synthesizer is an autonomous evolutionary compiler that searches the space of closed-form mathematical expressions:
* **ARM64 SIMD Vector Engine:** Evaluates candidate expression trees compiled to bytecode in native C++20 on Apple Silicon and Linux with zero dynamic memory allocation on the hot path.
* **Tri-Hurdle Validation Gate:** Validates candidate formulas across historical eras on out-of-sample data, enforcing:
  1. Performance Hurdle: Out-of-sample raw per-era Sharpe $\ge 1.05$.
  2. Orthogonality Hurdle: Max Spearman correlation to existing factors $\max_k |\rho| < 0.12$.
  3. Regime Stability Hurdle: Positive correlation in $\ge 65\%$ of all validation eras.
* **Alpha Vault:** Automatically catalogs winning orthogonal formulas in JSON format and augments live feature pipelines.

### Mission-Critical Architectural Invariants
The C++ core strictly enforces deterministic safety invariants:
* **Zero-Allocation Hot Path:** A fixed memory arena is allocated at boot; zero `malloc` or `new` calls during bytecode execution.
* **Atomic Function Geometry:** All functions strictly bounded to $\le 60$ lines for auditable cognitive clarity and instruction cache locality.
* **Continuous Invariant Assertions:** Minimum 2 assertions per function validating pointer non-nullness and index boundaries.
* **Bounded Execution Horizons:** Strict compile-time limits on bytecode instruction count ($L \le 64$) and tree depth ($D \le 4$).
* **Pedantic Static Compilation Gate:** Zero warnings under `-Wall -Wextra -Werror -std=c++20 -O3` verified by static AST parsing.

### Performance Benchmarks (Apple Silicon M5 Pro)
* **Row Evaluation Throughput:** 274,000,000 row-evaluations/sec.
* **Formula Evaluation Rate:** 328,000 candidate formulas/minute.
* **Execution Latency:** 500-iteration batch completes in 0.091 seconds.
* **Test Suite:** 17/17 automated unit and integration tests passing in 0.87 seconds.

---

## 4. Local Execution & Evaluation Commands (For Judges)

```bash
git clone https://github.com/Ishant5436/symbolic-alpha-synthesizer.git
cd symbolic-alpha-synthesizer

# Option A: Modern CMake Workflow
cmake -B build && cmake --build build
cmake --build build --target audit
cmake --build build --target run_tests

# Option B: Classic Make Workflow
make csrc
make test
make audit
make demo
```
