# AI assistance disclosure

This artifact — the encoding, the solver/checker pipeline, the certificates, and this
documentation — was produced with substantial assistance from **Anthropic's Claude**, operating as
the **Claude Code** agent, under human direction.

## What the AI did
- Wrote the CNF encoder, the certification driver, and the standalone verifier.
- Built the toolchain from source (kissat, drat-trim) and ran all computations.
- Machine-read the primary sources and drafted the openness provenance from their text.

## Primary-source verification chain (exact)
The conjecture numbering and the exact Frankl ranges in `README.md`/`CLAIMS.md` were taken from the
papers' own text, machine-read by the AI — not from the model's memory:
- **Balogh–Linz–Patkós (arXiv:2209.01656)** and **Yang–Zhang (arXiv:2607.03026)**: the AI fetched
  the arXiv PDFs and extracted their text; confirmed BLP Conjecture 1.7 and Yang–Zhang
  Conjecture 1.4 (even case), and Yang–Zhang Conjecture 1.6 = BLP Conjecture 1.8 (odd case).
- **Frankl, EJC 93 (2021) 103279**: this paper is *not* on arXiv and was behind a paywall, so the
  AI could **not** access it initially and said so. The **human then placed the PDF on local disk**;
  the AI machine-read that file with `pypdf` and confirmed **from the extracted text**: the
  even-case 2r-union/k-Sperner conjecture is **Frankl Conjecture 1.6**; **Theorem 1.11** (k=2,
  n ≥ 3r+1, |F| ≤ C(n,r)+C(n,r−1)); **Theorem 4.1** (2 ≤ k ≤ r, optimal for n > r(r+3)); odd
  companion **Conjecture 1.10**. (Per Elsevier copyright, the PDF and its text are **not** included
  in this bundle — cited only.)

## What the human directed and controls
- The research goals, the choice of targets, and the **evidentiary standard** (below).
- Supplying primary sources and requiring openness to be established from them, not from memory.
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
