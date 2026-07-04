# Graph

Rust workspace, two crates:

- `graph-core` — native binary (`build-graph`) that reads
  [`characters/`](../characters/) and [`knowledge/`](../knowledge/) and
  builds `data/graph.sqlite` (nodes/edges tables). Generated, not committed.
- `graph-wasm` — compiled to `wasm32-unknown-unknown` via
  [`sqlite-wasm-rs`](https://crates.io/crates/sqlite-wasm-rs), loads
  `graph.sqlite` and answers queries client-side. Consumed by
  [`site/`](../site/).

Neither crate's actual graph logic is implemented yet — this is a build
scaffold (workspace + `Cargo.toml`s + stub entry points) to confirm the
toolchain works before writing the real parsing/query code.

## Building

Requires a Rust toolchain (not yet installed in this environment) plus the
`wasm32-unknown-unknown` target for `graph-wasm`:

```
rustup target add wasm32-unknown-unknown
cargo build -p graph-core
cargo build -p graph-wasm --target wasm32-unknown-unknown
```
