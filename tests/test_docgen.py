"""Docs must not drift: the committed reference must equal the generator output,
and every host API Risu declares must appear in it.

Skipped when the Risu reference checkout (Refer/) is absent.
"""
import os

import pytest

from luapack import docgen

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(_REPO, "docs", "lua-api.md")

pytestmark = pytest.mark.skipif(
    not os.path.exists(docgen.DEFAULT_SCRIPTINGS),
    reason="Risu reference checkout (Refer/Risuai) not present",
)


def test_reference_is_current():
    generated = docgen.generate_from_repo()
    with open(DOC, "r", encoding="utf-8") as fh:
        current = fh.read()
    assert current == generated, "docs/lua-api.md is stale; run: python -m luapack docs"


def test_every_declared_api_is_documented():
    with open(docgen.DEFAULT_SCRIPTINGS, "r", encoding="utf-8") as fh:
        names = {a["name"] for a in docgen.parse_host_apis(fh.read())}
    doc = docgen.generate_from_repo()
    missing = sorted(n for n in names if f"`{n}(" not in doc)
    assert not missing, f"undocumented APIs: {missing}"
