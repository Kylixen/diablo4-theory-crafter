//! Browser-facing query layer over the graph SQLite database, built with
//! `sqlite-wasm-rs`. Not yet implemented — this is a build-verification stub.

use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}
