"""Independent exact group-order calculation using SymPy's Schreier-Sims.

Install the optional dependency: python -m pip install sympy==1.14.0
This computes a stabilizer chain, not a list of all group elements.
"""

import json
from math import factorial

from sympy.combinatorics import Permutation, PermutationGroup

from melinda_graph import STATE_COUNT, generators


def main():
    results = {}
    for fixed in (True, False):
        group = PermutationGroup([Permutation(list(perm)) for _, perm in generators(fixed)])
        order = int(group.order())
        expected = STATE_COUNT * (1 if fixed else 192)
        if order != expected:
            raise AssertionError((order, expected))
        corner_group = PermutationGroup([
            Permutation([perm[4 * corner] // 4 for corner in range(16)])
            for _, perm in generators(fixed)
        ])
        corner_order = int(corner_group.order())
        assert corner_order == factorial(15 if fixed else 16) // 2
        results["fixed" if fixed else "framed"] = {
            "generators": len(generators(fixed)),
            "order": str(order),
            "corner_permutation_order": str(corner_order),
            "matches_published_count": True,
        }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
