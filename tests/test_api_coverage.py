"""Drift guard: every host function Risu injects must be emulated.

Parses the `declareAPI('name', ...)` calls out of the vendored Risu source and
asserts the emulator implements each one. If Risu adds or renames an API, this
fails until the emulator catches up. Skipped when the reference checkout is
absent (e.g. a packaged release without Refer/).
"""
import os
import re

import pytest

from luapack.emulator import RisuEmulator, RisuState

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTINGS = os.path.join(
    _REPO, "Refer", "Risuai", "src", "ts", "process", "scriptings.ts"
)


def _declared_apis():
    with open(_SCRIPTINGS, "r", encoding="utf-8") as fh:
        src = fh.read()
    return set(re.findall(r"declareAPI\(\s*['\"]([A-Za-z0-9_]+)['\"]", src))


def _implemented_apis():
    emu = RisuEmulator(RisuState())
    return set(emu._sync_host().keys()) | set(emu._async_mocks().keys())


@pytest.mark.skipif(
    not os.path.exists(_SCRIPTINGS),
    reason="Risu reference checkout (Refer/Risuai) not present",
)
def test_emulator_covers_every_declared_api():
    declared = _declared_apis()
    implemented = _implemented_apis()
    missing = declared - implemented
    assert not missing, f"Host APIs declared by Risu but not emulated: {sorted(missing)}"
