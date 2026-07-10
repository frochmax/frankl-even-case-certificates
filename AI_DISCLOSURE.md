# AI assistance disclosure

This artifact — the encoding, the solver/checker pipeline, the certificates, and this
documentation — was produced with substantial assistance from **Anthropic's Claude**, operating as
the **Claude Code** agent, under human direction.

## What the AI did
- Wrote the CNF encoder, the certification driver, and the standalone verifier.
- Built the toolchain from source (kissat, drat-trim) and ran all computations.
- Located and read the primary sources; drafted the openness provenance.

## What the human directed and controls
- The research goals, the choice of targets, and the **evidentiary standard** (below).
- The requirement that provenance of *openness* be established from **primary sources** (Frankl EJC
  93 (2021) 103279; Balogh–Linz–Patkós arXiv:2209.01656; Yang–Zhang arXiv:2607.03026), not from
  the model's memory — the exact Frankl thresholds in `CLAIMS.md` were taken from the paper itself.
- The rule that a result counts **only** when an independent checker returns exit code 0.

## Why you should not have to trust the AI (or us)
Every mathematical claim here is backed by a **machine-checkable artifact**:
- The "≤ M" claims are **DRAT proofs** verifiable by *any* DRAT checker (we used `drat-trim`); the
  proof does not depend on trusting kissat or the encoder.
- The "≥ M" claims are **explicit families** checkable by *any* correct verifier in exact integer
  arithmetic; we include one (`tools/verifier_standalone.py`) that shares no code with the encoder.

Please re-run the checks (`REPRODUCE.md`) rather than trust any narrative. If a check disagrees
with a claim here, the check is right and we want to know.

## Honesty notes
- Openness is stated **"to the best of our determination"** with exact citations and a dated
  literature sweep — it is not itself a certified statement.
- We make **no claims** beyond the exact maxima of the specifically certified cells.
