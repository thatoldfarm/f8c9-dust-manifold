#!/usr/bin/env python3
import os
from raw_pi_fs import RawPiFS

def main():
    # Define your filenames
    target_file = "rosetta_map.txt"
    encoded_file = "rosetta_map.ledger"
    restored_file = "rosetta_map_RESTORED.txt"

    # Make sure the file actually exists before trying to encode it
    if not os.path.exists(target_file):
        print(f"[!] ERROR: '{target_file}' not found in this directory.")
        return

    # 1. Boot up the PiFS engine (this automatically calculates Pi and finds the map)
    print("Starting PiFS Engine...")
    fs = RawPiFS()

    # 2. Encode the file
    print(f"\n--- ENCODING ---")
    fs.store_file(target_file, encoded_file)
    print(f"[SUCCESS] Your file has been encoded into Pi coordinates as '{encoded_file}'")

    # 3. (Optional) Decode it right away to prove it worked!
    print(f"\n--- VERIFYING ---")
    fs.retrieve_file(encoded_file, restored_file)
    print(f"[SUCCESS] File successfully decoded back into '{restored_file}'")

if __name__ == "__main__":
    main()
