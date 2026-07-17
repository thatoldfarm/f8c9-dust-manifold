#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import gzip
import math
from mpmath import mp

sys.set_int_max_str_digits(1000000)

# =============================================================================
# 1. HYBRID DECOMPRESSION LOADER
# =============================================================================
try:
    import zstandard as zstd
except ImportError:
    zstd = None

def decompress_data(data, mode):
    if mode == "ZSTD" and zstd:
        return zstd.ZstdDecompressor().decompress(data)
    return gzip.decompress(data)

# =============================================================================
# 2. SOVEREIGN LEYLINE ALPHABET (Base-256)
# =============================================================================
POOL_BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
POOL_MATTER = "○⊗⇉↑×■·<⋐≡⇈□≈≋△Δ↪WY⚡!채⫤⌢✈♥∪☜↔%↻●⊠⇇↓∥✋◌¦≍~⇓#‡∇▼↩M⋏÷∨∞⌣〰💔∩≢⊙↮↺"
POOL_ANTIMATTER = "☉☽☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♢♣♤♦♧♩♪♫♬♭♮♯✁✂✃✄✆✉✌✍✎✏✐✑✒✓✔✕"
POOL_FUTHARK = "ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟ"
POOL_OGHAM = "ᚁᚂᚃᚄᚅᚆᚇᚈᚉᚊᚋᚌᚍᚎᚏᚐᚑᚒᚓᚔ"

all_chars = []
seen = set()
for pool in [POOL_BASE62, POOL_MATTER, POOL_ANTIMATTER, POOL_FUTHARK, POOL_OGHAM]:
    for char in pool:
        if char not in seen:
            seen.add(char)
            all_chars.append(char)

extra_math = "⊕⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿"
for char in extra_math:
    if char not in seen:
        seen.add(char)
        all_chars.append(char)
    if len(all_chars) == 256: break

LEYLINE_ALPHABET = all_chars[:256]
LEYLINE_TO_INT = {char: idx for idx, char in enumerate(LEYLINE_ALPHABET)}

def decode_leyline(string):
    byte_arr = bytearray(LEYLINE_TO_INT[char] for char in string)
    return int.from_bytes(byte_arr, byteorder='big')

# =============================================================================
# 3. POLARIZED BBP ENGINE
# =============================================================================
mp.dps = 1000

