# Certified even-case values for the Frankl / Balogh–Linz–Patkós t-intersecting k-Sperner conjecture

Machine-checkable certificates fixing the **exact maximum size** of small **t-intersecting,
k-Sperner** families in the Boolean lattice 2^[n], in the **even-parity** case (n+t even).

## The conjecture, and how each source numbers it
F ⊆ 2^[n] is **t-intersecting** if |A∩B| ≥ t for all A,B ∈ F, and **k-Sperner** if it contains no
chain of k+1 sets.

Note (WLOG): the encoding's variable universe excludes sets of size < t. This is lossless: any
set A with |A| < t satisfies |A ∩ B| ≤ |A| < t for every set B, so a t-intersecting family
containing A has size 1 and cannot approach the bound; families of size 1 trivially satisfy it.

The even-parity conjecture (n+t even, n>t) is
> |F| ≤ Σ_{i=0}^{k-1} C(n, (n+t)/2 + i).

It is **Frankl Conjecture 1.6** (Frankl, European J. Combin. 93 (2021), Paper 103279) =
**Balogh–Linz–Patkós Conjecture 1.7** (arXiv:2209.01656) = **Yang–Zhang Conjecture 1.4**
(arXiv:2607.03026) — each number cited to its own paper. In Frankl's own formulation it is the
**2r-union, k-Sperner** case with r = (n−t)/2 (equivalent by complementation).

## What is proven (each value certified in BOTH directions)
For each cell we certify the exact maximum M(n,t,k):
- **≤ M**: "some t-intersecting k-Sperner family has size ≥ M+1" is encoded in CNF and proven
  **UNSAT** by `kissat`; the DRAT proof is checked by `drat-trim` (**exit code 0**).
- **≥ M**: `kissat` finds a family of size M; the witness is checked by an **independent
  exact-arithmetic verifier** (`tools/verifier_standalone.py`, no shared code with the encoder).

| (n,t,k) | certified maximum M | = conjectured value? | ≤ M (drat-trim) | ≥ M (witness) |
|---------|--------------------:|:--------------------:|:---------------:|:-------------:|
| (9,3,2) | **120** | yes = C(9,6)+C(9,7) | exit 0 (VERIFIED) | verified |
| (9,3,3) | **129** | yes = C(9,6)+C(9,7)+C(9,8) | exit 0 (VERIFIED) | verified |

*Attempted but NOT certified (and not part of this bundle's claims): (10,2,2) and (10,2,3) did not
certify within our initial compute budget; further attempts may follow.* See `CLAIMS.md` for the
authoritative per-cell status.

## Complete resolution of n=9 (even parity)
With the two certificates above, **every even-parity cell at n=9 — t ∈ {1,3,5,7}, all k ≥ 1 — is
now determined**, and in every cell the conjectured value Σ_{i=0}^{k-1} C(9, (9+t)/2 + i) is the
exact maximum. The certificates in this repository settle **exactly the two cells — (9,3,2) and
(9,3,3) — where no classical or modern theorem applies**; every other cell in the table is a prior
result, and the table records why nothing new was needed there.

**Attribution:** the t=1, t=5 and t=7 values below are **prior literature, not contributions of this
work.** Only the two cells marked **[this repo]** are certified here.

| t (r=(9−t)/2) | k | M(9,t,k) | Provenance |
|---|---|---:|---|
| **t=7** (r=1) | 1 | 9 | Milner 1968 (t-intersecting antichain), C(9,8) |
|  | ≥2 | 10 | Katona collapse: k ≥ r+1=2, k-Sperner non-binding → full t-intersecting max (Katona 1964) |
| **t=5** (r=2) | 1 | 36 | Milner 1968, C(9,7) |
|  | 2 | 45 | Frankl 2021 (EJC 93, 103279), Thm 1.11: hypothesis n ≥ 3r+1 = 7 is satisfied (n=9) |
|  | ≥3 | 46 | Katona collapse: k ≥ r+1=3 (Katona 1964) |
| **t=3** (r=3) | 1 | 84 | Milner 1968, C(9,6) — used here as encoder ground-truth (see Verification standard) |
|  | 2 | **120** | **[this repo]** certified both directions (drat-trim exit 0; witness verified) |
|  | 3 | **129** | **[this repo]** certified both directions (drat-trim exit 0; witness verified) |
|  | ≥4 | 130 | Katona collapse: k ≥ r+1=4 (Katona 1964) |
| **t=1** (r=4) | 1 | 126 | Milner 1968, C(9,5) |
|  | 2 | 210 | Frankl 1990 (max intersecting k-Sperner) † |
|  | 3 | 246 | Frankl 1990 † |
|  | 4 | 255 | Frankl 1990 † |
|  | ≥5 | 256 | Full intersecting family (all sets of size ≥5); Katona collapse k ≥ r+1=5 |

† **Frankl**, *Canonical antichains on the circle and applications*, SIAM J. Discrete Math. **3**(3)
(1990), 355–363, which determines the maximum size of an intersecting (t=1) k-Sperner family for
**all n** (no threshold). For odd n it equals Σ_{i=(n+1)/2}^{(n+1)/2+k−1} C(n,i); at n=9 that is
Σ_{i=5}^{4+k} C(9,i) = 210 / 246 / 255 for k = 2 / 3 / 4. Re-proved by **Gerbner**, Combinatorica
**33** (2013), 199–216, and by **Gerbner–Methuku–Tompkins**, *Intersecting P-free families*, J.
Combin. Theory Ser. A **151** (2017), 61–83. The statement was verified verbatim against the GMT
arXiv version (arXiv:1506.00864v2, Theorem 8, with equality family H₀,ₙ,ₖ = the union of levels
⌊n/2⌋+1, …, ⌊n/2⌋+k); the Frankl-1990 origin follows Patkós's survey (GMT's Theorem 8 is itself
attributed there to Gerbner 2013).

