"""CBS (`{{...}}`) template validation: syntax + known function names.

CBS function names are parsed from the vendored, pinned `cbs.ts`
(`registerFunction({ name, alias })`), the same way the host API is parsed from
`scriptings.ts`. Validation is fully static -- balanced/nested `{{ }}` and known
names -- and never evaluates a template (no behavior, no risuChatParser).
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Set

from . import docgen

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# Leading chars that mark a block / special construct ({{#if}}, {{/if}},
# {{:else}}, {{? expr}}, {{// comment}}, ...) rather than a plain function call.
_SPECIAL_PREFIX = set("#/:?!@")

_names_cache: Optional[Set[str]] = None


def parse_cbs_names(src: str) -> Set[str]:
    """Extract CBS function names + aliases (lowercased) from cbs.ts source."""
    names: Set[str] = set()
    for chunk in src.split("registerFunction(")[1:]:
        head = chunk[:800]  # name + alias sit at the top of the object literal
        m = re.search(r"name:\s*['\"]([^'\"]+)['\"]", head)
        if m:
            names.add(m.group(1).lower())
        am = re.search(r"alias:\s*\[([^\]]*)\]", head)
        if am:
            for a in re.findall(r"['\"]([^'\"]+)['\"]", am.group(1)):
                names.add(a.lower())
    return names


def load_cbs_names(path: Optional[str] = None) -> Set[str]:
    global _names_cache
    if path is None and _names_cache is not None:
        return _names_cache
    with open(path or docgen.DEFAULT_CBS, "r", encoding="utf-8") as fh:
        names = parse_cbs_names(fh.read())
    if path is None:
        _names_cache = names
    return names


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a or not b:
        return len(a) or len(b)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def closest(name: str, candidates, max_dist: int = 2) -> Optional[str]:
    best, best_d = None, max_dist + 1
    for c in candidates:
        d = levenshtein(name, c)
        if d < best_d:
            best, best_d = c, d
    return best if best_d <= max_dist else None


def _first_top_separator(inner: str) -> int:
    """Index of the first `::` not inside a nested `{{ }}`, or -1."""
    depth, i, n = 0, 0, len(inner)
    while i < n - 1:
        two = inner[i:i + 2]
        if two == "{{":
            depth += 1
            i += 2
        elif two == "}}":
            depth -= 1
            i += 2
        elif depth == 0 and two == "::":
            return i
        else:
            i += 1
    return -1


def _check_name(inner: str, offset: int, names: Set[str], issues: List[Dict]) -> None:
    sep = _first_top_separator(inner)
    raw = (inner if sep < 0 else inner[:sep]).strip()
    if raw == "":
        issues.append({"severity": "warning", "offset": offset, "message": "empty CBS '{{}}'"})
        return
    if "{{" in raw:          # dynamic/nested name -- can't check statically
        return
    if raw[0] in _SPECIAL_PREFIX:  # block / special construct, not a function call
        return
    if not _IDENT_RE.match(raw):   # not a plain identifier -- skip
        return
    if raw.lower() in names:
        return
    suggestion = closest(raw.lower(), names, max_dist=2)
    if suggestion:
        issues.append({"severity": "warning", "offset": offset,
                       "message": f"unknown CBS function '{raw}' - did you mean '{{{{{suggestion}}}}}'?"})
    else:
        issues.append({"severity": "warning", "offset": offset,
                       "message": f"unknown CBS function '{raw}'"})


def validate(template: str, names: Optional[Set[str]] = None) -> List[Dict]:
    """Return issues (each {severity, offset, message}) for a CBS template string.

    Errors: unbalanced `{{`/`}}`. Warnings: unknown / likely-typo function names.
    """
    if names is None:
        names = load_cbs_names()
    issues: List[Dict] = []
    stack: List[int] = []
    i, n = 0, len(template)
    while i < n:
        two = template[i:i + 2]
        if two == "{{":
            stack.append(i)
            i += 2
        elif two == "}}":
            if not stack:
                issues.append({"severity": "error", "offset": i, "message": "unmatched '}}'"})
            else:
                start = stack.pop()
                _check_name(template[start + 2:i], start, names, issues)
            i += 2
        else:
            i += 1
    for start in stack:
        issues.append({"severity": "error", "offset": start, "message": "unclosed '{{'"})
    return issues
