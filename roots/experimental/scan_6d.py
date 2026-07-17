#!/usr/bin/env python3
import sys
import os
import time

def scan_6d_manifold(pi_file="333m.txt", output_file="positions_6d.txt"):
    if not os.path.exists(pi_file):
        print(f"[!] Critical Error: '{pi_file}' not found.")
        print("    Please ensure you have a large Pi file (15M+ digits) ready.")
        sys.exit(1)

    print(f"[*] Loading Pi digits from '{pi_file}'...")
    with open(pi_file, 'r') as f:
        pi_string = "".join(line.strip() for line in f if line.strip())

    # Strip the "3." if it exists
    if pi_string.startswith("3."):
        pi_string = pi_string[2:]

    print(f"[*] Loaded {len(pi_string)} digits.")
    print("[*] Initializing 6D Manifold Array (1,000,000 slots)...")
    
    # Pre-allocate an array of 1,000,000 slots, filled with -1
    # This is lightning fast and uses almost zero memory.
    first_occurrences = [-1] * 1000000
    found_count = 0
    max_position = 0
    last_found_seq = ""

    print("[*] Scanning the lattice... (This will be blazingly fast)")
    start_time = time.time()

    # Slide a 6-digit window across Pi
    for i in range(len(pi_string) - 5):
        chunk = pi_string[i : i+6]
        
        # Convert the 6-digit string to an integer index (0 to 999999)
        seq_idx = int(chunk)

        # If this is the FIRST time we've seen this integer...
        if first_occurrences[seq_idx] == -1:
            first_occurrences[seq_idx] = i
            found_count += 1
            
            # Track the deepest boundary dynamically
            if i > max_position:
                max_position = i
                last_found_seq = chunk

            # If we've found all 1,000,000 sequences, we can stop early!
            if found_count == 1000000:
                print("\n[+] DIMENSIONAL SATURATION ACHIEVED!")
                break

        # Periodic progress update
        if i % 2000000 == 0 and i > 0:
            print(f"    > Crossed {i:,} digits... Found {found_count:,} / 1,000,000")

    elapsed_time = time.time() - start_time
    print(f"\n[*] Scan completed in {elapsed_time:.2f} seconds.")

    # Write the results to the ledger
    print(f"[*] Writing map to '{output_file}'...")
    with open(output_file, 'w') as f_out:
        for seq_idx, pos in enumerate(first_occurrences):
            if pos != -1:
                # Format exactly like your 5D file: "00000 17533"
                f_out.write(f"{seq_idx:06d} {pos}\n")
            else:
                f_out.write(f"{seq_idx:06d} NOT_FOUND\n")

    # The Final Report
    print("================================================================")
    if found_count == 1000000:
        total_digits_needed = max_position + 6
        print(f"SUCCESS: The 6D Bulk is fully mapped.")
        print(f"The most stubborn sequence was: '{last_found_seq}'")
        print(f"It appeared at index: {max_position:,}")
        print(f"ABSOLUTE MINIMUM PI DIGITS NEEDED: {total_digits_needed:,}")
    else:
        missing = 1000000 - found_count
        print(f"WARNING: The Pi file was not large enough.")
        print(f"Found {found_count:,} sequences, missing {missing:,}.")
        print("You must provide a larger Pi dataset to map the 6D Manifold.")
    print("================================================================")

if __name__ == "__main__":
    # Make sure to update the filename here to whatever your 15M+ Pi file is named!
    scan_6d_manifold(pi_file="333m.txt", output_file="positions_6d.txt")
