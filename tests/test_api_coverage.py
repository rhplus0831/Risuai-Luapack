"""Drift guard: every host function Risu injects must be emulated.

Parses the `declareAPI('name', ...)` calls out of the vendored Risu source and
asserts the emulator implements each one. If Risu adds or renames an API, this
fails until the emulator catches up. Reads the vendored, pinned copy at
vendor/scriptings.ts (refresh with `python -m luapack sync-source`).
"""
import os
import re

import pytest

from luapack import docgen
from luapack.emulator import RisuEmulator, RisuState

_SCRIPTINGS = docgen.DEFAULT_SCRIPTINGS  # vendored, pinned copy of scriptings.ts


def _declared_apis():
    with open(_SCRIPTINGS, "r", encoding="utf-8") as fh:
        src = fh.read()
    return set(re.findall(r"declareAPI\(\s*['\"]([A-Za-z0-9_]+)['\"]", src))


def _implemented_apis():
    emu = RisuEmulator(RisuState())
    return set(emu._sync_host().keys()) | set(emu._async_mocks().keys())


@pytest.mark.skipif(
    not os.path.exists(_SCRIPTINGS),
    reason="vendored scriptings.ts not present",
)
def test_emulator_covers_every_declared_api():
    declared = _declared_apis()
    implemented = _implemented_apis()
    missing = declared - implemented
    assert not missing, f"Host APIs declared by Risu but not emulated: {sorted(missing)}"
