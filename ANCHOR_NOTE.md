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

---

# v2 — complement-anchor dichotomy (design + rehearsal, 2026-07-18)

**DRAFT, local. Human-designed this session.** The v1 redesign direction above ("complement anchors")
instantiated concretely, and rehearsed. **Result: NO-GO on the decisive leaf.**

## The dichotomy

Work inside the m≤7 bulk (all sets of size ≥8 forbidden). Let **G = the set of size-6 sets NOT in the
family**, g = |G|. Three leaves, exhaustive by construction (g≤1, or g≥2 with a spread pair, or g≥2
without one):

| Leaf | Condition | Anchor | Status |
|------|-----------|--------|--------|
| **(0)** | g ≤ 1 (near-full level 6, f₆ ≥ 209) | cardinality ≥209 on level 6 | expected pencil/trivial |
| **(A)** | some pair A,B ∈ G with \|A∩B\| = 2 ("spread pair") | WLOG A={1,…,6}, B={1,2,7,8,9,10} | **rehearsed — see below** |
| **(B)** | all pairs in G meet in ≥3: G is 3-intersecting 6-uniform | — | **UNVERIFIED**, pending an AK bound lookup; *not encoded, no compute* |

**Spread = exactly 2 (verified).** For 6-sets A,B ⊆ [10], |A∩B| = |A|+|B|−|A∪B| ≥ 6+6−10 = 2, so 2 is
the minimum possible intersection. Machine-checked this session alongside two further facts the WLOG
depends on: ordered spread pairs carry a **single** partition type (2,4,4,0), and there are exactly
**3150 = 10!/1152** of them — i.e. S₁₀ acts **transitively** on them, and the stabilizer
S₂×S₄×S₄ has order 1152 as designed. So Case A is genuinely **one** case up to S₁₀, and the
WLOG concretization is sound.

## Cube semantics

Both cubes extend the monolithic (10,2,1)@211 CNF (1013 x-vars / 170235 vars / 506481 clauses;
regenerated byte-identically to the 17:39 quarantined build) with `x_T = 0` for all |T| ≥ 8, plus:
leaf (0) a seqcounter cardinality ≥209 over the 210 size-6 vars; case (A) the two units `x_A = 0`,
`x_B = 0`. Case (A)'s cube is a *relaxation* of the leaf (it forbids A,B but constrains nothing else),
so its UNSAT would still soundly close the leaf — the cube is only ever weaker than the case.

## Rehearsal results (validation cell (10,2,1), target 211) — 2026-07-18

| cube | box | kissat | proof | drat-trim |
|------|-----|--------|-------|-----------|
| **leaf (0)** — m≤7 + f₆ ≥ 209 | 900 s | **UNSAT 0 s** | 841 KB | **exit 0, `s VERIFIED`** |
| **case (A)** — m≤7 + spread pair missing | 900 s | **TIMEOUT** | 1.67 GB (partial, invalid) | n/a |

Baselines this had to beat: monolithic (10,2,1) **>25 min unresolved**; un-anchored m≤7 cube
**TIMEOUT at 900 s**.

**Verdict: the complement anchor does not move the decisive leaf.** Leaf (0) is confirmed trivial (0 s,
certified) — but it was always expected to be, and it closes only the near-full corner. Case (A) hit
**the same 900 s wall as the un-anchored m≤7 cube**: two unit clauses out of 1013 variables did not
measurably dent the search. That is the honest read — the anchor bought nothing on the branch that
matters, exactly as max-size anchoring bought nothing in v1.

**Why, structurally.** Fixing one missing pair pins an *arrangement* only in a 12-element neighbourhood
of a 1013-variable problem, and it removes just the S₁₀ symmetry *between spread pairs* — the residual
stabilizer is still order 1152, and the symmetry among the ~200 remaining free size-6 sets is
untouched. The 1.67 GB partial proof (vs 73 MB for the whole certified n=9 cell) shows the solver
enumerating, not closing. Anchoring a *bounded-size* configuration inside an unbounded bulk appears to
be the recurring failure mode across v1 and v2: the hard core is the collective symmetry of the level-6
layer, and no O(1)-sized anchor reduces it.

