#!/usr/bin/env python3
"""Independent witness checker. Usage: check_witness.py <family.json> n t k min_size
Exit 0 iff the family is a valid t-intersecting k-Sperner family of size >= min_size."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier_standalone import check
fam=json.load(open(sys.argv[1])); n,t,k,ms=map(int,sys.argv[2:6])
r=check(fam,n,t,k,verbose=True)
ok = r['IS_VALID_FAMILY'] and r['size']>=ms
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
