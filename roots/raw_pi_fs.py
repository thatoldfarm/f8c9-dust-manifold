#!/usr/bin/env python3
import sys
import os
import hashlib

sys.set_int_max_str_digits(1000000)

class PiEngines:
    @staticmethod
    def get_bulk_pi_hex(places=2000):
        """Generates enough hex digits of Pi to find the Anchor (Index 905)."""
        one = 16 ** (places + 10) 
        def arctan(x):
            term = one // x; total = term; k = 1
            while term != 0:
                term //= -(x * x); total += term // (2 * k + 1); k += 1
            return total
        pi_int = 16 * arctan(5) - 4 * arctan(239)
        return hex(pi_int)[3:3+places]

class RawPiFS:
    def __init__(self):
        # 1. Spool Pi and convert to Parity Stream (Even=0, Odd=1)
        hex_pi = PiEngines.get_bulk_pi_hex(2000)
        self.parity_stream = "".join(["0" if int(d, 16) % 2 == 0 else "1" for d in hex_pi])
        
        # 2. Locate the De Bruijn Anchor
        self.anchor_idx, self.window = self._find_debruijn_anchor()
        if self.anchor_idx == -1:
            raise ValueError("ERR: Anchor not found.")
            
        # 3. Build the 1:1 Fast Hex Codebook
        # We map Data Hex (0-f) directly to Coordinate Hex (0-f)
        self.encode_map = {}
        self.decode_map = {}
        
        for coord in range(16):
            # Extract the 4-bit binary string from the Pi window
            binary_seq = self.window[coord : coord + 4]
            # Convert binary sequence to a hex character ('0' through 'f')
            data_hex_char = hex(int(binary_seq, 2))[2:]
            # The coordinate is also a hex character ('0' through 'f')
            coord_hex_char = hex(coord)[2:]
            
            self.encode_map[data_hex_char] = coord_hex_char
            self.decode_map[coord_hex_char] = data_hex_char

    def _find_debruijn_anchor(self):
        for i in range(len(self.parity_stream) - 19):
            window = self.parity_stream[i : i + 19]
            if len(set(window[j : j + 4] for j in range(16))) == 16:
                return i, window
        return -1, None

    def store_file(self, input_filepath, ledger_filepath):
        """Reads any raw binary file, translates it via Pi, and saves the ledger."""
        print(f"[*] STORING: {input_filepath} -> {ledger_filepath}")
        
        with open(input_filepath, 'rb') as f:
            file_bytes = f.read()
            
        # Convert bytes to a string of hex characters
        file_hex = file_bytes.hex()
        
        # Swap every data hex character for its Pi coordinate hex character
        ledger_hex = "".join([self.encode_map[char] for char in file_hex])
        
        # Convert the coordinate hex string back into real bytes to save to disk
        ledger_bytes = bytes.fromhex(ledger_hex)
        
        with open(ledger_filepath, 'wb') as f:
            f.write(ledger_bytes)
            
        print(f"    > Original Size: {len(file_bytes)} bytes")
        print(f"    > Ledger Size:   {len(ledger_bytes)} bytes")

    def retrieve_file(self, ledger_filepath, output_filepath):
        """Reads a ledger, translates the Pi coordinates back to data, and saves the file."""
        print(f"[*] RETRIEVING: {ledger_filepath} -> {output_filepath}")
        
        with open(ledger_filepath, 'rb') as f:
            ledger_bytes = f.read()
            
        # Convert ledger bytes to coordinate hex characters
        ledger_hex = ledger_bytes.hex()
        
        # Swap every coordinate hex character back to its original data hex character
        restored_hex = "".join([self.decode_map[char] for char in ledger_hex])
        
        # Convert the restored hex string back into the actual file bytes
        restored_bytes = bytes.fromhex(restored_hex)
        
        with open(output_filepath, 'wb') as f:
            f.write(restored_bytes)
            
        print(f"    > Restored Size: {len(restored_bytes)} bytes")


# =============================================================================
# [EXECUTION / DEMONSTRATION]
# =============================================================================
if __name__ == "__main__":
    fs = RawPiFS()
    
    # 1. Create a dummy "binary" file to simulate a .zip or .png
    # We'll fill it with 10,000 random bytes
    dummy_file = "test_archive.zip"
    ledger_file = "test_archive.ledger"
    restored_file = "test_archive_RESTORED.zip"
    
    print("\n--- Generating Dummy File ---")
    original_data = os.urandom(10000)
    with open(dummy_file, 'wb') as f:
        f.write(original_data)
        
    original_hash = hashlib.sha256(original_data).hexdigest()
    print(f"Created {dummy_file} (SHA256: {original_hash[:10]}...)")
    
    # 2. Store it in Pi (Create the Ledger)
    print("\n--- Writing to PiFS ---")
    fs.store_file(dummy_file, ledger_file)
    
    # 3. Retrieve it from Pi (Reconstruct the File)
    print("\n--- Reading from PiFS ---")
    fs.retrieve_file(ledger_file, restored_file)
    
    # 4. Verify flawless extraction
    with open(restored_file, 'rb') as f:
        restored_data = f.read()
        
    restored_hash = hashlib.sha256(restored_data).hexdigest()
    
    print("\n--- Validation ---")
    if original_hash == restored_hash:
        print("[SUCCESS] Hash match! The file was encoded and decoded flawlessly.")
        print(f"\n[*] Files have been left on your disk for inspection:")
        print(f"    1. {dummy_file} (Original)")
        print(f"    2. {ledger_file} (The Pi Encoded File)")
        print(f"    3. {restored_file} (The Decoded Result)")
    else:
        print("[FAILED] Corruption detected.")
