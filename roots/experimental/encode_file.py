#!/usr/bin/env python3
import os
from raw_pi_fs import RawPiFS

def main():
    target_file = "rosetta_map.txt"
    encoded_file = "rosetta_map.ledger"
    mapping_file = "rosetta_map_mapping.txt"

    if not os.path.exists(target_file):
        print(f"[!] ERROR: '{target_file}' not found in this directory.")
        return

    # 1. Initialize PiFS
    print("[*] Starting PiFS Engine...")
    fs = RawPiFS()

    # 2. Encode the file (Creates the .ledger)
    print(f"\n[*] Encoding '{target_file}'...")
    fs.store_file(target_file, encoded_file)

    # 3. Read both files to generate the mapping log
    print(f"[*] Generating detailed mapping log: '{mapping_file}'...")
    with open(target_file, 'rb') as f_in:
        orig_bytes = f_in.read()
        
    with open(encoded_file, 'rb') as f_out:
        encoded_bytes = f_out.read()

    # 4. Write the side-by-side comparison to a text file
    with open(mapping_file, 'w') as f_map:
        f_map.write(f"--- PIFS MAPPING LOG FOR: {target_file} ---\n")
        f_map.write(f"File Size: {len(orig_bytes)} bytes\n\n")
        f_map.write("Offset   | Original | Encoded (Pi Ledger)\n")
        f_map.write("-----------------------------------------\n")
        
        # Loop through every single byte and record the translation
        for i in range(len(orig_bytes)):
            offset_hex = f"{i:04x}"
            orig_hex = f"{orig_bytes[i]:02x}"
            enc_hex = f"{encoded_bytes[i]:02x}"
            
            f_map.write(f"0x{offset_hex}   |    {orig_hex}    |    {enc_hex}\n")

    print("\n[SUCCESS] Process complete!")
    print(f"    > Encoded File: {encoded_file}")
    print(f"    > Mapping Log:  {mapping_file}")

if __name__ == "__main__":
    main()
