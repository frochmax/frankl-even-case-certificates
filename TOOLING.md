# TOOLING

Provenance of the SAT toolchain used to produce and re-verify the certificates in
this repository. This file is **documentation only** — it does not alter any
certificate bytes. Success criterion for a certified UNSAT direction is, and remains,
**`drat-trim` exit code 0** on the frozen `.cnf` + `.drat` pair.

## Build environment

| Component | Value |
|-----------|-------|
| Platform  | macOS 26.5.1, Apple Silicon (arm64) |
| Compiler  | Apple clang 21.0.0 (clang-2100.1.1.101) |
| Location  | `~/solvers/` (outside the repo; binaries are not committed) |

Both binaries are native `Mach-O arm64`, built from source and ad-hoc code-signed by
the local toolchain (verified with `codesign -dv`); no additional signing was needed
to execute them.

## Pinned solver versions

### kissat (SAT solver)
- Source: https://github.com/arminbiere/kissat
- Pinned commit: `8af8e56f174b778aef3aa45af9f739b2a5f492c2` ("bumped VERSION", 2025-10-16)
- Reported version: **4.0.4**
- Build: `./configure && make`
- Binary: `~/solvers/kissat/build/kissat`

### drat-trim (proof checker)
- Source: https://github.com/marijnheule/drat-trim
- Pinned commit: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (2024-11-25)
- Build: `make`
- Binary: `~/solvers/drat-trim/drat-trim`

## Sanity gate (re-verification of a frozen certificate)

On 2026-07-18 the freshly built `drat-trim` re-checked the frozen `(9,3,2)`
UNSAT-direction certificate:

```
drat-trim certificates/even/9_3_2/cell_9_3_2_ge121.cnf \
          certificates/even/9_3_2/cell_9_3_2_ge121.drat
```

Result: parsed 42211 variables / 220132 clauses, `s VERIFIED`, **exit code 0**
(~63 s). This confirms the deposited certificate remains valid under an independently
rebuilt checker and that the toolchain is correctly installed for future cells.

---

# n=10 pseudo-Boolean toolchain (Option B ruling, 2026-07-18)

For the n=10 cells the certification standard is **VeriPB pseudo-Boolean proofs
checked by the formally verified CakeML checker `cake_pb`** (dual-standard: the
n=9 cells remain DRAT/drat-trim, frozen and untouched). Built on macOS 26.5.1,
Apple Silicon (arm64), Apple clang 21.

## Build dependencies (Homebrew)
- Homebrew 6.0.11 at `/opt/homebrew` (arm64).
- **boost 1.90.0_1**, **gmp 6.3.0** (`brew install boost gmp`).
- CMake 4.4.0 (pip, in `~/solvers/pbenv`); cargo/rustc 1.96.1.

## Solver — RoundingSat (native pseudo-Boolean, VeriPB proof logging)
- Source: gitlab.com/MIAOresearch/software/roundingsat, commit **d4edbf7** (2026-03-03).
- Build: `cmake -DCMAKE_BUILD_TYPE=Release -Dsoplex=OFF -Dgmp=OFF .. && make`
  (SoPlex off — not needed for PB decision/UNSAT; non-GMP uses header-only cpp_int).
