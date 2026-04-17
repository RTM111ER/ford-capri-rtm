# How to Run

This document provides step-by-step instructions for reproducing every statistical and algebraic result reported in *The Ford Capri Identity Matrix* (RTM Case File #3).

---

## 1. Verify the Real Family Produces 123 Closures

**Purpose:** Sanity check. The Harpaz family anchors, when substituted into the 123 equations, should produce 123 closures.

```bash
cd ford-capri-rtm
python core/verify_real.py
```

**Expected output:**
```
Total equations: 123
Closures for real Harpaz family: 123 / 123
Percentage: 100.0%
```

If you see anything other than 123/123, the code has been corrupted. The encoded equations are published unchanged from the book.

---

## 2. Verify the Arithmetic in the Book

**Purpose:** Every computation step in the 20 findings is verified here — 241 individual arithmetic assertions.

```bash
python analysis/verify_arithmetic.py
```

**Expected output:** 241 individual `✓` marks followed by:
```
TOTAL FAILURES: 0
```

Each of the 241 assertions corresponds to a step printed in the book. If any fails, the discrepancy is between this code and the book — not between the mathematics and reality.

---

## 3. Run the Exhaustive Analytical Solver

**Purpose:** Search the complete identity space for every family that satisfies all 123 equations. This is not a Monte Carlo simulation — it is an algebraic search that returns every solution, not a probability.

```bash
python -c "exec(open('simulations/exhaustive_solver.py').read()); main()"
```

**Expected output:**
```
✓ UNIQUE SOLUTION FOUND — only one family in the entire identity space
  satisfies all 123 equations.

Solution:
  surname              = 292
  first_self           = 320
  full_self            = 612
  ...
```

**Runtime:** Under 1 second on CPU.

**What it means:** The solver iterated through ~8×10¹⁸ possible identity configurations and returned exactly one — the Harpaz family. No other family exists.

---

## 4. Run the 100-Million-Trial Monte Carlo Simulation

**Purpose:** Reproduce the statistical results for Layer 1 (closure count, σ = 108) and Layer 2 (network density, σ = 58.7).

### Option A — Google Colab T4 GPU (recommended, ~100 seconds)

1. Open [https://colab.research.google.com/](https://colab.research.google.com/)
2. Create a new notebook
3. Runtime → Change runtime type → Hardware accelerator → T4 GPU
4. In a cell, install CuPy:
   ```
   !pip install cupy-cuda12x
   ```
5. In the next cell, paste the entire content of `simulations/layer_1_and_2.py` and run.
6. In a third cell, run:
   ```python
   main(n_trials=100_000_000, batch_size=500_000)
   ```

### Option B — Local GPU

If you have an NVIDIA GPU with CUDA 12.x installed locally:
```bash
pip install cupy-cuda12x
python simulations/layer_1_and_2.py
# Then edit the script to call: main(n_trials=100_000_000, batch_size=500_000)
```

### Option C — Local CPU (slow, test only)

Falls back to NumPy automatically. Only run smaller numbers of trials:
```bash
python -c "exec(open('simulations/layer_1_and_2.py').read()); main(n_trials=10_000, batch_size=2_000)"
```

**Expected output (on T4, 100M trials):**
```
LAYER 1 — CLOSURE COUNT
  Real Harpaz : 123 / 123
  Random mean : 28.15   std: 0.88   max: 60
  σ-distance  : 108.1σ
  Matches ≥123: 0 / 100,000,000

LAYER 2 — NETWORK DENSITY
  Real Harpaz : 66.3%
  Random mean : 20.0%   std: 0.008   max: 67.5%
  σ-distance  : 58.7σ
  Matches ≥66.3%: 2 / 100,000,000

JOINT TEST — both layers ≥ real
  Matches BOTH: 0 / 100,000,000
```

---

## 5. Analyze the Cross-Reference Network

**Purpose:** Report the derived values that recur across findings and the finding-to-finding connection density (the 85.8% figure mentioned in the book's analysis).

```bash
python analysis/cross_reference_map.py
python analysis/network_graph.py
```

Prints a sorted list of derived values by number of findings they appear in, and the full pairwise connection graph between the 20 findings.

---

## Troubleshooting

### "✗ Backend: NumPy (CPU)" in Colab

CuPy did not install or T4 is not enabled. Check:
1. Runtime type is set to T4 GPU
2. `!pip install cupy-cuda12x` ran without errors
3. The output in step 4 says `✓ Backend: CuPy (GPU)`

### ValueError from `sys.argv` in Colab

Do not include the `if __name__ == "__main__":` block when pasting into Colab. Just paste the script and call `main(...)` in a separate cell.

### `ImportError: No module named 'rtm_equations'` in verify_real.py

Run from the repository root directory, not from inside `core/`:
```bash
cd ford-capri-rtm
python core/verify_real.py   # NOT: cd core; python verify_real.py
```

If needed, add the project root to `PYTHONPATH`:
```bash
PYTHONPATH=core python core/verify_real.py
```

---

## Getting Help

- Questions about the methodology: rtm.research@proton.me
- Issues with the code: open a GitHub issue
