"""Pinned RisuAI source: paths, the commit ref, and the parsers that read it.

The host API surface and CBS name lists are derived from vendored, pinned copies
of Risu's ``scriptings.ts`` and ``cbs.ts`` (committed under ``vendor/``, GPLv3
like luapack). This module holds the pieces the rest of the tooling needs to
stay in sync with Risu:

- ``RISU_REF`` / ``VENDORED_SOURCES`` drive ``python -m luapack sync-source``.
- ``parse_host_apis`` / ``parse_helpers`` feed the lint (``lint.py``) and the
  emulator-coverage drift guard (``tests/test_api_coverage.py``).
- ``DEFAULT_CBS`` feeds CBS name validation (``cbs.py``).

Documentation is now hand-authored under ``docs/`` (see ``docs/README.md``); the
old generator that produced ``docs/lua-api.md`` from this source has been
removed.
"""
from __future__ import annotations

import os
import re
from typing import Dict, List

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The RisuAI commit the emulator and lint are validated against. `luapack
# sync-source` fetches scriptings.ts/cbs.ts at this ref by default; bump it to
# deliberately re-check against newer Risu (see CI's upstream-drift job).
RISU_REF = "fc7811d548784deb6db2f6946a19a5b2d7fe50be"

# Source of truth for the API surface: vendored, pinned copies of Risu's
# scriptings.ts (host API) and cbs.ts (CBS function names). Committed (GPLv3,
# like luapack) so lint/drift work on a fresh clone. Refresh with
# `python -m luapack sync-source`.
DEFAULT_SCRIPTINGS = os.path.join(_REPO_ROOT, "vendor", "scriptings.ts")
DEFAULT_CBS = os.path.join(_REPO_ROOT, "vendor", "cbs.ts")

# Risu files fetched by sync-source. `sentinel` rejects a non-source 200 body.
VENDORED_SOURCES = [
    {"raw": "src/ts/process/scriptings.ts", "dest": DEFAULT_SCRIPTINGS, "sentinel": "declareAPI("},
    {"raw": "src/ts/cbs.ts", "dest": DEFAULT_CBS, "sentinel": "registerFunction("},
]

# Internal wrapper plumbing not meant to be called directly.
_HELPER_DENYLIST = {"async", "callListenMain"}


def _clean_params(raw: str) -> str:
    names = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        name = part.split(":")[0].split("=")[0].strip()
        if name:
            names.append(name)
    return ", ".join(names)


def parse_host_apis(src: str) -> List[Dict]:
    """Parse ``declareAPI('name', (params) => { ...guards... })`` from scriptings.ts.

    Returns one dict per API with ``name``, ``params``, and ``tier`` (the
    permission tier inferred from which ``Scripting*Ids`` guard appears).
    """
    apis = []
    for chunk in src.split("declareAPI(")[1:]:
        m = re.match(r"\s*['\"](\w+)['\"]", chunk)
        if not m:
            continue
        name = m.group(1)
        head = chunk[: chunk.find("=>")] if "=>" in chunk else chunk[:200]
        paren = re.findall(r"\(([^)]*)\)", head)
        params = _clean_params(paren[-1]) if paren else ""
        if "ScriptingLowLevelIds" in chunk:
            tier = "low-level"
        elif "ScriptingEditDisplayIds" in chunk:
            tier = "safe-or-editdisplay"
        elif "ScriptingSafeIds" in chunk:
            tier = "safe"
        else:
            tier = "any"
        apis.append({"name": name, "params": params, "tier": tier})
    # de-dupe (a couple of APIs are declared twice in source), keep first
    seen, out = set(), []
    for a in apis:
        if a["name"] in seen:
            continue
        seen.add(a["name"])
        out.append(a)
    return out


def parse_helpers(wrapper_src: str) -> List[Dict]:
    """Parse ``function name(params)`` helpers from the ``luaCodeWrapper`` source."""
    helpers = []
    for m in re.finditer(r"function\s+(\w+)\s*\(([^)]*)\)", wrapper_src):
        name = m.group(1)
        if name in _HELPER_DENYLIST:
            continue
        helpers.append({"name": name, "params": _clean_params(m.group(2))})
    return helpers
