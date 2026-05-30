"""Example pack tests. Run with: python -m luapack test packs/example

Shows the load_pack pattern: build the real bundle and drive it like Risu would.
"""
import os

from luapack.testing import load_pack

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_starts_with_greeting():
    emu = load_pack(PACK, char_name="Rika")
    emu.run_mode("start")
    assert [m.data for m in emu.state.messages] == ["Hello, Rika!"]


def test_decorates_output():
    emu = load_pack(PACK)
    out = emu.run_mode("editOutput", data="hi")
    assert out["res"] == "[hi]"
