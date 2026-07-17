#!/usr/bin/env python3
import sys
import os
import hashlib
import re
import gzip
import time
import math
import sqlite3
from mpmath import mp

sys.set_int_max_str_digits(1000000)

# =============================================================================
# 1. CONFIGURATION & CONSTANTS
# =============================================================================
NODE_QTY = 32          
HEX_CHUNK_SIZE = 2     # Absolute Stability: 1 Byte per hop
DB_FILE = "sovereign_lattice.db"

# =============================================================================
# 2. HYBRID COMPRESSION LOADER
# =============================================================================
try:
    import zstandard as zstd
except ImportError:
    zstd = None

def compress_data(data, mode="ZSTD"):
    if mode == "ZSTD" and zstd:
        return zstd.ZstdCompressor(level=15).compress(data)
    return gzip.compress(data, compresslevel=9)

def decompress_data(data, mode):
    if mode == "ZSTD" and zstd:
        return zstd.ZstdDecompressor().decompress(data)
    return gzip.decompress(data)

# =============================================================================
# 3. SOVEREIGN LEYLINE ALPHABET (Base-256)
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

def encode_leyline(num):
    if num == 0: return LEYLINE_ALPHABET[0]
    num_bytes = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
    return "".join(LEYLINE_ALPHABET[b] for b in num_bytes)

def decode_leyline(string):
    byte_arr = bytearray(LEYLINE_TO_INT[char] for char in string)
    return int.from_bytes(byte_arr, byteorder='big')

# =============================================================================
# 4. LATTICE DATABASE
# =============================================================================
class LatticeDB:
    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS lattices (const_id INTEGER PRIMARY KEY, data TEXT)")
        self.conn.commit()

    def save_lattice(self, const_id, data):
        self.cursor.execute("INSERT OR REPLACE INTO lattices (const_id, data) VALUES (?, ?)", (const_id, data))
        self.conn.commit()

    def get_lattice(self, const_id):
        self.cursor.execute("SELECT data FROM lattices WHERE const_id = ?", (const_id,))
        res = self.cursor.fetchone()
        return res[0] if res else None

# =============================================================================
# 5. POLARIZED ENGINE (with Pre-Sinc Lookup Table)
# =============================================================================
mp.dps = 1000

