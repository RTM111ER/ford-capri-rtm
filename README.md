# Ford Capri Identity Matrix — RTM Case File #3

**Reproducible computational code for the statistical and algebraic analysis presented in *The Ford Capri Identity Matrix* (Case File #3) by Eran Harpaz.**

This repository contains the complete code used to verify the 123 arithmetic closures, run the Monte Carlo simulations, and perform the exhaustive analytical search reported in the book.

---

## What This Code Does

The book documents 20 findings containing 123 pre-declared arithmetic equations that close on biographical anchors of the Harpaz family, derived from the license plate, production data, and designer identity of a Ford Capri. This repository lets any reader reproduce every statistical and algebraic result in the book.

Five independent tests are implemented:

| Test | What It Measures | Reported Result |
|------|------------------|-----------------|
| Layer A | Statistical null against Hebrew name pool | σ = 37.4, 0/10⁸ |
| Layer B | Statistical null against random vehicles | σ = 31.9, 0/10⁷ |
| Layer 1 | Statistical null against full gematria space 1–999 | σ = 108.1, 0/10⁸ |
| Layer 2 | Network coherence density | σ = 58.7, 0/10⁸ |
| Exhaustive Solver | Analytical search over 8×10¹⁸ identity configurations | 1 solution found |

---

## Repository Structure

```
ford-capri-rtm/
├── README.md                    ← this file
├── LICENSE                      ← MIT License
├── requirements.txt             ← Python dependencies
├── core/
│   ├── rtm_equations.py         ← All 123 equations encoded as Python functions
│   └── verify_real.py           ← Sanity check: Harpaz family → 123/123 closures
├── simulations/
│   ├── layer_1_and_2.py         ← Vectorized Monte Carlo simulation (Colab/T4)
│   └── exhaustive_solver.py     ← Analytical search for uniqueness
├── analysis/
│   ├── verify_arithmetic.py     ← 241 arithmetic checks against the book
│   ├── cross_reference_map.py   ← Which values appear in which findings
│   └── network_graph.py         ← Finding-to-finding connection graph
└── docs/
    └── HOW_TO_RUN.md            ← Step-by-step instructions
```

---

## Quick Start — Local CPU

```bash
git clone https://github.com/YOUR_USERNAME/ford-capri-rtm.git
cd ford-capri-rtm
pip install numpy

# Verify real family produces 123/123
python core/verify_real.py

# Verify every arithmetic step in the book
python analysis/verify_arithmetic.py

# Find all families that satisfy 123 equations (exhaustive search)
python -c "exec(open('simulations/exhaustive_solver.py').read()); main()"
```

The exhaustive solver completes in under 1 second on CPU.

---

## Running the Full 100M Simulation (Google Colab T4)

The Monte Carlo simulation of 100,000,000 random families requires GPU acceleration:

1. Open [Google Colab](https://colab.research.google.com/) and create a new notebook.
2. Runtime → Change runtime type → Hardware accelerator → **T4 GPU**.
3. Install CuPy:
   ```
   !pip install cupy-cuda12x
   ```
4. Paste the entire content of `simulations/layer_1_and_2.py` into a new cell and run it.
5. In a separate cell, run:
   ```python
   main(n_trials=100_000_000, batch_size=500_000)
   ```

Expected runtime: approximately 100 seconds on T4.

---

## Reproducing the Book's Key Claims

### Claim 1: "123 closures for the Harpaz family"

```bash
python core/verify_real.py
```

Output: `Real Harpaz family closures: 123 / 123`

### Claim 2: "σ > 100 versus the full gematria space"

```python
# In Colab with T4 GPU + CuPy installed
main(n_trials=100_000_000, batch_size=500_000)
```

Output (approximately):
```
LAYER 1 — CLOSURE COUNT
  Real Harpaz : 123 / 123
  σ-distance  : 108.1σ
  Matches ≥123: 0 / 100,000,000
```

### Claim 3: "Exactly one family in 8×10¹⁸ satisfies the system"

```bash
python -c "exec(open('simulations/exhaustive_solver.py').read()); main()"
```

Output: `✓ UNIQUE SOLUTION FOUND` — displays the Harpaz family anchors.

### Claim 4: "Every arithmetic step in the book verified"

```bash
python analysis/verify_arithmetic.py
```

Output: `TOTAL FAILURES: 0`

---

## Dependencies

- Python ≥ 3.8
- NumPy ≥ 1.20
- CuPy (optional, for GPU acceleration — Layer 1 and Layer 2 only)

No other dependencies. No external data files. No calibration parameters.

---

## Citation

If this code is used in academic or derivative work, please cite:

```
Harpaz, E. (2026). The Ford Capri Identity Matrix.
RTM — Reflective Time Model, Case File #3.
Amazon KDP. Code: github.com/YOUR_USERNAME/ford-capri-rtm
```

---

## Contact

- Email: rtm.research@proton.me
- Book: Available on Amazon KDP

---

## License

MIT License. See `LICENSE` for full text.
