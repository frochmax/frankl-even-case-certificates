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
