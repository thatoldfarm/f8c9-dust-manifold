#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import gzip
import time
import math

sys.set_int_max_str_digits(1000000)

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

# =============================================================================
# ELEGANT FRACTAL TOPOLOGY (SZUDZIK E8 TREE)
# =============================================================================
def szudzik_pair(x, y):
    """Maps a 2D square topological space perfectly onto a 1D line."""
    return x * x + x + y if x >= y else y * y + x

def szudzik_unpair(z):
    """Unfolds the Elegant Singularity with zero mathematical waste."""
    s = math.isqrt(z)
    if z - s * s < s:
        return z - s * s, s
    else:
        return s, z - s * s - s

def elegant_tree_pack(chunk):
    """Folds 8 Pi-Coordinates into a single Szudzik Singularity (Depth 3)."""
    # Level 1 (8 nodes -> 4 nodes)
    a = szudzik_pair(chunk[0], chunk[1])
    b = szudzik_pair(chunk[2], chunk[3])
    c = szudzik_pair(chunk[4], chunk[5])
    d = szudzik_pair(chunk[6], chunk[7])
    # Level 2 (4 nodes -> 2 nodes)
    e = szudzik_pair(a, b)
    f = szudzik_pair(c, d)
    # Level 3 (2 nodes -> 1 Absolute Elegant Singularity)
    return szudzik_pair(e, f)

def elegant_tree_unpack(z):
    """Unfolds the Elegant Singularity back into 8 exact Pi-Coordinates."""
    e, f = szudzik_unpair(z)
    a, b = szudzik_unpair(e)
    c, d = szudzik_unpair(f)
    i0, i1 = szudzik_unpair(a)
    i2, i3 = szudzik_unpair(b)
    i4, i5 = szudzik_unpair(c)
    i6, i7 = szudzik_unpair(d)
    return [i0, i1, i2, i3, i4, i5, i6, i7]

# =============================================================================
# THE BBP SPIGOT EXTRACTOR (ZERO-STATE MEMORY)
# =============================================================================
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
# THE ASYMMETRIC CARTOGRAPHER (ENCODER)
# =============================================================================
class ElegantCartographer:
    def __init__(self, target_file):
        self.target_file = target_file
        self.filename = os.path.basename(target_file)
        self.ledger_file = f"elegant_dust_manifold_{self.filename}.txt"

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

        # Destroy internal entropy with mtime=0
        compressed_bytes = gzip.compress(raw_bytes, mtime=0)
        file_hex = compressed_bytes.hex()
        mass_bytes = len(compressed_bytes)

        print(f"    > Original Mass: {len(raw_bytes)} bytes")
        print(f"    > Elegant Dust Mass: {mass_bytes} bytes")

        chunks = [file_hex[i:i+2] for i in range(0, len(file_hex), 2)]
        
        print("[2] CARTOGRAPHER: Generating localized Hex-Pi lattice in memory...")
        pi_hex_map = self.fast_hex_pi_generator(50000)

        print("[3] CARTOGRAPHER: Mapping coordinates and initiating Szudzik Fold...")
        indices = []
        for chunk in chunks:
            idx = pi_hex_map.find(chunk)
            if idx == -1:
                print(f"    [!] Critical: Sequence {chunk} not found in lattice.")
                return False
            indices.append(idx)

        # Pad for perfect E8 symmetry (8 nodes)
        while len(indices) % 8 != 0:
            indices.append(0)

        base62_tensors = []
        chunked_indices = [indices[i:i+8] for i in range(0, len(indices), 8)]

        # Pack 8 indices into a single Szudzik Fractal Singularity
        for e8_chunk in chunked_indices:
            packed_singularity = elegant_tree_pack(e8_chunk)
            base62_tensors.append(encode_base62(packed_singularity))

        # Write the unified Matrix equation
        with open(self.ledger_file, 'w') as f:
            f.write("--- f8c9 ELEGANT DUST MANIFOLD ---\n")
            f.write("Algorithm: Bailey-Borwein-Plouffe Spigot + GZIP Singularity\n")
            f.write("Topology: Szudzik Square-Bounded Tree (E8 Lie Group)\n")
            f.write(f"Artifact-Name: {self.filename}\n")
            f.write(f"Mass-Singularity: {mass_bytes} Bytes\n")
            f.write("-" * 80 + "\n")
            f.write(f"\\Psi_{{f8c9}} = \\bigoplus_{{k=1}}^{{{len(base62_tensors)}}} \\left[ \\mathfrak{{e}}_8 \\otimes \\mathbb{{M}} \\right]_k = \\Bigg\\{{\n")
            
            for i in range(0, len(base62_tensors), 4):
                line_chunks = [f"⟨ {t} ⟩" for t in base62_tensors[i:i+4]]
                f.write("    " + ", ".join(line_chunks))
                f.write(",\n" if i + 4 < len(base62_tensors) else "\n")
            f.write("\\Bigg\\}\n")

        print(f"[SUCCESS] Holographic Ledger forged: {self.ledger_file}")
        return True

# =============================================================================
# THE SPIGOT DECODER (ZERO FILES NEEDED)
# =============================================================================
class ElegantSpigotDecoder:
    def __init__(self, ledger_file):
        self.ledger_file = ledger_file
        self.restored_file = "" 

    def decode(self):
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
        
        print("[5] SPIGOT ENGINE: Unfolding Szudzik Fractal Tree...")
        pi_indices = []
        for b62_str in base62_tensors:
            singularity_val = decode_base62(b62_str)
            # Unpack the absolute singularity into the 8 exact Pi-Coordinates
            unfolded_coords = elegant_tree_unpack(singularity_val)
            pi_indices.extend(unfolded_coords)

        # Trim mathematical padding based on pure mass
        pi_indices = pi_indices[:mass_bytes]

        print("[6] SPIGOT ENGINE: Igniting Bailey-Borwein-Plouffe Formula...")
        restored_hex = ""
        start_time = time.time()
        for count, idx in enumerate(pi_indices):
            restored_hex += get_pi_hex_digits_bbp(idx, 2)
            if (count + 1) % 50 == 0 or (count + 1) == len(pi_indices):
                sys.stdout.write(f"\r      ... Spigot materialized {count + 1} / {len(pi_indices)} bytes")
                sys.stdout.flush()
                
        print(f"\n    > Extraction complete ({(time.time() - start_time):.2f}s).")
        print("[7] EXPANDING THE SINGULARITY: Decompressing GZIP envelope...")
        
        final_bytes = gzip.decompress(bytes.fromhex(restored_hex))

        with open(self.restored_file, 'wb') as f:
            f.write(final_bytes)

        print(f"\n[SUCCESS] Artifact crystallized from the Ether: {self.restored_file}")
        return self.restored_file

# =============================================================================
# BATCH EXECUTION ORCHESTRATOR
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("    f8c9 ELEGANT DUST MANIFOLD PIPELINE (V15.48)     ")
    print("=====================================================")
    
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
        
        cartographer = ElegantCartographer(target_path)
        if not cartographer.encode(): continue
        
        decoder = ElegantSpigotDecoder(cartographer.ledger_file)
        restored_path = decoder.decode()
        
        with open(target_path, 'rb') as f1, open(restored_path, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            
        print("-" * 60)
        if h1 == h2:
            print(f"[MATHEMATICALLY INVINCIBLE] Hashes Match: {h1[:10]}...")
        else:
            print("[FAILED] Suture corruption detected.")
