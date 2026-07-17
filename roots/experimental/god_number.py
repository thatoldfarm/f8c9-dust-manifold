#!/usr/bin/env python3
import sys
import os

# Python recently added a safety limit for converting huge numbers to strings to prevent DOS attacks.
# We raise the limit here to easily allow our 1,200+ digit number.
sys.set_int_max_str_digits(20000)

def main():
    ledger_file = "rosetta_map.ledger"
    output_file = "rosetta_map_decimal.txt"

    if not os.path.exists(ledger_file):
        print(f"[!] ERROR: '{ledger_file}' not found. Make sure you encoded it first!")
        return

    print(f"[*] Reading '{ledger_file}'...")
    with open(ledger_file, 'rb') as f:
        ledger_bytes = f.read()

    print(f"[*] File size: {len(ledger_bytes)} bytes ({len(ledger_bytes) * 8} bits)")

    # This is where the magic happens!
    # We take all 4,096 bits and interpret them as a single integer.
    # byteorder='big' means we read it left-to-right, just like a normal number.
    print("[*] Converting entire file to a single decimal integer...")
    god_number = int.from_bytes(ledger_bytes, byteorder='big')

    # Convert the massive integer into a string of Base-10 digits so we can count them
    god_number_str = str(god_number)
    num_digits = len(god_number_str)

    print(f"[*] Conversion complete! The number has {num_digits} digits.")

    # Save the giant number to a text file for you to look at
    with open(output_file, 'w') as f:
        f.write(f"--- THE GOD NUMBER (Base-10 Representation of {ledger_file}) ---\n")
        f.write(f"Total Digits: {num_digits}\n")
        f.write("To find this file in Base-10 Pi, you must find this exact number.\n")
        f.write("-" * 70 + "\n\n")
        
        # Write the actual number
        f.write(god_number_str)
        f.write("\n")

    print(f"[SUCCESS] The giant decimal number has been saved to '{output_file}'")

if __name__ == "__main__":
    main()