## Ongoing campaign: the open (10,2,k) cells

Beyond the certified n=9 results, an **active, uncertified investigation** targets the n=10, t=2 cells
— **(10,2,2)**, **(10,2,3)** and **(10,2,4)**, conjectured to equal **330**, **375** and **385**
respectively. These are genuinely open: no citable theorem determines them at n=10, and **this
repository makes no claim about their values.** Work so far has been confined to a *validation cell*,
(10,2,1), whose answer is known independently (Milner 1968), so that methods can be measured against
ground truth before any open-cell compute; on that cell two leaves of a case tree are certified, while
one leaf remains open with two candidate routes closed by measurement.

**Entry point: [`notes/STATUS_10_2_k.md`](notes/STATUS_10_2_k.md)**, with the design and measurement
record in [`notes/ANCHOR_NOTE.md`](notes/ANCHOR_NOTE.md), [`notes/CUBES_NOTE.md`](notes/CUBES_NOTE.md),
[`notes/MIRSKY_NOTE.md`](notes/MIRSKY_NOTE.md) and [`notes/TOOLING.md`](notes/TOOLING.md).

## Why these instances
Frankl (EJC 93 (2021), Paper 103279) proves the even-parity conjecture only in certain ranges:
**Thm 1.11** (k=2) requires **n ≥ 3r+1**, where r=(n−t)/2; **Thm 4.1** (2≤k≤r) requires
**n > r(r+3)**; and the k-Sperner constraint is non-binding (reducing to Katona's t-intersecting
theorem) once **k ≥ r+1**. Balogh–Linz–Patkós (arXiv:2209.01656, Thm 1.10) settle fixed t and
"n large enough" **with no explicit threshold (ineffective)**. **(9,3,2) is the smallest
even-parity instance falling outside Frankl Thm 1.11** — it misses the hypothesis n ≥ 3r+1 = 10 by
exactly one. These cells are therefore not settled by any citable theorem (full openness
provenance, with exact citations and a dated literature sweep, is in `CLAIMS.md`).

## Context
Yang–Zhang (arXiv:2607.03026, 3 Jul 2026) **refuted** the *odd*-parity companion conjecture
(**Yang–Zhang Conjecture 1.6** = Balogh–Linz–Patkós Conjecture 1.8; Frankl's odd companion is his
Conjecture 1.10) for all t≥2,k≥2 with k(t−1)≥t+1, **including (t,k)=(3,2)**. This bundle is the *even*-parity counterpart at the same (t,k): at the smallest open
even instance, the conjectured value **holds** and is certified.

## What is NOT claimed
- **No claim about (11,3,2)** or any larger cell — those remain open and under separate work.
- **Openness is a best-determination**, not a theorem: it rests on the exact citations in
  `CLAIMS.md` and a literature sweep dated 2026-07-09, "to the best of our determination."
