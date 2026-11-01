"""Geometry, quotient, serialization and invalid-submission regression tests."""

from collections import Counter, deque
import csv
import json
from pathlib import Path
from random import Random
import tempfile
import unittest

import melinda_graph as graph
from benchmark import export, verify


class GraphTests(unittest.TestCase):
    def test_generator_structure(self):
        for fixed, count in ((True, 92), (False, 184)):
            moves = graph.generators(fixed)
            self.assertEqual(len(moves), count)
            self.assertEqual(len(dict(moves)), count)
            self.assertEqual(len({p for _, p in moves}), count)
            for _, perm in moves:
                self.assertEqual(sorted(perm), list(graph.SOLVED))
                self.assertNotEqual(perm, graph.SOLVED)
                self.assertEqual(graph.apply(perm, graph.inverse(perm)), graph.SOLVED)
                if fixed:
                    self.assertEqual(perm[60:], graph.REFERENCE)

    def test_cell_rotation_orders(self):
        # Cube rotation group: 9 half turns, 8 third turns, 6 quarter turns.
        counts = Counter()
        for _, perm in graph.generators():
            current = graph.SOLVED
            for order in range(1, 5):
                current = graph.apply(current, perm)
                if current == graph.SOLVED:
                    counts[order] += 1
                    break
            else:
                self.fail("Unexpected generator order")
        self.assertEqual(counts, {2: 36, 3: 32, 4: 24})

    def test_corner_integrity_and_parity(self):
        for _, perm in graph.generators(False):
            destination = graph.inverse(perm)
            corner_permutation = []
            for corner in range(16):
                slots = destination[4 * corner:4 * corner + 4]
                self.assertEqual(len({slot // 4 for slot in slots}), 1)
                self.assertEqual({slot % 4 for slot in slots}, set(range(4)))
                corner_permutation.append(slots[0] // 4)
            self.assertEqual(graph.parity(corner_permutation), 1)

    def test_named_quarter_turn_against_coordinates(self):
        # x=-1, y->y, z->-w, w->z; source corner (-,-,-,-) goes to (-,-,-,+).
        move = dict(graph.generators())["xn_+y_-w_+z"]
        destination = graph.inverse(move)
        self.assertEqual(destination[:4], (4, 5, 7, 6))
        self.assertEqual(destination[60:], graph.REFERENCE)

    def test_rigid_rotations(self):
        rotations = graph.rigid_rotations()
        self.assertEqual(len(set(rotations)), 192)
        for rotation in rotations:
            self.assertEqual(graph.normalize(rotation), graph.SOLVED)

    def test_reference_corner_orbit(self):
        # Enumerate only the ordered reference-corner orbit, not all states.
        moves = [graph.inverse(p) for _, p in graph.generators(False)]
        seen = {graph.REFERENCE}
        pending = deque([graph.REFERENCE])
        while pending:
            corner = pending.popleft()
            for move in moves:
                image = tuple(move[index] for index in corner)
                if image not in seen:
                    seen.add(image)
                    pending.append(image)
        rigid_images = {tuple(graph.inverse(p)[i] for i in graph.REFERENCE)
                        for p in graph.rigid_rotations()}
        self.assertEqual(len(seen), 192)
        self.assertEqual(seen, rigid_images)

    def test_quotient_neighbors_and_rotation_invariance(self):
        rng = Random(4)
        fixed = graph.generators()
        full = graph.generators(False)
        state = graph.SOLVED
        for _ in range(5):
            for _ in range(12):
                state = graph.apply(state, rng.choice(fixed)[1])
            neighbors = {graph.apply(state, p) for _, p in fixed}
            normalized = {graph.normalize(graph.apply(state, p)) for _, p in full}
            self.assertEqual(normalized, neighbors)
            self.assertEqual(len(neighbors), 92)
            for rotation in graph.rigid_rotations():
                self.assertEqual(graph.normalize(graph.apply(state, rotation)), state)

    def test_normalize_rejects_invalid_reference(self):
        for bad in ([0] * 64, list(range(63))):
            with self.assertRaises(ValueError):
                graph.normalize(bad)
        bad = list(graph.SOLVED)
        bad[60], bad[61] = bad[61], bad[60]  # Reflected corner.
        with self.assertRaises(ValueError):
            graph.normalize(bad)

    def test_inverse_words(self):
        rng = Random(123)
        moves = graph.generators()
        word = [rng.choice(moves)[1] for _ in range(300)]
        state = graph.SOLVED
        for perm in word:
            state = graph.apply(state, perm)
        for perm in reversed(word):
            state = graph.apply(state, graph.inverse(perm))
        self.assertEqual(state, graph.SOLVED)

    def test_export_reproducibility_and_baseline(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            export(first)
            export(second)
            for filename in ("puzzle_info.json", "framed_puzzle_info.json", "examples.json", "sample_submission.csv"):
                self.assertEqual((Path(first) / filename).read_bytes(), (Path(second) / filename).read_bytes())
            self.assertEqual(verify(Path(first) / "examples.json", Path(first) / "sample_submission.csv"), 800)
            spec = json.loads((Path(first) / "puzzle_info.json").read_text())
            self.assertEqual(spec, graph.graph_spec())

    def test_checked_in_data_matches_code(self):
        data = Path(__file__).resolve().parent / "data"
        self.assertEqual(json.loads((data / "puzzle_info.json").read_text()), graph.graph_spec())
        self.assertEqual(json.loads((data / "framed_puzzle_info.json").read_text()), graph.graph_spec(False))
        self.assertEqual(verify(data / "examples.json", data / "sample_submission.csv"), 800)

    def test_all_published_data_reproduces_byte_for_byte(self):
        data = Path(__file__).resolve().parent / "data"
        with tempfile.TemporaryDirectory() as directory:
            export(directory)
            for path in data.iterdir():
                if path.is_file():
                    self.assertEqual(path.read_bytes(), (Path(directory) / path.name).read_bytes(), path.name)

    def test_normalized_neighbors_from_unfixed_states(self):
        rng = Random(2026)
        full = graph.generators(False)
        state = graph.SOLVED
        for _ in range(10):
            for _ in range(20):
                state = graph.apply(state, rng.choice(full)[1])
            normalized = graph.normalize(state)
            expected = {graph.apply(normalized, p) for _, p in graph.generators()}
            actual = {graph.normalize(graph.apply(state, p)) for _, p in full}
            self.assertEqual(actual, expected)

    def test_csv_shape_empty_solution_and_unknown_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            examples = directory / "examples.json"
            submission = directory / "submission.csv"
            examples.write_text(json.dumps({"metric": graph.METRIC, "cases": [
                {"id": "0", "initial_state": list(graph.SOLVED)}
            ]}), encoding="utf-8")
            submission.write_text("id,moves\n0,\n", encoding="utf-8")
            self.assertEqual(verify(examples, submission), 0)
            for text in ("id,moves\n0\n", "id,moves\n0,,extra\n",
                         "id,moves\n1,\n", "moves,id\n,0\n"):
                submission.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    verify(examples, submission)

    def test_rejects_bad_submissions(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            export(directory)
            submission = directory / "sample_submission.csv"
            with submission.open(newline="") as stream:
                original = list(csv.DictReader(stream))
            variants = [original[:-1], original + [original[0]]]
            for replacement in ("invalid_move", "", original[0]["moves"].split(".")[0]):
                variants.append([dict(original[0], moves=replacement)] + original[1:])
            for rows in variants:
                with submission.open("w", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=["id", "moves"])
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaises(ValueError):
                    verify(directory / "examples.json", submission)


if __name__ == "__main__":
    unittest.main()
