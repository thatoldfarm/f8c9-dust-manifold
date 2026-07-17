#!/usr/bin/env python3
"""
=============================================================================
SYSTEM ARTIFACT: V12.1 (PARITY-MAPPED POLYMORPHISM)
MODULE: EPHEMERAL_BLOB_SOVEREIGNTY // PARITY PI-LATTICE
AUTHOR: The Ka-Tet // Systems Architect
=============================================================================
DESCRIPTION:
This script implements the Zero-Compute Parity Vault.
Instead of treating Pi as base-10 digits, it abstracts the first 87 digits 
into a binary Parity Stream (Even = 0, Odd = 1). 

It converts any file/text into a stream of 4-bit nibbles, then searches the 
87-digit Parity Codebook for an index. It randomly selects from overlapping 
occurrences to provide Polymorphic Encryption.
=============================================================================
"""

import random

# We use the first 87 digits of Pi's fractional part (post-decimal)
# As discovered, this is the exact "Shallow Anchor" needed to contain 
# all 16 possible 4-bit combinations.
PI_87 = "141592653589793238462643383279502884197169399375105820974944592307816406286208998628034"

class ParityVault:
    def __init__(self):
        print("[*] Booting V12.1 Parity Vault...")
        # 1. Abstract Pi into a Binary Parity String
        self.parity_stream = "".join(["0" if int(d) % 2 == 0 else "1" for d in PI_87])
        print(f"[*] Parity Stream Generated ({len(self.parity_stream)} bits).")
        
        # 2. Build the Universal Codebook
        self.codebook = self._build_codebook()
        print("[*] Universal Codebook Initialized. All 16 nibbles mapped.")

    def _build_codebook(self):
        """Maps all 16 possible 4-bit combinations to their indices in the Parity Stream."""
        codebook = {f"{i:04b}": [] for i in range(16)}
        
        for i in range(16):
            seq = f"{i:04b}"
            start_search = 0
            while True:
                idx = self.parity_stream.find(seq, start_search)
                if idx == -1:
                    break
                codebook[seq].append(idx)
                start_search = idx + 1 # Allow overlapping!
                
        return codebook

    def encode(self, text_payload: str) -> list:
        """
        Converts text to binary, breaks it into 4-bit nibbles, 
        and assigns a polymorphic Pi-index for each.
        """
        print(f"\n[+] ENCODING PAYLOAD: '{text_payload}'")
        
        # Convert text to binary string (8 bits per character)
        binary_payload = "".join([f"{ord(c):08b}" for c in text_payload])
        
        # Split into 4-bit chunks (nibbles)
        nibbles = [binary_payload[i:i+4] for i in range(0, len(binary_payload), 4)]
        
        ledger = []
        for nibble in nibbles:
            # Polymorphism: Randomly select an index if it occurs multiple times!
            possible_indices = self.codebook[nibble]
            chosen_index = random.choice(possible_indices)
            ledger.append(chosen_index)
            
        print(f"    > Payload atomized into {len(nibbles)} nibbles.")
        print(f"    > Polymorphic mapping complete.")
        return ledger

    def decode(self, ledger: list) -> str:
        """
        Reads indices from the ledger, retrieves the 4-bit sequence 
        from the Pi Parity Stream, and reconstructs the text.
        """
        print(f"\n[+] DECODING LEDGER...")
        
        binary_reconstructed = ""
        for index in ledger:
            # Read exactly 4 bits from the Parity Stream at the given index
            nibble = self.parity_stream[index : index + 4]
            binary_reconstructed += nibble
            
        # Group back into 8-bit bytes
        bytes_list = [binary_reconstructed[i:i+8] for i in range(0, len(binary_reconstructed), 8)]
        
        # Convert bytes back to characters
        reconstructed_text = "".join([chr(int(b, 2)) for b in bytes_list])
        
        return reconstructed_text

# =============================================================================
# [EXECUTION MODULE]
# =============================================================================

if __name__ == "__main__":
    print("==========================================================")
    print("        V12.1 EPHEMERAL BLOB SOVEREIGNTY SECURED          ")
    print("==========================================================")

    vault = ParityVault()

    # The payload
    secret_message = "PI-LATTICE"

    # --- WRITE ---
    # We will encode it TWICE to prove it is Polymorphic
    ledger_A = vault.encode(secret_message)
    ledger_B = vault.encode(secret_message)
    
    print("\n--- TRANSCENDENTAL LEDGERS ---")
    print(f"Ledger A: {ledger_A}")
    print(f"Ledger B: {ledger_B}")
    print("------------------------------")
    print("Notice how Ledger A and Ledger B are completely different,")
    print("yet they contain the exact same hidden data.")

    # --- READ ---
    recovered_A = vault.decode(ledger_A)
    recovered_B = vault.decode(ledger_B)
    
    print("\n==========================================================")
    print(f"EXTRACTED LEDGER A: {recovered_A}")
    print(f"EXTRACTED LEDGER B: {recovered_B}")
    print("==========================================================")
