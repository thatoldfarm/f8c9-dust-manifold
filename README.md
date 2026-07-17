# f8c9-dust-manifold

## Overview
The **f8c9 Dust Manifold** is a series of experimental scripts designed to encode binary artifacts into the transcendental fabric of $\pi$. By treating the digits of $\pi$ as a universal read-only memory (ROM), these scripts can represent any file as a set of coordinates, effectively "hiding" the data in the fundamental constants of the universe.

## 🚀 Version History & Script Descriptions

| Script | Name | Primary Innovation | Description |
| :--- | :--- | :--- | :--- |
| **v0** | `monstrous_moonshine_v0.py` | **The Genesis** | The original PoC. Uses simple Base-100k packing to store 8 indices. Hardcoded for single-file testing. |
| **v00** | `monstrous_moonshine_v00.py` | **Batch Processing** | First "Pipeline" version. Introduces directory scanning and filename preservation in the ledger. |
| **v1** | `monstrous_moonshine_v1.py` | **Cantor Pairing** | The prototype. Uses Cantor pairing to fold 8 $\pi$-indices into a single singularity. Uses GZIP and Base62. |
| **v1.1** | `monstrous_moonshine_v1_1.py` | **Szudzik Folding** | Introduces the Szudzik pairing function (more space-efficient) and adds support for `zstandard` (Zstd) compression. |
| **v2** | `monstrous_moonshine_v2.py` | **Elegant Refinement** | A streamlined version of the "Elegant Dust" concept, focusing on stability and the E8 Lie Group symmetry (8-node folding). |
| **v3** | `monstrous_moonshine_v3.py` | **Zstd Hybrid** | A polished version of v1.1, optimizing the interaction between Zstd compression and the recursive Szudzik tree. |
| **v4** | `monstrous_moonshine_v4.py` | **Hypersphere Volume** | Adds a conceptual layer where the file's binary mass is represented as the volume of an $n$-dimensional hypersphere in the ledger. |
| **v5** | `monstrous_moonshine_v5.py` | **SquashFS Integration** | **The System Encoder.** Instead of one file, it uses `mksquashfs` to compress an entire folder into a filesystem image, then encodes that image into $\pi$. |
| **v6** | `monstrous_moonshine_v6.py` | **Sovereign Leylines** | Replaces Base62 with a **Base-256 Unicode Alphabet**. The ledger now contains runes, alchemy symbols, and math glyphs for maximum density. |
| **v7** | `monstrous_moonshine_v7.py` | **Adaptive Resolution** | Introduces `HEX_CHUNK_SIZE`. Instead of mapping 1 byte at a time, it can map 3 or 6 hex digits per index, drastically reducing the ledger size. |
| **v8** | `monstrous_moonshine_v8.py` | **Omniversal Engine** | **The Final Form.** Combines Adaptive Resolution, Leyline Alphabet, and **2-adic Modular Caching** to speed up the BBP calculations. |

## 🛠 Technical Workflow

1. **Compression:** File $\rightarrow$ `Zstandard` or `GZIP` $\rightarrow$ Reduced Binary.
2. **Mapping:** Reduced Binary $\rightarrow$ Hex String $\rightarrow$ Search $\pi$ $\rightarrow$ Indices.
3. **Folding:** Indices $\rightarrow$ Recursive Szudzik Tree $\rightarrow$ Large Integers.
4. **Glyphing:** Large Integers $\rightarrow$ Base-256 Leyline Alphabet $\rightarrow$ Unicode Symbols.
5. **Forging:** Symbols $\rightarrow$ LaTeX Equation $\rightarrow$ `.txt` Ledger.

## 📦 Requirements
- **Python 3.10+**
- **Optional:** `pip install zstandard` (for high-performance compression)
- **For v5:** `squashfs-tools` (Linux/macOS) installed on the system.

## ⚠️ Notes on Performance
Calculating digits of $\pi$ via BBP is CPU-intensive. 
- **Resolution 2-3:** Fast, suitable for small files.
- **Resolution 4-6:** Slow, but results in much smaller ledgers. Requires a precomputed `pi_hex_30m.txt` file for maximum speed.

## 📜 [MIT License](https://github.com/thatoldfarm/f8c9-dust-manifold/blob/main/LICENSE)