## Standing

- Leaf (0): **closed** on the validation cell, DRAT-certified.
- Case (A): **NO-GO** at the rehearsal standard. No open-cell compute is justified on this design.
- Case (B): **not attempted.** Its premise (a bound on 3-intersecting 6-uniform families forcing g
  small) is unverified; per the design rule, no encoding until the AK lookup is done on a primary
  source.

**Open-cell compute remains NO-GO.** A third anchor design would need to reduce symmetry *collectively*
across the level-6 layer — e.g. an anchor whose size grows with the problem, or a genuine
canonical-form/lex-leader symmetry break — rather than pinning finitely many sets. That is a design
question, not a compute question, and route (ii)'s certified-SB tooling gap (see `TOOLING.md`) is the
standing obstacle to the lex-leader option.

## v2 addendum — the non-O(1) regime (case B-i, B-ii orbit count), 2026-07-18

The "no O(1) anchor helps" reading above was **correctly scoped down**: it covers anchors pinning
finitely many sets, not anchors whose size scales with the level. Case **B-i** tests the other regime —
it anchors **126 of the 210 level-6 variables positively**.

### B-i rehearsal (validation cell (10,2,1), target 211)

Cube: monolithic @211 + `x_T = 0` for all |T| ≥ 8 + **`x_T = 1` for all 126 six-sets T with 10 ∈ T**
(the "star of 10"). Premise self-contained: a sub-case by construction, so no Case-B tree
finalization or AK verification is needed to read the number.

| cube | box | kissat | proof | drat-trim |
|------|-----|--------|-------|-----------|
| **B-i** — m≤7 + star-of-10 present | 900 s | **UNSAT 0 s** | 5.0 MB | **exit 0, `s VERIFIED`** |

Baselines both TIMEOUT at 900 s: un-anchored m≤7, and case A. **B-i beats the wall outright** — the
first anchor in this campaign that does.

**Mechanism, measured.** The 126 positive units cascade through the antichain and 2-intersecting
constraints: 767 of the remaining variables are killed by one-step propagation, leaving **120 free
variables** (84 of size 6, 36 of size 7) out of the original 1013. That is the collective reduction an
O(1) anchor cannot produce, and it is the honest explanation of the 0 s.

**It is not a counting triviality.** After propagation the cube still admits 126 + 120 = **246 ≥ 211**
sets, so the target is *not* excluded by the trivial bound; the solver had to refute a genuine residual
problem, just a small one. The result is a real refutation, not an artifact of over-constraining.

**Calibration.** The star of 10 is close to the most propagation-friendly 126-set anchor available —
every member shares the element 10, maximising the comparability and low-intersection kills. One
maximally-structured leaf closing in 0 s does **not** establish that a full Case-B decomposition is
tractable; other leaves will reduce less sharply. What it does establish is that the **non-O(1) anchor
regime is alive**, which the v1/v2 O(1) results had left untested.

### B-ii orbit enumeration (pure counting, no SAT)

Triples (A,B,C) of 6-sets in [10] with |A∩B| = 3 (hence |A∪B| = 9, exactly one outside element e),
e ∈ C, |C∩A| ≥ 3, |C∩B| ≥ 3. Orbits counted exactly via the S₁₀-complete invariant for an ordered
tuple of subsets — the vector of 8 Venn-region sizes (no canonicalization search needed).

**1 612 800 ordered triples → 6 configuration types up to S₁₀** (4 up to the A↔B swap, under which
the constraints are symmetric).

| region sizes (ABC, AB!C, A!BC, A!B!C, !ABC, !AB!C, !A!BC, !A!B!C) | ordered triples |
|---|---:|
| (2,1,2,1,1,2,1,0) | 453 600 |
| (2,1,1,2,2,1,1,0) | 453 600 |
| (1,2,2,1,2,1,1,0) | 453 600 |
| (3,0,1,2,1,2,1,0) | 151 200 |
| (3,0,2,1,0,3,1,0) | 50 400 |
| (3,0,0,3,2,1,1,0) | 50 400 |

