import os
import sys

import pytest

# Make `import luapack` work without an editable install.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from luapack.testing import load  # noqa: E402


@pytest.fixture
def risu():
    """Factory fixture: risu(bundle, **state_kwargs) -> loaded RisuEmulator."""
    return load
