"""Generate reproducible examples and verify submitted paths without dependencies."""

import argparse
import csv
import json
from pathlib import Path
from random import Random

from melinda_graph import METRIC, SOLVED, apply, graph_spec

ROOT = Path(__file__).resolve().parent


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export(directory):
    """Write generators and a public, non-uniform sample benchmark."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    spec = graph_spec()
    write_json(directory / "puzzle_info.json", spec)
    write_json(directory / "framed_puzzle_info.json", graph_spec(False))
    moves = spec["moves"]
    rng = Random(20261101)
    cases, submissions = [], []
    for length in (10, 30, 60):
        for _ in range(8):
            state, word = SOLVED, []
            for _ in range(length):
                # Adjacent moves on the same cell collapse to at most one move.
                choices = [name for name in moves if not word or name[:2] != word[-1][:2]]
                name = rng.choice(choices)
                word.append(name)
                state = apply(state, moves[name])
            case_id = str(len(cases))
            cases.append({"id": case_id, "initial_state": list(state), "known_upper_bound": length})
            solution = [spec["inverse_moves"][name] for name in reversed(word)]
            submissions.append({"id": case_id, "moves": ".".join(solution)})
    write_json(directory / "examples.json", {
        "metric": METRIC,
        "seed": 20261101,
        "sampling": "non-uniform legal random walks; lengths are upper bounds, not distances",
        "cases": cases,
    })
    with (directory / "sample_submission.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "moves"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(submissions)
    print(f"Exported {len(moves)} generators and {len(cases)} example cases to {directory}")


def verify(examples_path, submission_path):
    """Validate every solution; return total move count or raise ValueError."""
    examples = json.loads(Path(examples_path).read_text(encoding="utf-8"))
    if examples["metric"] != METRIC:
        raise ValueError("Metric mismatch")
    cases = {item["id"]: item for item in examples["cases"]}
    if len(cases) != len(examples["cases"]):
        raise ValueError("Duplicate example IDs")
    moves = graph_spec()["moves"]
    seen, total = set(), 0
    with Path(submission_path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["id", "moves"]:
            raise ValueError("Submission header must be exactly id,moves")
        for row in reader:
            case_id = row["id"]
            if case_id in seen or case_id not in cases:
                raise ValueError(f"Duplicate or unknown case ID: {case_id}")
            if None in row or row["moves"] is None:
                raise ValueError(f"Malformed CSV row for {case_id}")
            seen.add(case_id)
            state = tuple(cases[case_id]["initial_state"])
            if len(state) != 64 or sorted(state) != list(SOLVED) or state[60:] != SOLVED[60:]:
                raise ValueError(f"Malformed fixed-corner state: {case_id}")
            word = row["moves"].split(".") if row["moves"] else []
            for name in word:
                if name not in moves:
                    raise ValueError(f"Unknown move for {case_id}: {name}")
                state = apply(state, moves[name])
            if state != SOLVED:
                raise ValueError(f"Case {case_id} is not solved")
            total += len(word)
    if seen != set(cases):
        raise ValueError("Submission is missing example IDs")
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("export")
    generate.add_argument("--output", type=Path, default=ROOT / "data")
    check = sub.add_parser("verify")
    check.add_argument("submission", type=Path)
    check.add_argument("--examples", type=Path, default=ROOT / "data/examples.json")
    args = parser.parse_args()
    if args.command == "export":
        export(args.output)
    else:
        try:
            score = verify(args.examples, args.submission)
        except (ValueError, KeyError, TypeError) as error:
            parser.exit(1, f"INVALID: {error}\n")
        print(f"VALID: total_moves={score} (smaller is better)")


if __name__ == "__main__":
    main()
