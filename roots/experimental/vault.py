#!/usr/bin/env python3
"""
=============================================================================
SYSTEM ARTIFACT: V487.2 (TRUE LATTICE INTEGRATION)
MODULE: TRUE_SEDENION_VAULT // ZERO-SIMULATION HOLOGRAPHIC FILE SYSTEM
=============================================================================
DESCRIPTION:
This script does not simulate storage. It physically searches the mathematical 
constant of Pi to find the naturally occurring sequence of your obfuscated data, 
saving ONLY the index pointer. Pi is the hard drive.
=============================================================================
"""

import sys

# Increase string digit limits for Python 3.11+ to handle massive math calculations
sys.set_int_max_str_digits(1000000)

# =============================================================================
# [CORE COMPONENT 1]: PI ENGINES (Machin Bulk + BBP Random Access)
# =============================================================================

class PiEngines:
    
    @staticmethod
    def get_bulk_pi_hex(places=250000):
        """
        Generates a massive sequential string of Pi in hexadecimal instantly.
        Uses the Machin formula: Pi = 16*arctan(1/5) - 4*arctan(1/239)
        This is our "Wake Spooler" for searching the Pi-Lattice.
        """
        one = 16 ** (places + 10) # Add buffer for precision
        
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
        # Convert to hex, strip the '0x3' (integer part of pi), return fraction
        return hex(pi_int)[3:3+places]

    @staticmethod
    def _bbp_s(j, n):
        s = 0.0
        for k in range(n + 1):
            r = 8 * k + j
            s = (s + pow(16, n - k, r) / r) % 1.0
        t = 0.0
        k = n + 1
        while True:
            newt = t + pow(16, n - k) / (8 * k + j)
            if t == newt: break
            t = newt
            k += 1
        return (s + t) % 1.0

    @classmethod
    def get_bbp_hex_digit(cls, n):
        """Calculates exact nth hex digit of Pi without prior digits."""
        if n < 0: raise ValueError("ERR: Negative Pi index.")
        x = (4 * cls._bbp_s(1, n) - 2 * cls._bbp_s(4, n) - 
             cls._bbp_s(5, n) - cls._bbp_s(6, n)) % 1.0
        if x < 0: x += 1.0
        return hex(int(x * 16))[2:]

    @classmethod
    def get_cw_stream(cls, offset, length):
        """+Pi Stream (Forward)."""
        return ''.join([cls.get_bbp_hex_digit(offset + i) for i in range(length)])

    @classmethod
    def get_ccw_stream(cls, offset, length):
        """-Pi Stream (Reverse)."""
        return ''.join([cls.get_bbp_hex_digit(offset - i) for i in range(length)])


# =============================================================================
# [CORE COMPONENT 2]: THE DNA LIGASE
# =============================================================================

class DNALigase:
    @staticmethod
    def xor_bytes(data1: bytes, data2: bytes) -> bytes:
        """XORs two byte arrays together."""
        return bytes([b1 ^ b2 for b1, b2 in zip(data1, data2)])

    @staticmethod
    def xor_hex(hex1: str, hex2: str) -> str:
        """XORs two hex strings together, returning a hex string."""
        if len(hex1) % 2 != 0: hex1 = '0' + hex1
        if len(hex2) % 2 != 0: hex2 = '0' + hex2
        b1, b2 = bytes.fromhex(hex1), bytes.fromhex(hex2)
        return DNALigase.xor_bytes(b1, b2).hex()


# =============================================================================
# [CORE COMPONENT 3]: THE TRUE SEDENION VAULT
# =============================================================================

