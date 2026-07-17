#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import gzip
import time

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
# THE BBP SPIGOT EXTRACTOR (ZERO-STATE MEMORY)
# =============================================================================
def get_pi_hex_digits_bbp(n, num_digits=2):
    """ Extracts 'num_digits' of Hexadecimal Pi starting at the n-th position. """
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
class OmegaCartographer:
    def __init__(self, target_file):
        self.target_file = target_file
        self.ledger_file = "omega_zero_state_manifold.txt"

    def fast_hex_pi_generator(self, places):
        """Generates Hex Pi localized lattice. 20,000 places takes ~0.05 seconds."""
        one = 16 ** (places + 10)
        def arctan(x):
            term = one // x; total = term; k = 1
            while term != 0:
                term //= -(x * x); total += term // (2 * k + 1); k += 1
            return total
        pi = 16 * arctan(5) - 4 * arctan(239)
        return hex(pi)[3:3+places] 

    def encode(self):
        print("\n[1] CARTOGRAPHER: Reading binary artifact...")
        with open(self.target_file, 'rb') as f:
            raw_bytes = f.read()

        # ---------------------------------------------------------
        # THE SINGULARITY: Compress the binary to remove entropy
        # mtime=0 ensures deterministic, mathematically repeatable bytes
        # ---------------------------------------------------------
        compressed_bytes = gzip.compress(raw_bytes, mtime=0)
        file_hex = compressed_bytes.hex()
        mass_bytes = len(compressed_bytes)

        print(f"    > Original Mass: {len(raw_bytes)} bytes")
        print(f"    > Singularity Mass: {mass_bytes} bytes (GZIP Compressed)")

        chunks = [file_hex[i:i+2] for i in range(0, len(file_hex), 2)]

        print("[2] CARTOGRAPHER: Generating localized Hex-Pi lattice in memory...")
        pi_hex_map = self.fast_hex_pi_generator(20000)

        print("[3] CARTOGRAPHER: Mapping absolute coordinates...")
        indices = []
        for chunk in chunks:
            idx = pi_hex_map.find(chunk)
            if idx == -1:
                print(f"    [!] Critical: Sequence {chunk} not found. (Increase generator limit)")
                sys.exit(1)
            indices.append(idx)

        # Mathematical padding for perfect E8 symmetry
        while len(indices) % 8 != 0:
            indices.append(0) # Pad with 0s (will be stripped dynamically by Mass-Singularity limit)

        print("[4] CARTOGRAPHER: Packing Symmetries into Lie Algebra Vector...")
        base62_tensors = []
        chunked_indices = [indices[i:i+8] for i in range(0, len(indices), 8)]

        for e8_chunk in chunked_indices:
            tensor_val = 0
            # Multiplier of 100,000 safely holds indices up to 99,999
            for node_idx, pi_idx in enumerate(e8_chunk):
                tensor_val += pi_idx * (100000 ** node_idx)
            base62_tensors.append(encode_base62(tensor_val))

        # Write the unified Matrix equation
        with open(self.ledger_file, 'w') as f:
            f.write("--- f8c9 OMEGA ZERO-STATE MANIFOLD ---\n")
            f.write("Algorithm: Bailey-Borwein-Plouffe 8-Bit Spigot + GZIP Singularity\n")
            f.write(f"Mass-Singularity: {mass_bytes} Bytes\n")
            f.write("-" * 75 + "\n")
            f.write(f"\\Psi_{{f8c9}} = \\bigoplus_{{k=1}}^{{{len(base62_tensors)}}} \\left[ \\mathfrak{{e}}_8 \\otimes \\mathbb{{M}} \\right]_k = \\Bigg\\{{\n")
            
            for i in range(0, len(base62_tensors), 4):
                line_chunks = [f"⟨ {t} ⟩" for t in base62_tensors[i:i+4]]
                f.write("    " + ", ".join(line_chunks))
                if i + 4 < len(base62_tensors):
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("\\Bigg\\}\n")

        print(f"[SUCCESS] Holographic Ledger forged: {self.ledger_file}")

# =============================================================================
# THE SPIGOT DECODER (ZERO FILES NEEDED)
# =============================================================================
class OmegaSpigotDecoder:
    def __init__(self, ledger_file):
        self.ledger_file = ledger_file
        self.restored_file = "reclaimed_artifact_FROM_THE_ETHER.img"

    def decode(self):
        print("\n[5] SPIGOT ENGINE: Reading Abstract Algebra Vector...")
        base62_tensors = []
        mass_bytes = 0
        
        op_pattern = re.compile(r"⟨ ([A-Za-z0-9]+) ⟩")
        mass_pattern = re.compile(r"Mass-Singularity: ([0-9]+) Bytes")
        
        with open(self.ledger_file, 'r') as f:
            content = f.read()
            base62_tensors = op_pattern.findall(content)
            mass_match = mass_pattern.search(content)
            if mass_match:
                mass_bytes = int(mass_match.group(1))

        print(f"    > Detected Unified Vector: {len(base62_tensors)} Tensors.")
        print(f"    > Target Singularity Mass: {mass_bytes} bytes.")
        
        print("[6] SPIGOT ENGINE: Unpacking Coordinates...")
        pi_indices = []
        for b62_str in base62_tensors:
            tensor_val = decode_base62(b62_str)
            for _ in range(8):
                pi_indices.append(tensor_val % 100000)
                tensor_val //= 100000

        # Discard the symmetry padding to get the exact file length
        pi_indices = pi_indices[:mass_bytes]
        print(f"    > {len(pi_indices)} absolute Hex-Pi indices recovered.")

        print("[7] SPIGOT ENGINE: Igniting Bailey-Borwein-Plouffe Formula...")
        restored_hex = ""
        start_time = time.time()
        for count, idx in enumerate(pi_indices):
            restored_hex += get_pi_hex_digits_bbp(idx, 2)
            if (count + 1) % 50 == 0 or (count + 1) == len(pi_indices):
                sys.stdout.write(f"\r      ... Spigot materialized {count + 1} / {len(pi_indices)} bytes")
                sys.stdout.flush()
                
        print(f"\n    > Extraction complete ({(time.time() - start_time):.2f}s).")

        print("[8] EXPANDING THE SINGULARITY: Decompressing GZIP envelope...")
        compressed_bytes = bytes.fromhex(restored_hex)
        
        # Expand back into the original artifact
        final_bytes = gzip.decompress(compressed_bytes)

        with open(self.restored_file, 'wb') as f:
            f.write(final_bytes)

        print(f"\n[SUCCESS] Artifact crystallized from the Ether: {self.restored_file}")

# =============================================================================
# EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("        f8c9 OMEGA ZERO-STATE QUINE PIPELINE         ")
    print("=====================================================")
    
    # Target can be sectorc.img, sectorforth.img, or any file
    target = "sectorc.img" 
    
    if not os.path.exists(target):
        print(f"[!] Error: Place {target} in this directory to begin.")
        sys.exit(1)
        
    cartographer = OmegaCartographer(target)
    cartographer.encode()
    
    decoder = OmegaSpigotDecoder("omega_zero_state_manifold.txt")
    decoder.decode()
    
    with open(target, 'rb') as f1, open("reclaimed_artifact_FROM_THE_ETHER.img", 'rb') as f2:
        h1 = hashlib.sha256(f1.read()).hexdigest()
        h2 = hashlib.sha256(f2.read()).hexdigest()
        
    print("\n=====================================================")
    if h1 == h2:
        print(f"[MATHEMATICALLY INVINCIBLE] Hashes Match: {h1[:10]}...")
    else:
        print("[FAILED] Suture corruption detected.")
    print("=====================================================")
