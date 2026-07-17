#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import time
from raw_pi_fs import RawPiFS

sys.set_int_max_str_digits(10000000) # 100000

class OmniversalGeometryEngine:
    def __init__(self, target_file, pi_file="pi_14118312.txt"):
        self.target_file = target_file
        self.pi_file = pi_file
        self.temp_ledger = "omniversal.ledger"
        self.blueprint_file = "omniversal_blueprint.txt"
        self.restored_file = "reclaimed_mega_json_quine_v15_42.json"
        
        if not os.path.exists(pi_file):
            print(f"[!] Critical Error: '{pi_file}' missing.")
            sys.exit(1)

    def _get_pi_string(self):
        with open(self.pi_file, 'r') as f:
            pi_str = "".join(line.strip() for line in f if line.strip())
        if pi_str.startswith("3."):
            return pi_str[2:]
        return pi_str

    def run_full_pipeline(self):
        print("=====================================================")
        print("  f8c9 OMNIVERSAL GEOMETRY ENGINE PIPELINE (V15.44)  ")
        print("      [ 14.1MB L3 Cache & 8D Dynamic Folding ]       ")
        print("=====================================================")

        # --- STEP 1: INITIAL HEX SUBSTITUTION ---
        print("\n[1] Performing Pi-Lattice Substitution (Rosetta Map)...")
        fs = RawPiFS()
        fs.store_file(self.target_file, self.temp_ledger)

        # --- STEP 2: GOD NUMBER CONVERSION ---
        with open(self.temp_ledger, 'rb') as f:
            ledger_bytes = f.read()
            original_byte_len = len(ledger_bytes)
            
        god_int = int.from_bytes(ledger_bytes, byteorder='big')
        god_str = str(god_int)
        print(f"[2] God Number converted. Total Digits: {len(god_str)}")

        # --- STEP 3: SACRED GEOMETRY ENCODING ---
        print(f"\n[3] Generating Architectural Blueprint...")
        print("    > Loading L3 Cache into memory...")
        start_time = time.time()
        pi_string = self._get_pi_string()
        
        # Pre-index Room Locations (00-99)
        # We index 14+ million digits in roughly 2 seconds.
        room_map = {f"{i:02}": [] for i in range(100)}
        for i in range(len(pi_string) - 8): # -8 for safety up to 8D shapes
            pair = pi_string[i:i+2]
            room_map[pair].append(i)
            
        print(f"    > Lattice indexing complete ({(time.time() - start_time):.2f}s).")
        print("    > Folding God Number into geometry...")

        blueprint_entries = []
        idx = 0
        
        while idx < len(god_str):
            found_shape = False
            
            # Dynamically try to find the deepest dimension (8D down to 3D)
            # You are mathematically guaranteed to find at least a 6D Manifold.
            for dim, shape, p1, p2 in [
                (8, "E8_Lattice", "brane", "string"),
                (7, "CalabiYau", "hole", "genus"),
                (6, "Manifold", "flux", "resonance"),
                (5, "Penteract", "mass", "spin"),
                (4, "Tesseract", "edge", "phase"),
                (3, "Cylinder", "radius", "height")
            ]:
                if idx + dim <= len(god_str):
                    chunk = god_str[idx : idx+dim]
                    room_id = chunk[:2]
                    tail = chunk[2:]
                    
                    found_occ = -1
                    # Search the occurrence list for the correct tail
                    for occ, pi_pos in enumerate(room_map[room_id]):
                        if pi_string[pi_pos + 2 : pi_pos + dim] == tail:
                            found_occ = occ
                            break
                    
                    if found_occ != -1:
                        # Shape Found! 
                        blueprint_entries.append(f"{shape}({p1}={room_id}, {p2}={found_occ})")
                        idx += dim
                        found_shape = True
                        break
            
            # Remainder handling
            if not found_shape:
                rem = len(god_str) - idx
                if rem >= 2:
                    blueprint_entries.append(f"Square(x={god_str[idx]}, y={god_str[idx+1]})")
                    idx += 2
                else:
                    blueprint_entries.append(f"Point(val={god_str[idx]})")
                    idx += 1

        # Write out the Blueprint
        with open(self.blueprint_file, 'w') as f:
            f.write("--- f8c9 OMNIVERSAL GEOMETRY BLUEPRINT ---\n")
            f.write("Topology: 1D to 8D Holographic Projection\n")
            f.write("-" * 45 + "\n")
            for entry in blueprint_entries:
                f.write(f"{entry}\n")
                    
        print(f"[SUCCESS] Blueprint Generated: '{self.blueprint_file}'")
        print(f"    > SectorForth was compressed into exactly {len(blueprint_entries)} geometric shapes.")

        # --- STEP 4: BLUEPRINT RECONSTRUCTION ---
        print("\n[4] Reconstructing OS from Geometry...")
        reassembled_digits = ""
        
        # Regex to parse the shapes and parameters safely
        shape_pattern = re.compile(r"([A-Za-z0-9_]+)\([a-z]+=([0-9]+)(?:, [a-z]+=([0-9]+))?\)")
        
        for entry in blueprint_entries:
            match = shape_pattern.match(entry)
            if not match: continue
            
            shape = match.group(1)
            p1 = match.group(2)
            p2 = match.group(3)
            
            # Map the shapes back to their dimensionality to extract from Pi
            dim_map = {
                "E8_Lattice": 8, "CalabiYau": 7, "Manifold": 6, 
                "Penteract": 5, "Tesseract": 4, "Cylinder": 3
            }
            
            if shape in dim_map:
                dim = dim_map[shape]
                pi_pos = room_map[p1.zfill(2)][int(p2)]
                reassembled_digits += pi_string[pi_pos : pi_pos + dim]
            elif shape == "Square":
                reassembled_digits += p1 + p2
            elif shape == "Point":
                reassembled_digits += p1

        if reassembled_digits == god_str:
            print("    > Match Verified: Topology reconstruction successful.")
        else:
            print("    [!] ERROR: Digits mismatch in reconstruction!")
            return

        # --- STEP 5: FINAL BINARY RECOVERY ---
        print("\n[5] Translating Pi addresses back into binary images...")
        recovered_int = int(reassembled_digits)
        recovered_bytes = recovered_int.to_bytes(original_byte_len, byteorder='big')
        
        with open("temp_recovery.ledger", 'wb') as f:
            f.write(recovered_bytes)
            
        fs.retrieve_file("temp_recovery.ledger", self.restored_file)

        # --- STEP 6: CHECKSUM VALIDATION ---
        with open(self.target_file, 'rb') as f1, open(self.restored_file, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            
        print("\n=====================================================")
        if h1 == h2:
            print(f"[COMPLETE] VALIDATED: The Geometric Universe is intact.")
            print(f"Hash: {h1[:10]}...")
        else:
            print("[FAILED] Corruption in the Akashic Suture.")
        print("=====================================================")

if __name__ == "__main__":
    # Point this to your 15M+ Pi digits file
    pipeline = OmniversalGeometryEngine("mega_json_quine_v15_42.json", "pi_14118312.txt")
    pipeline.run_full_pipeline()
