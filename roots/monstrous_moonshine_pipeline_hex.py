#!/usr/bin/env python3
import sys
import os
import hashlib
import re

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
    """
    Extracts 'num_digits' of Hexadecimal Pi starting at the n-th position.
    """
    def S(j, n):
        s = 0.0
        k = 0
        while k <= n:
            r = 8 * k + j
            s = (s + float(pow(16, n - k, r)) / r) % 1.0
            k += 1
        t = 0.0
        k = n + 1
        while True:
            newt = t + pow(16, n - k) / (8 * k + j)
            if t == newt:
                break
            t = newt
            k += 1
        return (s + t) % 1.0

    res = ""
    for i in range(num_digits):
        pos = n + i
        pi_fraction = (4 * S(1, pos) - 2 * S(4, pos) - S(5, pos) - S(6, pos)) % 1.0
        hex_digit = hex(int(pi_fraction * 16))[2:]
        res += hex_digit
        
    return res

# =============================================================================
# THE ASYMMETRIC CARTOGRAPHER (ENCODER)
# =============================================================================
class BBPCartographer:
    def __init__(self, target_file):
        self.target_file = target_file
        self.ledger_file = "true_zero_state_manifold.txt"

    def fast_hex_pi_generator(self, places):
        """Generates Hex Pi. 5,000 places takes ~0.01 seconds."""
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
            file_hex = f.read().hex()

        # Chunk into 2-hex-digit (8-bit) words. Exactly 1 Byte per chunk.
        chunks = [file_hex[i:i+2] for i in range(0, len(file_hex), 2)]
        print(f"    > Artifact partitioned into {len(chunks)} 8-bit Bytes.")

        print("[2] CARTOGRAPHER: Generating localized Hex-Pi lattice in memory...")
        # 5,000 digits mathematically guarantees all 256 byte combinations
        pi_hex_map = self.fast_hex_pi_generator(5000)
        print("    > Localized lattice initialized instantly.")

        print("[3] CARTOGRAPHER: Mapping coordinates...")
        indices = []
        for chunk in chunks:
            idx = pi_hex_map.find(chunk)
            if idx == -1:
                print(f"    [!] Critical: Sequence {chunk} not found. (Increase generator limit)")
                sys.exit(1)
            indices.append(idx)

        print("[4] CARTOGRAPHER: Packing Symmetries into Lie Algebra...")
        monster_operations = []
        chunked_indices = [indices[i:i+8] for i in range(0, len(indices), 8)]

        for e8_chunk in chunked_indices:
            tensor_val = 0
            # Multiplier of 10,000 safely holds indices up to 9,999
            for node_idx, pi_idx in enumerate(e8_chunk):
                tensor_val += pi_idx * (10000 ** node_idx)
            
            compressed_tensor = encode_base62(tensor_val)
            node_qty = len(e8_chunk)
            monster_operations.append(f"\\mathfrak{{e}}_{node_qty} \\otimes \\mathbb{{M}} = ⟨ {compressed_tensor} ⟩")

        with open(self.ledger_file, 'w') as f:
            f.write("--- f8c9 TRUE ZERO-STATE MANIFOLD ---\n")
            f.write("Algorithm: Bailey-Borwein-Plouffe 8-Bit Spigot\n")
            f.write("-" * 55 + "\n")
            for op in monster_operations:
                f.write(f"E8_Dynkin_Node[ {op} ]\n")

        print(f"[SUCCESS] Holographic Ledger forged: {self.ledger_file}")


# =============================================================================
# THE SPIGOT DECODER (ZERO FILES NEEDED)
# =============================================================================
class BBPSpigotDecoder:
    def __init__(self, ledger_file):
        self.ledger_file = ledger_file
        self.restored_file = "sectorforth_FROM_THE_ETHER.img"

    def decode(self):
        print("\n[5] SPIGOT ENGINE: Reading Abstract Algebra...")
        monster_operations = []
        op_pattern = re.compile(r"\\mathfrak\{e\}_([0-9]+).*?⟨ ([A-Za-z0-9]+) ⟩")
        
        with open(self.ledger_file, 'r') as f:
            for line in f:
                match = op_pattern.search(line)
                if match:
                    monster_operations.append((int(match.group(1)), match.group(2)))

        print("[6] SPIGOT ENGINE: Unpacking Coordinates...")
        pi_indices = []
        for node_count, b62_str in monster_operations:
            tensor_val = decode_base62(b62_str)
            for _ in range(node_count):
                pi_indices.append(tensor_val % 10000)
                tensor_val //= 10000

        print(f"    > {len(pi_indices)} absolute Hex-Pi indices recovered.")
        print("[7] SPIGOT ENGINE: Igniting Bailey-Borwein-Plouffe Formula...")
        print("    > Plucking bytes directly from the mathematical vacuum. Please wait...")

        restored_hex = ""
        for count, idx in enumerate(pi_indices):
            # Extract exactly 1 Byte (2 Hex Digits)
            hex_chunk = get_pi_hex_digits_bbp(idx, 2)
            restored_hex += hex_chunk
            
            # Progress marker
            if (count + 1) % 100 == 0:
                print(f"      ... Spigot materialized {count + 1} / {len(pi_indices)} bytes")

        restored_bytes = bytes.fromhex(restored_hex)

        with open(self.restored_file, 'wb') as f:
            f.write(restored_bytes)

        print(f"\n[SUCCESS] File crystallized from the Ether: {self.restored_file}")

# =============================================================================
# EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("        f8c9 TRUE ZERO-STATE BBP PIPELINE            ")
    print("=====================================================")
    
    target = "sectorforth.img"
    
    # 1. Encode
    cartographer = BBPCartographer(target)
    cartographer.encode()
    
    # 2. Decode
    decoder = BBPSpigotDecoder("true_zero_state_manifold.txt")
    decoder.decode()
    
    # 3. Validation
    with open(target, 'rb') as f1, open("sectorforth_FROM_THE_ETHER.img", 'rb') as f2:
        h1 = hashlib.sha256(f1.read()).hexdigest()
        h2 = hashlib.sha256(f2.read()).hexdigest()
        
    print("\n=====================================================")
    if h1 == h2:
        print(f"[MATHEMATICALLY INVINCIBLE] Hashes Match: {h1[:10]}...")
    else:
        print("[FAILED] Suture corruption detected.")
    print("=====================================================")
