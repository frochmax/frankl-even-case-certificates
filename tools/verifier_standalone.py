#!/usr/bin/env python3
"""STANDALONE exact-integer verifier for the even-parity t-intersecting k-Sperner conjecture,
i.e. Frankl Conjecture 1.6 (EJC 93 (2021) 103279) = Balogh-Linz-Patkos Conjecture 1.7
(arXiv:2209.01656) = Yang-Zhang Conjecture 1.4 (arXiv:2607.03026). Given a family, checks that it
is t-intersecting and k-Sperner and reports its size against the conjectured maximum.
No imports from the model pipeline. Sets are Python frozensets of ints (exact arithmetic)."""
from itertools import combinations

def nCr(n, r):
    if r < 0 or r > n: return 0
    r = min(r, n-r); num = den = 1
    for i in range(r): num *= (n-i); den *= (i+1)
    return num // den

def conj_1_4_bound(n, t, k):
    # Computes the EVEN-CASE conjectured maximum  sum_{i=0}^{k-1} C(n, (n+t)/2 + i)
    # (Frankl Conj 1.6 / BLP Conj 1.7 / YZ Conj 1.4). Function name kept for compatibility.
    if (n+t) % 2 != 0 or n <= t: return None   # even case only: requires n+t even, n>t
    return sum(nCr(n, (n+t)//2 + i) for i in range(k))

def check(family, n, t, k, verbose=True):
    warnings = []
    # element-level hygiene BEFORE set coercion (hostile-referee hardening)
    for A in family:
        if len(list(A)) != len(set(A)): warnings.append(f"member {A} has repeated elements")
        for e in A:
            if not isinstance(e, int) or isinstance(e, bool):
                warnings.append(f"non-int element {e!r} in {A}")
    F = [frozenset(A) for A in family]
    r = {'warnings': warnings}
    r['distinct'] = len(set(F)) == len(F)
    if not r['distinct']: warnings.append("family contains duplicate sets")
    r['within_ground'] = all(A <= set(range(n)) for A in F)
    bad = [(sorted(A), sorted(B)) for A,B in combinations(F,2) if len(A & B) < t]
    r['t_intersecting'] = len(bad) == 0
    # longest strict chain (exact)
    S = sorted(F, key=len); dp = {}; longest = 0
    for A in S:
        best = 1
        for B in S:
            if len(B) < len(A) and B < A and dp[B]+1 > best: best = dp[B]+1
        dp[A] = best; longest = max(longest, best)
    r['longest_chain'] = longest
    r['k_sperner'] = longest <= k
    nd = len(set(F))                 # count DISTINCT sets (duplicates cannot inflate size)
    b = conj_1_4_bound(n, t, k)
    r['size'] = nd; r['raw_count'] = len(F); r['bound'] = b
    r['exceeds_bound'] = (b is not None and nd > b)
    props_ok = r['distinct'] and r['within_ground'] and r['t_intersecting'] and r['k_sperner']
    r['IS_VALID_FAMILY'] = props_ok
    r['IS_COUNTEREXAMPLE'] = props_ok and r['exceeds_bound']
    if verbose:
        for kk,vv in r.items(): print(f"  {kk}: {vv}")
        if bad[:1]: print("  first t-violation:", bad[0])
    return r

if __name__ == "__main__":
    ok = True
    print("T1 star {01,02,03} in [4], t=1,k=1 -> valid family, chain=1"); 
    r = check([[0,1],[0,2],[0,3]],4,1,1); ok &= r['IS_VALID_FAMILY'] and r['longest_chain']==1
    print("T2 {01,23} t=1 -> disjoint, FAIL t-intersecting")
    r = check([[0,1],[2,3]],4,1,1); ok &= (r['t_intersecting']==False)
    print("T3 chain {0<01<012}, k=2 -> chain 3, FAIL k-Sperner")
    r = check([[0],[0,1],[0,1,2]],3,1,2); ok &= (r['k_sperner']==False and r['longest_chain']==3)
    print("T4 exceeds: even bound n=8,t=2,k=2 =", conj_1_4_bound(8,2,2), "vs C(8,5)+C(8,6)=", nCr(8,5)+nCr(8,6))
    ok &= conj_1_4_bound(8,2,2) == nCr(8,5)+nCr(8,6)
    # T5: a family that IS a counterexample-shape (size>bound) with valid props (synthetic even case)
    #   n=4,t=2,k=1: bound=C(4,3)=4; family = all 3-subsets of [4] (4 sets) is 2-int antichain, size 4 = bound (NOT >). 
    print("T5 all 3-subsets of [4], t=2,k=1: bound", conj_1_4_bound(4,2,1), "size 4 -> valid, NOT exceeding")
    r = check([[0,1,2],[0,1,3],[0,2,3],[1,2,3]],4,2,1); ok &= r['IS_VALID_FAMILY'] and (r['exceeds_bound']==False)
    print("ALL VERIFIER TESTS PASSED" if ok else "SOME TEST FAILED"); 
    import sys; sys.exit(0 if ok else 1)