- **No source patch required.** The documented Apple-clang `__int128` `abs`
  ambiguity (gitlab issue #2) is already fixed upstream by an `#ifdef __APPLE__`
  block in `src/auxmath.hpp` (provides `abs`/`gcd`/`msb`/`pow` for `int128`).
- Native cardinality: constraints are stated directly in OPB (e.g. `+1 x1 ... >= k ;`);
  no sequential-counter encoding. Proof logging via `--proof-log=<file>` (VeriPB v2.0).

## Elaborator / pre-checker — VeriPB 3.0.2 (Rust)
- Source: gitlab.com/MIAOresearch/software/VeriPB, commit **4bb10c2**, version **3.0.2**.
- Build: `cargo build --release` -> `target/release/veripb` (no patch).
- Roles: (a) fast verification pre-check; (b) **`--elaborate` translates the solver's
  VeriPB proof into the kernel format that `cake_pb` consumes** (mandatory stage).
  Accepts RoundingSat's v2.0 proofs (auto-switches; emits v3.0 kernel).

## Trusted checker — cake_pb (formally verified, CakeML)
- Source: gitlab.com/MIAOresearch/software/cakepb, commit **904eed4**; ships
  pre-generated CakeML assembly. Build: `cc basis_ffi.c cake_pb_arm8.S -o cake_pb_arm8`
  (**builds and runs natively on arm64 Mach-O, no patch**).
- Provenance: CakeML `1dbe30334d...`, HOL4 `63f2eb9c...`, PolyML 5.9 (CakePB build 2026-04-13).
- **ACCEPTANCE CRITERION (rule 3 for n=10): stdout must contain `s VERIFIED
  UNSATISFIABLE`.** The exit code is NOT reliable — `cake_pb` returns 0 even on a
  rejected proof (it prints `c Checking failed ...`). Certification keys on the
  `s VERIFIED` line, never on exit status.

## Verified pipeline (toy gate, 2026-07-18)
20-variable native-cardinality UNSAT OPB (`sum >= 11` and `sum <= 10`):
```
roundingsat --proof-log=toy.pbp toy.opb           # s UNSATISFIABLE, VeriPB v2.0 proof
veripb --opb --elaborate toy.elab.pbp toy.opb toy.pbp   # s VERIFIED UNSATISFIABLE; kernel v3.0
cake_pb_arm8 toy.opb toy.elab.pbp                 # s VERIFIED UNSATISFIABLE   <-- TRUSTED
```
All three stages pass. Native-PB certification pipeline is functional on this machine.

## Certified symmetry breaking — BreakID (LIMITATION, blocks native-PB SB)
- Source: bitbucket.org/krr/breakid branch `veriPB`, commit **1f4df70**, BreakID 2.5.
- Build patches (its plain Makefile): `-std=c++11` -> `-std=gnu++17` (boost 1.90 needs
  >=C++14; gnu for BSD types), add `-Duint=unsigned` (saucy uses the BSD `uint`), add
  brew include/lib paths, drop `-static` (unsupported on macOS). Builds arm64.
- **veriPB proof emission works for CNF input only** (confirmed: 983-line lex-leader
  proof on pigeonhole). For **PB/OPB input it is unimplemented**: BreakID exits with
  "Logging is only implemented with CNF input (not with asp or pb input yet)".
- **Consequence:** certified symmetry breaking and native-PB cardinality are currently
  MUTUALLY EXCLUSIVE with this tooling. Native cardinality (RoundingSat/OPB) has no
  certified symmetry-breaking proof; certified symmetry breaking (BreakID) requires CNF
  input, which reintroduces clausal cardinality.

## n=10 certification standard (ruling 2026-07-18)
The baseline n=10 standard is: **native-PB OPB encoding (cardinality as first-class
constraints) -> RoundingSat with VeriPB proof logging -> `veripb --elaborate` to kernel
-> `cake_pb` as the trusted checker; acceptance = stdout contains
`s VERIFIED UNSATISFIABLE`.** Symmetry breaking is **NOT** part of the baseline standard.
It is a per-cell arsenal decision: if a specific cell needs it, use the BreakID/CNF route
(clausal cardinality, certified symmetry breaking) for that cell; revisit if BreakID
gains native-PB proof logging. The n=9 cells are unaffected (DRAT/drat-trim, frozen).

## Additional tools built 2026-07-18 (symmetry-breaking investigation; n=10 parked)

The n=10 open cells (10,2,k) are PARKED — see `PARKED_10_2_k.md`. The relevant toolchain state:

- **satsuma** (modern structure-based symmetry breaker): github.com/markusa4/satsuma commit
  **c6ad1b5** (v1.4, dejavu 2.1). Build: `cmake . && make satsuma` (dejavu auto-fetched). Builds
  arm64. `satsuma lex --proof-file <f> --veripb <cnf>` emits **VeriPB version 3.0** (modern
  `red ... : x->0` substitution steps) — **its SB prefix parses cleanly in our `veripb` 3.0.2**.
  Proof output is marked "experimental" upstream. AAAI'26 pinned source: Zenodo 10.5281/zenodo.17607863.
- **VeriPB (Rust)**: gitlab.com/MIAOresearch/software/VeriPB, **v3.0.2**, commit 4bb10c2
  (`cargo build --release`). Elaborates v2.0/v3.0; rejects v1.2.
- **pboxide** (paper's VeriPB, "VeriPB rewritten in Rust", **v0.2.0**): AAAI'26 Zenodo
  10.5281/zenodo.17608873 (`cargo build -p pboxide-veripb`). Behaves like `veripb` 3.0.2 on our tests.
- **cake_pb** OPB frontend `cake_pb_arm8` and CNF frontend `cake_pb_cnf_arm8`: both built from the
  shipped ARMv8 assembly (`cc basis_ffi.c cake_pb*_arm8.S`), run native arm64. CakePB AAAI'26 Zenodo
  10.5281/zenodo.17609070.
- **kissat_fork** (MIAO, commit a6443a0, 2023): emits an OLD VeriPB v2.0 dialect (`f` with no count)
  that `veripb` 3.0.2 rejects. Not usable.

**Composition failure point (recorded for resumption):** a full certified UNSAT proof = satsuma's
v3.0 SB prefix + a SAT solver's refutation proof, composed and checked against the original CNF. Our
only compatible solver, RoundingSat, emits VeriPB **v2.0**; splicing satsuma's v3.0 prefix with
RoundingSat's v2.0 body is rejected by BOTH `veripb` 3.0.2 and pboxide 0.2.0 at the solver's `p`
(v2.0 cutting-planes abbreviation) — `Expected a top level rule name ... but found 'p'`. **Blocker:
no VeriPB-3.0-emitting SAT solver is available on arm64** (RoundingSat=v2.0; kissat/CaDiCaL=DRAT/LRAT;
kissat_fork=2023-broken; the AAAI'26 artifacts bundle no solver and no DRAT->VeriPB bridge). See
`PARKED_10_2_k.md` for the resumption condition.
