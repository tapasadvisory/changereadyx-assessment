# CHANGEReadyX™ Assessment Toolkit

An open-source, evidence-based change-readiness diagnostic for ERP and AI
transformation programmes — the assessment instrument from the
[CHANGEReadyX™](https://tapasadvisory.com/changereadyx) framework by
[TAPAS Advisory](https://tapasadvisory.com).

Most transformations don't fail at go-live. They fail at adoption — because the
organisation was never diagnosed for readiness before the milestones were set.
This toolkit gives programme leaders, change practitioners and GCC/transformation
heads a fast, structured way to measure readiness across the ten dimensions that
decide whether a change actually holds.

## What it does

- **30 questions, 10 dimensions**, answered on a 1–5 evidence scale
  (1 = not in place, no evidence · 5 = embedded, practised and reviewed).
- Scores each dimension on a **0–100** scale and computes an **overall
  readiness index**.
- Assigns a **readiness band** — Exposed, Emerging, Ready or Commanding — with
  plain-language guidance for each.
- Flags the **three lowest dimensions**: where adoption will break first, and
  where to intervene before scaling commitment.
- Emits a clean **Markdown report** you can paste into a steering pack.

## The 10 dimensions

1. **Leadership Alignment** — one story, told the same way, by every leader.
2. **Sponsorship & Governance** — a sponsor who decides, and governance that
   reviews readiness evidence, not just dates.
3. **Stakeholder Readiness** — every affected group mapped, including the ones
   planning to work around the change.
4. **Capability & Skills** — role-by-role diagnosis of what people can do today
   versus what the new way of working requires.
5. **Process Readiness** — future-state processes documented, exceptions
   decided, high-volume flows rehearsed.
6. **Technology Adoption Readiness** — real users practised, legacy tools
   retired, usage visible from system data.
7. **Communication & Engagement** — specific to each audience, two-way, and
   sequenced around need rather than the reporting calendar.
8. **Manager Enablement** — managers equipped before their teams, with routines
   to reinforce the new way of working.
9. **Measurement & Feedback** — adoption metrics defined before go-live and
   reviewed on a cadence, with a funded path to act on them.
10. **Culture & Conviction** — people believe the change improves their work,
    and can say so — or safely say it isn't working.

## Quickstart

Python 3, standard library only. No installation, no dependencies.

```bash
git clone <this-repo> changereadyx-assessment
cd changereadyx-assessment

# Score the bundled example
python3 tools/score.py examples/sample-answers.json

# Score your own answers, writing the report to a file
python3 tools/score.py my-answers.json --out my-report.md
```

Your answers file is a single JSON object mapping each question ID to a score
from 1 to 5:

```json
{ "LA1": 4, "LA2": 3, "LA3": 3, "SG1": 4, "...": 0 }
```

Every question must be answered. An unanswered question is not a zero — it is
unknown readiness, and unknown readiness is exactly what this instrument exists
to remove. The scorer stops with a clear error listing anything missing or out
of range.

## How scoring works

- Each dimension's score is the mean of its three question scores, rescaled
  from the 1–5 scale to 0–100: `(mean − 1) / 4 × 100`.
- The **overall readiness index** is the mean of the ten dimension scores.
- Bands: **0–39 Exposed** · **40–59 Emerging** · **60–79 Ready** ·
  **80–100 Commanding**.

Read the *pattern*, not just the headline number. A programme scoring 75 on
process readiness and 30 on manager enablement will not average its way to
adoption — it will fail at the weakest point. The report's "Where to intervene
first" section exists for exactly that reason.

## Sample output

From `examples/sample-answers.json` (full report:
[`examples/sample-report.md`](examples/sample-report.md)):

```text
# CHANGEReadyX™ Readiness Assessment — Report

**Overall readiness index: 37.5 / 100 — Exposed**

## Where to intervene first

- **Technology Adoption Readiness** — 16.7
- **Manager Enablement** — 16.7
- **Stakeholder Readiness** — 33.3
```

A familiar pattern: leadership and process work look respectable, while manager
enablement and adoption visibility lag — the classic signature of a programme
that will hit its go-live date and miss its business case.

## The method

The instrument follows the CHANGEReadyX™ discipline: **readiness before
milestones**, **role-based diagnosis** rather than whole-population averages,
and **adoption-to-value measurement** after go-live. See
[`docs/method.md`](docs/method.md) for the full method and an honest statement
of limitations: this is a self-report, evidence-based diagnostic — a starting
point for a readiness conversation, not a validated psychometric instrument and
not a verdict.

## Repository layout

```text
assessment/questions.json   The instrument: 10 dimensions × 3 questions
tools/score.py              The scorer (Python 3, stdlib only)
examples/                   Sample answers + the report they generate
docs/method.md              Method, scoring detail and limitations
```

## Roadmap

- Answer-set comparison (baseline vs. re-assessment deltas)
- Role-segmented scoring (executives vs. managers vs. end users)
- HTML report output
- Additional question packs (AI adoption, operating-model change)

## Contributing

Contributions to the code and documentation are welcome — see
[`CONTRIBUTING.md`](CONTRIBUTING.md). Proposed question changes are reviewed
against the method in `docs/method.md`; the instrument's structure (10
dimensions × 3 questions) is stable by design.

## License and trademarks

The **code** in this repository is released under the MIT License — see
[`LICENSE`](LICENSE).

**CHANGEReadyX™** and **TII™** (Transformation Intelligence Index) are
trademarks of TAPAS Advisory. The MIT license covers the code only; it does not
grant rights to the marks or to the proprietary CHANGEReadyX™ diagnostic
methodology. See [`TRADEMARK.md`](TRADEMARK.md).

---

*Ram Narayanan – Transformation Leader · Architect of CHANGEReadyX™, TAPAS Advisory*

*Full diagnostic: [tapasadvisory.com/diagnostic](https://tapasadvisory.com/diagnostic)*
