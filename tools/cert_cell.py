#!/usr/bin/env python3
import sys, itertools, subprocess, os, re, time
sys.path.insert(0,'.')
from math import comb
from pysat.card import CardEnc, EncType
from verifier_standalone import check
K="tools/kissat/build/kissat"; D="tools/drat-trim/drat-trim"
CERTROOT="/Users/maxfroch/Desktop/conj-refute/certificates/even"
def pc(x): return bin(x).count('1')
# even-parity formula only; all certified cells here have n+t even
# Conjectured even-case maximum (Balogh–Linz–Patkós, arXiv:2209.01656):
# the sum of the k largest set-size "layers", C(n,(n+t)/2+i) for i=0..k-1.
def conj_bound(n,t,k): return sum(comb(n,(n+t)//2+i) for i in range(k))

def build_cnf(n,t,k,target,path):
    # Variable universe: one Boolean per subset of [n] of size t..n
    # (bitmask representation). Sets of size < t are excluded WLOG —
    # see README, "Verification standard". One variable per set: x_A = 1
    # iff A is in the family.
    verts=[sum(1<<i for i in c) for s in range(t,n+1) for c in itertools.combinations(range(n),s)]
    xid={v:i+1 for i,v in enumerate(verts)}; sz={v:pc(v) for v in verts}; N=len(verts)
    # t-intersecting: for every pair with |A ∩ B| < t (bitwise AND +
    # popcount), forbid selecting both. Enforces |A ∩ B| >= t for all
    # pairs in the family.
    cl=[[-xid[a],-xid[b]] for a,b in itertools.combinations(verts,2) if pc(a&b)<t]
    vbs={}
    for v in verts: vbs.setdefault(sz[v],[]).append(v)
    # k-Sperner: enumerate every strict containment chain of exactly k+1
    # sets (sizes strictly increasing, containment = bitmask test) and
    # forbid selecting all k+1. Bans all chains of length k+1, including
    # non-consecutive jumps.
    def ext(ch):
        if len(ch)==k+1: cl.append([-xid[v] for v in ch]); return
        for s2 in range(sz[ch[-1]]+1,n+1):
            for v in vbs.get(s2,[]):
                if (ch[-1]&v)==ch[-1]: ext(ch+[v])
    for v in verts: ext([v])
    # Cardinality: require at least `target` sets selected (PySAT
    # sequential counter; auxiliary vars start above N). UNSAT at
    # target = bound+1 proves max <= bound.
    card=CardEnc.atleast(lits=list(xid.values()),bound=target,top_id=N,encoding=EncType.seqcounter)
    allc=cl+card.clauses
    with open(path,'w') as f:
        f.write(f"p cnf {card.nv} {len(allc)}\n")
        for c in allc: f.write(" ".join(map(str,c))+" 0\n")
    return N, verts

def cert(n,t,k):
    bound=conj_bound(n,t,k); r=(n-t)//2
    d=f"{CERTROOT}/{n}_{t}_{k}"; os.makedirs(d,exist_ok=True)
    log=open(f"{d}/RESULT.txt","w")
    def P(*a): print(*a); print(*a,file=log); log.flush()
    P(f"=== CELL (n,t,k)=({n},{t},{k})  bound(conjectured max)={bound}  r=(n-t)/2={r}  @ {time.strftime('%F %T')} ===")
    # ---- UNSAT direction: family of size >= bound+1 is impossible ----
    # UNSAT direction: kissat exit 20 + drat-trim exit 0 certifies that
    # no valid family of size >= bound+1 exists.
    cu=f"{d}/cell_{n}_{t}_{k}_ge{bound+1}.cnf"; pu=f"{d}/cell_{n}_{t}_{k}_ge{bound+1}.drat"
    build_cnf(n,t,k,bound+1,cu)
    t0=time.time(); ec=subprocess.run([K,"-q",cu,pu],capture_output=True).returncode; ku=time.time()-t0
    t0=time.time(); dr=subprocess.run([D,cu,pu],capture_output=True,text=True); dec=dr.returncode; du=time.time()-t0
    open(f"{d}/drat_ge{bound+1}.log","w").write(dr.stdout+dr.stderr)
    P(f"[UNSAT dir] kissat ge{bound+1}: exit={ec}(20=UNSAT) {ku:.1f}s | drat-trim EXIT={dec} ({'VERIFIED' if dec==0 else 'FAIL'}) {du:.1f}s")
    unsat_ok = (ec==20 and dec==0)
    # ---- SAT direction: family of size >= bound exists (bound is achieved) ----
    # SAT direction: decode witness (positive literals <= N only,
    # excluding cardinality auxiliaries), then re-check it with the
    # independent verifier (no shared encoding logic).
    cs=f"{d}/cell_{n}_{t}_{k}_ge{bound}.cnf"
    _,verts=build_cnf(n,t,k,bound,cs)
    rs=subprocess.run([K,cs],capture_output=True,text=True); secode=rs.returncode
    true=set()
    for line in rs.stdout.splitlines():
        if line.startswith('v'):
            for tok in line.split()[1:]:
                m=re.match(r'^-?(\d+)$',tok); 
                if m and int(tok)>0 and int(tok)<=len(verts): true.add(int(tok))
    fam=[[b for b in range(n) if verts[j-1]>>b&1] for j in sorted(true)]
    chk=check(fam,n,t,k,verbose=False)
    import json; open(f"{d}/witness_ge{bound}.json","w").write(json.dumps(fam))
    sat_ok=(secode==10 and chk['IS_VALID_FAMILY'] and chk['size']>=bound)
    P(f"[SAT dir]  kissat ge{bound}: exit={secode}(10=SAT) | witness size={chk['size']} valid_family={chk['IS_VALID_FAMILY']} tint={chk['t_intersecting']} k_sperner={chk['k_sperner']} (>= bound {bound}: {chk['size']>=bound})")
    P(f"CELL RESULT: UNSAT-dir certified={unsat_ok}  SAT-dir verified={sat_ok}  => BOTH-DIRECTIONS={unsat_ok and sat_ok}")
    log.close()
    return unsat_ok and sat_ok

if __name__=="__main__":
    n,t,k=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    ok=cert(n,t,k)
    open(f"{CERTROOT}/{n}_{t}_{k}/DONE","w").write("OK" if ok else "FAIL")
