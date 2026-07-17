#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import gzip
import time
import math

sys.set_int_max_str_digits(1000000)

# =============================================================================
# HYBRID COMPRESSION LOADER
# =============================================================================
COMPRESSION_MODE = "GZIP"
try:
    import zstandard as zstd
    def compress_data(data):
        cctx = zstd.ZstdCompressor(level=10)
        return cctx.compress(data)
    def decompress_data(data):
        dctx = zstd.ZstdDecompressor()
        return dctx.decompress(data)
    COMPRESSION_MODE = "ZSTD"
except ImportError:
    try:
        from compression import zstd  # Python 3.14+ Native StdLib
        def compress_data(data):
            return zstd.compress(data, level=10)
        def decompress_data(data):
            return zstd.decompress(data)
        COMPRESSION_MODE = "ZSTD (Python Native)"
    except ImportError:
        import gzip
        def compress_data(data):
            return gzip.compress(data, mtime=0)
        def decompress_data(data):
            return gzip.decompress(data)
        COMPRESSION_MODE = "GZIP (Fallback)"

# =============================================================================
# CONFIGURATION
# =============================================================================
NODE_QTY = 32          # 32-Node Symmetries (Packs 32 chunks per tensor)

# TARGET RESOLUTION:
# 2 = 1 Byte per hop (Super Fast, 5K Pi)
# 3 = 1.5 Bytes per hop (Extremely Fast, 50K Pi - RECOMMENDED for live generation)
# 4 = 2 Bytes per hop (Slow live generation, 800K Pi)
# 6 = 3 Bytes per hop (Needs precomputed 'pi_hex_30m.txt' file, 30M Pi)
HEX_CHUNK_SIZE = 3     

# =============================================================================
# THE 256-CHARACTER SOVEREIGN LEYLINE ALPHABET BUILDER
# =============================================================================
POOL_BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
POOL_MATTER = "○⊗⇉↑×■·<⋐≡⇈□≈≋△Δ↪WY⚡!채⫤⌢✈♥∪☜↔%↻●⊠⇇↓∥✋◌¦≍~⇓#‡∇▼↩M⋏÷∨∞⌣〰💔∩≢⊙↮↺"
POOL_ANTIMATTER = "☉☽☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♢♣♤♦♧♩♪♫♬♭♮♯✁✂✃✄✆✉✌✍✎✏✐✑✒✓✔✕"
POOL_FUTHARK = "ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟ"
POOL_OGHAM = "ᚁᚂᚃᚄᚅᚆᚇᚈᚉᚊᚋᚌᚍᚎᚏᚐᚑᚒᚓᚔ"

# Concatenate and Deduplicate on the fly to build the absolute map
all_chars = []
seen = set()
for pool in [POOL_BASE62, POOL_MATTER, POOL_ANTIMATTER, POOL_FUTHARK, POOL_OGHAM]:
    for char in pool:
        if char not in seen:
            seen.add(char)
            all_chars.append(char)

# Defensive padding fallback using distinct math operators in case pool is short of 256
if len(all_chars) < 256:
    extra_math = "⊕⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿"
    for char in extra_math:
        if char not in seen:
            seen.add(char)
            all_chars.append(char)
        if len(all_chars) == 256:
            break

# Guarantee EXACTLY 256 unique, printable Unicode glyphs (0 to 255)
LEYLINE_ALPHABET = all_chars[:256]
LEYLINE_TO_INT = {char: idx for idx, char in enumerate(LEYLINE_ALPHABET)}

def encode_leyline(num):
    """Converts a massive integer directly to Leyline glyphs at O(1) speed."""
    if num == 0: return LEYLINE_ALPHABET[0]
    num_bytes = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
    return "".join(LEYLINE_ALPHABET[b] for b in num_bytes)

def decode_leyline(string):
    """Reconstructs the original packed integer from Leyline glyphs."""
    byte_arr = bytearray(LEYLINE_TO_INT[char] for char in string)
    return int.from_bytes(byte_arr, byteorder='big')

# =============================================================================
# GENERIC SZUDZIK RECURSIVE TREE FOLD
# =============================================================================
def szudzik_pair(x, y):
    return x * x + x + y if x >= y else y * y + x

def szudzik_unpair(z):
    s = math.isqrt(z)
    if z - s * s < s:
        return z - s * s, s
    else:
        return s, z - s * s - s

