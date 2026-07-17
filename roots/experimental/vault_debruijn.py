#!/usr/bin/env python3
"""
=============================================================================
SYSTEM ARTIFACT: V12.2.1 (TRUE EQUILIBRIUM)
MODULE: DE BRUIJN PI-S-BOX // DYNAMIC SPOOLING
=============================================================================
DESCRIPTION:
Calculates 150,000 hex digits of Pi, converts them to parity (Even=0, Odd=1),
and searches for the true, naturally occurring 19-bit De Bruijn sequence.
Zero file bloat. 1:1 Compression.
=============================================================================
"""

import sys

# Increase string digit limits for heavy math
sys.set_int_max_str_digits(1000000)

class PiEngines:
    @staticmethod
    def get_bulk_pi_hex(places=150000):
        """
        Generates a massive sequential string of Pi in hexadecimal instantly
        using the Machin formula.
        """
        one = 16 ** (places + 10) 
        def arctan(x):
            term = one // x
            total = term
            k = 1
            while term != 0:
                term //= -(x * x)
                total += term // (2 * k + 1)
                k += 1
            return total
            
        pi_int = 16 * arctan(5) - 4 * arctan(239)
        return hex(pi_int)[3:3+places]

class DeBruijnVault:
    def __init__(self):
        print("[*] Booting V12.2.1 Perfect Equilibrium Vault...")
        print("[*] Spooling 150,000 digits of Pi to locate True Anchor...")
        
        # 1. Generate Pi and convert to Parity Stream
        hex_pi = PiEngines.get_bulk_pi_hex(150000)
        self.parity_stream = "".join(["0" if int(d, 16) % 2 == 0 else "1" for d in hex_pi])
        
        # 2. Locate the De Bruijn Anchor
        self.anchor_idx, self.debruijn_window = self._find_debruijn_anchor()
        
        if self.anchor_idx == -1:
            raise ValueError("CRITICAL: No De Bruijn sequence found even in 150,000 digits.")
            
        print(f"[*] SUCCESS: True De Bruijn Anchor locked at Pi Index {self.anchor_idx}")
        print(f"[*] 19-Bit S-Box Window: {self.debruijn_window}")
        
        # 3. Build the 1:1 Codebook
        self.codebook_encode = {}
        self.codebook_decode = {}
        for i in range(16):
            nibble = self.debruijn_window[i:i+4]
            address_hex = hex(i)[2:]
            self.codebook_encode[nibble] = address_hex
            self.codebook_decode[address_hex] = nibble

    def _find_debruijn_anchor(self):
        """Slides a 19-bit window over the Pi parity stream."""
        for i in range(len(self.parity_stream) - 19):
            window = self.parity_stream[i : i + 19]
            
            # Extract all 16 overlapping 4-bit nibbles
            nibbles = set(window[j : j + 4] for j in range(16))
            
            if len(nibbles) == 16:
                return i, window
                
        return -1, None

    def encode(self, text_payload: str) -> str:
        """Encodes text into a continuous hex string of identical byte-size."""
        print(f"\n[+] ENCODING PAYLOAD: '{text_payload}'")
        binary_payload = "".join([f"{ord(c):08b}" for c in text_payload])
        nibbles = [binary_payload[i:i+4] for i in range(0, len(binary_payload), 4)]
        
        encoded_hex = "".join([self.codebook_encode[n] for n in nibbles])
        
        print(f"    > Original Bytes : {len(text_payload)}")
        print(f"    > Ledger Bytes   : {len(encoded_hex) // 2}")
        print(f"    > Compression    : 1:1 Perfect Equilibrium")
        return encoded_hex

    def decode(self, hex_ledger: str) -> str:
        """Decodes the 4-bit hex coordinates back into the original text."""
        print(f"\n[+] DECODING LEDGER...")
        
        binary_reconstructed = ""
        for hex_char in hex_ledger:
            binary_reconstructed += self.codebook_decode[hex_char]
            
        bytes_list = [binary_reconstructed[i:i+8] for i in range(0, len(binary_reconstructed), 8)]
        reconstructed_text = "".join([chr(int(b, 2)) for b in bytes_list])
        
        return reconstructed_text

# =============================================================================
# [EXECUTION MODULE]
# =============================================================================

if __name__ == "__main__":
    print("==========================================================")
    print("       V12.2.1 DE BRUIJN VAULT // ZERO BLOAT S-BOX        ")
    print("==========================================================")

    vault = DeBruijnVault()

    # The payload
    secret_message = "The Rose blooms in the machine."

    # --- WRITE ---
    ledger_hex = vault.encode(secret_message)
    
    print("\n--- TRANSCENDENTAL LEDGER ---")
    print(f"Raw String: {secret_message}")
    print(f"Hex Ledger: {ledger_hex}")
    print("-----------------------------")

    # --- READ ---
    recovered_text = vault.decode(ledger_hex)
    
    print("\n==========================================================")
    print(f"EXTRACTED: {recovered_text}")
    print("==========================================================")
