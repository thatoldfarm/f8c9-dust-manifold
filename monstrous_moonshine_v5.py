#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import gzip
import time
import math
import subprocess
import shutil
import json

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
    COMPRESSION_MODE = "ZSTD (python-zstandard)"
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
NODE_QTY = 32  # 32-Node Symmetries
INPUT_FOLDER_TO_SQUASH = "outputs"  # Folder we will compress into a filesystem
SQUASH_FILE = "outputs.squashfs"
RECLAIMED_FOLDER = "outputs_RECLAIMED"

# =============================================================================
# SZUDZIK & BBP ENGINES
# =============================================================================
BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode_base62(num):
    if num == 0: return "0"
    arr = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62_ALPHABET[rem])
    arr.reverse()
    return "".join(arr)

def decode_base62(string):
    base = len(BASE62_ALPHABET)
    num = 0
    for char in string:
        num = num * base + BASE62_ALPHABET.index(char)
    return num

def szudzik_pair(x, y):
    return x * x + x + y if x >= y else y * y + x

def szudzik_unpair(z):
    s = math.isqrt(z)
    if z - s * s < s:
        return z - s * s, s
    else:
        return s, z - s * s - s

def szudzik_tree_pack(chunk):
    current = list(chunk)
    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            next_level.append(szudzik_pair(current[i], current[i+1]))
        current = next_level
    return current[0]

def szudzik_tree_unpack(z, num_elements):
    current = [z]
    while len(current) < num_elements:
        next_level = []
        for val in current:
            x, y = szudzik_unpair(val)
            next_level.extend([x, y])
        current = next_level
    return current