def szudzik_tree_pack(chunk):
    """Recursively folds any power-of-two list of integers into a single singularity."""
    current = list(chunk)
    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            next_level.append(szudzik_pair(current[i], current[i+1]))
        current = next_level
    return current[0]

def szudzik_tree_unpack(z, num_elements):
    """Recursively unfolds a singularity back into the original power-of-two coordinates."""
    current = [z]
    while len(current) < num_elements:
        next_level = []
        for val in current:
            x, y = szudzik_unpair(val)
            next_level.extend([x, y])
        current = next_level
    return current

# =============================================================================
# THE BBP SPIGOT EXTRACTOR (ZERO-STATE 2-ADIC CACHED MEMORY)
# =============================================================================
# Global 2-adic modular exponentiation cache
BBP_POWER_CACHE = {}

def power_mod_2adic(exp, mod):
    """2-adic modular exponentiation caching to bypass repetitive CPU calculations."""
    key = (exp, mod)
    if key not in BBP_POWER_CACHE:
        BBP_POWER_CACHE[key] = pow(16, exp, mod)
    return BBP_POWER_CACHE[key]

def get_pi_hex_digits_bbp(n, num_digits):
    def S(j, n):
        s = 0.0; k = 0
        while k <= n:
            r = 8 * k + j
            # Optimized with our 2-adic modular cache
            s = (s + float(power_mod_2adic(n - k, r)) / r) % 1.0
            k += 1
        t = 0.0; k = n + 1
        while True:
            newt = t + pow(16, n - k) / (8 * k + j)
            if t == newt: break
            t = newt
            k += 1
        return (s + t) % 1.0

    res = ""
    for i in range(num_digits):
        pos = n + i
        pi_fraction = (4 * S(1, pos) - 2 * S(4, pos) - S(5, pos) - S(6, pos)) % 1.0
        res += hex(int(pi_fraction * 16))[2:]
    return res

