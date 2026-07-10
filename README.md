# Certified even-case values for Frankl's Conjecture 1.7 (Balogh–Linz–Patkós)

Machine-checkable certificates fixing the **exact maximum size** of small **t-intersecting,
k-Sperner** families in the Boolean lattice 2^[n], in the **even-parity** case (n+t even) — the
case of **Frankl's Conjecture 1.7** (= Balogh–Linz–Patkós, = Yang–Zhang's Conjecture 1.4).

## Definitions
F ⊆ 2^[n] is **t-intersecting** if |A∩B| ≥ t for all A,B ∈ F, and **k-Sperner** if it contains no
chain of k+1 sets. Conjecture 1.7 (n+t even, n>t): |F| ≤ Σ_{i=0}^{k-1} C(n, (n+t)/2 + i).

## What is proven (each value certified in BOTH directions)
For each cell we certify the exact maximum M(n,t,k):
- **≤ M**: the formula "some t-intersecting k-Sperner family has size ≥ M+1" is encoded in CNF and
  proven **UNSAT** by `kissat`, with the DRAT proof checked by `drat-trim` (**exit code 0**).
- **≥ M**: `kissat` finds a family of size M; the witness is checked by an **independent
  exact-arithmetic verifier** (`tools/verifier_standalone.py`, no shared code with the encoder).

| (n,t,k) | certified maximum M | = conjectured value? | UNSAT proof | witness |
|---------|--------------------:|:--------------------:|:-----------:|:-------:|
| (9,3,2) | **120** | yes (C(9,6)+C(9,7)) | drat-trim exit 0 | verified |
| (9,3,3) | **129** | yes (C(9,6)+C(9,7)+C(9,8)) | drat-trim exit 0 | verified |
| (10,2,2) | 330 *(landing)* | yes | — | — |
| (10,2,3) | 375 *(landing)* | yes | — | — |

(Table is updated as the remaining certifications complete; see `CLAIMS.md` for the authoritative
per-cell status and provenance.)

## Why these instances
Frankl (EJC 93 (2021), Paper 103279) proves Conjecture 1.7 only in certain ranges: **Thm 1.11**
(k=2) requires **n ≥ 3r+1** where r=(n−t)/2; **Thm 4.1** (2≤k≤r) requires **n > r(r+3)**; and the
k-Sperner constraint is non-binding (reducing to Katona's t-intersecting theorem) once **k ≥ r+1**.
Balogh–Linz–Patkós (arXiv:2209.01656, Thm 1.10) settle fixed t and "n large enough" **with no
explicit threshold (ineffective)**. **(9,3,2) is the smallest even-parity instance falling outside
Frankl Thm 1.11** — it misses the hypothesis n ≥ 3r+1 = 10 by exactly one. These cells are
therefore not settled by any citable theorem (see `CLAIMS.md` for the full openness provenance).

## Context
Yang–Zhang (arXiv:2607.03026, 3 Jul 2026) **refuted** the *odd*-parity companion conjecture (BLP
Conjecture 1.8) for all t≥2,k≥2 with k(t−1)≥t+1, **including (t,k)=(3,2)**. This bundle is the
*even*-parity counterpart at the same (t,k): at the smallest open even instance, the conjectured
value **holds** and is certified.

## What is NOT claimed
- **No claim about (11,3,2)** or any larger cell — those remain open and under separate work.
- **Openness is a best-determination**, not a theorem: it rests on the exact citations in
  `CLAIMS.md` and a literature sweep dated 2026-07-09, "to the best of our determination."
- We claim only the **exact maxima** of the certified cells; we do not claim the general conjecture.

## Verification standard
Success is judged by **checker exit code 0**, never by parsing a status line. DRAT proofs are
checked by `drat-trim`; SAT witnesses by an **independent** exact-integer verifier. Everything is
reproducible from source in minutes — see `REPRODUCE.md`. All artifacts are checksummed in
`SHA256SUMS`.

See `AI_DISCLOSURE.md` for how this work was produced.