- We claim only the **exact maxima** of the certified cells; we do not claim the general conjecture.

## Verification standard
Success is judged by **checker exit code 0**, never by parsing a status line. DRAT proofs are
checked by `drat-trim`; SAT witnesses by an **independent** exact-integer verifier. Everything is
reproducible from source in minutes — see `REPRODUCE.md`. All artifacts are checksummed in
`SHA256SUMS`. See `AI_DISCLOSURE.md` for how this work was produced.

**Encoder validation (Milner ground truth).** The encoder was validated against a human-proven
theorem: for (n,t,k)=(9,3,1) — t-intersecting antichains — Milner's theorem (1968) gives the exact
maximum C(9,6)=84. The pipeline, never tuned for k=1, reproduced 84 in both directions: kissat
UNSAT at ≥85 with drat-trim exit 0, and a size-84 witness accepted by the standalone verifier. This
checks that the encoding is faithful to the definitions, independently of the certificates
themselves. The run is reproducible in minutes via `tools/cert_cell.py` with (n,t,k)=(9,3,1);
validation artifacts are retained locally and available on request.

## References

**Papers**
- P. Frankl, *Analogues of Milner's theorem for families without long chains and of vector spaces*,
  European J. Combin. 93 (2021), Paper 103279.
- J. Balogh, W. B. Linz, B. Patkós, *On the sizes of t-intersecting k-chain-free families*,
  arXiv:2209.01656.
- J.-B. Yang, L. Zhang, *Counterexamples to the Balogh–Linz–Patkós Conjecture*, arXiv:2607.03026
  (2026).
- E. C. Milner, *A combinatorial theorem on systems of sets*, J. London Math. Soc. 43 (1968),
  204–206. (Cited as Theorem 1.5 in Frankl, EJC 93 (2021).)
- P. Frankl, *Canonical antichains on the circle and applications*, SIAM J. Discrete Math. 3 (1990),
  355–363. (Maximum size of an intersecting k-Sperner family — settles the t=1 column above.)
- D. Gerbner, *Profile polytopes of some classes of families*, Combinatorica 33 (2013), 199–216.
  (Re-proof of the intersecting k-Sperner maximum.)
- D. Gerbner, A. Methuku, C. Tompkins, *Intersecting P-free families*, J. Combin. Theory Ser. A 151
  (2017), 61–83 (arXiv:1506.00864). (Re-proof; Theorem 8 quoted to verify the t=1 values above.)
- G. O. H. Katona, *Intersection theorems for systems of finite sets*, Acta Math. Acad. Sci. Hungar.
  15 (1964), 329–337. (Maximum t-intersecting family — the k ≥ r+1 "collapse" values above.)

**Tools**
- A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks, F. Pollitt, *CaDiCaL, Gimsatul, IsaSAT
  and Kissat Entering the SAT Competition 2024*, in: Proc. SAT Competition 2024 – Solver, Benchmark
  and Proof Checker Descriptions, Dept. of Computer Science Report Series B, vol. B-2024-1, Univ. of
  Helsinki, 2024, pp. 8–10. (Preferred citation per the kissat README.)
- N. Wetzler, M. J. H. Heule, W. A. Hunt Jr., *DRAT-trim: Efficient Checking and Trimming Using
  Expressive Clausal Proofs*, in: Theory and Applications of Satisfiability Testing – SAT 2014,
  Lecture Notes in Computer Science 8561, Springer, 2014, pp. 422–429.
- A. Ignatiev, A. Morgado, J. Marques-Silva, *PySAT: A Python Toolkit for Prototyping with SAT
  Oracles*, in: Theory and Applications of Satisfiability Testing – SAT 2018.

## Citation
This archive is deposited on Zenodo.
- **Cite this version:** DOI [10.5281/zenodo.21287287](https://doi.org/10.5281/zenodo.21287287)
- **All versions (concept DOI, resolves to latest):** [10.5281/zenodo.21287286](https://doi.org/10.5281/zenodo.21287286)

> *Certified even-case values for the Frankl / Balogh–Linz–Patkós t-intersecting k-Sperner
> conjecture.* Zenodo (2026). https://doi.org/10.5281/zenodo.21287287

(Author/depositor metadata is carried by the Zenodo record; see `AI_DISCLOSURE.md` for how the
work was produced.)
