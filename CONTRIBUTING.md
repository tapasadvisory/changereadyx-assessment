# Contributing

Thanks for your interest in improving the CHANGEReadyX™ assessment toolkit.

## What contributions are welcome

- **Code** — improvements to `tools/score.py` and additional tooling (report
  formats, comparison views). Keep the scorer dependency-free: Python 3
  standard library only.
- **Documentation** — clarifications, worked examples, translations of the
  method notes.
- **Bug reports** — open an issue with the answers file (anonymised), the
  command you ran, and the output you expected versus what you got.

## Ground rules

- The instrument's structure — 10 dimensions × 3 questions — is stable by
  design. Proposals to reword a question are welcome with a rationale tied to
  the method in `docs/method.md`; proposals to add or remove dimensions need a
  strong evidence case.
- Questions must stay behaviour/evidence-phrased and assessable. If a competent
  practitioner couldn't answer it from observable evidence, it doesn't belong
  in the instrument.
- Keep claims honest: the toolkit is evidence-based. Do not describe it as a
  validated instrument anywhere in contributed text.
- By contributing, you agree your contribution is licensed under the MIT
  License. The CHANGEReadyX™ and TII™ trademarks remain with TAPAS Advisory —
  see `TRADEMARK.md`.

## Process

1. Fork, branch, make the change.
2. If you touch the scorer, run it against `examples/sample-answers.json` and
   confirm the sample report still generates.
3. Open a pull request describing what changed and why.
