# Contributing and sharing solutions

This is an open proposal for graph search on Melinda Green's physical 2×2×2×2
puzzle. It is not an official contest announcement. The current move metric is
`CTM-free-rotations-v1`; see [GRAPH_SPEC.md](GRAPH_SPEC.md) for its exact meaning.

## Run the baseline

```bash
git clone https://github.com/Grisha-Pochuev/melinda-4d-cube-graph.git
cd melinda-4d-cube-graph
python -m unittest -v
python benchmark.py verify data/sample_submission.csv
```

Python 3.9+ is sufficient; these commands need no additional packages.
The baseline solves all 24 examples in 800 moves. A lower total is better;
800 is not a proven optimum. The starting states and baseline solutions are
public, and the scrambles can be reproduced with `python benchmark.py export`.
This is a reproducible starting benchmark, not a hidden test set.

## Produce a candidate

Read the 92 move permutations in `data/puzzle_info.json` and the starting states
in `data/examples.json`. Move application is `new_state[j] = state[move[j]]`.
Keep sticker IDs distinct; do not replace them with color IDs.

Create a CSV with exactly the columns `id,moves`, one row for every example.
Separate move names with periods, as in `data/sample_submission.csv`.
Check your candidate with:

```bash
python benchmark.py verify results/my_submission.csv
```

## Share a reproducible result

Open an [issue](https://github.com/Grisha-Pochuev/melinda-4d-cube-graph/issues)
with your CSV (or a public link), or submit a pull request adding it under
`results/` together with a short explanation. Include:

- The repository commit and metric version used.
- The verifier output and total move count.
- Your algorithm, parameters and random seeds.
- Runtime, hardware and relevant dependency versions.
- Commands or code sufficient to reproduce your result.

A valid solution establishes an upper bound. Claim optimality only with a
separate proof or exhaustive search certificate. Different metrics or example
sets must be reported separately; their totals are not directly comparable.

## Improve the project

Documentation fixes, solver implementations and additional validation are
welcome. Run the unit tests and baseline verifier before submitting code.
Discuss changes to generators, state encoding or move costs in an issue first,
because they change the problem being solved. Contributions use this
repository's [Apache-2.0 license](LICENSE). Credit Melinda Green for the original
physical puzzle; this project does not claim her endorsement.
