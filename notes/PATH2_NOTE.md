# Path 2, direction 1 — stability for Milner's theorem at t=2, n=10

**DRAFT, local, 2026-07-19. Literature recon only. No encoding, no compute, nothing pushed.**

Motivation: the g ≤ 75 leaf (see `ANCHOR_NOTE.md`) needs a splitting variable **orthogonal to
set-membership**. At k=2, Mirsky gives F = A₁ ⊔ A₂ with both A_i antichains; each A_i ⊆ F is
therefore also 2-intersecting, so Milner caps each at C(10,6) = 210, and |F| ≥ 331 forces
**|A_i| ≥ 331 − 210 = 121** for both. The design hope was that 121 (= 57.6 % of Milner's max)
forces structural rigidity that names positive units per antichain.

## 1. Milner's theorem and the extremal level — verified, four independent statements

The bound is stated identically across all primary/secondary sources found, in two dual
formulations. **t-intersecting form**, Patkós survey Thm 0.1 and Balogh–Linz–Patkós Thm 1.5,
verbatim:

> **Theorem (Milner).** If F ⊆ 2^[n] is a t-intersecting antichain, then |F| ≤ C(n, ⌊(n+t+1)/2⌋).

Yang–Zhang (arXiv:2607.03026) state it verbatim the same way. **s-union form**, "Analogues of
Katona's and Milner's Theorems for two families" (arXiv:2006.12602) Thm 1.8, verbatim:

> **Theorem 1.8 (Milner [4])** Fix n > s > 0 and let F ⊂ 2^X be an s-union antichain. Then
> |F| ≤ C(n, ⌊s/2⌋).

**Level check, confirmed by both routes.** t-intersecting: ⌊(n+t+1)/2⌋ = ⌊13/2⌋ = **6**,
C(10,6) = 210. s-union (F t-intersecting ⟺ F^c is (n−t)-union, s = 8): ⌊8/2⌋ = **4**,
C(10,4) = 210, complementing back to level 6. The level is **6**, as the question supposed.

## 2. Uniqueness — NOT stated anywhere found. The omission is systematic.

**No source found states an equality characterization for Milner's theorem.** This is not an
absence of evidence; the sources make the omission conspicuous by decorating the *neighbouring*
theorems and leaving Milner bare. Three instances:

- **BLP** state Sperner (Thm 1.3) as "|F| ≤ C(n,⌊n/2⌋). *Furthermore, equality holds only if F is
  one of the largest layers in the Boolean lattice 2^[n].*" and Frankl's intersecting k-Sperner
  theorem (Thm 1.6) with a full two-case "*equality holds only if …*". Their **Milner (Thm 1.5) has
  no such clause.**
- **arXiv:2006.12602** states Sperner (Thm 1.7) as "with *strict inequality unless* F = (X choose
  ⌊n/2⌋) or F = (X choose ⌈n/2⌉)", then **Milner (Thm 1.8) immediately after, bare.**
- **Patkós survey** likewise: Thm 0.2 (Frankl) and Thm 0.3 (BLP) carry "equality holds only if" /
  "if and only if"; **Thm 0.1 (Milner) does not.**

The one uniqueness statement in this family that *does* exist is **BLP's own even-case theorem**,
and it is unusable here: Patkós's survey renders it as "*Furthermore equality holds if and only if
F = ⋃_{i=0}^{k−1} ([n] choose (n+t)/2 + i)*" — but it is gated on "**n is large enough**"
(BLP Thm 1.10 as published carries no uniqueness clause at all, only the bound). n₀(t,k) is
**ineffective**; n=10 is not known to be inside it. This is the same gate already recorded in
`STATUS_10_2_k.md`.

**Honest read:** the uniqueness of the level-6 family as the unique maximum 2-intersecting
antichain in 2^[10] is *plausible and unstated*. It is not available for citation.

## 3. Stability — no off-the-shelf theorem reaches our parameters

