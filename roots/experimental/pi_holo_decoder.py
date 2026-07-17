#!/usr/bin/env python3
import sys
import os

def generate_holographic_map(pi_file, data_decimal_file, output_map_file):
    if not os.path.exists(pi_file):
        print(f"[!] Error: {pi_file} missing.")
        return
    
    # 1. Load Pi string
    with open(pi_file, 'r') as f:
        pi_string = "".join(line.strip() for line in f if line.strip())
    
    # 2. Load SectorForth God Number (Decimal)
    with open(data_decimal_file, 'r') as f:
        full_digits = "".join(line.strip() for line in f if line.isdigit())
        
    # 3. Create the appearance dictionary for Rooms (00-99)
    # We pre-calculate all positions of 2-digit sequences to make lookup O(1)
    print("[*] Pre-indexing Room occurrences in Pi...")
    room_map = {f"{i:02}": [] for i in range(100)}
    for i in range(len(pi_string) - 2):
        pair = pi_string[i:i+2]
        if pair in room_map:
            room_map[pair].append(i)

    # 4. Break file into 3-digit "Corridors"
    # We split 1,233 digits into 411 x 3-digit sequences
    chunks = [full_digits[i:i+3] for i in range(0, len(full_digits), 3)]
    
    print(f"[*] Mapping {len(chunks)} corridors to Room Boundary...")
    holographic_ledger = []
    
    for count, corridor in enumerate(chunks):
        room_id = corridor[:2]    # The 2D Boundary (first 2 digits)
        target_tail = corridor[2] # The depth digit (3rd digit)
        
        found = False
        # Look through appearances of the room until we find the 3-digit match
        for occurrence_idx, pi_pos in enumerate(room_map[room_id]):
            # If the next digit at this location matches our corridor's tail
            if pi_string[pi_pos + 2] == target_tail:
                # We save the Room and WHICH occurrence it was
                holographic_ledger.append({
                    "seq": count + 1,
                    "room": room_id,
                    "occ": occurrence_idx,
                    "pi_idx": pi_pos
                })
                found = True
                break
        
        if not found:
            print(f"    [!] Sequence {corridor} not found in lattice context!")

    # 5. Write the Holographic Map
    with open(output_map_file, 'w') as f:
        f.write(f"--- f8c9 HOLOGRAPHIC ROUTING MAP ---\n")
        f.write(f"Boundary: 00-99 | Bulk: 000-999\n")
        f.write("-" * 45 + "\n")
        for entry in holographic_ledger:
            # We only really need to store 'room' and 'occ'
            # That is enough to perfectly rebuild the corridor.
            f.write(f"[{entry['seq']:03}] Room: {entry['room']} | Use Occurrence: {entry['occ']:<5}\n")

    print(f"[SUCCESS] Holographic Map created: {output_map_file}")
    print(f"    Note: Each entry now only points to a Room ID and an Occurrence Index.")

if __name__ == "__main__":
    generate_holographic_map("pi_10m.txt", "sectorforth_decimal.txt", "pi_holographic_ledger.txt")
