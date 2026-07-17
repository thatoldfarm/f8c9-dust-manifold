#!/usr/bin/env python3
import sys
import os

def run_pi_file_search():
    segments_file = "sectorforth_segments.txt"
    pi_data_file = "pi_10m.txt" # MAKE SURE THIS MATCHES YOUR FILENAME
    output_file = "pi_locations.txt"
    
    # 1. Check if the Pi file exists
    if not os.path.exists(pi_data_file):
        print(f"[!] ERROR: '{pi_data_file}' not found.")
        print("    Please ensure your pi digits file is in this folder.")
        return

    # 2. Load and clean the Pi string
    print(f"[*] Reading Pi digits from '{pi_data_file}'...")
    with open(pi_data_file, 'r') as f:
        # We strip spaces and newlines in case the file is formatted
        pi_string = "".join(line.strip() for line in f if line.strip())
    
    print(f"[*] Loaded {len(pi_string)} digits of Pi.")

    # 3. Load your 6-digit (and 5-digit) sequences
    segments = []
    try:
        with open(segments_file, 'r') as f:
            for line in f:
                if "->" in line:
                    parts = line.split("->")
                    # We strip to catch Seq #207 which is 5 digits
                    segments.append(parts[1].strip())
    except FileNotFoundError:
        print(f"[!] Error: {segments_file} not found.")
        return

    # 4. Search
    print(f"[*] Searching for {len(segments)} segments...")
    results = []
    found_count = 0
    
    for idx, seg in enumerate(segments):
        # seg_len handles the 5-digit remainder case correctly
        seg_len = len(seg)
        pos = pi_string.find(seg)
        
        if pos != -1:
            # We store index and length to ensure perfect reconstruction later
            results.append(f"Seq #{idx+1:03} | Index: {pos:<8} | Len: {seg_len} | Data: {seg}")
            found_count += 1
        else:
            results.append(f"Seq #{idx+1:03} | NOT FOUND in file | Data: {seg}")

    # 5. Save results
    with open(output_file, 'w') as f_out:
        f_out.write(f"--- PIFS COORDINATE MAP ---\n")
        f_out.write(f"Source Pi File: {pi_data_file}\n")
        f_out.write(f"Total Matches:  {found_count} / {len(segments)}\n")
        f_out.write("-" * 50 + "\n")
        f_out.writelines("\n".join(results))

    print(f"\n[SUCCESS] Search complete!")
    print(f"    > Found: {found_count}/{len(segments)}")
    print(f"    > Locations saved to: '{output_file}'")

if __name__ == "__main__":
    run_pi_file_search()