Every type has last region 0, as forced: |A∪B| = 9 and e ∈ C, so nothing lies outside A∪B∪C.
**A 6-way (or 4-way) split is small enough to be a practical case tree** if each leaf behaves like B-i.

### The propagation law (measured, 2026-07-18/19)

The B-ii leaf rehearsal was designed to test whether a *cleverer* anchor pattern helps. It does not,
and the measurement says why. **What governs is not anchor size but whether the anchor pins variables
TRUE.**

| cube | anchor | free vars (of 1013) | verdict |
|------|--------|--------------------:|---------|
| **B-i** | 126 **positive units** (star of 10 present) | **120** | **UNSAT 0 s**, `s VERIFIED` |
| case A | 2 negative units (missing pair) | 955 | TIMEOUT 900 s |
| B-ii L1 | 3 negative units, type (3,0,2,1,0,3,1,0) | 954 | TIMEOUT 600 s |
| B-ii L2 | 3 negative units, type (3,0,1,2,1,2,1,0) | 954 | TIMEOUT 600 s |
| f₆ ≥ 135 | cardinality, **positive but not unit** | 957 | TIMEOUT 600 s |
| leaf (0) f₆ ≥ 209 | cardinality, **positive, near-unit** | 957 | **UNSAT 0 s**, `s VERIFIED` |

**Mechanism.** Both structural constraint families — the antichain (k-Sperner) clauses and the
2-intersecting clauses — are **entirely negative**. A negative clause only fires once some variable is
set TRUE. Therefore:

- **Positive units cascade.** Forcing a set present immediately kills every comparable set (antichain)
  and every set meeting it in < t (intersecting), which kills further sets in turn. B-i's 126 units
  removed 767 more variables, collapsing 1013 → 120.
- **Negative units land in vacuum.** Forbidding a set fires nothing at all: it removes exactly the
  variables it names and no more. Case A (2 units → 955 free) and B-ii L1/L2 (3 units → 954 free) are
  the same measurement three times over, across three different intersection patterns. **No amount of
  cleverness in choosing *which* sets to forbid changes this** — it is a property of clause polarity,
  not of the configuration.

**Refinement — positivity is necessary but not sufficient; it must bite.** The f₆ ≥ 135 cube tested the
Hilton–Milner-licensed g ≤ 75 region as *positive pressure* rather than negative anchors. It **timed
out** (600 s, 958 MB partial proof, free = 957). A cardinality lower bound pins no variable, so it
propagates nothing; it only constrains the counter. So the operative distinction is not "positive vs
negative" but **"does the anchor force variables TRUE?"** — B-i does, f₆ ≥ 135 does not.

**But tightness converts pressure into propagation.** The *same encoder and same shape* at f₆ ≥ 209
(leaf 0) closes in 0 s, while f₆ ≥ 135 times out. Somewhere in **135 < b < 209** the constraint becomes
tight enough that the counter starts forcing level-6 variables TRUE and the cascade ignites. Locating
that threshold by bisection is a cheap, well-defined next experiment and is the most concrete design
lead this session produced.

### Design consequence

Any anchor for the m≤7 bulk must **force presence**, not absence, and must be tight enough to
propagate. The whole complement-anchor family (v2 case A, all six B-ii leaves) is negative by
construction and is therefore **dead as a tractability device**, independently of the Case-B
completeness question. B-i is the only member of the campaign that works, and it works because it is a
forced-presence anchor.

### Hilton–Milner licensing of the B-i WLOG, and the constant D

AK's Theorem 1.1 does **not** cleanly apply at (n,k,t) = (10,6,3): with k−t+1 = 4 and t−1 = 2, n = 10
is *exactly* the left endpoint of the r=3 regime, (k−t+1)(2+(t−1)/(r+1)) = 4(2+2/4) = 10, so the
boundary clause fires and asserts |Sl(F₃,₃;6)| = |Sl(F₃,₄;6)| — but F₃,₄ = {S ⊆ [11] : |S| ≥ 7} has an
**empty** 6-slice on [10], so the tie reads 84 = 0 and the uniqueness statement is unusable verbatim.

