# Cube-and-conquer by level profile — feasibility note (DRAT-pure)

**DRAFT, 2026-07-18.** Design for attacking the open (10,2,k) cells by partitioning the search on the
**level profile** (f_2,…,f_10), f_i = number of size-i sets in the family. Every cube is the Mirsky
CNF plus assumptions pinning the profile, solved by **kissat + drat-trim** (DRAT standard, identical
to the n=9 certificates — no VeriPB anywhere). This note records the provable per-level bounds and
their provenance, the cube counts, and the completeness-certificate design.

## Step 1 — Provable per-level bounds (t=2, ground set [10])

Within a single level i, the size-i members form a **2-intersecting i-uniform** family, so f_i is
bounded by the exact max of such a family. These are **proved** bounds (used for completeness), not
heuristics.

| Level i | f_i ≤ | C(10,i) | Provenance |
|--------:|------:|--------:|------------|
| 2 | **1**  | 45  | Two distinct 2-sets meet in ≤1 pt (elementary); = AK F_0 = C(8,0) |
| 3 | **8**  | 120 | Ahlswede–Khachatrian, F_0 = 3-sets ⊇ fixed pair = C(8,1) |
| 4 | **28** | 210 | Ahlswede–Khachatrian, F_0 = C(8,2) |
| 5 | **66** | 252 | Ahlswede–Khachatrian, F_1 = C(4,3)C(6,2)+C(4,4)C(6,1)=66 (> F_0=56) |
| 6 | 210 | 210 | **Auto:** any two 6-sets in [10] meet in ≥ 2·6−10 = 2 pts, so all C(10,6) are pairwise 2-intersecting |
| 7 | 120 | 120 | Auto (2·7−10=4 ≥ 2) |
| 8 | 45  | 45  | Auto |
| 9 | 10  | 10  | Auto |
| 10 | 1  | 1   | Auto |

- **Citation (i ≤ 5):** R. Ahlswede, L. H. Khachatrian, *The complete intersection theorem for
  systems of finite sets*, European J. Combin. **18** (1997), 125–136. It gives the exact maximum
  t-intersecting k-uniform family on [n] as max_r |F_r|, F_r = {A ∈ [n]^(k) : |A ∩ [t+2r]| ≥ t+r};
  the values above were computed from this formula (t=2) and cross-checked (F_0 = all i-sets through
  a fixed 2-set = C(8,i−2)).
- **(a) trivial bound** f_i ≤ C(10,i) is definitional; the AK bounds (b) strengthen it on levels
  2–5 and do the bulk of the pruning (see counts).
- **(c) cross-level / Mirsky-label bounds** (within one Mirsky label class the sets form an
  antichain) are available but coarse and are **NOT** used for completeness pruning — a cube is
  skipped only when a **proved** bound (AK or the counting arithmetic in Step 3) excludes it; never
  by a heuristic. Cross-level 2-intersection and the k-Sperner structure are enforced *inside* each
  cube's CNF and resolved by the solver, not assumed.
- **(d) target:** Σ f_i ≥ 331 (k=2) / 376 (k=3) / 386 (k=4).

## Step 2 — Cube counts

Sum of proved per-level bounds = **489** (≥ every target, so no upper-bound pruning without the
conjecture). Pinning **all** levels exactly is infeasible:

| Cell | raw profiles, trivial bounds | raw profiles, AK bounds |
|------|------:|------:|
| (10,2,2) | 7.0×10¹⁵ | 1.24×10¹¹ |
| (10,2,3) | 6.5×10¹⁵ | 3.27×10¹⁰ |
| (10,2,4) | 6.4×10¹⁵ | 2.16×10¹⁰ |

AK cuts ~4 orders of magnitude but the count is still ~10¹¹ — **coarsen by pinning only a few
levels** (the rest stay free inside each cube's CNF). Live-cube counts (pinned combos not excluded
by AK or the counting bound Σ_pinned + Σ_free AK ≥ target):

| Pinned levels S | (10,2,2) | (10,2,3) | (10,2,4) |
|---|--:|--:|--:|
| {6}        | 159    | 114    | 104    |
| {5,6}      | 8,442  | 5,427  | 4,757  |
| {6,7}      | 11,979 | 6,555  | 5,460  |
| {6,7,8}    | 425,855| 198,720| 158,700|
| {5,6,7}    | 538,716| 235,036| 183,781|

**Feasible campaign granularity: pin 2 levels** (≈5k–12k cubes) — or {6} alone (~100–160 very coarse
cubes). Pinning ≥3 levels overflows ~10⁵. The right granularity depends on per-cube difficulty
(Step 4).

## Step 3 — Completeness certificate design

**Claim to certify:** M(10,2,k) ≤ target−1 (no valid family of size ≥ target). Combined with the
existing SAT witness at target−1 (`verifier_standalone.py`, unchanged), this pins the exact maximum.