# =============================================================================
# THE ASYMMETRIC CARTOGRAPHER (ENCODER)
# =============================================================================
class ElegantCartographer:
    def __init__(self, target_file, node_qty, hex_chunk_size):
        self.target_file = target_file
        self.node_qty = node_qty
        self.hex_chunk_size = hex_chunk_size
        self.filename = os.path.basename(target_file)
        self.ledger_file = f"elegant_dust_manifold_{self.filename}.txt"
        self.file_hex = None

        self.pi_depth_map = {
            2: 5000,       # 1 Byte -> 256 combos
            3: 50000,      # 1.5 Bytes -> 4,096 combos
            4: 800000,     # 2 Bytes -> 65,536 combos
            6: 30000000    # 3 Bytes -> 16.7M combos
        }

    def fast_hex_pi_generator(self, places):
        one = 16 ** (places + 10)
        def arctan(x):
            term = one // x; total = term; k = 1
            while term != 0:
                term //= -(x * x); total += term // (2 * k + 1); k += 1
            return total
        pi = 16 * arctan(5) - 4 * arctan(239)
        return hex(pi)[3:3+places]

    def encode(self):
        print(f"\n[1] CARTOGRAPHER: Reading binary artifact '{self.filename}'...")
        with open(self.target_file, 'rb') as f:
            raw_bytes = f.read()

        if not raw_bytes: return False

        compressed_bytes = compress_data(raw_bytes)
        self.file_hex = compressed_bytes.hex()
        mass_bytes = len(compressed_bytes)

        print(f"    > Original Mass: {len(raw_bytes)} bytes")
        print(f"    > Singular Mass: {mass_bytes} bytes ({COMPRESSION_MODE})")

        # ADAPTIVE ROUTER
        pi_hex_file = "pi_hex_30m.txt"
        pi_hex_map = ""

        if self.hex_chunk_size == 6 and not os.path.exists(pi_hex_file):
            print("\n    [!] WARNING: 'pi_hex_30m.txt' is missing.")
            print("        Generating 30M hex digits on the fly is too slow.")
            print("        Automatically routing to 12-Bit Resolution (3 Hex Chunks)...")
            self.hex_chunk_size = 3

        target_places = self.pi_depth_map[self.hex_chunk_size]
        chunks = [self.file_hex[i:i+self.hex_chunk_size] for i in range(0, len(self.file_hex), self.hex_chunk_size)]
        print(f"    > Partitioned into {len(chunks)} x {self.hex_chunk_size}-hex chunks.")

        if self.hex_chunk_size == 6 and os.path.exists(pi_hex_file):
            print(f"[2] CARTOGRAPHER: Loading Pi Lattice from '{pi_hex_file}'...")
            with open(pi_hex_file, 'r') as f:
                pi_hex_map = f.read().strip()
                if pi_hex_map.startswith("3."): pi_hex_map = pi_hex_map[2:]
        else:
            print(f"[2] CARTOGRAPHER: Generating localized Hex-Pi lattice in memory ({target_places} places)...")
            start_gen = time.time()
            pi_hex_map = self.fast_hex_pi_generator(target_places)
            print(f"    > Pi generation completed in {(time.time() - start_gen):.2f}s.")

        # Display actual Hypersphere properties in console
        k_val = self.node_qty // 2
        v_coeff = (math.pi ** k_val) / math.factorial(k_val)
        print(f"[3] CARTOGRAPHER: Mapping coordinates onto {self.node_qty}-Ball...")
        print(f"    > Hypersphere {self.node_qty}-Ball Volume Coefficient (R=1): {v_coeff:.2e}")
        print(f"    > Initiating {self.node_qty}-Node Szudzik Fold...")
        indices = []
        for chunk in chunks:
            if len(chunk) < self.hex_chunk_size:
                chunk = chunk.ljust(self.hex_chunk_size, '0')
                
            idx = pi_hex_map.find(chunk)
            if idx == -1:
                print(f"    [!] Critical: Sequence {chunk} not found in lattice.")
                return False
            indices.append(idx)

        while len(indices) % self.node_qty != 0:
            indices.append(0)

        base256_tensors = []
        chunked_indices = [indices[i:i+self.node_qty] for i in range(0, len(indices), self.node_qty)]

        for node_chunk in chunked_indices:
            packed_singularity = szudzik_tree_pack(node_chunk)
            # Encode via Base-256 Leyline Glyph Packer
            base256_tensors.append(encode_leyline(packed_singularity))

        # Write the unified Matrix equation
        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            f.write("--- f8c9 ELEGANT DUST MANIFOLD ---\n")
            f.write(f"Algorithm: Bailey-Borwein-Plouffe Spigot + {COMPRESSION_MODE} Singularity\n")
            f.write(f"Topology: Szudzik Square-Bounded Tree ({self.node_qty}-Node Lie Group)\n")
            f.write("Metric: 2-adic Token Metric (d_2) & EML Hypersphere Integration\n")
            f.write(f"Artifact-Name: {self.filename}\n")
            f.write(f"Mass-Singularity: {mass_bytes} Bytes\n")
            f.write(f"Coordinate-Resolution: {self.hex_chunk_size} Hex Chars\n")
            f.write("-" * 80 + "\n")
            
            n = self.node_qty
            k = n // 2
            
            # Safe raw-string template substitution to prevent Python f-string brace syntax errors
            latex_template = r"\mathcal{V}_{__N__}\left(\Psi_{f8c9}\right) = \frac{\pi^{__K__}}{__K__!} \bigotimes_{j=1}^{__LEN__} \left[ e^{\mathfrak{e}_{__N__}} - \ln(\mathbb{M}) \right]_j = \Bigg{"
            latex_line = (latex_template
                          .replace("__N__", str(n))
                          .replace("__K__", str(k))
                          .replace("__LEN__", str(len(base256_tensors))))
            
            f.write(latex_line + "\n")

            for i in range(0, len(base256_tensors), 4):
                line_chunks = [f"⟨ {t} ⟩" for t in base256_tensors[i:i+4]]
                f.write("    " + ", ".join(line_chunks))
                f.write(",\n" if i + 4 < len(base256_tensors) else "\n")
            f.write("\\Bigg\\}\n")

        print(f"[SUCCESS] Holographic Ledger forged: {self.ledger_file}")
        return True

