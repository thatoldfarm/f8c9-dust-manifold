#!/usr/bin/env python3
import sys
import os
import hashlib
import re
from raw_pi_fs import RawPiFS

sys.set_int_max_str_digits(100000)

class SacredGeometryEngine:
    def __init__(self, target_file, pi_file="pi_100k.txt"):
        self.target_file = target_file
        self.pi_file = pi_file
        self.temp_ledger = "geometry.ledger"
        self.blueprint_file = "sacred_geometry_blueprint.txt"
        self.restored_file = "reclaimed_sectorforth.img"
        
        if not os.path.exists(pi_file):
            print(f"[!] Critical Error: '{pi_file}' missing.")
            sys.exit(1)

    def _get_pi_string(self):
        with open(self.pi_file, 'r') as f:
            return "".join(line.strip() for line in f if line.strip())

    def run_full_pipeline(self):
        print("=====================================================")
        print("    f8c9 SACRED GEOMETRY ENGINE PIPELINE (V15.43)    ")
        print("      [ Dynamic Dimensionality & 100K L2 Cache ]     ")
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
        print("\n[3] Generating Architectural Blueprint (Greedy Holographic Map)...")
        pi_string = self._get_pi_string()
        
        # Pre-index Room Locations (00-99)
        room_map = {f"{i:02}": [] for i in range(100)}
        for i in range(len(pi_string) - 6): # -6 for safety up to 6D manifolds
            pair = pi_string[i:i+2]
            room_map[pair].append(i)

        blueprint_entries = []
        idx = 0
        
        while idx < len(god_str):
            found_shape = False
            
            # Dynamically try to find the deepest dimension (6D down to 3D)
            for dim, shape, p1, p2 in [
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
            
            # If no mathematical occurrence is found (or we hit remainder digits)
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
            f.write("--- f8c9 SACRED GEOMETRY BLUEPRINT ---\n")
            f.write("Topology: 1D to 6D Holographic Projection\n")
            f.write("-" * 45 + "\n")
            for entry in blueprint_entries:
                f.write(f"{entry}\n")
                    
        print(f"[SUCCESS] Blueprint Generated: '{self.blueprint_file}'")
        print(f"    > The OS was compressed into {len(blueprint_entries)} geometric shapes.")

        # --- STEP 4: BLUEPRINT RECONSTRUCTION ---
        print("\n[4] Reconstructing OS from Geometry...")
        reassembled_digits = ""
        
        shape_pattern = re.compile(r"([A-Za-z]+)\([a-z]+=([0-9]+)(?:, [a-z]+=([0-9]+))?\)")
        
        for entry in blueprint_entries:
            match = shape_pattern.match(entry)
            if not match: continue
            
            shape = match.group(1)
            p1 = match.group(2)
            p2 = match.group(3)
            
            if shape == "Manifold":
                pi_pos = room_map[p1.zfill(2)][int(p2)]
                reassembled_digits += pi_string[pi_pos : pi_pos + 6]
            elif shape == "Penteract":
                pi_pos = room_map[p1.zfill(2)][int(p2)]
                reassembled_digits += pi_string[pi_pos : pi_pos + 5]
            elif shape == "Tesseract":
                pi_pos = room_map[p1.zfill(2)][int(p2)]
                reassembled_digits += pi_string[pi_pos : pi_pos + 4]
            elif shape == "Cylinder":
                pi_pos = room_map[p1.zfill(2)][int(p2)]
                reassembled_digits += pi_string[pi_pos : pi_pos + 3]
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
    pipeline = SacredGeometryEngine("sectorforth.img", "pi_100k.txt")
    pipeline.run_full_pipeline()