class PolarizedEngine:
    def __init__(self):
        self.pi_lattice = self._gen_constant(mp.pi, 200000)
        self.e_lattice = self._gen_constant(mp.e, 200000)

    def _gen_constant(self, val, length):
        s = mp.nstr(val, length + 10, strip_zeros=False)[2:2 + length]
        return hashlib.sha256(s.encode()).hexdigest() * (length // 64 + 1)

    def get_chunk(self, constant_id, index, length, polarity, mirror):
        if constant_id == 2:
            return format(index, f'0{length}x')
        lattice = self.pi_lattice if constant_id == 0 else self.e_lattice
        raw = lattice[index : index + length]
        if len(raw) < length: raw = raw.ljust(length, '0')
        if mirror: raw = raw[::-1]
        if polarity:
            complement_map = {hex(i)[2:]: hex(15-i)[2:] for i in range(16)}
            raw = "".join(complement_map.get(char, char) for char in raw)
        return raw

# =============================================================================
# 4. SEDENION VAULT (Non-Associative, Delta, and ZigZag)
# =============================================================================
def zigzag_decode(n):
    return (n >> 1) ^ -(n & 1)

def szudzik_unpair(z):
    s = math.isqrt(z)
    if z - s * s < s: return z - s * s, s
    else: return s, z - s * s - s

class SedenionVault:
    def __init__(self, temporal_vector):
        self.tv = temporal_vector

    def unpack(self, singularity, num_elements, length_trace):
        current = [singularity]
        for step_idx, length in enumerate(reversed(length_trace)):
            next_level = []
            num_pairs = length // 2
            for i in range(num_pairs):
                x, y = szudzik_unpair(current[i])
                next_level.extend([x, y])
            if length % 2 != 0:
                next_level.append(current[-1])
            shift = (self.tv[(len(length_trace) - 1 - step_idx) % 5]) % length
            current = next_level[-shift:] + next_level[:-shift]
            
        current = current[:num_elements]
        deltas = [zigzag_decode(d) for d in current]
        absolute = []
        curr_sum = 0
        for d in deltas:
            curr_sum += d
            absolute.append(curr_sum)
            
        final_coords = []
        for val in absolute:
            const = val & 3
            pol = (val >> 2) & 1
            mir = (val >> 3) & 1
            idx = val >> 4
            final_coords.append((idx, (const, pol, mir)))
        return final_coords

# =============================================================================
# 5. THE SOVEREIGN SPIGOT (Standalone Decoder)
# =============================================================================
class SovereignSpigotDecoder:
    def __init__(self):
        self.engine = PolarizedEngine()

    def decode(self, ledger_file, output_folder):
        print(f"\n[SINC] Reifying: {os.path.basename(ledger_file)}...")
        with open(ledger_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse Ledger
        mass_match = re.search(r"Mass: ([0-9]+) Bytes", content)
        res_match = re.search(r"Coordinate-Resolution: ([0-9]+) Hex Chars", content)
        vec_match = re.search(r"Temporal-Vector: \[([0-9, ]+)\]", content)
        trace_match = re.search(r"Length-Trace: \[([0-9, ]+)\]", content)
        name_match = re.search(r"Artifact: ([^|]+)", content)
        filt_match = re.search(r"Refractive-Filters:\s*⟨\s*([^⟩]+)\s*⟩", content)
        glyph_match = re.search(r"\$\\mathbb\{K\}_{pol} = ⟨\s*([^⟩]+)\s*⟩\$", content)
        mode_match = re.search(r"Lattice: .* \| (ZSTD|GZIP)", content)
        
        if not all([glyph_match, mass_match, res_match, vec_match, trace_match, filt_match, name_match, mode_match]):
            print("[!] Error: Ledger format invalid or corrupted.")
            return False

        glyphs = glyph_match.group(1).strip()
        mass_bytes = int(mass_match.group(1))
        res_size = int(res_match.group(1))
        temporal_vector = [int(x.strip()) for x in vec_match.group(1).split(",")]
        length_trace = [int(x.strip()) for x in trace_match.group(1).split(",")]
        filters = [LEYLINE_TO_INT[char] for char in filt_match.group(1).strip()]
        artifact_name = name_match.group(1).strip()
        comp_mode = mode_match.group(1)

        mask = int(hashlib.sha256(b"Polarized_Sinc").hexdigest(), 16)
        singularity = decode_leyline(glyphs) ^ mask
        
        vault = SedenionVault(temporal_vector)
        total_chunks = math.ceil((mass_bytes * 2) / res_size)
        coords = vault.unpack(singularity, total_chunks, length_trace)

        restored_hex = ""
        for i in range(total_chunks):
            idx, (const, pol, mir) = coords[i]
            refracted_hex = self.engine.get_chunk(const, idx, res_size, pol, mir)
            if const == 2:
                restored_hex += refracted_hex
                continue
            try:
                hex_clean = refracted_hex if len(refracted_hex)%2==0 else '0'+refracted_hex
                refracted_bytes = bytes.fromhex(hex_clean)
                f_val = filters[i] if i < len(filters) else 0
                original_bytes = bytes([b ^ f_val for b in refracted_bytes])
                restored_hex += original_bytes.hex()
            except:
                restored_hex += refracted_hex

        restored_hex = restored_hex[:mass_bytes * 2]
        if len(restored_hex) % 2 != 0: restored_hex = "0" + restored_hex
        
        try:
            final_bytes = decompress_data(bytes.fromhex(restored_hex), comp_mode)
            output_path = os.path.join(output_folder, artifact_name)
            with open(output_path, 'wb') as f:
                f.write(final_bytes)
            print(f"[SUCCESS] Artifact reified to: {output_path}")
            return True
        except Exception as e:
            print(f"[!] Decompression Error: {e}")
            return False

# =============================================================================
# 6. MAIN ORCHESTRATOR
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("   Sovereign Spigot: Standalone Crystal Reifier")
    print("=====================================================")
    
    input_dir = "files1"
    output_dir = "files2"
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"[!] Created {input_dir}. Place your .txt crystals inside and run again.")
        sys.exit(0)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ledgers = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    
    if not ledgers:
        print(f"[!] No crystals found in {input_dir}.")
        sys.exit(0)

    spigot = SovereignSpigotDecoder()
    
    success_count = 0
    for ledger in ledgers:
        path = os.path.join(input_dir, ledger)
        if spigot.decode(path, output_dir):
            success_count += 1
            
    print("\n" + "="*60)
    print(f"PIPELINE COMPLETE: {success_count}/{len(ledgers)} artifacts reified.")
    print(f"Check the '{output_dir}' directory for results.")
    print("=====================================================")