# =============================================================================
# THE SPIGOT DECODER (ZERO FILES NEEDED)
# =============================================================================
class ElegantSpigotDecoder:
    def __init__(self, ledger_file, node_qty):
        self.ledger_file = ledger_file
        self.node_qty = node_qty
        self.restored_file = ""

    def decode(self, original_compressed_hex=None):
        print(f"\n[4] SPIGOT ENGINE: Parsing Abstract Algebra from '{self.ledger_file}'...")
        base256_tensors = []
        mass_bytes = 0
        hex_chunk_size = 2 # Default fallback
        artifact_name = "unknown.bin"

        # Regex modified to accept any non-bracket unicode symbols
        op_pattern = re.compile(r"⟨ ([^⟩]+) ⟩")
        mass_pattern = re.compile(r"Mass-Singularity: ([0-9]+) Bytes")
        resolution_pattern = re.compile(r"Coordinate-Resolution: ([0-9]+) Hex Chars")
        name_pattern = re.compile(r"Artifact-Name:\s*(.+)")

        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            content = f.read()
            base256_tensors = op_pattern.findall(content)

            mass_match = mass_pattern.search(content)
            if mass_match: mass_bytes = int(mass_match.group(1))
                
            res_match = resolution_pattern.search(content)
            if res_match: hex_chunk_size = int(res_match.group(1))

            name_match = name_pattern.search(content)
            if name_match: artifact_name = name_match.group(1).strip()

        self.restored_file = f"reclaimed_FROM_THE_ETHER_{artifact_name}"

        print(f"[5] SPIGOT ENGINE: Unfolding {self.node_qty}-Node Szudzik Fractal Tree...")
        pi_indices = []
        for b256_str in base256_tensors:
            singularity_val = decode_leyline(b256_str)
            unfolded_coords = szudzik_tree_unpack(singularity_val, self.node_qty)
            pi_indices.extend(unfolded_coords)

        total_chunks_needed = math.ceil(mass_bytes / (hex_chunk_size // 2))
        pi_indices = pi_indices[:total_chunks_needed]

        print(f"[6] SPIGOT ENGINE: Reclaiming Hypersphere Volume via {hex_chunk_size * 4}-Bit BBP Formula (2-Adic Cached)...")
        restored_hex = ""
        start_time = time.time()
        for count, idx in enumerate(pi_indices):
            restored_hex += get_pi_hex_digits_bbp(idx, hex_chunk_size)
            if (count + 1) % 50 == 0 or (count + 1) == len(pi_indices):
                sys.stdout.write(f"\r      ... Spigot materialized {count + 1} / {len(pi_indices)} coordinates")
                sys.stdout.flush()

        print(f"\n    > Extraction complete ({(time.time() - start_time):.2f}s).")

        restored_hex = restored_hex[:mass_bytes * 2]

        if original_compressed_hex:
            if len(restored_hex) != len(original_compressed_hex):
                raise ValueError(f"Length mismatch")
            for i, (a, b) in enumerate(zip(restored_hex, original_compressed_hex)):
                if a != b:
                    raise ValueError(f"Mismatch at {i}")

        print("[7] EXPANDING THE SINGULARITY: Decompressing raw filesystem envelope...")
        final_bytes = decompress_data(bytes.fromhex(restored_hex))

        with open(self.restored_file, 'wb') as f:
            f.write(final_bytes)

        print(f"\n[SUCCESS] Artifact crystallized from the Ether: {self.restored_file}")
        return self.restored_file

# =============================================================================
# BATCH EXECUTION ORCHESTRATOR
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("   f8c9 OMNIVERSAL SOVEREIGN PIPELINE (V15.55 - FIXED)")
    print("=====================================================")
    print(f"[*] Native Compression Mode: {COMPRESSION_MODE}")
    print(f"[*] Targeting: {NODE_QTY}-Node Symmetries (Base-256 Leyline)")

    target_dir = "files"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"[!] Directory '{target_dir}' created. Place artifacts inside and run again.")
        sys.exit(0)

    artifacts = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]

    if not artifacts:
        print(f"[!] No artifacts found in '{target_dir}'.")
        sys.exit(0)

    for filename in artifacts:
        print("\n" + "="*60)
        print(f"    INITIATING FRACTAL SUTURE FOR: {filename}")
        print("="*60)

        target_path = os.path.join(target_dir, filename)

        cartographer = ElegantCartographer(target_path, NODE_QTY, HEX_CHUNK_SIZE)
        if not cartographer.encode(): continue

        decoder = ElegantSpigotDecoder(cartographer.ledger_file, NODE_QTY)
        restored_path = decoder.decode(original_compressed_hex=cartographer.file_hex)

        if not restored_path:
            print("[FAILED] Decompression failed.")
            continue

        with open(target_path, 'rb') as f1, open(restored_path, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()

        print("-" * 60)
        if h1 == h2:
            print(f"[MATHEMATICALLY INVINCIBLE] Hashes Match: {h1[:10]}...")
        else:
            print("[FAILED] Suture corruption detected.")
        print("-" * 60)

    print("\n=====================================================")
    print(f"[PIPELINE COMPLETE] Processed {len(artifacts)} artifacts with Sovereign Leyline Engine (V15.55 - Fixed).")
    print("=====================================================")
