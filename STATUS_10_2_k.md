# STATUS: n=10, t=2 cells (10,2,k), k = 2, 3, 4

**Open, active investigation. Updated 2026-07-18.** These cells are **not** certified and **no claim
is made** about their exact maxima. The repository's certified results and certification standards are
**unchanged** (n=9: DRAT/drat-trim, frozen). This note records the cells, the openness provenance,
the three solver routes probed and mapped this session, and the active next direction.

## The cells and conjectured values

For n=10, t=2 (n+t even; r=(n−t)/2=4), conjectured maximum Σ_{i=0}^{k-1} C(10, 6+i):

| Cell | Conjectured maximum |
|------|--------------------:|
| (10,2,2) | 330 = C(10,6)+C(10,7) |
| (10,2,3) | 375 = +C(10,8) |
| (10,2,4) | 385 = +C(10,9) |

Adjacent settled cells (prior literature, not part of this work): **(10,2,1)=210** (Milner 1968),
**k≥5 → 386** (Katona 1964 collapse at k≥r+1=5).

## Openness provenance (audit 2026-07-18, "to the best of our determination")

Genuinely open — no citable theorem determines them at n=10:
- **Frankl, EJC 93 (2021) 103279:** Thm 1.11 (k=2) needs n≥3r+1=13; Thm 4.1 needs n>r(r+3)=28. n=10 misses both.
- **Balogh–Linz–Patkós, Combinatorial Theory 3(2) (2023), Thm 1.10:** even case only for "n large
  enough" (ineffective n₀(t,k)); their Conjecture 1.7 = the values above.
- **Yang–Zhang, arXiv:2607.03026:** refutes only the odd-parity conjecture; even case untouched.
- Profile-polytope / Milner–Frankl school settles t=1 and general k=1, not general t≥2 k-Sperner.

## Three routes probed and mapped this session

**(i) Native-PB without symmetry breaking — UNSAT direction infeasible.** Mirsky-encoded OPB →
RoundingSat → `veripb --elaborate` → `cake_pb` works end-to-end (both n=9 SAT witnesses reproduced,
sizes 120/129; toy UNSAT certified). But the UNSAT direction does not scale without symmetry breaking:
(9,3,2) at bound 121 ran **~35 min unresolved** (proof 1.7 GB) vs the DRAT baseline **87 s / 73 MB**.
The witness direction is instant; proving non-existence over the unbroken S₁₀ symmetry is intractable.

**(ii) Certified symmetry breaking — architecture validated, blocked on an ecosystem gap.** The
checker spine is sound: **satsuma 1.4** (modern SB) builds on arm64 and emits **VeriPB v3.0**, whose
SB prefix **parses cleanly in our `veripb` 3.0.2**, and `cake_pb`/`cake_pb_cnf` verify (`s VERIFIED`).
The blocker is external: completing a proof needs a SAT solver proof composed after satsuma's prefix,
and **no VeriPB-3.0-emitting SAT solver is available on arm64** — RoundingSat emits v2.0 (mixing
v3.0+v2.0 is rejected by both `veripb` 3.0.2 and the paper's pboxide), mainline kissat/CaDiCaL emit
DRAT/LRAT, the 2023 BreakID/kissat_fork are dialect-dead, and the AAAI'26 satsuma artifacts bundle no
solver and no DRAT→VeriPB bridge. See `TOOLING.md`.

**(iii) Profile cube-and-conquer — structural negative.** Partitioning by level profile (f_2..f_10)
with proved Ahlswede–Khachatrian per-level bounds yields ~5k–12k cubes when pinning 2 levels (see
`CUBES_NOTE.md`), and cube-and-conquer helps enormously at profile extremes (monolith >22 min → f_6∈
{0,210} cubes in 0–1 s, DRAT-pure, drat-trim `s VERIFIED`). **But profile cubes partition *counts*,
not *arrangements*:** an interior cube (0 < f_6 < 210) leaves the S₁₀ symmetry over *which* size-6
sets are chosen intact, so it retains full monolithic hardness. Probe (validation cell (10,2,1), pin
f_5,f_6, 10-min box): extremes 0–1 s, but (66,145) and (0,120) **timed out at 600 s**. Diagnosis in
`CUBES_NOTE.md`. Profile cubing alone does not resolve the symmetry hardness.

## ACTIVE NEXT — route (c): anchor-based, symmetry-aware case splitting

Branch on **structural configurations up to S₁₀** rather than on profile counts: fix a small
"anchor" (e.g. a few sets with prescribed sizes and intersection pattern), WLOG-concretized against
the symmetric group so each branch pins an *arrangement*, not just a count — directly attacking the
symmetry hardness that defeats route (iii). Requires a **finite case-split completeness lemma** (that
the anchored configurations are exhaustive up to S₁₀), documented as a prose note to the same standard
as `MIRSKY_NOTE.md` and the size-<t WLOG note, and potentially itself SAT-certifiable. **Design phase
(human-side) precedes any compute.** First compute will be the standard probe protocol on the
validation cell (10,2,1). Assets ready to reuse: `CUBES_NOTE.md` (AK bounds + Option-B "certify the
bounds" design + probe data), `MIRSKY_NOTE.md`, the RoundingSat/veripb/cake_pb spine, and the DRAT
kissat/drat-trim toolchain.

## Passive watch (alternative resumption)

Route (ii) resumes automatically if a **VeriPB-3.0-emitting SAT solver on arm64** appears (watch:
RoundingSat releases, satsuma's experimental output maturing, SAT-Comp 2026 certified-track solvers,
any DRAT→VeriPB-3.0 bridge). The satsuma toy gate stays scripted for a ~10-minute re-run.

*No n=10 exact-maximum claim exists. Certification standards are unchanged.*
