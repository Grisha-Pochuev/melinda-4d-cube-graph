"""Implicit 2x2x2x2 graph: arbitrary cell turns, free whole-puzzle rotations.

Pure Python, no dependencies. See GRAPH_SPEC.md for the exact metric and its
relationship to Melinda Green's physical puzzle. This is a proposed benchmark
definition, not an assertion of an official CayleyPy competition rule.
"""

from functools import lru_cache
from itertools import permutations, product
from math import factorial, prod

AXES = "xyzw"
CORNERS = tuple(product((-1, 1), repeat=4))
SLOTS = tuple((corner, axis) for corner in CORNERS for axis in range(4))
SLOT_INDEX = {slot: index for index, slot in enumerate(SLOTS)}
SOLVED = tuple(range(64))
REFERENCE = tuple(range(60, 64))  # Four stickers of the (+,+,+,+) corner.
STATE_COUNT = factorial(16) * 12**16 // (6 * 192)
SCHEMA_VERSION = 1
METRIC = "CTM-free-rotations-v1"


def parity(perm):
    """Sign of a permutation in one-line notation."""
    inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return (-1) ** inversions


def proper_rotations(dimension):
    """Signed permutation matrices, represented by (destination axes, signs).

    Input basis vector e_i maps to signs[i] * e_axes[i]. Only determinant +1
    matrices are returned. Order is deterministic and part of export version 1.
    """
    for axes in permutations(range(dimension)):
        for signs in product((-1, 1), repeat=dimension):
            if parity(axes) * prod(signs) == 1:
                yield axes, signs


def inverse(perm):
    """Inverse permutation (also an inverse gather operation)."""
    result = [0] * len(perm)
    for source, target in enumerate(perm):
        result[target] = source
    return tuple(result)


def apply(state, move):
    """CayleyPy gather convention: new_state[j] = state[move[j]]."""
    return tuple(state[source] for source in move)


def _geometric_permutation(axes, signs, cell=None):
    """Convert a geometric source-to-destination map into a gather array."""
    destination = []
    for corner, sticker_axis in SLOTS:
        if cell is not None and corner[cell[0]] != cell[1]:
            destination.append(SLOT_INDEX[(corner, sticker_axis)])
            continue
        new_corner = [0] * 4
        for axis in range(4):
            new_corner[axes[axis]] = signs[axis] * corner[axis]
        destination.append(SLOT_INDEX[(tuple(new_corner), axes[sticker_axis])])
    return inverse(destination)


@lru_cache(maxsize=2)
def generators(fixed_corner=True):
    """Return (name, gather permutation) pairs, 92 fixed or 184 framed moves.

    Fixed-corner mode retains all 64 slots but fixes slots 60..63. The framed
    mode is an auxiliary representation; its identity-only distance differs
    from distance modulo free rigid rotations.
    """
    moves = []
    local_rotations = tuple(proper_rotations(3))
    for axis in range(4):
        tangent_axes = tuple(a for a in range(4) if a != axis)
        for side in ((-1,) if fixed_corner else (-1, 1)):
            for local_axes, local_signs in local_rotations:
                if local_axes == (0, 1, 2) and local_signs == (1, 1, 1):
                    continue
                axes, signs = list(range(4)), [1] * 4
                for index, tangent in enumerate(tangent_axes):
                    axes[tangent] = tangent_axes[local_axes[index]]
                    signs[tangent] = local_signs[index]
                # Example: xn_+y_-w_+z maps y->y, z->-w, w->z on x=-1.
                name = AXES[axis] + ("n" if side == -1 else "p")
                name += "_" + "_".join(
                    ("+" if signs[a] > 0 else "-") + AXES[axes[a]] for a in tangent_axes
                )
                moves.append((name, _geometric_permutation(axes, signs, (axis, side))))
    return tuple(moves)


@lru_cache(maxsize=1)
def rigid_rotations():
    """All 192 proper tesseract rotations as gather permutations."""
    return tuple(_geometric_permutation(axes, signs) for axes, signs in proper_rotations(4))


def normalize(state):
    """Return the unique representative with reference stickers in slots 60..63.

    Accepts a permutation of unique sticker IDs, not a color array. The check
    verifies the reference corner and its handedness, not full reachability.
    States for search should be produced by legal moves from SOLVED.
    """
    if len(state) != 64 or sorted(state) != list(SOLVED):
        raise ValueError("State must be a permutation of sticker IDs 0..63")
    for rotation in rigid_rotations():
        if all(state[rotation[index]] == index for index in REFERENCE):
            return apply(state, rotation)
    raise ValueError("Reference corner is split or has an impossible reflected orientation")


def graph_spec(fixed_corner=True):
    """Portable, explicit JSON-ready graph definition; no vertex enumeration."""
    moves = generators(fixed_corner)
    by_permutation = {permutation: name for name, permutation in moves}
    return {
        "schema_version": SCHEMA_VERSION,
        "name": "melinda-2222-" + ("fixed-ctm" if fixed_corner else "framed-ctm"),
        "status": "community proposal; not an official competition",
        "metric": METRIC if fixed_corner else "CTM-fixed-frame-v1",
        "state_size": 64,
        "state_encoding": "unique sticker IDs; corner-major, axis-minor",
        "permutation_convention": "new_state[j] = state[move[j]]",
        "solved_state": list(SOLVED),
        "fixed_sticker_indices": list(REFERENCE) if fixed_corner else [],
        "vertex_count": str(STATE_COUNT * (1 if fixed_corner else 192)),
        "number_of_generators": len(moves),
        "move_cost": 1,
        "moves": {name: list(perm) for name, perm in moves},
        "inverse_moves": {name: by_permutation[inverse(perm)] for name, perm in moves},
        "slots": [
            {"id": index, "corner": list(corner), "sticker_axis": AXES[axis],
             "solved_color": AXES[axis] + ("-" if corner[axis] == -1 else "+")}
            for index, (corner, axis) in enumerate(SLOTS)
        ],
    }


def as_cayleypy(fixed_corner=True):
    """Create CayleyGraphDef; import CayleyPy only when requested."""
    from cayleypy import CayleyGraphDef

    spec = graph_spec(fixed_corner)
    return CayleyGraphDef.create(
        generators=list(spec["moves"].values()),
        generator_names=list(spec["moves"]),
        central_state=spec["solved_state"],
        name=spec["name"],
    )
