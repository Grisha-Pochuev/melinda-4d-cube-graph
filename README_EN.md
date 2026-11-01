# Melinda's 2×2×2×2 — an implicit graph for short-solution search

[Русский README](README.md) · [Formal specification](GRAPH_SPEC.md)
· [Melinda Green's original puzzle page](https://superliminal.com/cube/2x2x2x2/)

## Photograph and demonstrations

[![Ernő Rubik examining Melinda Green's physical 2×2×2×2 puzzle](https://superliminal.com/cube/2x2x2x2/erno2x2x2x2g4g13.jpg)](https://superliminal.com/cube/2x2x2x2/)

*Ernő Rubik examining the puzzle at Gathering for Gardner 13.
Photo from [Melinda Green's website](https://superliminal.com/cube/2x2x2x2/),
displayed from its original URL; image rights remain with the rights holder.*

- [Introduction and demonstration](https://www.youtube.com/watch?v=_1ZPQV-ejtA): the main video linked by the puzzle's author.
- [Canonical Moves](https://www.youtube.com/watch?v=DzRH8BOJL8Q): permitted physical manipulations.
- [Physical puzzle alongside its virtual 4D counterpart](https://www.youtube.com/watch?v=k6ZSu0xOPbQ): Marc Ringuette's side-by-side demonstration.

These videos illustrate physical manipulations. The search metric used here is
defined separately in [GRAPH_SPEC.md](GRAPH_SPEC.md).

Melinda Green created a physical realization of the four-dimensional analogue
of the 2×2×2 Rubik's cube. Her site describes it as the first physical 3D
embodiment of a 4D twisty puzzle; its earliest listed solutions date to 2017.
The magnetic construction represents a tesseract puzzle with eight cubic cells
and sixteen four-colored corner pieces. A completed `gyro` changes its 4D
orientation, making other cells accessible.

This repository supplies a small, executable graph definition so the CayleyPy
community can search for short solutions without enumerating the enormous state
space. It is a **community proposal**, not an official competition or a claim of
endorsement by Melinda Green or CayleyPy.

The proposed metric counts any nonidentity proper rotation of one cell as one
move, with whole-puzzle rotations (including completed gyros) free. Fixing one
oriented corner removes rigid rotations and leaves 92 generators on 64 sticker
slots. Its exact group order is
`16! * 12**16 / (6 * 192) = 3357894533384932272635904000`, matching the puzzle's
published rotation-reduced state count. The fixed-corner reduction preserves
distances in this metric. It does not measure physical snaps, regrips or time.

See [CONTRIBUTING.md](CONTRIBUTING.md) to submit solutions, reproduce results,
or discuss the move metric.

Python 3.9+; the core needs no dependencies:

```bash
python -m unittest -v
python benchmark.py verify data/sample_submission.csv
```

The supplied 24 public scrambles have valid baseline solutions totaling 800
moves. They are reproducible, non-uniform random walks of lengths 10, 30 and 60;
these lengths are upper bounds, not optimal distances. Return CSV columns
`id,moves`, using dot-separated move names. All cases must be solved exactly.

`data/puzzle_info.json` contains explicit gather permutations:
`new_state[j] = state[move[j]]`. This is this repository's JSON schema, not an
assertion of a Kaggle standard. The graph adapter uses CayleyPy's public API:

```python
from melinda_graph import as_cayleypy
from cayleypy import CayleyGraph
graph = CayleyGraph(as_cayleypy(), device="cpu")
```

To regenerate data: `python benchmark.py export`. To verify the group order
independently, install `sympy==1.14.0` and run `python check_group_order.py`.
See [GRAPH_SPEC.md](GRAPH_SPEC.md) for coordinates, indexing, the normalization
proof, physical interpretation and limitations.

Puzzle design: **Melinda Green**. Graph package prepared for **Grisha Pochuev**
with AI assistance. Original coordinate-based implementation, Apache-2.0 licensed;
the license does not cover the physical design or third-party materials.
The photo above is embedded from its original website. No simulator implementation has been copied.
