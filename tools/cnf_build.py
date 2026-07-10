import itertools, time, sys
from math import comb
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
def pc(x): return bin(x).count("1")
def conj_bound(n,t,k):
    if (n+t)%2==0: return sum(comb(n,(n+t)//2+i) for i in range(k))
    q=(n+t-1)//2; return comb(n-t,q-t)+sum(comb(n,q+i) for i in range(1,k+1))-comb(n-t,q+k-t)

def build_cnf(n,t,k, materialize_chains=True):
    verts=[sum(1<<i for i in c) for s in range(t,n+1) for c in itertools.combinations(range(n),s)]
    sz={v:pc(v) for v in verts}
    xid={v:i+1 for i,v in enumerate(verts)}   # DIMACS vars 1..N
    N=len(verts)
    clauses=[]
    # t-intersecting: forbid both of a <t-meeting pair
    npair=0
    for a,b in itertools.combinations(verts,2):
        if pc(a&b)<t: clauses.append([-xid[a],-xid[b]]); npair+=1
    # k-Sperner: forbid every (k+1)-chain
    nchain=0
    if materialize_chains:
        vbs={}
        for v in verts: vbs.setdefault(sz[v],[]).append(v)
        def extend(ch):
            nonlocal nchain
            if len(ch)==k+1:
                clauses.append([-xid[v] for v in ch]); nchain+=1; return
            last=ch[-1]
            for s2 in range(sz[last]+1,n+1):
                for v in vbs.get(s2,[]):
                    if (last&v)==last: extend(ch+[v])
        for v in verts: extend([v])
    # cardinality: at least target = bound+1 selected
    target=conj_bound(n,t,k)+1
    card=CardEnc.atleast(lits=list(xid.values()), bound=target, top_id=N, encoding=EncType.seqcounter)
    card_clauses=card.clauses
    aux=card.nv - N
    return dict(N=N, npair=npair, nchain=nchain, ncard=len(card_clauses), aux=aux,
                total_vars=card.nv, total_clauses=npair+nchain+len(card_clauses),
                clauses=clauses+card_clauses, target=target)

if __name__=="__main__":
    import sys
    _run=True
# ---- VALIDATE on n=9    ,t=3,k=2 (known INFEASIBLE => CNF must be UNSAT) ----
    t0=time.time(); c=build_cnf(9,3,2); bt=time.time()-t0
    print(f"[n=9 t=3 k=2] xvars={c['N']} aux(card)={c['aux']} total_vars={c['total_vars']} | "
          f"pair_cl={c['npair']} chain_cl={c['nchain']} card_cl={c['ncard']} total_cl={c['total_clauses']} | build {bt:.1f}s target={c['target']}")
    from pysat.solvers import Cadical153
    s=Cadical153(bootstrap_with=c['clauses']); t0=time.time(); sat=s.solve(); st=time.time()-t0
    print(f"[n=9 VALIDATE] Cadical result: {'SAT (BUG!)' if sat else 'UNSAT (correct = HOLDS)'} in {st:.1f}s")
    s.delete()

    # ---- ESTIMATE for n=11,t=3,k=2 (build sizes, do NOT solve) ----
    t0=time.time(); c=build_cnf(11,3,2); bt=time.time()-t0
    print(f"[n=11 t=3 k=2] xvars={c['N']} aux(card)={c['aux']} total_vars={c['total_vars']} | "
          f"pair_cl={c['npair']} chain_cl={c['nchain']} card_cl={c['ncard']} total_cl={c['total_clauses']} | build {bt:.1f}s target={c['target']}")