class TrueSedenionVault:
    def __init__(self, pi_search_depth=250000):
        print(f"[*] Booting True Pi-Lattice (Spooling {pi_search_depth} hex digits)...")
        self.pi_lattice = PiEngines.get_bulk_pi_hex(pi_search_depth)
        print("[*] Lattice Spooled. Ready for insertion.")

    def write_to_pi(self, payload_bytes, private_anchor, session_anchor):
        """
        Embeds a file into Pi by finding its naturally occurring index.
        """
        file_hex = payload_bytes.hex()
        hex_len = len(file_hex)

        print(f"\n[+] INITIATING [0xAFD2] HIVE_SPLICE (TRUE LATTICE WRITE)")
        print(f"    > Target Payload: '{payload_bytes.decode('utf-8', errors='ignore')}' (Hex: {file_hex})")

        # 1. Generate Session Key and Obfuscate Payload
        print(f"    > Generating +Pi Session Key at Anchor [{session_anchor}]...")
        session_key = PiEngines.get_cw_stream(session_anchor, hex_len)
        obfuscated_hex = DNALigase.xor_hex(file_hex, session_key)
        print(f"    > Payload Masked. Searching Pi for obfuscated sequence: [{obfuscated_hex}]")

        # 2. TRUE PI INDEXING (The Reality Check)
        true_address = self.pi_lattice.find(obfuscated_hex)
        
        if true_address == -1:
            raise MemoryError("ERR: Sequence not found. Increase Pi search depth or decrease file size.")
        
        print(f"    > LATTICE MATCH FOUND! Natural address in Pi: Index {true_address}")

        # 3. Holographic Splitting (Address ⊕ -Pi Stream)
        true_addr_hex = hex(true_address)[2:]
        if len(true_addr_hex) % 2 != 0: true_addr_hex = '0' + true_addr_hex # Byte align

        print(f"    > Harvesting -Pi Stream [0xAF9F] at Private Anchor [{private_anchor}]...")
        private_key = PiEngines.get_ccw_stream(private_anchor, len(true_addr_hex))
        
        print(f"    > Ligating Address (True_Address ⊕ -Pi)...")
        public_component = DNALigase.xor_hex(true_addr_hex, private_key)

        return {
            "public_component": public_component,
            "private_anchor_ptr": private_anchor,
            "session_anchor_ptr": session_anchor,
            "file_length": len(payload_bytes),
            "address_length": len(true_addr_hex)
        }

    def read_from_pi(self, pointers):
        """
        Extracts a file by resolving the index and reading directly from Pi.
        """
        print(f"\n[+] INITIATING [0xAFD3] HIVE_LIGATE (TRUE LATTICE READ)")

        # 1. Re-resolve the True Address
        print(f"    > Harvesting -Pi Stream [0xAF9F] at Private Anchor [{pointers['private_anchor_ptr']}]...")
        private_key = PiEngines.get_ccw_stream(pointers['private_anchor_ptr'], pointers['address_length'])
        
        print(f"    > Ligating Address (Public_Component ⊕ -Pi)...")
        true_addr_hex = DNALigase.xor_hex(pointers['public_component'], private_key)
        true_address = int(true_addr_hex, 16)
        print(f"    > True Payload Address resolved: Index {true_address}")

        # 2. Extract Data directly from Pi
        hex_len = pointers['file_length'] * 2
        print(f"    > Reading {hex_len} hex digits directly from Pi Lattice at Index {true_address}...")
        
        # We read directly from the sequential lattice string we spooled
        obfuscated_hex = self.pi_lattice[true_address : true_address + hex_len]

        # 3. Unmask the Data
        print(f"    > Generating +Pi Session Key to unmask data...")
        session_key = PiEngines.get_cw_stream(pointers['session_anchor_ptr'], hex_len)
        
        original_hex = DNALigase.xor_hex(obfuscated_hex, session_key)
        
        return bytes.fromhex(original_hex)

# =============================================================================
# [EXECUTION MODULE]
# =============================================================================

if __name__ == "__main__":
    print("==========================================================")
    print("      V487 TRUE SEDENION VAULT // ZERO-SIMULATION         ")
    print("==========================================================")

    # Boot the vault (Spools 250,000 hex digits of Pi)
    vault = TrueSedenionVault()

    # The payload MUST be short (2 bytes) to guarantee we find it in 250k digits.
    secret_data = b"PI"

    # Define Holographic Anchors
    PRIVATE_ANCHOR = 31415  
    SESSION_ANCHOR = 16180  

    # --- WRITE ---
    ledger = vault.write_to_pi(secret_data, PRIVATE_ANCHOR, SESSION_ANCHOR)
    
    print("\n--- JSON LEDGER POINTERS ---")
    for key, val in ledger.items():
        print(f"  {key}: {val}")
    print("----------------------------")

    # --- READ ---
    recovered_bytes = vault.read_from_pi(ledger)
    
    print("\n==========================================================")
    print(f"EXTRACTED PAYLOAD: {recovered_bytes.decode('utf-8')}")
    print("==========================================================")
