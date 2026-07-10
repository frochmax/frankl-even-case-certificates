# Reproduce the certificates (< 10 minutes)

You need: Python 3 with `pysat` (`pip install python-sat`), and the two solvers
[`kissat`](https://github.com/arminbiere/kissat) and
[`drat-trim`](https://github.com/marijnheule/drat-trim) (build each from source; both are standard
`./configure && make` / `make`). Point the paths below at your builds.

## Option A — re-check the shipped certificates (fastest, no solving)
For the "≤ M" direction, verify the shipped DRAT proof directly:

    drat-trim certificates/even/9_3_2/cell_9_3_2_ge121.cnf \
              certificates/even/9_3_2/cell_9_3_2_ge121.drat
    echo "exit code: $?"     # 0 == VERIFIED  (this is the pass/fail signal)

For the "≥ M" direction, re-check the shipped witness with the independent verifier:

    python3 tools/check_witness.py certificates/even/9_3_2/witness_ge120.json 9 3 2 120
    echo "exit code: $?"     # 0 == valid t-intersecting k-Sperner family of size >= 120

Confirm nothing drifted:  `shasum -c SHA256SUMS`

## Option B — regenerate everything from source
This rebuilds the CNFs and re-solves (kissat is deterministic here):

    # UNSAT direction: max <= M  (example: (9,3,2), M=120, so encode ">= 121" and expect UNSAT)
    python3 tools/cert_cell.py 9 3 2        # builds CNFs, runs kissat + drat-trim + verifier

Expected for (9,3,2):
    kissat on ">= 121" : exit 20  (UNSATISFIABLE)
    drat-trim          : exit 0   (VERIFIED)      => maximum <= 120
    kissat on ">= 120" : exit 10  (SATISFIABLE)   => witness of size 120
    verifier on witness: valid t-intersecting 2-Sperner family, size 120  => maximum >= 120
    Therefore maximum = 120 (= the conjectured value).

Run `python3 tools/cert_cell.py <n> <t> <k>` for any certified cell; each writes a `RESULT.txt`.

## The encoding (what the CNF says)
Variables x_A for every A ⊆ [n] with |A| ≥ t (sizes < t are WLOG excluded: in a t-intersecting
family of ≥2 sets every member has size ≥ t). Clauses:
- t-intersecting: for each pair with |A∩B| < t, (¬x_A ∨ ¬x_B).
- k-Sperner: for each chain A₀⊊…⊊A_k, (¬x_{A₀} ∨ … ∨ ¬x_{A_k}).
- cardinality Σ x_A ≥ target, via a sequential-counter encoding (`pysat`).
UNSAT of the "≥ M+1" instance ⇒ no family exceeds M ⇒ maximum ≤ M.
