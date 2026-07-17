#!/usr/bin/env python3
import sys
import os
from raw_pi_fs import RawPiFS

sys.set_int_max_str_digits(10000)

def run_pi_reconstruction():
    locations_file = "pi_locations.txt"
    pi_data_file = "pi_10m.txt"
    restored_ledger = "pi_recovered.ledger"
    final_output = "sectorforth_FROM_PI.img"
    
    # 1. Load Pi data
    if not os.path.exists(pi_data_file):
        print(f"[!] ERROR: {pi_data_file} missing.")
        return
    with open(pi_data_file, 'r') as f:
        pi_string = "".join(line.strip() for line in f if line.strip())

    # 2. Parse the Coordinate Map
    print(f"[*] Reading coordinates from '{locations_file}'...")
    segments = []
    try:
        with open(locations_file, 'r') as f:
            for line in f:
                if "|" in line and "Index:" in line:
                    parts = line.split("|")
                    idx = int(parts[1].split(":")[1].strip())
                    length = int(parts[2].split(":")[1].strip())
                    segments.append((idx, length))
    except Exception as e:
        print(f"[!] Error reading locations: {e}")
        return

    # 3. Dig up the numbers from Pi
    print(f"[*] Extracting {len(segments)} segments from Pi...")
    god_number_str = ""
    for idx, length in segments:
        god_number_str += pi_string[idx : idx + length]

    # 4. Convert Decimal God Number back to bytes
    print("[*] Reassembling ledger from God Number...")
    god_int = int(god_number_str)
    # Calculate how many bytes are actually needed
    num_bytes = (god_int.bit_length() + 7) // 8
    ledger_bytes = god_int.to_bytes(num_bytes, byteorder='big')
    
    with open(restored_ledger, 'wb') as f:
        f.write(ledger_bytes)

    # 5. Final Step: Decode via RawPiFS engine
    print("[*] Decoding Pi coordinates into final binary...")
    fs = RawPiFS()
    fs.retrieve_file(restored_ledger, final_output)

    print(f"\n[SUCCESS] Archaeology complete!")
    print(f"    > Reconstructed File: {final_output}")
    print(f"    > Checksum should match original sectorforth.img!")

if __name__ == "__main__":
    run_pi_reconstruction()
