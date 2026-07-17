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
        self.filename = os.path.basename(target_file)
        self.ledger_file = f"omega_zero_state_manifold_{self.filename}.txt"

    def fast_hex_pi_generator(self, places):
        """Generates Hex Pi localized lattice. 50,000 places accommodates slightly larger files."""
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

        if len(raw_bytes) == 0:
            print("    [!] File is empty. Skipping.")
            return False

        # THE SINGULARITY
        compressed_bytes = gzip.compress(raw_bytes, mtime=0)
        file_hex = compressed_bytes.hex()
        mass_bytes = len(compressed_bytes)

        print(f"    > Original Mass: {len(raw_bytes)} bytes")
        print(f"    > Singularity Mass: {mass_bytes} bytes (GZIP Compressed)")

        chunks = [file_hex[i:i+2] for i in range(0, len(file_hex), 2)]

        print("[2] CARTOGRAPHER: Generating localized Hex-Pi lattice in memory...")
        pi_hex_map = self.fast_hex_pi_generator(50000)

        print("[3] CARTOGRAPHER: Mapping absolute coordinates...")
        indices = []
        for chunk in chunks:
            idx = pi_hex_map.find(chunk)
            if idx == -1:
                print(f"    [!] Critical: Sequence {chunk} not found. (Needs larger generator limit)")
                return False
            indices.append(idx)

        # Mathematical padding for perfect E8 symmetry
        while len(indices) % 8 != 0:
            indices.append(0)

        print("[4] CARTOGRAPHER: Packing Symmetries into Lie Algebra Vector...")
        base62_tensors = []
        chunked_indices = [indices[i:i+8] for i in range(0, len(indices), 8)]

        for e8_chunk in chunked_indices:
            tensor_val = 0
            for node_idx, pi_idx in enumerate(e8_chunk):
                tensor_val += pi_idx * (100000 ** node_idx)
            base62_tensors.append(encode_base62(tensor_val))

        # Write the unified Matrix equation including Original Filename
        with open(self.ledger_file, 'w') as f:
            f.write("--- f8c9 OMEGA ZERO-STATE MANIFOLD ---\n")
            f.write("Algorithm: Bailey-Borwein-Plouffe 8-Bit Spigot + GZIP Singularity\n")
            f.write(f"Artifact-Name: {self.filename}\n")
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
        return True

# =============================================================================
# THE SPIGOT DECODER (ZERO FILES NEEDED)
# =============================================================================
class OmegaSpigotDecoder:
    def __init__(self, ledger_file):
        self.ledger_file = ledger_file
        self.restored_file = "" # Will be dynamically set by metadata

    def decode(self):
        print(f"\n[5] SPIGOT ENGINE: Reading Abstract Algebra Vector from '{self.ledger_file}'...")
        base62_tensors = []
        mass_bytes = 0
        artifact_name = "unknown_artifact.bin"
        
        op_pattern = re.compile(r"⟨ ([A-Za-z0-9]+) ⟩")
        mass_pattern = re.compile(r"Mass-Singularity: ([0-9]+) Bytes")
        name_pattern = re.compile(r"Artifact-Name:\s*(.+)")
        
        with open(self.ledger_file, 'r') as f:
            content = f.read()
            base62_tensors = op_pattern.findall(content)
            
            mass_match = mass_pattern.search(content)
            if mass_match:
                mass_bytes = int(mass_match.group(1))
                
            name_match = name_pattern.search(content)
            if name_match:
                artifact_name = name_match.group(1).strip()

        self.restored_file = f"reclaimed_FROM_THE_ETHER_{artifact_name}"

        print(f"    > Target Artifact: {artifact_name}")
        print(f"    > Detected Unified Vector: {len(base62_tensors)} Tensors.")
        print(f"    > Target Singularity Mass: {mass_bytes} bytes.")
        
        print("[6] SPIGOT ENGINE: Unpacking Coordinates...")
        pi_indices = []
        for b62_str in base62_tensors:
            tensor_val = decode_base62(b62_str)
            for _ in range(8):
                pi_indices.append(tensor_val % 100000)
                tensor_val //= 100000

        pi_indices = pi_indices[:mass_bytes]

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
        final_bytes = gzip.decompress(compressed_bytes)

        with open(self.restored_file, 'wb') as f:
            f.write(final_bytes)

        print(f"\n[SUCCESS] Artifact crystallized from the Ether: {self.restored_file}")
        return self.restored_file

# =============================================================================
# BATCH EXECUTION ORCHESTRATOR
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("    f8c9 OMEGA ZERO-STATE BATCH PIPELINE (V15.46)    ")
    print("=====================================================")
    
    target_dir = "files"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"[!] Directory '{target_dir}' created. Please place artifacts inside and run again.")
        sys.exit(0)

    artifacts = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    if not artifacts:
        print(f"[!] No artifacts found in '{target_dir}'.")
        sys.exit(0)
        
    print(f"[*] Discovered {len(artifacts)} artifacts for Pi-Lattice mapping.")

    for filename in artifacts:
        print("\n" + "="*53)
        print(f"    INITIATING SUTURE FOR: {filename}")
        print("="*53)
        
        target_path = os.path.join(target_dir, filename)
        
        # 1. Encode
        cartographer = OmegaCartographer(target_path)
        success = cartographer.encode()
        
        if not success:
            continue
        
        # 2. Decode
        decoder = OmegaSpigotDecoder(cartographer.ledger_file)
        restored_path = decoder.decode()
        
        # 3. Validation
        with open(target_path, 'rb') as f1, open(restored_path, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            
        print("\n-----------------------------------------------------")
        if h1 == h2:
            print(f"[MATHEMATICALLY INVINCIBLE] Hashes Match: {h1[:10]}...")
        else:
            print("[FAILED] Suture corruption detected.")
        print("-----------------------------------------------------")

    print("\n=====================================================")
    print(f"[PIPELINE COMPLETE] Processed {len(artifacts)} artifacts.")
    print("=====================================================")