For a scheme pinning levels S, a cube c = (f_i = v_i)_{i∈S} is **solved** iff not excluded by a
proved bound: (i) v_i ≤ AK_i for all i∈S; and (ii) Σ_{i∈S} v_i + Σ_{i∉S} AK_i ≥ target. Each solved
cube's CNF = [Mirsky CNF ∧ (f_i = v_i, i∈S) ∧ Σf ≥ target]; kissat proves it UNSAT, **drat-trim
verifies (exit 0)** — certifying no valid family with that S-profile reaches the target.

**Completeness (the split covers everything):** every family has a unique S-profile, so it lands in
exactly one cube. A cube is legitimately skipped only if (i) some v_i > AK_i — then no such family
exists (AK theorem); or (ii) the counting bound fails — then even filling the free levels to their
AK maxima cannot reach the target, so no family with that S-profile has size ≥ target. Hence the
solved cubes exhaust all families of size ≥ target. Two ways to make this machine-checkable:

- **Option A (AK as prose lemma):** trust AK for the per-level caps; verify the *enumeration* is
  complete by re-running the (deterministic) cube generator over all (v_i) with v_i ∈ [0, C(10,i)],
  confirming every non-solved combo is AK- or counting-excluded. Trusted base gains the AK theorem.
- **Option B (AK machine-checked, fully DRAT):** additionally certify each cap f_i ≤ AK_i (i=2..5)
  with kissat+drat-trim — "no 2-intersecting i-uniform family on [10] of size AK_i+1" (small UNSAT
  instances). This removes AK from the trusted base. Recommended (cheap).

The residual-UNSAT check the design brief mentions ("profile within bounds but matching no cube") is
**empty by construction** here, since cubes enumerate every in-range S-profile; the enumeration
itself is the completeness certificate (optionally re-expressed as a trivial UNSAT over the integer
profile variables).

**Prose lemmas joining the trusted base:**
1. Counting arithmetic (Σ_pinned + Σ_free AK < target ⟹ no family) — elementary.
2. Auto-intersection for i ≥ 6 (2i−10 ≥ 2) — elementary.
3. Mirsky's theorem — for the k-Sperner label encoding (see `MIRSKY_NOTE.md`); k ≥ 2 cells.
4. Size-<t WLOG (existing).
5. **Option A only:** Ahlswede–Khachatrian complete intersection theorem (per-level caps). Under
   Option B this is replaced by DRAT certificates.

## Step 4 — Calibration probe (validation cell (10,2,1), target 211)

Pin f_5, f_6; representative cubes, kissat, 10-min box each (2026-07-18):

| cube (f_5, f_6) | vars | clauses | kissat result |
|---|---:|---:|---|
| (0, 210) | 170,235 | 506,943 | **UNSAT 0 s** (all size-6 pinned → instant contradiction) |
| (0, 0)   | 170,235 | 506,943 | **UNSAT 1 s** |
| (33, 178)| 196,081 | 558,173 | **UNSAT 157 s** |
| (66, 145)| 213,637 | 593,285 | **TIMEOUT >600 s** |
| (0, 120) | 191,835 | 549,933 | **TIMEOUT >600 s** |

**DRAT-pure chain confirmed:** cube (0,0) → kissat UNSAT (exit 20) → `drat-trim` **`s VERIFIED`**.

**Verdict (mixed — decision-relevant):** cube-and-conquer by level profile is **very effective at the
extremes** (monolithic >22 min unresolved → f_6∈{0,210} cubes in 0–1 s) but **pinning f_5,f_6 alone
is insufficient** — 2 of 5 representative cubes timed out at 10 min. The hard cubes are those with a
**partial middle level** (0 < f_6 < 210): pinning the *count* f_6 does not break the S_n symmetry over
*which* size-6 sets are chosen, so those subproblems retain the same symmetry hardness that stalls the
monolith. Extreme counts (f_6 = 0 or 210) leave no choice and trivialize.

**Consequences for a campaign:** (i) profile-count cubing does not by itself resolve the symmetry
hardness of interior cubes — a fraction will need finer splitting or long solves; (ii) candidate
mitigations: pin 3 levels incl. the two largest (f_6,f_7) [~10^5–10^6 cubes], recursively re-split
timed-out cubes, or pick a symmetry-aware split variable; (iii) this probe is **k=1** (easiest) — the
real cells (10,2,k), k≥2, add Mirsky label variables and are per-cube harder. Baselines: monolithic
(9,3,2) ≈ 87 s; monolithic (10,2,1) unresolved >22 min. A full campaign is **not yet justified** on
f_5,f_6 cubing alone; the hard-cube fraction and finer-cubing cost must be characterized first.
