# Claims and openness provenance

Archived on Zenodo — this version: DOI 10.5281/zenodo.21287287 ; all versions (concept): 10.5281/zenodo.21287286 .

Each entry states an EXACT maximum we certify, with both-direction evidence and the openness
provenance for that cell. Openness is stated **to the best of our determination** as of 2026-07-09,
per the exact citations shown. We claim only these exact maxima — not the general conjecture.

**Certification standards (dual).** The n=9 cells below are certified in the SAT/DRAT standard:
UNSAT direction by `drat-trim` (exit 0), SAT witness by `tools/verifier_standalone.py`. Any future
**n=10** cells use the pseudo-Boolean standard: native-PB OPB encoding (cardinality as first-class
constraints), RoundingSat with VeriPB proof logging, `veripb --elaborate` to kernel format, and the
formally verified CakeML checker **`cake_pb`** as the trusted checker — acceptance is `cake_pb`
printing `s VERIFIED UNSATISFIABLE` (its exit code is not a reliable signal). The SAT/witness
direction is unchanged (`verifier_standalone.py`, exact arithmetic). Symmetry breaking is not part of
the baseline; see `notes/TOOLING.md`. No n=10 exact-maximum claims appear yet.

## (9,3,2) — certified maximum = 120

**CLAIM.** The maximum size of a t-intersecting 2-Sperner family in 2^[9] with t=3 is exactly **120** (= the conjectured value). Certified both directions: drat-trim exit 0 for the ≤ 120 bound; independent exact-arithmetic verifier for a witness of size 120.

```
=== CELL (n,t,k)=(9,3,2)  bound(conjectured max)=120  r=(n-t)/2=3  @ 2026-07-09 17:56:47 ===
[UNSAT dir] kissat ge121: exit=20(20=UNSAT) 86.8s | drat-trim EXIT=0 (VERIFIED) 202.2s
[SAT dir]  kissat ge120: exit=10(10=SAT) | witness size=120 valid_family=True tint=True k_sperner=True (>= bound 120: True)
CELL RESULT: UNSAT-dir certified=True  SAT-dir verified=True  => BOTH-DIRECTIONS=True
```

