#!/usr/bin/env python3
import sys
import os
import hashlib
from raw_pi_fs import RawPiFS

# Set limits for massive integer handling
sys.set_int_max_str_digits(100000)

class HolographicPiFS:
    def __init__(self, target_file, pi_file="pi_8555.txt"):
        self.target_file = target_file
        self.pi_file = pi_file
        self.temp_ledger = "holographic.ledger"
        self.holographic_map = "holographic_routing_map.txt"
        self.restored_file = "reclaimed_sectorforth.img"
        
        if not os.path.exists(pi_file):
            print(f"[!] Critical Error: '{pi_file}' missing.")
            sys.exit(1)

    def _get_pi_string(self):
        with open(self.pi_file, 'r') as f:
            return "".join(line.strip() for line in f if line.strip())

    def run_full_pipeline(self):
        print("=====================================================")
        print("      f8c9 HOLOGRAPHIC PiFS PIPELINE (V15.41)        ")
        print("=====================================================")

        # --- STEP 1: INITIAL HEX SUBSTITUTION ---
        print("\n[1] Performing Pi-Lattice Substitution (Rosetta Map)...")
        fs = RawPiFS()
        fs.store_file(self.target_file, self.temp_ledger)

        # --- STEP 2: GOD NUMBER CONVERSION ---
        with open(self.temp_ledger, 'rb') as f:
            ledger_bytes = f.read()
        god_int = int.from_bytes(ledger_bytes, byteorder='big')
        god_str = str(god_int)
        print(f"[2] God Number converted. Digits: {len(god_str)}")

        # --- STEP 3: HOLOGRAPHIC ENCODING (THE LATTICE) ---
        print("\n[3] Encoding: Mapping 3D Corridors to 2D Room Boundaries...")
        pi_string = self._get_pi_string()
        
        # Pre-index Room Locations (00-99)
        room_map = {f"{i:02}": [] for i in range(100)}
        for i in range(len(pi_string) - 3):
            pair = pi_string[i:i+2]
            room_map[pair].append(i)

        # Break into 3-digit corridors
        chunks = [god_str[i : i+3] for i in range(0, len(god_str), 3)]
        ledger_entries = []

        for count, chunk in enumerate(chunks):
            if len(chunk) < 3: # Handle remainder digit
                ledger_entries.append({"raw": chunk})
                continue
                
            room_id = chunk[:2]
            tail = chunk[2]
            
            # Find the specific occurrence of the room that matches the tail
            found_idx = -1
            for occ_idx, pi_pos in enumerate(room_map[room_id]):
                if pi_string[pi_pos + 2] == tail:
                    found_idx = occ_idx
                    break
            
            if found_idx != -1:
                ledger_entries.append({"room": room_id, "occ": found_idx})
            else:
                ledger_entries.append({"raw": chunk}) # Fallback logic

        # Write out the Coordinate Map (The actual tiny file)
        with open(self.holographic_map, 'w') as f:
            for entry in ledger_entries:
                if "room" in entry:
                    f.write(f"R:{entry['room']}|O:{entry['occ']}\n")
                else:
                    f.write(f"L:{entry['raw']}\n")
        print(f"[SUCCESS] Routing Map generated: '{self.holographic_map}'")

        # --- STEP 4: HOLOGRAPHIC RECONSTRUCTION ---
        print("\n[4] Reconstructing: Projecting 2D addresses back into Bulk...")
        reassembled_digits = ""
        for entry in ledger_entries:
            if "room" in entry:
                room_id = entry["room"]
                occ_idx = entry["occ"]
                # Go to pi, find index, grab 3
                pi_pos = room_map[room_id][occ_idx]
                reassembled_digits += pi_string[pi_pos : pi_pos + 3]
            else:
                reassembled_digits += entry["raw"]

        if reassembled_digits == god_str:
            print("    > Match Verified: Holographic reconstruction successful.")
        else:
            print("    [!] ERROR: Digits mismatch in reconstruction!")
            return

        # --- STEP 5: FINAL BINARY RECOVERY ---
        print("\n[5] Translating Pi addresses back into binary images...")
        recovered_int = int(reassembled_digits)
        # 512 bytes = bit_length() approx
        recovered_bytes = recovered_int.to_bytes(512, byteorder='big')
        
        with open("temp_recovery.ledger", 'wb') as f:
            f.write(recovered_bytes)
            
        fs.retrieve_file("temp_recovery.ledger", self.restored_file)

        # --- STEP 6: CHECKSUM VALIDATION ---
        with open(self.target_file, 'rb') as f1, open(self.restored_file, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            
        print("\n=====================================================")
        if h1 == h2:
            print(f"[COMPLETE] VALIDATED: SectorForth is mathematically intact.")
            print(f"Hash: {h1[:10]}...")
        else:
            print("[FAILED] Corruption in the Holographic suture.")
        print("=====================================================")

if __name__ == "__main__":
    pipeline = HolographicPiFS("sectorforth.img", "pi_8555.txt")
    pipeline.run_full_pipeline()
