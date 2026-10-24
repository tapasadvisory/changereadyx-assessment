#!/usr/bin/env python3
"""CHANGEReadyX(TM) Readiness Assessment scorer.

Reads an answers JSON file ({question_id: 1..5}), scores each of the 10
readiness dimensions on a 0-100 scale, computes an overall readiness index,
assigns a readiness band, flags the three lowest-scoring dimensions, and
writes a Markdown report to stdout (or to the path given with --out).

Python 3 standard library only. No dependencies.

Usage:
    python3 tools/score.py examples/sample-answers.json
    python3 tools/score.py examples/sample-answers.json --out report.md
    python3 tools/score.py answers.json --questions assessment/questions.json
"""

import argparse
import json
import sys
from pathlib import Path

BANDS = [
    (80, "Commanding", "Readiness is a strength. Protect it: keep measuring adoption "
                        "after go-live and hold leaders to the evidence cadence."),
    (60, "Ready", "The foundations are in place. Close the flagged gaps before "
                  "scale-up, and keep readiness evidence in front of governance."),
    (40, "Emerging", "Readiness is partial. Committing to full milestones now carries "
                     "real adoption risk — intervene on the flagged dimensions first."),
    (0, "Exposed", "Readiness is not yet sufficient for the commitment being made. "
                   "Diagnose before you invest further: pause, build readiness, "
                   "then re-assess."),
]


def load_questions(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    questions = []
    for dim in data["dimensions"]:
        for q in dim["questions"]:
            questions.append((q["id"], dim["id"], dim["name"], q["text"]))
    return data, questions


def band_for(score):
    for threshold, name, guidance in BANDS:
        if score >= threshold:
            return name, guidance
    raise AssertionError("unreachable")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Score a CHANGEReadyX(TM) readiness assessment.")
    parser.add_argument("answers", help="Path to answers JSON ({question_id: 1..5})")
    parser.add_argument("--questions",
                        default=str(Path(__file__).resolve().parent.parent
                                    / "assessment" / "questions.json"),
                        help="Path to questions JSON (default: assessment/questions.json)")
    parser.add_argument("--out", help="Write the report to this path instead of stdout")
    args = parser.parse_args(argv)

    _, questions = load_questions(args.questions)

    try:
        with open(args.answers, encoding="utf-8") as fh:
            answers = json.load(fh)
    except FileNotFoundError:
        print(f"error: answers file not found: {args.answers}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: answers file is not valid JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(answers, dict):
        print("error: answers JSON must be an object of {question_id: score}",
              file=sys.stderr)
        return 2

    expected = {qid for qid, _, _, _ in questions}
    provided = set(answers)
    missing = sorted(expected - provided)
    unknown = sorted(provided - expected)
    if unknown:
        print(f"error: unknown question id(s) in answers: {', '.join(unknown)}",
              file=sys.stderr)
        return 2
    if missing:
        print(f"error: {len(missing)} question(s) unanswered: {', '.join(missing)}",
              file=sys.stderr)
        print("Every question needs a 1-5 score. An unanswered question is not a "
              "zero — it is unknown readiness, and unknown readiness is exactly what "
              "this instrument exists to remove.", file=sys.stderr)
        return 2

    for qid, value in answers.items():
        if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
            print(f"error: score for {qid} must be an integer from 1 to 5 "
                  f"(got {value!r})", file=sys.stderr)
            return 2

    # Per-dimension mean of 1..5 Likert scores, rescaled to 0..100.
    dim_scores = {}
    dim_order = []
    for qid, dim_id, dim_name, _ in questions:
        if dim_id not in dim_scores:
            dim_scores[dim_id] = {"name": dim_name, "values": []}
            dim_order.append(dim_id)
        dim_scores[dim_id]["values"].append(answers[qid])

    results = []
    for dim_id in dim_order:
        values = dim_scores[dim_id]["values"]
        mean = sum(values) / len(values)
        results.append((dim_scores[dim_id]["name"], (mean - 1) / 4 * 100))

    overall = sum(score for _, score in results) / len(results)
    band, guidance = band_for(overall)
    lowest = sorted(results, key=lambda r: r[1])[:3]
    strongest = max(results, key=lambda r: r[1])

    lines = []
    lines.append("# CHANGEReadyX™ Readiness Assessment — Report")
    lines.append("")
    lines.append(f"**Overall readiness index: {overall:.1f} / 100 — {band}**")
    lines.append("")
    lines.append(guidance)
    lines.append("")
    lines.append("## Dimension scores (0–100)")
    lines.append("")
    lines.append("| Dimension | Score |")
    lines.append("| --- | ---: |")
    for name, score in results:
        lines.append(f"| {name} | {score:.1f} |")
    lines.append("")
    lines.append("## Where to intervene first")
    lines.append("")
    lines.append("The three lowest-scoring dimensions. Adoption fails at the weakest "
                 "point of the system, not the average — work these before scaling "
                 "commitment:")
    lines.append("")
    for name, score in lowest:
        lines.append(f"- **{name}** — {score:.1f}")
    lines.append("")
    lines.append(f"Strongest dimension: **{strongest[0]}** ({strongest[1]:.1f}). "
                 "Use it — a strength in one dimension is the lever for lifting the "
                 "ones below it.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Scores are self-reported on a 1–5 evidence scale and rescaled to "
                 "0–100 per dimension; the overall index is the mean of the ten "
                 "dimensions. This is an evidence-based diagnostic, not a validated "
                 "psychometric instrument — treat the pattern of scores as the "
                 "starting point for a readiness conversation, not a verdict. "
                 "See docs/method.md.")
    lines.append("")
    lines.append("CHANGEReadyX™ is a trademark of TAPAS Advisory. "
                 "Diagnostic: https://tapasadvisory.com/diagnostic")
    lines.append("")

    report = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Report written to {args.out} "
              f"(overall {overall:.1f}/100 — {band})")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
