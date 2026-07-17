#!/usr/bin/env python3
import os
from raw_pi_fs import RawPiFS  # Imports the core engine!

def generate_rosetta_stone():
    print("==========================================================")
    print("        GENERATING THE ROSETTA BLOB (S-BOX MATRIX)        ")
    print("==========================================================")

    fs = RawPiFS()

    # 1. Create the "Perfect File" (0x00 to 0xFF)
    perfect_file_bytes = bytes(range(256))
    
    with open("rosetta_input.bin", "wb") as f:
        f.write(perfect_file_bytes)
        
    print("[*] Created 256-byte Perfect File (0x00 to 0xFF).")

    # 2. Encode the Perfect File using PiFS
    fs.store_file("rosetta_input.bin", "rosetta_output.ledger")
    
    # 3. Read the resulting Ledger
    with open("rosetta_output.ledger", "rb") as f:
        ledger_bytes = f.read()

    # 4. Generate the Text Map and Console Output
    print("\n--- THE PI-LATTICE MASTER TRANSLATION MAP ---")
    
    # Open a text file to write ALL 256 mappings
    with open("rosetta_map.txt", "w") as map_file:
        map_file.write("--- THE PI-LATTICE MASTER TRANSLATION MAP ---\n")
        map_file.write("Original Byte -> PiFS Ledger Byte\n")
        map_file.write("-" * 40 + "\n")
        
        for i in range(256):
            # Format as 2-character hex (e.g., '0a')
            orig_hex = f"{perfect_file_bytes[i]:02x}"
            encoded_hex = f"{ledger_bytes[i]:02x}"
            
            # Write every single mapping to the text document
            map_file.write(f"      {orig_hex}       ->       {encoded_hex}\n")
            
            # Print just the first 16 to the terminal to keep it clean
            if i < 16:
                print(f"      {orig_hex}       ->       {encoded_hex}")
                
    print("      ...      ->       ...")
    print(f"      {perfect_file_bytes[-1]:02x}       ->       {ledger_bytes[-1]:02x}")
    print("-" * 40)
    
    print("[!] The Rosetta Blob successfully generated.")
    print("[!] Full dictionary saved to: 'rosetta_map.txt'")
    print("\n[*] Files left on disk for inspection:")
    print("    1. rosetta_input.bin      (The raw 0x00-0xFF bytes)")
    print("    2. rosetta_output.ledger  (The encoded Pi coordinates)")
    print("    3. rosetta_map.txt        (The human-readable cipher key)")

if __name__ == "__main__":
    generate_rosetta_stone()
