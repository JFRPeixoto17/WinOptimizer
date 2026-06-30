"""
WinOptimizer Pro - License Key Generator (DEVELOPER TOOL)

Run this to mint a Pro license key for a customer. Do NOT ship this file
inside the public installer — it is for the author's use only.

Usage:
    python keygen.py "customer@email.com"
    python keygen.py            # interactive prompt
"""

import sys
from license_manager import generate_key, validate_key


def main():
    if len(sys.argv) > 1:
        name = " ".join(sys.argv[1:])
    else:
        name = input("Licensee name / email: ").strip()

    if not name:
        print("No name provided.")
        sys.exit(1)

    key = generate_key(name)
    assert validate_key(name, key), "internal error: key did not validate"
    print()
    print("  Licensee :", name)
    print("  Pro Key  :", key)
    print()
    print("  Send the customer their name + this key. They paste both into")
    print("  WinOptimizer > Upgrade to Pro > Enter License Key.")


if __name__ == "__main__":
    main()
