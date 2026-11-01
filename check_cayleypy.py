"""Optional integration check; requires an installed CayleyPy and its dependencies."""

from cayleypy import CayleyGraph

from melinda_graph import SOLVED, apply, as_cayleypy, generators


def main():
    definition = as_cayleypy()
    assert definition.state_size == 64
    assert definition.n_generators == 92
    assert definition.generators_inverse_closed
    assert definition.central_state == list(SOLVED)
    moves = [perm for _, perm in generators()]
    first = {apply(SOLVED, perm) for perm in moves}
    second = {apply(state, perm) for state in first for perm in moves}
    expected = [1, len(first), len(second - first - {SOLVED})]
    actual = CayleyGraph(definition, device="cpu").bfs(max_diameter=2).layer_sizes
    assert list(actual) == expected == [1, 92, 6150]
    print("CayleyPy integration passed; BFS layers:", list(actual))


if __name__ == "__main__":
    main()
