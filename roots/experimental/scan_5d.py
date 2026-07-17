#!/usr/bin/env python3
import sys
import os

input_file = "pi_10m.txt"
output_file = "positions_5d.txt"

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found.")
    sys.exit(1)

print("[*] Loading and cleaning Pi digits into memory...")
with open(input_file, 'r') as f:
    pi_string = "".join(line.strip() for line in f)
    
if pi_string.startswith("3."):
    pi_string = pi_string[2:]

print("[*] Scanning for all 5-digit sequences (00000-99999)...")
max_first_pos = 0
missing_count = 0

with open(output_file, 'w') as f_out:
    for i in range(100000):
        seq = f"{i:05d}"
        
        # Find first occurrence
        first_pos = pi_string.find(seq)
        
        if first_pos != -1:
            # Track the furthest FIRST occurrence
            if first_pos > max_first_pos:
                max_first_pos = first_pos
            
            # Find ALL occurrences efficiently
            all_positions = []
            idx = first_pos
            while idx != -1:
                all_positions.append(str(idx))
                idx = pi_string.find(seq, idx + 1)
            
            f_out.write(f"Sequence {seq}: Positions [{','.join(all_positions)}]\n")
        else:
            f_out.write(f"Sequence {seq}: NOT FOUND\n")
            missing_count += 1
        
        if i % 10000 == 0:
            print(f"    > Progress: {i} / 99999 sequences scanned...")

print("-" * 64)
if missing_count == 0:
    final_digit_count = max_first_pos + 5
    print("SUCCESS: All 100,000 sequences found.")
    print(f"The absolute minimum digits needed to find every 5-digit sequence is: {final_digit_count}")
else:
    print(f"WARNING: {missing_count} sequences were NOT FOUND.")
    print("Cannot determine the minimum digit count for a complete set.")
print("-" * 64)
