import sys
import os
import re
import math
import gzip
import time

# =============================================================================
# RECONSTRUCTING THE SOVEREIGN LEYLINE ENVIRONMENT
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

if len(all_chars) < 256:
    extra_math = "⊕⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿"
    for char in extra_math:
        if char not in seen:
            seen.add(char)
            all_chars.append(char)
        if len(all_chars) == 256:
            break

LEYLINE_ALPHABET = all_chars[:256]
LEYLINE_TO_INT = {char: idx for idx, char in enumerate(LEYLINE_ALPHABET)}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def decode_leyline(string):
    byte_arr = bytearray(LEYLINE_TO_INT[char] for char in string)
    return int.from_bytes(byte_arr, byteorder='big')

def szudzik_unpair(z):
    s = math.isqrt(z)
    if z - s * s < s:
        return z - s * s, s
    else:
        return s, z - s * s - s

def szudzik_tree_unpack(z, num_elements):
    current = [z]
    while len(current) < num_elements:
        next_level = []
        for val in current:
            x, y = szudzik_unpair(val)
            next_level.extend([x, y])
        current = next_level
    return current

BBP_POWER_CACHE = {}
def power_mod_2adic(exp, mod):
    key = (exp, mod)
    if key not in BBP_POWER_CACHE:
        BBP_POWER_CACHE[key] = pow(16, exp, mod)
    return BBP_POWER_CACHE[key]

def get_pi_hex_digits_bbp(n, num_digits):
    def S(j, n):
        s = 0.0; k = 0
        while k <= n:
            r = 8 * k + j
            s = (s + float(power_mod_2adic(n - k, r)) / r) % 1.0
            k += 1
        t = 0.0; k = n + 1
        while True:
            newt = t + pow(16, n - k) / (8 * k + j)
            if t == newt: break
            t = newt
            k += 1
        return (s + t) % 1.0

    res = ""
    for i in range(num_digits):
        pos = n + i
        pi_fraction = (4 * S(1, pos) - 2 * S(4, pos) - S(5, pos) - S(6, pos)) % 1.0
        res += hex(int(pi_fraction * 16))[2:]
    return res

# =============================================================================
# THE DYNAMIC DECODE ENGINE
# =============================================================================
def process_ledger_file(file_path, output_folder):
    print(f"\nReading Ledger: {os.path.basename(file_path)}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Dynamically extract metadata using Regex
    name_match = re.search(r"Artifact-Name:\s*(.+)", content)
    mass_match = re.search(r"Mass-Singularity: ([0-9]+) Bytes", content)
    res_match = re.search(r"Coordinate-Resolution: ([0-9]+) Hex Chars", content)
    
    if not (name_match and mass_match and res_match):
        print(f"  [!] Skipping {file_path}: Missing metadata (Name, Mass, or Resolution).")
        return

    name = name_match.group(1).strip()
    mass = int(mass_match.group(1))
    res = int(res_match.group(1))
    
    # 2. Extract Tensors
    tensors = re.findall(r'⟨([^⟩]+)⟩', content)
    tensors = [t.replace(" ", "").replace("\t", "").replace("\n", "") for t in tensors]

    print(f"  > Artifact: {name} | Mass: {mass} | Resolution: {res}")

    # 3. Unfold coordinates
    pi_indices = []
    for t in tensors:
        val = decode_leyline(t)
        unfolded = szudzik_tree_unpack(val, 32) # Standard 32-node symmetry
        pi_indices.extend(unfolded)

    total_indices_needed = math.ceil((mass * 2) / res)
    pi_indices = pi_indices[:total_indices_needed]

    # 4. Materialize Hex from Pi
    restored_hex = ""
    for idx in pi_indices:
        restored_hex += get_pi_hex_digits_bbp(idx, res)

    restored_hex = restored_hex[:mass * 2]

    # 5. Decompress and Save
    try:
        import zstandard as zstd
        dctx = zstd.ZstdDecompressor()
        decompressed_data = dctx.decompress(bytes.fromhex(restored_hex))
        method = "ZSTD"
    except (ImportError, Exception):
        try:
            decompressed_data = gzip.decompress(bytes.fromhex(restored_hex))
            method = "GZIP"
        except Exception as e:
            print(f"  [!] Decompression failed: {e}")
            decompressed_data = bytes.fromhex(restored_hex)
            method = "RAW HEX"

    output_path = os.path.join(output_folder, name)
    with open(output_path, "wb") as f:
        f.write(decompressed_data)
    
    print(f"  > [SUCCESS] Recovered via {method} to {output_path}")

# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================
if __name__ == "__main__":
    input_folder = "files1"
    output_folder = "files2"

    # Create folders if they don't exist
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"[!] Created {input_folder} folder. Please place your .txt ledgers there.")
        sys.exit(0)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all .txt files in files1
    ledger_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    
    if not ledger_files:
        print(f"[!] No .txt files found in {input_folder}.")
        sys.exit(0)

    print(f"Found {len(ledger_files)} ledgers to process.")
    
    for filename in ledger_files:
        full_path = os.path.join(input_folder, filename)
        process_ledger_file(full_path, output_folder)

    print("\n=====================================================")
    print("All processed files are located in 'files2'")
    print("=====================================================")