Searched: Frankl stability papers, Hilton–Milner analogues, Gerbner/Patkós-school results, and
2010–2026 work citing Milner 1968. Nothing of the form "a t-intersecting antichain of size
≥ (1−ε)·max is contained in / close to the extremal family" was found **for t-intersecting
antichains in 2^[n]**. The near misses, and why each misses:

| candidate | what it does | why it misses |
|---|---|---|
| Shan–Zhou, *Suboptimal s-union families and s-union antichains* (Discrete Math. 2023, arXiv:2207.06727) | determines optimal **and suboptimal** (= second-largest) s-union antichains — exactly the right *shape* of theorem | **vector spaces only** (subspaces of F_q^n), not 2^[n]. Their own abstract notes that for the ambient problem "*the structures of optimal ones have not been displayed*". |
| Frankl–Wang, *The overflow in the Katona Theorem* (arXiv:2506.05704) | near-extremal structure for Katona's s-union theorem | range **n ≥ 6r** or **n > 3.5r**; ours is n=10, r=4, needing n > 14. **Out of range.** |
| Hilton–Milner and its many descendants | stability for **EKR** (uniform, intersecting) | wrong theorem — uniform families, not antichains in 2^[n]. (Already exploited in `ANCHOR_NOTE.md` where it *does* apply, via complementation.) |
| BLP Thm 1.10 uniqueness | exact equality case, even n+t | ineffective n₀; and it is *equality only*, not stability. |

**Strongest available statement, and it is not a stability theorem.** Nothing bounds a family of
size 121 away from arbitrary.

## 4. What the literature DOES give: two genuine rungs, and one trap

### Rung A (real, applicable, no range restriction) — the shade inequality