OPENNESS PROVENANCE for the even-parity (2r-union / k-Sperner) conjecture, namely Frankl Conjecture 1.6 (Frankl, European J. Combin. 93 (2021) Paper 103279) = Balogh-Linz-Patkos Conjecture 1.7 (arXiv:2209.01656) = Yang-Zhang Conjecture 1.4 (arXiv:2607.03026), at (n,t,k)=(9,3,2); r=(n-t)/2=3.
Status: OPEN as of 2026-07-09.
- Frankl, European J. Combin. 93 (2021) Paper 103279 (theorem numbers per the author's paper):
    Thm 1.11 (k=2) proves the conjectured value only for n >= 3r+1 = 10; here n=9 < 10 (misses by 1).
    Thm 4.1 (2<=k<=r) proves it only for n > r(r+3) = 18; here n=9 (not > 18).
    Katona t-intersecting theorem settles it when the k-Sperner constraint is non-binding, i.e. k >= r+1 = 4; here k=2 < 4.
- Balogh-Linz-Patkos, arXiv:2209.01656 (v1, no revision), Thm 1.10: settles fixed t and 'n large enough' with NO explicit n_0 (ineffective) -> does not cover any specific n.
- Cross-check Yang-Zhang, arXiv:2607.03026 (v1, 3 Jul 2026): refutes only the ODD-parity conjecture (Yang-Zhang Conjecture 1.6 = BLP Conjecture 1.8; Frankl's odd companion is his Conjecture 1.10); the even case is untouched.
- Literature sweep 2026-07-09: BLP v1-only; no post-3-Jul-2026 follow-up closing even-parity cells; no paper computes the even-case maximum at n=9.
- NOTE: (9,3,2) is the smallest even-parity instance not covered by Frankl Thm 1.11 (misses the hypothesis n>=3r+1=10 by exactly one).

## (9,3,3) — certified maximum = 129

**CLAIM.** The maximum size of a t-intersecting 3-Sperner family in 2^[9] with t=3 is exactly **129** (= the conjectured value). Certified both directions: drat-trim exit 0 for the ≤ 129 bound; independent exact-arithmetic verifier for a witness of size 129.

```
=== CELL (n,t,k)=(9,3,3)  bound(conjectured max)=129  r=(n-t)/2=3  @ 2026-07-09 18:03:20 ===
[UNSAT dir] kissat ge130: exit=20(20=UNSAT) 87.8s | drat-trim EXIT=0 (VERIFIED) 131.6s
[SAT dir]  kissat ge129: exit=10(10=SAT) | witness size=129 valid_family=True tint=True k_sperner=True (>= bound 129: True)
CELL RESULT: UNSAT-dir certified=True  SAT-dir verified=True  => BOTH-DIRECTIONS=True
```

OPENNESS PROVENANCE for the even-parity (2r-union / k-Sperner) conjecture, namely Frankl Conjecture 1.6 (Frankl, European J. Combin. 93 (2021) Paper 103279) = Balogh-Linz-Patkos Conjecture 1.7 (arXiv:2209.01656) = Yang-Zhang Conjecture 1.4 (arXiv:2607.03026), at (n,t,k)=(9,3,3); r=(n-t)/2=3.
Status: OPEN as of 2026-07-09.
- Frankl, European J. Combin. 93 (2021) Paper 103279 (theorem numbers per the author's paper):
    Thm 1.11 applies to k=2 only (this cell has k=3).
    Thm 4.1 (2<=k<=r) proves it only for n > r(r+3) = 18; here n=9 (not > 18).
    Katona t-intersecting theorem settles it when the k-Sperner constraint is non-binding, i.e. k >= r+1 = 4; here k=3 < 4.
- Balogh-Linz-Patkos, arXiv:2209.01656 (v1, no revision), Thm 1.10: settles fixed t and 'n large enough' with NO explicit n_0 (ineffective) -> does not cover any specific n.
- Cross-check Yang-Zhang, arXiv:2607.03026 (v1, 3 Jul 2026): refutes only the ODD-parity conjecture (Yang-Zhang Conjecture 1.6 = BLP Conjecture 1.8; Frankl's odd companion is his Conjecture 1.10); the even case is untouched.
- Literature sweep 2026-07-09: BLP v1-only; no post-3-Jul-2026 follow-up closing even-parity cells; no paper computes the even-case maximum at n=9.

## Complete resolution of n=9 (even parity)

With the two certified cells above, every even-parity cell at n=9 (t in {1,3,5,7}, all k>=1) is
determined, and in every cell the conjectured value Sum_{i=0}^{k-1} C(9,(9+t)/2+i) is the exact
maximum. This repository's certificates settle EXACTLY the two cells -- (9,3,2)=120 and (9,3,3)=129
-- where no classical or modern theorem applies. All other cells are prior literature and are NOT
claimed as contributions of this work. Verified per-cell provenance (r=(9-t)/2):

- t=7 (r=1): k=1 -> 9 = C(9,8), Milner 1968; k>=2 -> 10, Katona collapse (k>=r+1=2; full
  t-intersecting maximum, Katona 1964).
- t=5 (r=2): k=1 -> 36 = C(9,7), Milner 1968; k=2 -> 45, Frankl EJC 93 (2021) 103279 Thm 1.11
  (hypothesis n>=3r+1=7 satisfied at n=9); k>=3 -> 46, Katona collapse (k>=r+1=3).
- t=3 (r=3): k=1 -> 84 = C(9,6), Milner 1968 (used as encoder ground-truth here); k=2 -> 120 and
  k=3 -> 129, THIS REPOSITORY (certified both directions, drat-trim exit 0 + verified witness);
  k>=4 -> 130, Katona collapse (k>=r+1=4).
- t=1 (r=4): k=1 -> 126 = C(9,5), Milner 1968; k=2,3,4 -> 210/246/255, Frankl "Canonical antichains
  on the circle and applications", SIAM J. Discrete Math. 3 (1990) 355-363 (maximum intersecting
  k-Sperner family, all n; odd-n value Sum_{i=(n+1)/2}^{(n+1)/2+k-1} C(n,i)); re-proved by Gerbner
  (Combinatorica 33, 2013) and Gerbner-Methuku-Tompkins (JCTA 151, 2017). Statement verified verbatim
  against the GMT arXiv version (arXiv:1506.00864v2, Theorem 8); the Frankl-1990 origin follows
  Patkos's survey (GMT state Theorem 8 as attributed to Gerbner 2013). k>=5 -> 256 (full intersecting
  family, all sets of size >=5; Katona collapse k>=r+1=5).

Attribution note: the t=1, t=5, and t=7 values are established prior results (Milner 1968; Frankl
1990; Frankl EJC 2021 Thm 1.11; Katona 1964). This work contributes only the two t=3 certificates.
