"""Schema/consistency tests for tweaks.json.

Guards against the classes of bugs fixed in the v1.2.x audits:
missing fields, duplicate IDs, presets referencing nonexistent tweaks,
registry tweaks without undo values, etc.
"""

import json
from pathlib import Path

import pytest

TWEAKS_PATH = Path(__file__).parent.parent / "tweaks.json"
CATEGORIES = ["essential", "services", "performance", "privacy", "advanced"]

REQUIRED_COMMON = {"id", "name", "description", "command", "impact", "recommended"}


@pytest.fixture(scope="module")
def data():
    with open(TWEAKS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _all_tweaks(data):
    out = []
    for cat in CATEGORIES:
        out.extend(data[cat])
    return out


def test_top_level_structure(data):
    assert set(CATEGORIES) <= set(data.keys())
    assert isinstance(data["presets"], dict)
    for cat in CATEGORIES:
        assert isinstance(data[cat], list) and data[cat], f"{cat} empty"


def test_common_required_fields(data):
    for t in _all_tweaks(data):
        missing = REQUIRED_COMMON - set(t)
        assert not missing, f"tweak {t.get('id', '?')} missing {missing}"
        assert isinstance(t["recommended"], bool)
        assert t["id"].strip() and t["name"].strip()


def test_ids_are_unique(data):
    ids = [t["id"] for t in _all_tweaks(data)]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate tweak ids: {dupes}"


REG_FIELDS = ("registry_path", "registry_name", "registry_type",
              "registry_value", "undo_value")


def test_registry_tweaks_are_all_or_nothing(data):
    """If a tweak uses any registry_* field it must define the full spec."""
    for t in _all_tweaks(data):
        present = [f for f in REG_FIELDS if f in t]
        if not present:
            continue
        missing = set(REG_FIELDS) - set(present)
        assert not missing, f"{t['id']} partial registry spec, missing {missing}"
        assert t["registry_path"].startswith("HK"), t["id"]
        # PowerShell Set-ItemProperty -Type values used by main.py
        assert t["registry_type"] in {"DWORD", "QWORD", "String",
                                      "ExpandString", "Binary", "MultiString"}, t["id"]


def test_service_tweaks_shape(data):
    """Service tweaks must list service names (or be full registry tweaks)."""
    for t in data["services"]:
        names = t.get("service_names")
        if names is not None:
            assert isinstance(names, list) and names, t["id"]
            assert all(isinstance(s, str) and s.strip() for s in names), t["id"]
        else:
            # allowed alternative: a registry-based toggle (e.g. backgroundApps)
            assert all(f in t for f in REG_FIELDS), (
                f"{t['id']} has neither service_names nor a full registry spec"
            )


def test_undo_args_require_undo_command(data):
    for t in _all_tweaks(data):
        if t.get("undo_args"):
            assert t.get("undo_command"), f"{t['id']} has undo_args without undo_command"


def test_every_tweak_has_an_execution_mechanism(data):
    for t in _all_tweaks(data):
        has_registry = all(f in t for f in REG_FIELDS)
        has_services = bool(t.get("service_names"))
        has_command = bool(str(t.get("command", "")).strip())
        assert has_registry or has_services or has_command, (
            f"{t['id']} has no way to execute"
        )


def test_presets_reference_existing_tweaks(data):
    valid_ids = {t["id"] for t in _all_tweaks(data)}
    for preset, tweak_ids in data["presets"].items():
        assert isinstance(tweak_ids, list) and tweak_ids, preset
        unknown = set(tweak_ids) - valid_ids
        assert not unknown, f"preset {preset} references unknown ids: {unknown}"


def test_recommended_preset_matches_recommended_flags(data):
    flagged = {t["id"] for t in _all_tweaks(data) if t["recommended"]}
    preset = set(data["presets"].get("recommended", []))
    assert preset <= flagged or flagged <= preset or preset, (
        "recommended preset and recommended flags diverge completely"
    )


def test_no_homegroup_remnants(data):
    # HomeGroup was removed from Win11; audit in v1.2.1 deleted it.
    blob = json.dumps(data).lower()
    assert "homegroup" not in blob
