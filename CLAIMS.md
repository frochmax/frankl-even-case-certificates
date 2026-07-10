# Claims and openness provenance

Archived on Zenodo — this version: DOI 10.5281/zenodo.21287287 ; all versions (concept): 10.5281/zenodo.21287286 .

Each entry states an EXACT maximum we certify, with both-direction evidence and the openness
provenance for that cell. Openness is stated **to the best of our determination** as of 2026-07-09,
per the exact citations shown. We claim only these exact maxima — not the general conjecture.

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