The clean route is **complementation to EKR**: for 6-sets in [10], |A∩B| ≥ 3 ⟺ |Aᶜ∩Bᶜ| ≥ 1
(8 − |Aᶜ∩Bᶜ| ≤ 7), machine-verified over all pairs. So 3-intersecting 6-uniform on [10] ↔ intersecting
4-uniform on [10], where n = 10 > 2k = 8 **strictly**:

- **max = C(9,3) = 84**, agreeing with the A_r computation (35, 55, 70, **84**);
- **uniqueness holds**: the unique optimum is a star, i.e. back in the original picture **all 6-subsets
  of a fixed 9-set** — exactly the B-i configuration.

**Hilton–Milner** at **(n,k) = (10,4)** — H consists of 4-subsets of [10] — then bounds non-trivial
families: HM(10,4) = C(9,3) − C(5,3) + 1 = 84 − 10 + 1 = **75**, giving the dichotomy

> **either G ⊆ the 6-subsets of some 9-set (= B-i, up to S₁₀), or g = |G| ≤ 75.**

So for **g ≥ 76 the B-i WLOG is forced, not assumed**; for g ≤ 75 it is **not** licensed and that region
needs separate treatment.

**D = 53.** In the g ≤ 75 leaf, the maximum number of missing sets through any single element:
deg_G(x) = |H_x| with H_x intersecting 4-uniform on the 9 points [10]\{x}. **Note the two HM
instantiations sit at different (n,k):** the 75 above is HM(10,4) because H lives on all of [10],
whereas the bound here is HM(9,4) because H_x lives on the 9 points [10]\{x}. (HM(9,4) = 53 ≠ 75;
the C(9,3) in the first has n−1 = 9, i.e. n = 10.) If H_x is non-star, HM on
(9,4) (strict 9 > 8) gives |H_x| ≤ C(8,3) − C(4,3) + 1 = 53; if H_x is a star through y, non-starness
of H forces a T ∋ x, y ∉ T meeting all of H_x, excluding C(5,3) = 10 members, so |H_x| ≤ 56 − 10 = 46.
Hence **D = 53**, attained by the HM family on [9] (size 53, intersecting, non-star, and machine-checked
**locally maximal**: none of the 126 4-sets can be added). *Scope: achievability and local maximality
are machine-checked; the exhaustive upper bound is cited to Hilton–Milner, not enumerated.*

**Consequence.** Two distinct floors, with different quantifiers — neither implies the other:

- **Worst case (HM, D = 53):** *every* element has deg_G(x) ≤ 53, so **every** star of F is at least
  (126 − 53)/126 ≈ 58 % present — **≥ 73 forced-present sets in every star**.
- **Averaging (pigeonhole):** g ≤ 75 and each missing 6-set covers 6 elements, so the degrees sum to
  6g ≤ 450 over 10 elements; the minimum is ≤ 45. Hence **some** star is **≥ 81/126 present**.

Given that 126 positive units drove 1013 → 120 free,
a forced 73 is a substantial positive-pressure handle, and it is *forced-presence* in the sense the
propagation law requires. **Not encoded; design item only.**

*Timing provenance: the host slept between runs during this session (an expired `caffeinate`), which
is why wall-clock stamps across the log are non-monotonic. It did not affect any measurement — every
boxed run was observed at ~99–100 % CPU against wall-clock while executing, so no cube was suspended
mid-box.*

### Standing after the addendum

- The **O(1)-anchor NO-GO stands** (v1 max-size, v2 case A).
- The **non-O(1) regime is not closed** — B-i is a certified 0 s win where every prior anchor timed out.
- Case B's completeness still rests on the **unverified AK bound**; that lookup remains the gate.
- **Open-cell compute remains NO-GO** regardless, per standing instruction.
