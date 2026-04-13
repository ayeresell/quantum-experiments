<p align="center">
  <img src="https://app-eta-seven-61.vercel.app/banner-quantum.svg" width="900"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Quantum_Computing-8B5CF6?style=flat"/>
  <img src="https://img.shields.io/badge/QPanda3-Origin_Quantum-06B6D4?style=flat"/>
  <img src="https://img.shields.io/badge/72--qubit_hardware-real-A78BFA?style=flat"/>
</p>

<h2 align="center">quantum-experiments — Quantum Algorithms on Real Hardware</h2>
<p align="center">Quantum algorithm implementations in Python, executed on a real 72-qubit quantum computer via Origin Quantum cloud.</p>

---

## Grover's Search Algorithm

Quantum search with quadratic speedup over classical brute force.

```
Step 1 — Superposition
  H(0), H(1)  →  |ψ⟩ = ¼(|00⟩ + |01⟩ + |10⟩ + |11⟩)
  All 4 states equally probable (25% each)

Step 2 — Oracle
  Marks the target state |11⟩ with a phase flip
  Implemented via CZ gate (H + CNOT)

Step 3 — Grover Diffusion
  Amplifies the marked state's amplitude
  Suppresses all others

Step 4 — Measurement
  |11⟩ collapses with ~100% probability
  Classical search: 4 checks → Quantum: 1
```

## Quantum Random Number Generator

Uses the fundamental randomness of quantum mechanics — wavefunction collapse on measurement. Unlike classical PRNGs, the result is **physically unpredictable**.

## Classical vs Quantum

| | Classical Search | Grover's Algorithm |
|---|---|---|
| N elements | O(N) | O(√N) |
| 4 elements | 4 checks | ~1 iteration |
| 1,000,000 | 1,000,000 | ~1,000 |

## Tech Stack

- **Python 3**
- **QPanda3** — quantum SDK by Origin Quantum
- Runs on a real **72-qubit** quantum cloud backend

## Files

| File | Description |
|------|-------------|
| `grover.py` | Grover's search algorithm (2 qubits) |
| `quantum_random.py` | Quantum random number generator |
| `comparison.py` | Classical vs quantum benchmark |

## Setup

```bash
pip install pyqpanda3
python grover.py
```
