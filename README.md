# Melinda's 4D Cube — the 2×2×2×2 puzzle graph

**An executable graph description of Melinda Green's physical four-dimensional
Rubik's puzzle, for the CayleyPy community and anyone searching for short solutions.**

[Formal specification](GRAPH_SPEC.md) · [Contributing](CONTRIBUTING.md)
· [Melinda Green's original puzzle page](https://superliminal.com/cube/2x2x2x2/)

## The physical puzzle in motion

[![Animated demonstration of a gyro on Melinda Green's physical 2×2×2×2 puzzle](https://superliminal.com/cube/wiki/images/GyroGif.gif)](https://superliminal.com/cube/wiki/Physical_2%5E4_Methods.html)

*A gyro reorientation demonstrated with the physical puzzle.
Source: [Physical 2^4 Methods — Superliminal Wiki](https://superliminal.com/cube/wiki/Physical_2%5E4_Methods.html).
The animation is embedded from the original website; rights remain with its
respective rights holder.*

This sequence changes the puzzle's four-dimensional orientation. In the
proposed free-reorientation metric below, the completed gyro has zero cost;
its intermediate physical actions are not separate graph edges.

## Photograph and demonstrations

[![Ernő Rubik examining Melinda Green's physical 2×2×2×2 puzzle](https://superliminal.com/cube/2x2x2x2/erno2x2x2x2g4g13.jpg)](https://superliminal.com/cube/2x2x2x2/)

*Ernő Rubik examining the puzzle at Gathering for Gardner 13.
Photo from [Melinda Green's website](https://superliminal.com/cube/2x2x2x2/),
displayed from its original URL; image rights remain with the rights holder.*

- [Introduction and demonstration](https://www.youtube.com/watch?v=_1ZPQV-ejtA): the main video linked by the puzzle's author.
- [Canonical Moves](https://www.youtube.com/watch?v=DzRH8BOJL8Q): permitted physical manipulations.
- [Physical puzzle alongside its virtual 4D counterpart](https://www.youtube.com/watch?v=k6ZSu0xOPbQ): Marc Ringuette's side-by-side demonstration.

These videos illustrate physical manipulations. The search metric used here is
defined separately below and in [GRAPH_SPEC.md](GRAPH_SPEC.md).

## What makes this puzzle special?

An ordinary Rubik's cube is three-dimensional. Melinda's 2×2×2×2 represents its
four-dimensional analogue: a tesseract has eight cubic cells instead of six
square faces. The puzzle has sixteen corner pieces, each bearing four colors.

Melinda Green created a physical version that can be held and manipulated.
On her website, she describes it as the world's first physical 3D embodiment of
a 4D twisty puzzle. The earliest solutions in her list date to 2017.

The object itself exists in our three-dimensional world. Its magnetic
construction implements transformations of the 4D puzzle. A special sequence
called a `gyro` changes its four-dimensional orientation, making other cells
accessible.

According to the author, the number of states, up to whole-puzzle rotation, is

**3,357,894,533,384,932,272,635,904,000 — approximately 3.36 × 10²⁷.**

Enumerating every vertex is therefore impractical. This repository defines the
graph through a small set of permutations, allowing neighboring states to be
computed on demand. The code makes the definitions and counts independently
checkable.

## The challenge for the community

Find short paths from scrambled states to the solved state. The optimal solution
length does not need to be known in advance. A valid solution establishes an
upper bound on distance unless its optimality is proved separately.

This is a **proposal for a standalone community problem**, not an announcement
of an approved CayleyPy or Kaggle competition. The repository supplies a graph
definition, data and a solution verifier; it does not establish prizes,
deadlines or the rules of an external competition.

## What counts as one move?

The proposed **cell-turn metric** is named `CTM-free-rotations-v1`:

- One move is any nonidentity proper rotation of one cubic cell. Each cell has
  23 such rotations, including quarter-turns, half-turns and 120° rotations
  about its body diagonals.
- Whole-puzzle rotations, including completed `gyro` reorientations, have zero
  cost. This is a rule of the proposed mathematical problem.
- Intermediate physical actions within a `gyro` are not separate graph edges.

This metric searches physical-puzzle states with free reorientation. It
**does not count regrips, magnetic connections or hands-on solving time**.
Charging for `gyro` operations would require a different formulation that
retains orientation and assigns costs to those operations.

To avoid storing 192 equivalent rotations of each state, one oriented corner
is fixed. This leaves **92 generators**: 23 rotations for each of the four cells
not containing that corner. The reduction preserves shortest-path distances
in the chosen metric; see [GRAPH_SPEC.md](GRAPH_SPEC.md) for the proof.

## Two graph representations of the same puzzle

This repository publishes **both a 184-move fixed-frame model and a 92-move
rotation-reduced model**. These describe the same physical puzzle under different
state conventions; the 92-move version does not discard half of the puzzle.

| Representation | Cells used | Rotations per cell | Generators |
| --- | ---: | ---: | ---: |
| Fixed coordinate frame | All 8 cells | 23 | **184** |
| Fixed oriented corner; whole-puzzle rotations identified | 4 cells not containing that corner | 23 | **92** |

**184-move model:** [data/framed_puzzle_info.json](data/framed_puzzle_info.json)
retains the puzzle's orientation relative to fixed coordinate axes. Rotated
copies are separate states. Its state space is 192 times larger than the
rotation-reduced state space. Solving to the exact framed identity can require
a different number of moves than solving up to a free whole-puzzle rotation.

**92-move model (the current default):**
[data/puzzle_info.json](data/puzzle_info.json) identifies states that differ
only by a proper whole-puzzle rotation. One chosen corner is always returned
to its reference position and orientation. A turn of a cell containing that
corner, followed by this normalization, is equivalent to an inverse turn of
the opposite cell. Thus all eight cells' turns are represented using only
four cells in the normalized coordinates.

We chose the 92-move representation to avoid duplicate orientations and reduce
the number of neighbors searched. **It preserves shortest-path distances only
for the stated problem with free whole-puzzle reorientation**, as proved in
[GRAPH_SPEC.md](GRAPH_SPEC.md#5-why-fixing-a-corner-is-valid).
It does not claim equality with distances to the exact identity in the
unreduced fixed-frame graph.

The supplied examples, baseline solutions, verifier and default CayleyPy adapter
use the **92-move model**. Do not mix the 184-move file with this benchmark.

### What must be agreed before a competition?

Both representations are proposals for community review, not an approved
CayleyPy competition specification. Before a competition is launched,
organizers should confirm:

- **Allowed generators and their costs:** should every one of the 23 cell
  rotations cost one move, or should a smaller set of elementary turns be used?
- **Treatment of reorientation:** are whole-puzzle rotations, including
  completed gyros, free, or should physical actions carry a cost?
- **The target state:** must a solution restore an exact coordinate frame,
  or is any whole-puzzle orientation of the solved puzzle acceptable?

The existing 184-move model does not by itself count the intermediate physical
actions of a gyro. Such a scoring system would require a separate model.
Technical compatibility with CayleyPy does not imply approval of these choices;
see its [graph contribution guide](https://github.com/cayleypy/cayleypy#how-to-add-a-new-cayley-graph).

## Getting started

Download the repository or clone it:

```bash
git clone https://github.com/Grisha-Pochuev/melinda-4d-cube-graph.git
cd melinda-4d-cube-graph
```

The graph implementation and solution verifier require **Python 3.9+** and no
third-party packages:

```bash
python -m unittest -v
python benchmark.py verify data/sample_submission.csv
```

Apply one move:

```python
from melinda_graph import SOLVED, generators, apply

moves = dict(generators())
name = next(iter(moves))
state = apply(SOLVED, moves[name])
# Neighbors: apply(state, permutation) for each permutation in moves.values().
```

With CayleyPy installed:

```python
from melinda_graph import as_cayleypy
from cayleypy import CayleyGraph

definition = as_cayleypy()
graph = CayleyGraph(definition, device="cpu")
# Use CayleyPy search algorithms with this graph definition.
```

## How to participate

1. Run the tests and baseline verifier above.
2. Use the states in `data/examples.json` and moves in
   `data/puzzle_info.json` to search for shorter solutions.
3. Save your results as a CSV following `data/sample_submission.csv`, then run
   `python benchmark.py verify path/to/your.csv`.
4. Share your result through [Issues](https://github.com/Grisha-Pochuev/melinda-4d-cube-graph/issues)
   or a pull request. Include the total move count, algorithm, runtime, hardware
   and code version, along with your CSV and reproduction instructions.

Improvements to algorithms, tests and explanations are also welcome.
See [CONTRIBUTING.md](CONTRIBUTING.md) for submission details.

## Repository contents

| File | Purpose |
| --- | --- |
| [GRAPH_SPEC.md](GRAPH_SPEC.md) | Formal definitions of vertices, edges and the metric |
| [melinda_graph.py](melinda_graph.py) | Geometric move construction and CayleyPy adapter |
| [data/puzzle_info.json](data/puzzle_info.json) | 92 explicit permutations, solved state and inverse moves |
| [data/framed_puzzle_info.json](data/framed_puzzle_info.json) | Auxiliary fixed-frame model with 184 moves |
| [data/examples.json](data/examples.json) | 24 reachable scrambled states |
| [data/sample_submission.csv](data/sample_submission.csv) | Verified baseline solutions totaling 800 moves |
| [benchmark.py](benchmark.py) | Data generation and solution verification |
| [test_graph.py](test_graph.py) | Geometry, inverse, orientation and invalid-submission checks |
| [check_group_order.py](check_group_order.py) | Independent exact group-order verification with SymPy |
| [check_cayleypy.py](check_cayleypy.py) | Integration check using CayleyPy |
| [VALIDATION.md](VALIDATION.md) | Recorded validation results |
| [AUDIT.md](AUDIT.md) | Review findings, fixes and remaining limitations |

`puzzle_info.json` uses **this repository's portable schema**; it is not presented
as a standard Kaggle upload format. The `as_cayleypy()` function provides the
CayleyPy adapter.

A state is an array of 64 **distinct sticker labels**, not merely eight color
IDs. Permutations follow the gather convention:
`new_state[j] = state[move[j]]`.

The submission CSV has columns `id,moves`, with period-separated move names.
The verifier requires a solution for every example and sums the solution
lengths. Lower totals are better.

The examples are reproducible random walks, not uniform samples of states.
Their scramble lengths of 10, 30 and 60 are known upper bounds, **not proven
minimum distances**. This is a public starting dataset for experiments, not a
hidden test set for an official competition.

GitHub Actions checks are **manual only** to reserve shared runner capacity.
Pushes and pull requests do not launch them. The commands above run locally.

## Verifying the state count

```bash
python -m pip install sympy==1.14.0
python check_group_order.py
```

The Schreier–Sims algorithm checks the order of the generated group without
enumerating every state. For the fixed-corner model, the result matches
Melinda's published count: `16! × 12^16 / (6 × 192)`.
The auxiliary fixed-frame model has 192 times as many states.

## Sources and credits

- **Physical puzzle designer: Melinda Green** —
  [Melinda's 2×2×2×2](https://superliminal.com/cube/2x2x2x2/).
- [Canonical Moves](https://superliminal.com/cube/wiki/Canonical_Moves.html):
  physical moves and reorientations.
- [Physical 2^4 Methods](https://superliminal.com/cube/wiki/Physical_2%5E4_Methods.html):
  explanations of `gyro` and solving methods.
- [CayleyPy](https://github.com/cayleypy/cayleypy): graph-search library.

The graph description and software package were prepared for **Grisha Pochuev's**
initiative with AI assistance. The implementation constructs moves from
coordinates; no physical simulator implementation was copied. The photograph and animation
above are embedded from their original websites.

Repository code is licensed under [Apache-2.0](LICENSE). This license does not
cover the physical puzzle design, its name or third-party materials.
This repository is not affiliated with Melinda Green and does not claim her
endorsement of the proposed metric.
