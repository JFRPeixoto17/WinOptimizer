"""Unit tests for license_manager.py (offline HMAC licensing)."""

import json
import re

import pytest

import license_manager as lm


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Redirect the license file into a temp dir so tests never touch %APPDATA%."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    yield tmp_path


# ── key generation ───────────────────────────────────────────

def test_key_format():
    key = lm.generate_key("customer@example.com")
    assert re.fullmatch(r"WO(-[A-Z2-7]{5}){4}", key)


def test_key_is_deterministic():
    assert lm.generate_key("a@b.com") == lm.generate_key("a@b.com")


def test_key_normalizes_name_case_and_whitespace():
    base = lm.generate_key("joao@example.com")
    assert lm.generate_key("  JOAO@Example.COM ") == base


def test_different_names_get_different_keys():
    assert lm.generate_key("a@b.com") != lm.generate_key("c@d.com")


# ── validation ───────────────────────────────────────────────

def test_validate_roundtrip():
    key = lm.generate_key("x@y.com")
    assert lm.validate_key("x@y.com", key)


def test_validate_accepts_lowercase_and_spaced_key():
    key = lm.generate_key("x@y.com")
    assert lm.validate_key("x@y.com", key.lower().replace("-", "- "))


def test_validate_rejects_wrong_name():
    key = lm.generate_key("x@y.com")
    assert not lm.validate_key("other@y.com", key)


def test_validate_rejects_tampered_key():
    key = lm.generate_key("x@y.com")
    bad = key[:-1] + ("A" if key[-1] != "A" else "B")
    assert not lm.validate_key("x@y.com", bad)


@pytest.mark.parametrize("name,key", [("", ""), (None, None), ("x@y.com", ""), ("", "WO-AAAAA-AAAAA-AAAAA-AAAAA")])
def test_validate_rejects_empty_inputs(name, key):
    assert not lm.validate_key(name, key)


# ── persistence ──────────────────────────────────────────────

def test_save_and_load_license():
    key = lm.generate_key("x@y.com")
    assert lm.save_license("x@y.com", key)
    data = lm.load_license()
    assert data == {"name": "x@y.com", "key": key}
    assert lm.is_pro()
    assert lm.licensee_name() == "x@y.com"


def test_save_rejects_invalid_key():
    assert not lm.save_license("x@y.com", "WO-AAAAA-AAAAA-AAAAA-AAAAA")
    assert lm.load_license() is None
    assert not lm.is_pro()


def test_load_tolerates_corrupt_file():
    lm.license_path().parent.mkdir(parents=True, exist_ok=True)
    lm.license_path().write_text("{not json", encoding="utf-8")
    assert lm.load_license() is None
    assert not lm.is_pro()


def test_load_tolerates_non_dict_json():
    lm.license_path().parent.mkdir(parents=True, exist_ok=True)
    lm.license_path().write_text(json.dumps(["a", "b"]), encoding="utf-8")
    assert lm.load_license() is None


def test_is_pro_false_when_stored_license_invalid():
    lm.license_path().parent.mkdir(parents=True, exist_ok=True)
    lm.license_path().write_text(
        json.dumps({"name": "x@y.com", "key": "WO-AAAAA-AAAAA-AAAAA-AAAAA"}),
        encoding="utf-8",
    )
    assert not lm.is_pro()


def test_deactivate_removes_license():
    key = lm.generate_key("x@y.com")
    lm.save_license("x@y.com", key)
    lm.deactivate()
    assert lm.load_license() is None
    assert not lm.is_pro()
    lm.deactivate()  # idempotent


def test_masked_key_hides_middle_groups():
    key = lm.generate_key("x@y.com")
    lm.save_license("x@y.com", key)
    masked = lm.masked_key()
    parts = key.split("-")
    assert masked.startswith(f"{parts[0]}-{parts[1]}-")
    assert masked.endswith(parts[-1])
    assert "*****" in masked
    assert parts[2] not in masked


def test_masked_key_empty_when_no_license():
    assert lm.masked_key() == ""
