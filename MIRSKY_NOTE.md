# Mirsky height-label encoding of the k-Sperner constraint

The n=10 pseudo-Boolean encoding does **not** materialize one clause per (k+1)-chain (which
explodes: millions of clauses for k=3,4). Instead it encodes the k-Sperner property with
**height labels**, justified by a classical theorem of Mirsky. This note states the theorem, proves
the two-direction equivalence the encoding relies on, and — in the same spirit as the size-`<t`
WLOG note in `README.md` — states **explicitly which certified direction depends on it**.

## The classical theorem

> **Mirsky's theorem** (L. Mirsky, *A dual of Dilworth's decomposition theorem*, American
> Mathematical Monthly **78** (1971), 876–877). In any finite poset, the maximum length of a chain
> equals the minimum number of antichains needed to cover the poset.

Equivalently, a poset has no chain of `k+1` elements **iff** it can be partitioned into `k`
antichains, **iff** it admits a *height labelling* `ℓ` into `{1,…,k}` that is strictly increasing
along the order.

## Setup

Let `F ⊆ 2^[n]` be a family of sets, partially ordered by inclusion `⊊`. `F` is **k-Sperner** if it
contains no chain `A_0 ⊊ A_1 ⊊ … ⊊ A_k` of `k+1` sets. A **height labelling** is a map
`ℓ : F → {1,…,k}` such that `A ⊊ B ⇒ ℓ(A) < ℓ(B)` for all comparable `A,B ∈ F`.

**Claim (the equivalence the encoder uses).** `F` is k-Sperner **iff** it admits a height labelling
`ℓ : F → {1,…,k}`.

### (⇐) A labelling forbids a (k+1)-chain (pigeonhole — the direction the UNSAT proof needs)

Suppose `ℓ : F → {1,…,k}` is strictly increasing along `⊊`. Take any chain
`A_0 ⊊ A_1 ⊊ … ⊊ A_m` in `F`. Then `ℓ(A_0) < ℓ(A_1) < … < ℓ(A_m)` are `m+1` strictly increasing
integers, all lying in `{1,…,k}`, so `m+1 ≤ k`, i.e. `m ≤ k−1`. Hence `F` has no chain of `k+1`
sets: `F` is k-Sperner. (This direction is elementary and does **not** use Mirsky; it is pure
pigeonhole.)

### (⇒) A k-Sperner family has such a labelling (this is Mirsky's theorem)

Suppose `F` is k-Sperner. For `A ∈ F` define
`ℓ(A) = ` (the number of sets in a longest chain of `F` whose top element is `A`).
Then `1 ≤ ℓ(A)`, and if `A ⊊ B` any longest chain ending at `A` extends by appending `B`, so
`ℓ(B) ≥ ℓ(A)+1 > ℓ(A)`. Because `F` has no chain of `k+1` sets, every chain has at most `k` sets, so
`ℓ(A) ≤ k`. Thus `ℓ : F → {1,…,k}` is a valid height labelling. (This is exactly Mirsky's
dual-of-Dilworth construction.)

∎

## What the encoding does, and which direction depends on Mirsky

For each candidate set `A` (of size `≥ t`) the encoder introduces the selection variable `x_A` and
a thermometer of label bits `L_{A,j} = [ℓ(A) ≥ j]`, with `L_{A,1} := x_A`. It posts:
monotonicity `L_{A,j} ≥ L_{A,j+1}`; and, for **every comparable pair** `A ⊊ B` (both of size `≥ t`)
and every level `j`, the implication `x_A ∧ x_B ∧ (ℓ(A) ≥ j) ⇒ (ℓ(B) ≥ j+1)` — i.e. a strictly
increasing labelling on the selected comparable pairs, with only `k` levels available. By the Claim,
a selection `{A : x_A = 1}` extends to a satisfying label assignment **iff** that selection is
k-Sperner.

- **UNSAT direction (`≤ M`, the certified bound).** "No k-Sperner, t-intersecting family of size
  `≥ M+1` exists" is certified by the OPB being UNSAT at cardinality `M+1`. This relies on the
  **(⇒) direction = Mirsky's theorem**: if some size-`≥M+1` selection were k-Sperner, Mirsky
  guarantees a label assignment satisfying the OPB, contradicting UNSAT. So **the UNSAT certificate
  depends on this classical, human-proved theorem** — exactly as the `≤ M` claim already depends on
  the size-`<t` WLOG reduction. It does *not* depend on trusting the encoder's chain logic, because
  there is no chain enumeration.
- **SAT / witness direction (`≥ M`).** Independent of Mirsky and of the label variables. The witness
  is decoded from the `x_A` variables only; `tools/verifier_standalone.py` recomputes the longest
  chain directly (exact arithmetic) and checks the family is t-intersecting and k-Sperner of size
  `≥ M`. A bug in the label encoding cannot produce a false witness.

Mirsky's theorem is classical and widely reproduced; we cite it rather than re-prove it in a
machine-checked form, and record here the exact reliance so a referee can audit it.
