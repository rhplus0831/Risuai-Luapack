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

__all__ = ["load", "RisuEmulator", "RisuState", "Message"]


def load(bundle: str, state: Optional[RisuState] = None, **state_kwargs) -> RisuEmulator:
    """Build a RisuState (from kwargs unless ``state`` is given), load the bundle."""
    emu = RisuEmulator(state if state is not None else RisuState(**state_kwargs))
    emu.load(bundle)
    return emu
