# Repository review — 2026-11-01

Reviewed starting revision: `6b3e0b0763109f6b50fb2f7d322a7ce6592b6fa7`.
The review and checks were performed locally with AI assistance; this is not
an independent external peer review or approval by the puzzle designer.

## Findings and fixes

No critical error was found in the coordinate construction, the exported move
permutations, or the stated fixed-corner reduction under the proposed metric.
The underlying generators, example states and baseline solutions are unchanged.

- **Documentation:** CONTRIBUTING.md incorrectly said that the examples contain
  scramble sequences. They contain starting states; scrambles are reproducible
  through the exporter, and inverse baseline solutions are supplied separately.
  The description now says this explicitly.
- **Regression coverage:** the previous tests checked that two fresh exports
  match each other, but did not compare every checked-in example file against a
  fresh export. Added a byte-for-byte comparison for all four published files.
- **Reduction coverage:** added normalized-neighborhood checks starting from
  unrestricted full-model random walks, and an exhaustive 192-element orbit
  check for the ordered reference corner. Earlier neighborhood tests started
  only from fixed-corner states.
- **Input coverage:** added malformed CSV row, unknown-ID, reordered-header and
  valid zero-move solution cases. The existing verifier handled these correctly;
  no change to its acceptance rules was needed.
- **Automation:** removed push and pull-request triggers at the owner's request.
  The workflow is manual only, with a 15-minute job limit. This edit does not
  cancel jobs already queued under older workflow revisions.

## Local verification

| Check | Result |
| --- | --- |
| Unit tests after changes | 15 passed |
| All four published data files regenerated | Byte-for-byte identical |
| Baseline verifier | 24 solved examples, total 800 moves |
| SymPy 1.14.0 Schreier–Sims | Both exact graph orders and corner permutation orders matched |
| Reference-corner orbit | Exactly 192 ordered images, matching rigid-rotation images |
| Actual CayleyPy integration on CPU | BFS layers `[1, 92, 6150]` |

CayleyPy was tested at upstream revision
`3cd11ecefc98e54d6fc0ccdec967d0bcc8ca4a93`, with Python 3.12 and CPU PyTorch.
The proposed minimum Python version of 3.9 was not separately executed here.

The independently computed group orders satisfy `|G| / |H| = 192`. The orbit
check gives 192 possible ordered images of the reference corner under `G`.
Since `H` fixes that corner, orbit–stabilizer confirms that `H` is the full
pointwise stabilizer, rather than a smaller subgroup that misses states.
This supports the geometric distance-preservation argument in GRAPH_SPEC.md;
group orders alone do not prove distance preservation.

## Interpretation and limits

The physical [canonical move description](https://superliminal.com/cube/wiki/Canonical_Moves.html)
permits arbitrary rotations of the two exposed cubic cells and describes gyros
as reorientations that expose other cells. Extending arbitrary cell turns to
all eight cells at unit cost assumes free reorientation. This is a proposed
search metric, not a physical snap count or an approved competition rule.

The 184-move framed graph has an exact-frame goal. Its distances must not be
interchanged with the 92-move free-reorientation distances without applying the
normalization and goal convention. Both remain clearly separated in the data.

The examples are public, non-uniform and accompanied by valid baseline paths.
No optimality, representative difficulty, graph diameter, hand-move translator,
or acceptance by CayleyPy organizers was established by this audit.
GitHub-hosted execution was not used as evidence; checks were run locally.
