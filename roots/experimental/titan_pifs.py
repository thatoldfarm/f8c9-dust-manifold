#!/usr/bin/env python3
import sys
import os
import hashlib
from raw_pi_fs import RawPiFS

# Increase integer conversion limit for massive numbers
sys.set_int_max_str_digits(100000)

class PiFSPipeline:
    def __init__(self, target_file, pi_source_file, chunk_size=6):
        self.target_file = target_file
        self.pi_source_file = pi_source_file
        self.chunk_size = chunk_size
        
        # Intermediate filenames
        self.ledger_file = "pipeline.ledger"
        self.decimal_file = "pipeline_decimal.txt"
        self.segments_file = "pipeline_segments.txt"
        self.map_file = "pipeline_map.txt"
        self.restored_ledger = "pipeline_recovered.ledger"
        self.final_output = "pipeline_FINAL.img"

    def run(self):
        print("=====================================================")
        print("          STARTING FULL PiFS PIPELINE               ")
        print("=====================================================")

        # --- STEP 1: INITIALIZE RawPiFS AND ENCODE ---
        print("\n[STEP 1] Running Hex Substitution (RawPiFS)...")
        fs = RawPiFS()
        fs.store_file(self.target_file, self.ledger_file)

        # --- STEP 2: CONVERT TO GOD NUMBER ---
        print("\n[STEP 2] Converting Ledger Binary to God Number...")
        with open(self.ledger_file, 'rb') as f:
            ledger_bytes = f.read()
        
        god_int = int.from_bytes(ledger_bytes, byteorder='big')
        god_str = str(god_int)
        
        with open(self.decimal_file, 'w') as f:
            f.write(god_str)
        print(f"    > Total Digits in God Number: {len(god_str)}")

        # --- STEP 3: SEGMENTATION ---
        print("\n[STEP 3] Segmenting God Number into Chunks...")
        segments = [god_str[i : i + self.chunk_size] for i in range(0, len(god_str), self.chunk_size)]
        
        with open(self.segments_file, 'w') as f:
            for idx, seg in enumerate(segments):
                f.write(f"{idx+1:03}->{seg}\n")
        print(f"    > Created {len(segments)} segments.")

        # --- STEP 4: SEARCH Pi DIGITS ---
        print(f"\n[STEP 4] Searching for coordinates in '{self.pi_source_file}'...")
        if not os.path.exists(self.pi_source_file):
            print(f"    [!] Error: {self.pi_source_file} missing. Abortion pipeline.")
            return

        with open(self.pi_source_file, 'r') as f:
            pi_string = "".join(line.strip() for line in f if line.strip())

        coordinate_list = []
        found_count = 0
        
        for seg in segments:
            pos = pi_string.find(seg)
            if pos != -1:
                coordinate_list.append((pos, len(seg)))
                found_count += 1
        
        # Save results map
        with open(self.map_file, 'w') as f:
            for idx, (pos, length) in enumerate(coordinate_list):
                f.write(f"Seq #{idx+1:03} | Index: {pos:<8} | Len: {length}\n")

        print(f"    > Located {found_count}/{len(segments)} segments successfully.")

        # --- STEP 5: RECONSTRUCTION FROM Pi ---
        print("\n[STEP 5] Reconstructing from Pi coordinates...")
        recovered_god_str = ""
        for pos, length in coordinate_list:
            recovered_god_str += pi_string[pos : pos + length]

        # Verify string matches
        if god_str == recovered_god_str:
            print("    > Success: Reassembled God Number matches perfectly.")
        else:
            print("    [!] CORRUPTION: Reassembled digits do not match!")
            return

        # --- STEP 6: BACK TO BYTES ---
        print("\n[STEP 6] Converting God Number back to bytes...")
        recovered_int = int(recovered_god_str)
        # Use automated bit length to avoid overflow errors
        num_bytes = (recovered_int.bit_length() + 7) // 8
        recovered_ledger_bytes = recovered_int.to_bytes(num_bytes, byteorder='big')
        
        with open(self.restored_ledger, 'wb') as f:
            f.write(recovered_ledger_bytes)

        # --- STEP 7: FINAL DECODE ---
        print("\n[STEP 7] Applying Reverse Pi Substitution...")
        fs.retrieve_file(self.restored_ledger, self.final_output)

        print("\n=====================================================")
        print("              PIPELINE SUCCESSFUL                   ")
        print("=====================================================")
        print(f"Original:  {self.target_file}")
        print(f"Restored:  {self.final_output}")
        
        # SHA256 Verification
        with open(self.target_file, 'rb') as f1, open(self.final_output, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            if h1 == h2:
                print(f"Integrity: VALID (Hashes Match: {h1[:10]})")
            else:
                print("Integrity: FAILED (Hashes do not match)")

if __name__ == "__main__":
    # Ensure you use your large Pi file here
    pipeline = PiFSPipeline(
        target_file="sectorforth.img", 
        pi_source_file="pi_10m.txt"
    )
    pipeline.run()