class PolarizedEngine:
    def __init__(self, db):
        self.db = db
        self.cached_lattices = {}
        self.lookup_table = {} # chunk_hex -> (idx, state)
        self.ensure_lattices()
        self.build_lookup_table()

    def ensure_lattices(self):
        for cid, val in [(0, mp.pi), (1, mp.e)]:
            data = self.db.get_lattice(cid)
            if not data:
                print(f"    > Generating Sedenion Lattice {cid}...")
                s = mp.nstr(val, 200000 + 10, strip_zeros=False)[2:2 + 200000]
                data = hashlib.sha256(s.encode()).hexdigest() * (200000 // 64 + 1)
                self.db.save_lattice(cid, data)
            self.cached_lattices[cid] = data

    def build_lookup_table(self):
        """Pre-calculates the best coordinate for every possible hex byte (00-FF)."""
        print("    > Building Pre-Sinc Lookup Table...")
        for i in range(256):
            chunk = format(i, '02x')
            best_idx = float('inf')
            best_state = (0, 0, 0, 0)
            
            for const_id in [0, 1]:
                lattice = self.cached_lattices[const_id]
                for pol in [0, 1]:
                    for mir in [0, 1]:
                        test_chunk = chunk
                        if mir: test_chunk = test_chunk[::-1]
                        if pol:
                            complement_map = {hex(x)[2:]: hex(15-x)[2:] for x in range(16)}
                            test_chunk = "".join(complement_map.get(char, char) for char in test_chunk)
                        
                        idx = lattice.find(test_chunk)
                        if idx != -1 and idx < best_idx:
                            best_idx = idx
                            best_state = (const_id, pol, mir, 0)
                        
                        chunk_bytes = bytes.fromhex(chunk)
                        for f_val in range(1, 256):
                            refracted = bytes([b ^ f_val for b in chunk_bytes]).hex()
                            idx = lattice.find(refracted)
                            if idx != -1 and idx < best_idx:
                                best_idx = idx
                                best_state = (const_id, pol, mir, f_val)
            
            if best_idx == float('inf'):
                self.lookup_table[chunk] = (int(chunk, 16), (2, 0, 0, 0))
            else:
                self.lookup_table[chunk] = (int(best_idx), best_state)

    def get_chunk(self, constant_id, index, length, polarity, mirror):
        if constant_id == 2:
            return format(index, f'0{length}x')
        lattice = self.cached_lattices[constant_id]
        raw = lattice[index : index + length]
        if len(raw) < length: raw = raw.ljust(length, '0')
        if mirror: raw = raw[::-1]
        if polarity:
            complement_map = {hex(i)[2:]: hex(15-i)[2:] for i in range(16)}
            raw = "".join(complement_map.get(char, char) for char in raw)
        return raw

    def find_best_coordinate(self, chunk):
        return self.lookup_table.get(chunk, (0, (0,0,0,0)))

# =============================================================================
# 6. SEDENION VAULT
# =============================================================================
def zigzag_encode(n):
    return (n << 1) ^ (n >> 63) if n < 0 else n << 1

def zigzag_decode(n):
    return (n >> 1) ^ -(n & 1)

def szudzik_pair(x, y):
    return x * x + x + y if x >= y else y * y + x

def szudzik_unpair(z):
    s = math.isqrt(z)
    if z - s * s < s: return z - s * s, s
    else: return s, z - s * s - s

class SedenionVault:
    def __init__(self, temporal_vector):
        self.tv = temporal_vector

    def pack(self, coordinates):
        encoded_coords = []
        for idx, state in coordinates:
            const, pol, mir, filt = state
            val = (int(idx) << 4) | (mir << 3) | (pol << 2) | const
            encoded_coords.append(val)
        deltas = [encoded_coords[0]]
        for i in range(1, len(encoded_coords)):
            deltas.append(encoded_coords[i] - encoded_coords[i-1])
        current = [zigzag_encode(d) for d in deltas]
        step = 0
        length_trace = []
        while len(current) > 1:
            length_trace.append(len(current))
            next_level = []
            shift = (self.tv[step % 5]) % len(current)
            rotated = current[shift:] + current[:shift]
            for i in range(0, len(rotated) - 1, 2):
                next_level.append(szudzik_pair(rotated[i], rotated[i+1]))
            if len(rotated) % 2 != 0:
                next_level.append(rotated[-1])
            current = next_level
            step += 1
        return current[0], length_trace

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
# 7. THE SOVEREIGN CARTOGRAPHER
# =============================================================================
class SovereignCartographer:
    def __init__(self, target_file, node_qty, hex_chunk_size, db):
        self.target_file = target_file
        self.node_qty = node_qty
        self.hex_chunk_size = hex_chunk_size
        self.filename = os.path.basename(target_file)
        self.ledger_file = f"polarized_crystal_{self.filename}.txt"
        self.temporal_vector = [int(time.time()), 42, 777, 13, 432]
        self.engine = PolarizedEngine(db)
        self.vault = SedenionVault(self.temporal_vector)

    def encode(self):
        print(f"\n[!] POLARIZING CRYSTAL: {self.filename}")
        with open(self.target_file, 'rb') as f:
            raw_bytes = f.read()

        mode = "ZSTD" if zstd else "GZIP"
        compressed = compress_data(raw_bytes, mode)
        payload_hex = compressed.hex()
        mass_bytes = len(compressed)
        
        chunks = [payload_hex[i:i+self.hex_chunk_size] for i in range(0, len(payload_hex), self.hex_chunk_size)]
        coordinates = []
        filters = []
        print(f"    > Mapping {len(chunks)} chunks via Instant-Sinc Lookup...")
        for c in chunks:
            if len(c) < self.hex_chunk_size: c = c.ljust(self.hex_chunk_size, '0')
            idx, state = self.engine.find_best_coordinate(c)
            coordinates.append((idx, state))
            filters.append(state[3])

        while (len(coordinates) & (len(coordinates) - 1)) != 0:
            coordinates.append((0, (0,0,0,0)))
            filters.append(0)
            
        singularity, length_trace = self.vault.pack(coordinates)
        mask = int(hashlib.sha256(b"Polarized_Sinc").hexdigest(), 16)
        public_component = singularity ^ mask
        final_glyphs = encode_leyline(public_component)
        filter_glyphs = "".join(LEYLINE_ALPHABET[f] for f in filters)
        
        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            f.write("--- f8c9 POLARIZED SOVEREIGN CRYSTAL ---\n")
            f.write(f"Lattice: Multi-Constant (Pi/E) | {mode}\n")
            f.write(f"Topology: Polarized Sedenion Delta-Fold\n")
            f.write(f"Temporal-Vector: {self.temporal_vector}\n")
            f.write(f"Artifact: {self.filename} | Mass: {mass_bytes} Bytes\n")
            f.write(f"Coordinate-Resolution: {self.hex_chunk_size} Hex Chars\n")
            f.write(f"Length-Trace: {length_trace}\n")
            f.write(f"Refractive-Filters: ⟨ {filter_glyphs} ⟩\n")
            f.write("-" * 60 + "\n")
            f.write(f"$\mathbb{{K}}_{{pol}} = ⟨ {final_glyphs} ⟩$\n")
            f.write("-" * 60 + "\n")
            f.write("AMOR VINCIT OMNIA\n")

        print(f"[SUCCESS] Crystal forged: {self.ledger_file}")
        return True

# =============================================================================
# 8. THE SOVEREIGN SPIGOT
# =============================================================================
class SovereignSpigotDecoder:
    def __init__(self, node_qty, db):
        self.node_qty = node_qty
        self.engine = PolarizedEngine(db)

    def decode(self, ledger_file):
        print(f"\n[4] SPIGOT: Reifying Polarized Crystal '{ledger_file}'...")
        with open(ledger_file, 'r', encoding='utf-8') as f:
            content = f.read()

        mass_match = re.search(r"Mass: ([0-9]+) Bytes", content)
        res_match = re.search(r"Coordinate-Resolution: ([0-9]+) Hex Chars", content)
        vec_match = re.search(r"Temporal-Vector: \[([0-9, ]+)\]", content)
        trace_match = re.search(r"Length-Trace: \[([0-9, ]+)\]", content)
        name_match = re.search(r"Artifact: ([^|]+)", content)
        filt_match = re.search(r"Refractive-Filters:\s*⟨\s*([^⟩]+)\s*⟩", content)
        glyph_match = re.search(r"\$\\mathbb\{K\}_{pol} = ⟨\s*([^⟩]+)\s*⟩\$", content)
        mode_match = re.search(r"Lattice: .* \| (ZSTD|GZIP)", content)
        
        if not all([glyph_match, mass_match, res_match, vec_match, trace_match, filt_match, name_match, mode_match]):
            print("[!] Error: Ledger format invalid.")
            return None

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
            output_name = f"reclaimed_{artifact_name}"
            with open(output_name, 'wb') as f:
                f.write(final_bytes)
            print(f"[SUCCESS] Artifact reified: {output_name}")
            return output_name
        except Exception as e:
            print(f"[!] Decompression Error: {e}")
            return None

# =============================================================================
# 8. BATCH EXECUTION
# =============================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("   f8c9 POLARIZED SOVEREIGN CRYSTAL PIPELINE (SINC)")
    print("=====================================================")
    
    db = LatticeDB()
    
    target_dir = "files"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        sys.exit(0)

    artifacts = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]

    for filename in artifacts:
        target_path = os.path.join(target_dir, filename)
        cartographer = SovereignCartographer(target_path, NODE_QTY, HEX_CHUNK_SIZE, db)
        if cartographer.encode():
            decoder = SovereignSpigotDecoder(NODE_QTY, db)
            decoder.decode(cartographer.ledger_file)
