"""Test-authoring helpers for Risu Lua bundles.

The pattern coding agents and humans write against::

    from luapack.testing import load

    def test_greeting():
        emu = load(\"\"\"
            function onStart(id)
                setChatVar(id, 'greeted', 'yes')
            end
        \"\"\")
        emu.run_mode('start')
        assert emu.state.chat_vars['greeted'] == 'yes'

Seed initial state with keyword args (forwarded to ``RisuState``) or by passing
a prebuilt ``RisuState``. ``run_mode(..., low_level=True)`` grants the low-level
tier for that call.
"""
from __future__ import annotations

from typing import Optional

from .emulator import Message, RisuEmulator, RisuState

__all__ = ["load", "load_pack", "RisuEmulator", "RisuState", "Message"]


def load(bundle: str, state: Optional[RisuState] = None, **state_kwargs) -> RisuEmulator:
    """Build a RisuState (from kwargs unless ``state`` is given), load the bundle."""
    emu = RisuEmulator(state if state is not None else RisuState(**state_kwargs))
    emu.load(bundle)
    return emu


def load_pack(pack_dir: str, state: Optional[RisuState] = None, **state_kwargs) -> RisuEmulator:
    """Bundle a pack directory in memory and load the result, like Risu would.

    Tests the actual amalgamated output (module require resolution, handler
    registration), not a hand-written single file.
    """
    from . import bundler

    bundle = bundler.build_pack(pack_dir)["bundle"]
    return load(bundle, state=state, **state_kwargs)