BLP Lemma 2.2, attributed to Milner [7], with the sharper constant visible in their proof
(via Katona's shadow t-intersection theorem, BLP Thm 2.1, which has **no** range condition):

> For i ≤ ⌊(n+t−1)/2⌋, if F ⊆ 2^[n] is t-intersecting, then |∇_{i+1}(F_i)| ≥ |F_i|.

Their proof actually yields the stronger **|∇_{i+1}(F_i)| ≥ ((n−i)/(i−t+1))·|F_i|**. At n=10,
t=2 this applies for **i ≤ 5**, with factor (10−i)/(i−1): 2× at i=4, 1.25× at i=5.

**Sharpening for antichains (elementary, ours).** If F is also an antichain, ∇_{i+1}(F_i) contains
no member of F (any such set would contain a member of F). So ∇_{i+1}(F_i) and F_{i+1} are
**disjoint**, giving a linear level-profile constraint:

> ((10−i)/(i−1))·|F_i| + |F_{i+1}| ≤ C(10, i+1)  for i ≤ 5.

This is a **forced level-profile** statement — the thing the question asked for — obtained from
primary sources with no largeness gate. It is the first genuinely usable rung.

### Rung B — the "push to the middle" lemma, and why it is a TRAP

Patkós survey Lemma 8 / BLP §2.1 compression: for any t-intersecting k-Sperner F there **exists**
G with |F| ≤ |G| and G supported on levels ⌈(n+t)/2⌉−k+1 … ⌈(n+t)/2⌉+2(k−1) — at (10,2,2),
levels **5…8**.

**This does not constrain F.** G is a *different* family. The lemma is a bound-transfer device,
not a structure theorem about the family we hold. Recording it explicitly so it is not
mis-cited later as "our antichains live on levels 5–8." **They are not known to.**

## 5. Assessment of the bespoke ladder — and a serious headwind

### The first rung (M₋₆) is knife-edge, not comfortable

The proposed rung: M₋₆ := max 2-intersecting antichain in 2^[10] avoiding level 6; if M₋₆ < 121
then every A_i must touch level 6.

**M₋₆ ≥ 120, by an explicit witness: all of level 7.** C(10,7) = 120; two 7-subsets of [10] meet
in ≥ 4 ≥ 2, it is an antichain, and it avoids level 6. It is also maximal among level-6-avoiding
families (any 8-set contains a 7-set; any 5-set is contained in a 7-set — both comparable).

So the rung **requires M₋₆ = 120 exactly**. The margin against the needed strict inequality
M₋₆ < 121 is **one single set**. This is computable (and looks tractable by the cyclic-permutation
weight argument that Patkós's survey gives in full for Milner, re-run with level 6 deleted), but it
is not a comfortable rung — it either barely holds or fails outright, and nothing in the
literature predicts which.

### The decisive headwind: 121 is on the wrong side of our own measured ignition threshold

This is the finding that most affects the direction, and it comes from this campaign's own data,
not the literature. `ANCHOR_NOTE.md` establishes the **propagation law** and the measured
**ignition threshold**: cardinality pressure converts into forced-TRUE variables only near
saturation — global ignition b\* ∈ (185, 190] of 210 (**~90 %**), star-local s\* ∈ (110, 126] of
126 (**87–100 %**). Floors at 73/126 (58 %) and 81/126 (64 %) were probed and measured
**out of reach**; even 110/126 (87 %) timed out.

**|A_i| ≥ 121 of 210 is 57.6 % saturation** — numerically the *same regime* as the 58 % every-star
floor already measured far below ignition, and roughly 32 percentage points below the global
ignition bracket.

Therefore: **a stability theorem that delivers a size (121, or any constant fraction near it) is
dead on arrival** — the campaign has already measured that cardinality pressure at that fraction
does not propagate. Only a stability theorem delivering **structure** — containment in a *named*
family, as Hilton–Milner does for g ≥ 76 and B-i exploits — would produce forced-present units.
That is precisely the kind of statement §2 and §3 establish **does not exist** at (n,t) = (10,2).

## 6. Verdict (three lines)

1. **Off-the-shelf stability: DOES NOT EXIST at (n,t)=(10,2).** No equality characterization for
   Milner is stated in any source found (BLP Thm 1.5, Patkós Thm 0.1, arXiv:2006.12602 Thm 1.8 all
   bare, while adjacent theorems carry explicit "equality only if"); the only uniqueness statement
   in the family (BLP even case) is gated on an ineffective n₀, and the only genuine
   suboptimal-structure theorem (Shan–Zhou 2023) is for vector spaces, not 2^[n].
2. **Bespoke ladder: TRACTABLE BUT THIN.** Two rungs are literature-given and gate-free — the
   Katona-shadow/Milner shade inequality |∇_{i+1}(F_i)| ≥ ((n−i)/(i−t+1))|F_i| for i ≤ 5, which
   with the antichain-disjointness sharpening yields real level-profile inequalities; and Milner's
   cyclic-permutation weight argument, re-runnable with a level deleted to compute M₋₆ by hand.
   But the first rung is knife-edge (M₋₆ ≥ 120 by an explicit witness; it must equal 120 exactly),
   and "push to the middle" is a trap that constrains a different family, not ours.
3. **Direction WEAKENS — on measurement, not on literature.** Even a successful ladder would
   output a *cardinality* fact at 121/210 = 57.6 % saturation, which sits in the regime this
   campaign has already measured as far below ignition (b\* ~90 %; the 58 % and 64 % floors were
   probed and timed out). Path 2 direction 1 only becomes viable if it can be redirected to
   produce **forced containment in a named family** rather than a size bound — and no such theorem
   exists at these parameters.

**Recommendation: do not compute M₋₆ yet.** It is cheap, but its value is only decision-relevant
if the ladder's *output* is redesigned to be structural. Resolve that design question first.

---

*Recon scope: literature only. No encoding, no solver run, no certificate touched, nothing pushed.
This file is not in `SHA256SUMS` (draft, not frozen).*
