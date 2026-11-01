# Validation record — 2026-11-01

The follow-up [repository audit](AUDIT.md) reran these checks and expanded the
unit suite to **15 passing tests**. The table below records the original run.

Executed locally before the initial publication:

| Check | Result |
| --- | --- |
| `python -m unittest -v` | 11 tests passed |
| `python benchmark.py verify data/sample_submission.csv` | All 24 examples solved; 800 total moves |
| `python check_group_order.py` with SymPy 1.14.0 | Both exact orders matched |
| `python check_cayleypy.py` | Passed on CPU; BFS layers `[1, 92, 6150]` |

The CayleyPy integration used the actual upstream repository at commit
`3cd11ecefc98e54d6fc0ccdec967d0bcc8ca4a93`, Python 3.12 and CPU PyTorch.
No substitute for `CayleyGraphDef` or `CayleyGraph` was used. The second BFS
layer was also computed independently by ordinary Python sets.

Exact group orders computed using Schreier-Sims:

- Fixed oriented corner: `3357894533384932272635904000`.
- Fixed coordinate frame: `644715750409906996346093568000`.
- Induced corner permutation orders: `15!/2 = 653837184000` and
  `16!/2 = 10461394944000`, respectively.

These checks establish properties of the implemented graph and consistency
with the published state count. They do not establish optimality of the sample
solutions, physical ergonomics, a graph diameter, or community approval of the
chosen free-reorientation metric. The physical move interpretation and the
fixed-corner equivalence are explained in `GRAPH_SPEC.md`.
