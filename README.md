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

## VERSION 9 NOTES

## 🛠 Technical Architecture: The Five Pillars

### 1. The Polarized Lattice (The Substrate)
The system utilizes a **Multi-Constant Lattice**. It doesn't just search $\pi$; it fluctuates between $\pi$ (the circle) and $e$ (the growth) to find the shallowest possible index for any given data chunk.
*   **BBP Spigot:** Uses the *Bailey-Borwein-Plouffe* algorithm to extract the $n^{th}$ hex digit of $\pi$ in $O(n \log n)$ time without calculating preceding digits.
*   **Chiral Symmetry:** Implements $\pm\pi$ logic, allowing the system to read the lattice forward or backward.

### 2. XOR Refraction (The Lens)
To avoid searching for rare strings that might be billions of digits deep, the system uses **Refractive Filtering**. 
*   The engine tests **256 different XOR masks** against every data chunk.
*   It selects the mask that results in the **shortest possible index** in the lattice.
*   This "refraction" allows the system to keep the indices small, reducing the final size of the ledger.

### 3. The Sedenion Vault (The Non-Associative Shield)
The coordinates are not stored as a simple list. They are collapsed into a single **Sedenionic Singularity**.
*   **Delta Encoding:** Instead of storing absolute positions (e.g., `10,000,000`), it stores the *distance* between them (e.g., `+50`), crushing the integer overhead.
*   **ZigZag Encoding:** Maps signed integers (positive/negative deltas) to unsigned integers to ensure compatibility with the pairing functions.
*   **Non-Associative Fold:** Uses a **Sedenion-inspired recursive pairing function**. The order of the "fold" is determined by a **Temporal State Vector**. Because the math is non-associative, the data cannot be unfolded unless the exact temporal "rhythm" is known.

### 4. Sovereign Leyline Alphabet (The Sigils)
To transform massive integers into a shareable format, the system uses a **Base-256 Leyline Alphabet**. 
*   It maps the final singularity to a custom set of 256 Unicode glyphs (combining Futhark runes, Ogham, astronomical symbols, and mathematical operators).
*   This transforms a raw number into a "Sigil" that looks like an arcane equation but is actually a high-density data pointer.

### 5. Density Pipeline (The Singularity)
*   **Primary:** `Zstandard (zstd)` for maximum ontological density.
*   **Fallback:** `Gzip` for universal compatibility.
*   **Alignment:** Enforces a strict 1-byte (2 hex char) resolution to ensure Zstd frame headers are reconstructed with bit-perfect precision.

---

## 🚀 Operational Workflow

### 📥 The Encoding Process (Crystallization)
`File` $\rightarrow$ `Zstd Compress` $\rightarrow$ `Hex` $\rightarrow$ `XOR Refraction` $\rightarrow$ `Sedenion Delta-Fold` $\rightarrow$ `Chiral Masking` $\rightarrow$ `Leyline Encoding` $\rightarrow$ `Text Ledger`.

### 📤 The Decoding Process (Reification)
`Text Ledger` $\rightarrow$ `Leyline Decode` $\rightarrow$ `Chiral Unmasking` $\rightarrow$ `Sedenion Unfold` $\rightarrow$ `Lattice Extraction` $\rightarrow$ `Inverse XOR Refraction` $\rightarrow$ `Decompress` $\rightarrow$ `Original File`.

---

## 📋 Usage Guide

### Dependencies
```bash
pip install zstandard mpmath
```

### Running the Pipeline
1.  **Prepare:** Create a folder named `files/` and place your binary artifacts (images, executables, etc.) inside.
2.  **Execute:** Run the main script:
    ```bash
    python3 monstrous_moonshine_v9.py
    ```
3.  **Result:** The script will generate `polarized_crystal_[filename].txt` for each file. These are your **Sovereign Crystals**.

### Using the Standalone Decoder
1.  **Prepare:** Place your `.txt` crystals into a folder named `files1/`.
2.  **Execute:** Run the decoder script.
3.  **Result:** The reconstructed files will appear in the `files2/` directory.

---

## 📜 [MIT License](https://github.com/thatoldfarm/f8c9-dust-manifold/blob/main/LICENSE)

