# Symbolic Alpha Synthesizer

[![CI](https://github.com/Ishant5436/symbolic-alpha-synthesizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Ishant5436/symbolic-alpha-synthesizer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standards: Power of 10](https://img.shields.io/badge/Safety_Critical-Power_of_10-brightgreen.svg)](https://en.wikipedia.org/wiki/The_Power_of_10:__Rules_for_Developing_Safety-Critical_Code)
[![Platform: Apple Silicon & Linux](https://img.shields.io/badge/Platform-Apple_Silicon_%7C_Linux_ARM64_%7C_x86_64-blueviolet.svg)](#)

A deterministic, high-performance C++20 and Python evolutionary engine for continuous mathematical alpha discovery in quantitative financial markets.

---

## 1. Problem Formulation: The Tabular Factor Ceiling

In institutional quantitative tournaments (e.g., Numerai, CrunchDAO) and statistical arbitrage strategies, practitioners predominantly train gradient-boosted decision trees (LightGBM, CatBoost) or multilayer perceptrons directly on normalized tabular features $X \in \mathbb{R}^{N \times K}$.

Because tree splits are restricted to axis-aligned coordinate hyperplanes ($\mathbb{I}[x_j > c]$), gradient-boosted models struggle to capture continuous, non-linear geometric relationships such as:

$$f(x_1, x_2) = \tanh\left(\frac{x_1 - x_2}{1 + |x_1| + |x_2|}\right)$$

Consequently, models converge on identical feature interactions, creating high meta-model collinearity. Under competitive payout regimes where payouts reward Meta-Model Contribution (orthogonal predictive return):

$$\text{Payout} \propto \text{Stake} \times (\text{CORR} + 2 \times \text{MMC})$$

standard tabular models experience decaying residual edge.

---

## 2. Architecture & Evolutionary Pipeline

`Symbolic Alpha Synthesizer` automates the discovery of orthogonal, closed-form mathematical expressions through a multi-stage genetic programming compiler:

```
[ Raw Market Factors X ] ───► [ Fixed Scratch Memory Arena ]
                                            │
[ AST Grammar Generator ] ───► [ Bytecode Compiler ] ───► [ ARM64 Vectorized C++ Kernel ]
                                                                      │
                                                          [ Tri-Hurdle Validation Gate ]
                                                          ├── 1. Sharpe Ratio >= 1.05
                                                          ├── 2. Max Factor Corr < 0.12
                                                          └── 3. Era Consistency >= 65%
                                                                      │
                                                          [ Alpha Vault Serializer ]
```

### Supported Mathematical Primitives

* **Unary Operators:** $\tanh(x)$, $\text{sigmoid}(x)$, $\text{sign}(x)$, $\text{abs}(x)$, $\log(1 + |x|)$, $\text{zscore}(x)$.
* **Binary Operators:** $+$, $-$, $\times$, $\div_{\text{safe}}$ (where $x \div 0 = 0.0$), $\max(x, y)$, $\min(x, y)$.
* **Grammar Depth Bounds:** Strictly clamped to depth $D \le 4$ to eliminate formula bloating and pathological overfitting.

---

## 3. High-Throughput C++20 Vector Engine (`libchimera_eval`)

The execution kernel processes candidate bytecode expressions natively on vectorized memory buffers:

* **Zero Dynamic Allocation on Hot Path:** A contiguous memory arena (`ChimeraArena`) of 16 float register planes is pre-allocated at initialization. Hot-path evaluations execute zero `malloc`, `new`, `free`, or `delete` calls.
* **Apple Silicon ARM64 Optimization:** Compiles with `-std=c++20 -O3 -mcpu=apple-m5 -ffast-math -arch arm64` to maximize hardware instruction pipelines and cache locality.

### Measured Performance Benchmarks (Apple Silicon M5 Pro)

| Benchmark Metric | Measured Performance | Operational Equivalent |
| :--- | :--- | :--- |
| **Row Evaluation Throughput** | **259,416,384 rows/sec** | Real-time cross-sectional processing |
| **Candidate Formula Rate** | **311,300 formulas/min** | Rapid multi-generation convergence |
| **500-Iteration Batch Latency** | **0.0964 seconds** | Sub-second genetic cycle |
| **Heap Allocations on Hot Path** | **0** | Deterministic memory safety |

---

## 4. Mission-Critical Architectural Invariants

The C++ vector engine enforces deterministic high-assurance safety invariants for mission-critical financial computing:

1. **Control Flow Determinism:** Zero `goto`, `setjmp`, `longjmp`, or direct/indirect recursion.
2. **Bounded Execution Horizons:** All iteration bounds across row counts are strictly checked against `CHIMERA_MAX_ROWS`.
3. **Zero-Allocation Hot Path:** Scratch memory buffers are pre-allocated at startup; zero dynamic allocation occurs during bytecode execution.
4. **Atomic Function Geometry:** Every function is strictly $\le 60$ lines of code for auditable comprehension and cache locality.
5. **Continuous Invariant Assertions:** Minimum of 2 assertions per operational function validating pointer non-nullness, array boundaries, and parameter invariants.
6. **Minimal Scope Enclosure:** All loop iterators and intermediate variables are declared at the smallest possible scope.
7. **Exhaustive Parameter & Return Verification:** All return values and input parameters are explicitly validated at function boundaries.
8. **Zero-Macro Preprocessor Hygiene:** Zero preprocessor function macros or complex `#ifdef` blocks to prevent AST divergence.
9. **Single-Indirection Pointer Safety:** Maximum of one level of dereferencing; zero function pointers on the hot path.
10. **Pedantic Static Compilation Gate:** Compiles under pedantic `-Wall -Wextra -Werror -std=c++20 -O3` with zero warnings, verified by mechanical static AST parsing (`scripts/audit_safety_invariants.py`).

---

## 5. Quickstart & Usage

### 1. Build and Test (< 3 Seconds)

```bash
# Clone repository
git clone https://github.com/Ishant5436/symbolic-alpha-synthesizer.git
cd symbolic-alpha-synthesizer

# Compile native C++ dynamic library
make csrc

# Run complete 17-test suite
make test

# Run Power of 10 static AST audit
make audit

# Run 1-second live benchmark and demo
make demo
```

### 2. Autonomous Alpha Mining via CLI

```bash
# Mine candidate alphas across 10 features, 10 eras, and 50,000 rows
symbolic-alpha mine --features 10 --rows 5000 --eras 10 --generations 5 --vault data/alpha_vault.json
```

### 3. Python API Integration

```python
import numpy as np
import pandas as pd
from symbolic_alpha.evaluator import ChimeraEngine, InstructionBuilder
from symbolic_alpha.alpha_vault import AlphaVault

# Load serialized alpha vault
vault = AlphaVault.load("data/alpha_vault.json")

# Augment raw tabular DataFrame with synthesized closed-form features
df = pd.DataFrame(np.random.randn(1000, 10), columns=[f"feat_{i}" for i in range(10)])
augmented_df = vault.augment_dataframe(df, feature_cols=[f"feat_{i}" for i in range(10)])

print(f"Original shape: {df.shape} -> Augmented shape: {augmented_df.shape}")
```

---

## 6. Repository Layout

```text
symbolic-alpha-synthesizer/
├── csrc/
│   ├── chimera_eval.hpp           # Power of 10 struct layouts, opcodes, memory arena
│   ├── chimera_eval.cpp           # ARM64 SIMD evaluation kernel
│   └── Makefile                   # Cross-platform Clang build (Darwin .dylib / Linux .so)
├── src/
│   └── symbolic_alpha/
│       ├── __init__.py
│       ├── evaluator.py           # ctypes zero-copy wrapper to C++ core
│       ├── ast_generator.py       # Expression trees, mutation, and crossover
│       ├── orthogonality_filter.py# Tri-Hurdle validation gate
│       ├── alpha_vault.py         # JSON serializer and DataFrame feature injector
│       ├── genetic_synthesizer.py # Evolutionary loop & population orchestrator
│       └── cli.py                 # Click CLI runner (mine / benchmark / audit / demo)
├── tests/
│   ├── test_chimera_eval.py       # Numerical parity (C++ vs NumPy)
│   ├── test_ast_generator.py      # Grammar and mutation invariant tests
│   ├── test_orthogonality.py      # Tri-Hurdle acceptance and rejection tests
│   ├── test_alpha_vault.py        # Serialization and round-trip integrity tests
│   └── test_genetic_synthesizer.py# Multi-generation evolutionary convergence tests
├── scripts/
│   └── audit_safety_invariants.py # Static AST analyzer checking Power of 10 rules
├── .github/workflows/
│   └── ci.yml                     # Multi-OS CI (macOS-14 + Ubuntu)
├── Makefile                       # Top-level build and test automation
├── pyproject.toml                 # Package metadata and CLI entrypoints
└── README.md                      # Institutional documentation
```

---

## 7. License

MIT License. Engineered for deterministic safety, zero collinearity, and high-frequency quantitative execution.
