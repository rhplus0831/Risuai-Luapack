"""Bundler tests: the example pack must amalgamate, compile, and run as Risu would."""
import os

from luapack import bundler
from luapack.emulator import RisuEmulator
from luapack.testing import load_pack

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE = os.path.join(_REPO, "packs", "example")


def test_discovers_modules_and_emits_entry_call():
    res = bundler.build_pack(EXAMPLE)
    assert set(res["modules"]) == {"main", "utils"}
    assert "__require('main')" in res["bundle"]
    # source markers aid error tracing back to files
    assert "-- <<< src/utils.lua >>>" in res["bundle"]


def test_bundle_compiles():
    res = bundler.build_pack(EXAMPLE)
    RisuEmulator.compile_check(res["bundle"])  # raises on syntax error


def test_require_resolves_local_module_and_runs():
    # The whole point: require('utils') inside main must resolve to the bundled
    # module (no package.preload, no host mountFile), and handlers register.
    emu = load_pack(EXAMPLE, char_name="Rika")
    emu.run_mode("start")
    assert [m.data for m in emu.state.messages] == ["Hello, Rika!"]
    out = emu.run_mode("editOutput", data="hi")
    assert out["res"] == "[hi]"


def test_entry_not_found_is_clear():
    import pytest

    with pytest.raises(bundler.BundleError):
        bundler.build_bundle({"utils": {"path": "utils.lua", "source": "return {}"}},
                             entry="main", pack_name="x")