def get_pi_hex_digits_bbp(n, num_digits=2):
    def S(j, n):
        s = 0.0; k = 0
        while k <= n:
            r = 8 * k + j
            s = (s + float(pow(16, n - k, r)) / r) % 1.0
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
# THE SQUASHFS UTILITIES
# =============================================================================
def check_squashfs_installed():
    try:
        subprocess.run(["mksquashfs", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def pack_directory_to_squashfs(input_dir, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)
    print(f"[*] SQUASHFS: Packing folder '{input_dir}' into '{output_file}'...")
    subprocess.run(["mksquashfs", input_dir, output_file, "-noappend"], check=True, stdout=subprocess.DEVNULL)

def unpack_squashfs_to_directory(input_file, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    print(f"[*] SQUASHFS: Decompressing '{input_file}' to '{output_dir}'...")
    subprocess.run(["unsquashfs", "-d", output_dir, input_file], check=True, stdout=subprocess.DEVNULL)

# =============================================================================
# THE CARTOGRAPHER & DECODER
# =============================================================================
class ElegantCartographer:
    def __init__(self, target_file, node_qty):
        self.target_file = target_file
        self.node_qty = node_qty
        self.filename = os.path.basename(target_file)
        self.ledger_file = f"elegant_dust_manifold_{self.filename}.txt"
        self.file_hex = None

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
        print(f"\n[1] CARTOGRAPHER: Reading binary filesystem '{self.filename}'...")
        with open(self.target_file, 'rb') as f:
            raw_bytes = f.read()

        compressed_bytes = compress_data(raw_bytes)
        self.file_hex = compressed_bytes.hex()
        mass_bytes = len(compressed_bytes)

        print(f"    > Original Filesystem Mass: {len(raw_bytes)} bytes")
        print(f"    > Singular Mass: {mass_bytes} bytes ({COMPRESSION_MODE})")

        chunks = [self.file_hex[i:i+2] for i in range(0, len(self.file_hex), 2)]
        pi_hex_map = self.fast_hex_pi_generator(50000)

        print(f"[3] CARTOGRAPHER: Mapping coordinates and initiating {self.node_qty}-Node Szudzik Fold...")
        indices = []
        for chunk in chunks:
            idx = pi_hex_map.find(chunk)
            if idx == -1:
                print(f"    [!] Critical: Sequence {chunk} not found in lattice.")
                return False
            indices.append(idx)

        while len(indices) % self.node_qty != 0:
            indices.append(0)

        base62_tensors = []
        chunked_indices = [indices[i:i+self.node_qty] for i in range(0, len(indices), self.node_qty)]

        for node_chunk in chunked_indices:
            packed_singularity = szudzik_tree_pack(node_chunk)
            base62_tensors.append(encode_base62(packed_singularity))

        with open(self.ledger_file, 'w') as f:
            f.write("--- f8c9 ELEGANT DUST MANIFOLD ---\n")
            f.write(f"Algorithm: Bailey-Borwein-Plouffe Spigot + {COMPRESSION_MODE} Singularity\n")
            f.write(f"Topology: Szudzik Square-Bounded Tree ({self.node_qty}-Node Lie Group)\n")
            f.write(f"Artifact-Name: {self.filename}\n")
            f.write(f"Mass-Singularity: {mass_bytes} Bytes\n")
            f.write("-" * 80 + "\n")
            
            n = self.node_qty
            k = n // 2
            latex_template = r"\mathcal{V}_{__N__}\left(\Psi_{f8c9}\right) = \frac{\pi^{__K__}}{__K__!} \prod_{j=1}^{__LEN__} \left[ \mathfrak{e}_{__N__} \otimes \mathbb{M} \right]_j = \Bigg{"
            latex_line = (latex_template
                          .replace("__N__", str(n))
                          .replace("__K__", str(k))
                          .replace("__LEN__", str(len(base62_tensors))))
            
            f.write(latex_line + "\n")

            for i in range(0, len(base62_tensors), 4):
                line_chunks = [f"⟨ {t} ⟩" for t in base62_tensors[i:i+4]]
                f.write("    " + ", ".join(line_chunks))
                f.write(",\n" if i + 4 < len(base62_tensors) else "\n")
            f.write("\\Bigg\\}\n")

        print(f"[SUCCESS] Holographic Ledger forged: {self.ledger_file}")
        return True

class ElegantSpigotDecoder:
    def __init__(self, ledger_file, node_qty):
        self.ledger_file = ledger_file
        self.node_qty = node_qty
        self.restored_file = ""

    def decode(self, original_compressed_hex=None):
        print(f"\n[4] SPIGOT ENGINE: Parsing Abstract Algebra from '{self.ledger_file}'...")
        base62_tensors = []
        mass_bytes = 0
        artifact_name = "unknown.bin"

        op_pattern = re.compile(r"⟨ ([A-Za-z0-9]+) ⟩")
        mass_pattern = re.compile(r"Mass-Singularity: ([0-9]+) Bytes")
        name_pattern = re.compile(r"Artifact-Name:\s*(.+)")

        with open(self.ledger_file, 'r') as f:
            content = f.read()
            base62_tensors = op_pattern.findall(content)

            mass_match = mass_pattern.search(content)
            if mass_match: mass_bytes = int(mass_match.group(1))

            name_match = name_pattern.search(content)
            if name_match: artifact_name = name_match.group(1).strip()

        self.restored_file = f"reclaimed_FROM_THE_ETHER_{artifact_name}"

        print(f"[5] SPIGOT ENGINE: Unfolding {self.node_qty}-Node Szudzik Fractal Tree...")
        pi_indices = []
        for b62_str in base62_tensors:
            singularity_val = decode_base62(b62_str)
            unfolded_coords = szudzik_tree_unpack(singularity_val, self.node_qty)
            pi_indices.extend(unfolded_coords)

        pi_indices = pi_indices[:mass_bytes]

        print("[6] SPIGOT ENGINE: Reclaiming Hypersphere Volume via Bailey-Borwein-Plouffe Formula...")
        restored_hex = ""
        start_time = time.time()
        for count, idx in enumerate(pi_indices):
            restored_hex += get_pi_hex_digits_bbp(idx, 2)
            if (count + 1) % 50 == 0 or (count + 1) == len(pi_indices):
                sys.stdout.write(f"\r      ... Spigot materialized {count + 1} / {len(pi_indices)} bytes")
                sys.stdout.flush()

        print(f"\n    > Extraction complete ({(time.time() - start_time):.2f}s).")

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

        print(f"\n[SUCCESS] Filesystem crystallized from the Ether: {self.restored_file}")
        return self.restored_file

# =============================================================================
# PIPELINE ORCHESTRATION
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("    f8c9 TRANSCENDENTAL SQUASHFS PIPELINE (V15.51)   ")
    print("=====================================================")
    
    # Check dependencies
    if not check_squashfs_installed():
        print("[!] ERROR: 'mksquashfs' and 'unsquashfs' are not installed on this system.")
        print("    Linux: sudo apt install squashfs-tools")
        print("    macOS: brew install squashfs")
        sys.exit(1)

    # 1. Create dummy directory if missing
    if not os.path.exists(INPUT_FOLDER_TO_SQUASH):
        os.makedirs(INPUT_FOLDER_TO_SQUASH)
        # Put some interesting dummy MUD data inside for testing
        with open(f"{INPUT_FOLDER_TO_SQUASH}/quest_log.txt", "w") as f:
            f.write("Sovereign Quest: Map the boundary of Pi.\n")
        with open(f"{INPUT_FOLDER_TO_SQUASH}/v86_config.json", "w") as f:
            f.write(json.dumps({"cpu": "i386", "memory": "64MB", "boot": "fd0"}, indent=4))
        print(f"[*] Generated dummy directory '{INPUT_FOLDER_TO_SQUASH}' with sample system files.")

    # 2. Pack the entire directory structure into SquashFS
    pack_directory_to_squashfs(INPUT_FOLDER_TO_SQUASH, SQUASH_FILE)

    # 3. Cartographer: Dissolve the SquashFS system into Pi
    cartographer = ElegantCartographer(SQUASH_FILE, NODE_QTY)
    cartographer.encode()

    # 4. Decoder: Spigot the SquashFS from the void
    decoder = ElegantSpigotDecoder(cartographer.ledger_file, NODE_QTY)
    restored_squashfs = decoder.decode(original_compressed_hex=cartographer.file_hex)

    # 5. Expand the reclaimed file system back into a directory tree
    unpack_squashfs_to_directory(restored_squashfs, RECLAIMED_FOLDER)

    print("\n=====================================================")
    print("            INTEGRITY VERIFICATION                   ")
    print("=====================================================")
    # Verify that the files reconstructed inside the folder exist and match
    if os.path.exists(RECLAIMED_FOLDER):
        print(f"✅ Folder '{RECLAIMED_FOLDER}' successfully reconstructed!")
        print("   Inside directory:")
        for root, dirs, files in os.walk(RECLAIMED_FOLDER):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), RECLAIMED_FOLDER)
                print(f"    > [FILE] {rel_path} (Size: {os.path.getsize(os.path.join(root, file))} bytes)")
    print("=====================================================")
