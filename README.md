<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Quantum_Computing-8A2BE2?style=flat" />
  <img src="https://img.shields.io/badge/QPanda3-Origin_Quantum-6A0DAD?style=flat" />
</p>

<h1 align="center">quantum-experiments</h1>
<p align="center">Quantum computing algorithms implemented in Python and executed on a real quantum cloud backend (Origin Quantum / QPanda3).</p>

---

## Algorithms

### Grover's Search Algorithm
Demonstrates quadratic speedup over classical search. Finds a target state among 4 possibilities (2 qubits) in fewer iterations than brute force.

```
Steps:
1. Initialize qubits in superposition (H gate)
2. Apply oracle — marks the target state |11⟩
3. Apply diffusion operator — amplifies the target
4. Measure — collapses to the answer with high probability
```

### Quantum Random Number Generation
Generates true random numbers using quantum superposition and measurement collapse — fundamentally unpredictable unlike classical PRNGs.

### Classical vs Quantum Comparison
Side-by-side benchmark of classical search vs Grover's algorithm showing the probability advantage at scale.

## Tech Stack

- **Python 3**
- **QPanda3** — quantum SDK by Origin Quantum
- Runs on real 72-qubit quantum cloud hardware

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
