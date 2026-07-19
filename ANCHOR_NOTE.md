# Anchor-based symmetry-aware case split — design note (route c)

**DRAFT, 2026-07-18.** Design for attacking the open (10,2,k) cells by branching on **structural
configurations up to S₁₀**, not on profile counts (which failed — interior profile cubes retain the
symmetry over *which* sets are chosen; see `CUBES_NOTE.md`). Every branch is a plain kissat +
drat-trim job (DRAT standard, as for the n=9 certificates).

## The case split: branch on the maximum set size m

Every non-empty family F has a maximum member size m = max_{A∈F} |A|. Branch on m; within each branch,
by the S₁₀ orbit argument WLOG a maximum-size member is the canonical set S = {1,…,m}. (Prose
completeness lemma, to the standard of `MIRSKY_NOTE.md` / the size-<t WLOG note; the orbit argument is
elementary and, if desired, itself SAT-certifiable.)

Bounds below use two primary-source-verified theorems from this session's audits:
- **Milner (1968):** max 2-intersecting antichain in 2^[n] is C(n, (n+2)/2) — Milner(10,2,1)=210,
  Milner(9)=C(9,6)=84.
- **Frankl (1990, SIAM J. Discrete Math. 3, 355–363):** max intersecting k-Sperner; the t=1 values,
  e.g. the (9,1,2) figure 210 used in the m=9 trace bound.

| Case | WLOG anchor | Bound sketch | Status |
|------|-------------|--------------|--------|
| m=10 | S=[10] ∈ F | The size-10 set is comparable to everything ⇒ F = {[10]} ∪ (antichain avoiding [10]); ≤ 1 + Milner(10,2,1) = 1+210 = 211 < 331 | **closed by counting** |
| m=9  | S={1..9} ∈ F | subsets of S: 2-int antichain in 2^[9] ≤ Milner=84; sets meeting the outside element: 1-int 2-Sperner traces in 2^[9] ≤ Frankl-1990 (9,1,2)=210; total ≤ 294 < 331 | **closed by counting** |
| m=8  | S={1..8} ∈ F | naive sleeve bounds ≤ 393 — NOT < 331 | **first real anchor cube** |
| m≤7  | — | main branch | future work |

## Cube semantics used in the rehearsal (this probe)

Each case-m cube = monolithic CNF for the cell at bound `target` PLUS unit clauses: `x_S = 1` for
S={1..m}, and `x_T = 0` for every T with |T| ≥ m, T ≠ S ("the max member is exactly S, and it is the
unique member of size ≥ m"). **Design note:** this pins S as the *unique* top-size member; full
coverage of case m for families with several size-m members is a completeness refinement (enumerate
the top-layer content, or use a canonical-max tie-break) — a design item for the campaign, not needed
for the tractability rehearsal.

## Rehearsal plan (validation cell (10,2,1), target 211; k=1 so no Mirsky labels)

Run the m=10, m=9, m=8 anchored cubes; expect m=10/9 near-instant (heavy counting closure) and m=8 as
the first substantive cube (15-min box). If m=8 is fast (<2 min), also run the m≤7 cube (forbid all
size ≥8 sets) to complete a full anchored decomposition of (10,2,1) and re-prove ≤210 by the anchor
method on DRAT. Baselines: monolithic (10,2,1) unresolved >25 min; profile cubes 0 s–600 s+.
Per-cube results are appended to `~/cube_log.txt`.

## Rehearsal results (validation cell (10,2,1), target 211) — 2026-07-18

| cube | box | kissat | drat-trim (hand-verified) |
|------|-----|--------|---------------------------|
| m=10 (S=[10]) | 120 s | **UNSAT 0 s** | **s VERIFIED** |
| m=9 (S={1..9}) | 120 s | TIMEOUT | — |
| m=8 (S={1..8}) | 900 s | TIMEOUT | — |
| **m≤7 (main branch, all size≥8 forbidden)** | 900 s | **TIMEOUT** | — |

(The runner's inline drat column read DRAT-FAIL due to a `\r`-prefix grep bug in drat-trim's progress
output; m=10 verifies under a CR-robust check. m=9/m=8 are counting-closable — anchored antichains
≤~127/~183 < 211 — so their timeouts are CDCL-vs-pigeonhole, not anchor measurements, and per the
design rule such cases go to counting, never the solver.)

**Verdict: max-size anchoring alone does NOT beat the monolithic wall.** The decisive cube is m≤7 —
the main branch, where counting does not close and the k=1 extremum (the full size-6 layer, 210 sets)
lives. It **timed out at 15 min**, the same wall as the monolithic (10,2,1) (>25 min unresolved).
Branching on the maximum set size only peels off the top (m=10 trivial; m=9,8 pigeonhole-closable) and
leaves the hard core (m≤7 ≈ the whole problem minus a few top layers) intact and monolithic-hard. And
this is k=1, the easiest cell; k≥2 are harder.

**Design consequence:** the anchor must split *within* the m≤7 bulk — a structural sub-configuration
that reduces the S₁₀ symmetry in the region where the search actually happens — not merely stratify by
max size. Open-cell case-8 compute is **NO-GO** under the current (max-size-only) design; a finer
in-bulk split must be designed and rehearsed on the validation cell first.

## Redesign direction (open design task, human-side)

Split *inside* the m≤7 bulk rather than stratifying by max size. Candidate anchors that partition the
region where the search actually happens (reducing S₁₀ symmetry there):
- **Complement anchors:** branch on the minimum complement size / a fixed excluded pair-pattern, WLOG
  canonicalized — dual to max-size but acting on the bulk's structure.
- **Multi-set configuration anchors:** fix a small sub-configuration of 2–3 members with a prescribed
  mutual intersection pattern that every family must contain (up to S₁₀), so each branch pins an
  *arrangement*, concretely reducing symmetry across the whole family, not just the top layer.

Each needs a finite case-split completeness lemma (to the MIRSKY_NOTE/WLOG standard, potentially
SAT-certifiable) and must be rehearsed on the validation cell (10,2,1) to sub-monolithic times before
any open-cell compute. **Design pending.**
