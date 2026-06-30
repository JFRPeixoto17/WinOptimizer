"""
WinOptimizer Pro - Licensing System
Simple offline, name-bound license keys signed with HMAC-SHA256.

Design goals (matches the project's "simple licensing" objective):
  - No server / no internet required to validate a key.
  - Keys are bound to a licensee name/email so they can be issued per-customer.
  - A key cannot be forged without the secret (HMAC), so casual sharing of a
    *different* name will not validate. (This is deterrence, not DRM — a
    determined user can still extract the embedded secret. That is an accepted
    trade-off for a lightweight desktop product.)

License file location:  %APPDATA%\\WinOptimizer\\license.json
Format:                 {"name": "<licensee>", "key": "WO-XXXXX-XXXXX-XXXXX-XXXXX"}

Author: João Filipe Reis Peixoto
Copyright (c) 2025 João Filipe Reis Peixoto. All rights reserved.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────
#  Secret. Change this ONCE before issuing real keys, then keep
#  it private. Anyone with this string can mint Pro keys.
#  (Kept here for simplicity; for stronger protection move it to
#   an obfuscated/compiled location.)
# ─────────────────────────────────────────────────────────────
_SECRET = b"WinOptimizer-Pro::change-me-before-release::2025::JFRP"

_KEY_PREFIX = "WO"
_GROUPS = 4          # number of 5-char groups after the prefix
_GROUP_LEN = 5
_SIG_BYTES = 12      # 12 bytes -> 96 bits -> exactly 20 base32 chars (4x5)


def _normalize_name(name: str) -> str:
    """Canonical form so 'Joao ', ' joao' and 'JOAO' map to one signature."""
    return (name or "").strip().lower()


def _b32(data: bytes) -> str:
    # RFC4648 base32 without padding, uppercase, '0/1' kept out by base32 alphabet.
    return base64.b32encode(data).decode("ascii").rstrip("=")


def generate_key(name: str) -> str:
    """Deterministically derive the license key for a given licensee name."""
    norm = _normalize_name(name).encode("utf-8")
    sig = hmac.new(_SECRET, norm, hashlib.sha256).digest()[:_SIG_BYTES]
    body = _b32(sig)[: _GROUPS * _GROUP_LEN]
    groups = [body[i:i + _GROUP_LEN] for i in range(0, len(body), _GROUP_LEN)]
    return "-".join([_KEY_PREFIX] + groups)


def _canonical_key(key: str) -> str:
    return (key or "").strip().upper().replace(" ", "")


def validate_key(name: str, key: str) -> bool:
    """True if `key` is the valid license key for `name`."""
    if not name or not key:
        return False
    expected = _canonical_key(generate_key(name))
    provided = _canonical_key(key)
    # constant-time compare
    return hmac.compare_digest(expected, provided)


# ─────────────────────────────────────────────────────────────
#  Persistence
# ─────────────────────────────────────────────────────────────

def _config_dir() -> Path:
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    d = Path(base) / "WinOptimizer"
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return d


def license_path() -> Path:
    return _config_dir() / "license.json"


def save_license(name: str, key: str) -> bool:
    """Validate then persist. Returns True on success."""
    if not validate_key(name, key):
        return False
    try:
        with open(license_path(), "w", encoding="utf-8") as f:
            json.dump({"name": name.strip(), "key": _canonical_key(key)}, f, indent=2)
        return True
    except Exception:
        return False


def load_license() -> dict | None:
    try:
        with open(license_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def clear_license() -> None:
    try:
        os.remove(license_path())
    except Exception:
        pass


def is_pro() -> bool:
    """Single source of truth for Pro entitlement."""
    data = load_license()
    if not data:
        return False
    return validate_key(data.get("name", ""), data.get("key", ""))


def licensee_name() -> str:
    data = load_license() or {}
    return data.get("name", "")


if __name__ == "__main__":
    # Quick self-demo
    demo = "demo@example.com"
    k = generate_key(demo)
    print(f"name={demo!r}  key={k}")
    print("valid     :", validate_key(demo, k))
    print("wrong name:", validate_key("someone@else.com", k))


def config_dir() -> Path:
    """Public accessor for the WinOptimizer config directory."""
    return _config_dir()
