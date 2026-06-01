"""Static lint for Risu Lua packs: name validation + CBS scanning. No behavior.

- Lexes Lua into code vs string/comment regions (so names aren't matched inside
  strings, and CBS templates can be pulled out of string literals).
- Name checks: misspelled host-API calls, misspelled/miscased event handlers,
  invalid `listenEdit` types, and shadowing of reserved globals.
- CBS: every string literal containing `{{` is handed to `cbs.validate`.

Known API/helper names come from the vendored, pinned `scriptings.ts` + the
`luaCodeWrapper`, so the lint tracks Risu like the docs do.
"""
from __future__ import annotations

import os
import re
from typing import Dict, List, Optional, Set, Tuple

from . import bundler, cbs, vendored
from .emulator import RisuEmulator, lua_src
from .emulator.runtime import LuaSyntaxError

LUA_STDLIB = {
    "print", "type", "tostring", "tonumber", "pairs", "ipairs", "next", "select",
    "error", "assert", "pcall", "xpcall", "setmetatable", "getmetatable", "rawget",
    "rawset", "rawequal", "rawlen", "string", "table", "math", "os", "io",
    "coroutine", "require", "unpack", "collectgarbage", "load", "loadstring",
    "dofile", "utf8", "_G", "_ENV", "_VERSION",
}
LUA_KEYWORDS = {
    "and", "break", "do", "else", "elseif", "end", "false", "for", "function",
    "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then",
    "true", "until", "while",
}
# Globals wasmoon / luaCodeWrapper inject (must not be shadowed; not typos).
INJECTED = {"json", "Promise", "throw", "async", "callListenMain"}
HANDLERS = {"onStart", "onInput", "onOutput", "onButtonClick"}
LISTEN_TYPES = {"editRequest", "editInput", "editOutput", "editDisplay"}


# --------------------------------------------------------------------------- #
# Lua lexer: split code from strings/comments
# --------------------------------------------------------------------------- #
def _long_open(src: str, pos: int) -> Optional[Tuple[int, int]]:
    """If a long-bracket opener `[=*[` starts at pos, return (level, after_idx)."""
    if pos >= len(src) or src[pos] != "[":
        return None
    j = pos + 1
    while j < len(src) and src[j] == "=":
        j += 1
    if j < len(src) and src[j] == "[":
        return j - (pos + 1), j + 1
    return None


def _long_close(src: str, start: int, level: int) -> Optional[Tuple[int, int]]:
    closer = "]" + "=" * level + "]"
    idx = src.find(closer, start)
    if idx < 0:
        return None
    return idx, idx + len(closer)


def scan(src: str) -> Tuple[str, List[Tuple[int, str]]]:
    """Return (code, strings).

    `code` is `src` with string/comment bytes blanked to spaces (newlines kept,
    so offsets/line numbers stay aligned). `strings` is a list of
    (content_start_offset, content) for each string literal.
    """
    n = len(src)
    out = list(src)
    strings: List[Tuple[int, str]] = []

    def blank(a: int, b: int) -> None:
        for k in range(a, min(b, n)):
            if out[k] != "\n":
                out[k] = " "

    i = 0
    while i < n:
        two = src[i:i + 2]
        if two == "--":  # comment
            lo = _long_open(src, i + 2)
            if lo:
                _level, after = lo
                close = _long_close(src, after, _level)
                end = close[1] if close else n
            else:
                nl = src.find("\n", i)
                end = n if nl < 0 else nl
            blank(i, end)
            i = end
            continue
        lo = _long_open(src, i)
        if lo:  # long string [[ ]] / [=[ ]=]
            level, after = lo
            close = _long_close(src, after, level)
            content_end = close[0] if close else n
            end = close[1] if close else n
            strings.append((after, src[after:content_end]))
            blank(i, end)
            i = end
            continue
        if src[i] in ("'", '"'):  # short string
            q = src[i]
            j = i + 1
            while j < n:
                c = src[j]
                if c == "\\":
                    j += 2
                    continue
                if c == q:
                    j += 1
                    break
                if c == "\n":
                    break  # unterminated; stop at end of line
                j += 1
            strings.append((i + 1, src[i + 1:max(i + 1, j - 1)]))
            blank(i, j)
            i = j
            continue
        i += 1
    return "".join(out), strings


def _line_col(src: str, offset: int) -> Tuple[int, int]:
    line = src.count("\n", 0, offset) + 1
    col = offset - (src.rfind("\n", 0, offset) + 1) + 1
    return line, col


# --------------------------------------------------------------------------- #
# Known names (from vendored Risu source)
# --------------------------------------------------------------------------- #
_api_cache: Optional[Tuple[Set[str], Set[str]]] = None


def _api_and_helper_names() -> Tuple[Set[str], Set[str]]:
    global _api_cache
    if _api_cache is None:
        with open(vendored.DEFAULT_SCRIPTINGS, "r", encoding="utf-8") as fh:
            apis = {a["name"] for a in vendored.parse_host_apis(fh.read())}
        helpers = {h["name"] for h in vendored.parse_helpers(lua_src.WRAPPER)}
        _api_cache = (apis, helpers)
    return _api_cache


# --------------------------------------------------------------------------- #
# Lua name lint
# --------------------------------------------------------------------------- #
_CALL_RE = re.compile(r"(?<![\w.:])([A-Za-z_]\w*)\s*\(")
_DEF_FUNC_RE = re.compile(r"\bfunction\s+([A-Za-z_][\w.:]*)\s*\(")
_LOCAL_FUNC_RE = re.compile(r"\blocal\s+function\s+([A-Za-z_]\w*)")
_LOCAL_RE = re.compile(r"\blocal\s+([A-Za-z_][\w\s,]*?)\s*(?:=|\bfunction\b|$)", re.M)
_ASSIGN_RE = re.compile(r"(?<![\w.:=~<>])([A-Za-z_]\w*)\s*=(?!=)")
_PARAMS_RE = re.compile(r"\bfunction\b[^(\n]*\(([^)]*)\)")
_LISTEN_RE = re.compile(r"\blistenEdit\s*\(\s*['\"]([^'\"]+)['\"]")


def _collect_defined(code: str) -> Set[str]:
    defined: Set[str] = set()
    for m in _DEF_FUNC_RE.finditer(code):
        defined.update(re.split(r"[.:]", m.group(1)))
    for m in _LOCAL_FUNC_RE.finditer(code):
        defined.add(m.group(1))
    for m in _LOCAL_RE.finditer(code):
        defined.update(p.strip() for p in m.group(1).split(",") if p.strip())
    for m in _ASSIGN_RE.finditer(code):
        defined.add(m.group(1))
    for m in _PARAMS_RE.finditer(code):
        for p in m.group(1).split(","):
            p = p.strip().lstrip(".")  # handle '...'
            if p:
                defined.add(p)
    return defined


def lint_names(src: str) -> List[Dict]:
    code, _strings = scan(src)
    apis, helpers = _api_and_helper_names()
    callable_names = apis | helpers
    reserved = apis | helpers | INJECTED
    defined = _collect_defined(code)
    known = callable_names | defined | LUA_STDLIB | LUA_KEYWORDS | INJECTED | HANDLERS

    findings: List[Dict] = []

    def add(off: int, severity: str, code_id: str, msg: str) -> None:
        line, col = _line_col(src, off)
        findings.append({"line": line, "col": col, "severity": severity,
                         "code": code_id, "message": msg})

    # Reserved-global shadowing (global function defs only, to stay precise).
    for m in _DEF_FUNC_RE.finditer(code):
        name = m.group(1)
        preceding = code[max(0, m.start() - 7):m.start()]
        if preceding.rstrip().endswith("local"):
            continue
        if name in reserved:
            add(m.start(1), "warning", "shadow",
                f"defining '{name}' shadows a reserved Risu global")
        # Event-handler typo / wrong case
        if name.startswith("on") and name not in HANDLERS:
            sugg = cbs.closest(name, HANDLERS, max_dist=2)
            if sugg and sugg.lower() == name.lower():
                add(m.start(1), "warning", "handler",
                    f"handler '{name}' should be '{sugg}' (names are case-sensitive); it will never fire")
            elif sugg:
                add(m.start(1), "warning", "handler",
                    f"'{name}' looks like a typo of handler '{sugg}'; if intentional (a custom mode) ignore this")

    # listenEdit type validation (the type is a string literal, so read it from
    # the original source; guard that the call itself is real code, not text
    # that happens to sit inside another string/comment).
    for m in _LISTEN_RE.finditer(src):
        if code[m.start():m.start() + len("listenEdit")] != "listenEdit":
            continue
        t = m.group(1)
        if t not in LISTEN_TYPES:
            sugg = cbs.closest(t, LISTEN_TYPES, max_dist=3)
            hint = f" - did you mean '{sugg}'?" if sugg else ""
            add(m.start(1), "error", "listen-type",
                f"invalid listenEdit type '{t}'{hint}")

    # Misspelled host-API calls (near-miss only -> high precision)
    for m in _CALL_RE.finditer(code):
        name = m.group(1)
        if name in known:
            continue
        sugg = cbs.closest(name, callable_names, max_dist=1)
        if sugg:
            add(m.start(1), "warning", "call-typo",
                f"unknown call '{name}' - did you mean '{sugg}'?")

    return findings


# --------------------------------------------------------------------------- #
# Combined checks
# --------------------------------------------------------------------------- #
_SYNTAX_LINE_RE = re.compile(r"]:(\d+):")


def check_source(rel_path: str, src: str) -> List[Dict]:
    findings: List[Dict] = []

    # 1. Syntax (per file -> accurate line numbers)
    try:
        RisuEmulator.compile_check(src)
    except LuaSyntaxError as exc:
        msg = str(exc)
        m = _SYNTAX_LINE_RE.search(msg)
        line = int(m.group(1)) if m else 1
        findings.append({"file": rel_path, "line": line, "col": 1,
                         "severity": "error", "code": "syntax", "message": msg})
        # If it doesn't parse, name/CBS scanning is unreliable; stop here.
        return findings

    # 2. Name lint
    for f in lint_names(src):
        findings.append({"file": rel_path, **f})

    # 3. CBS in string literals. Only NAME issues (unknown-function typos) are
    # reported here: a Lua string literal is often a fragment of a concatenated
    # pattern (e.g. '{{raw::'..x..'}}'), so brace-balance within one literal is
    # meaningless. `check-cbs` validates complete templates including braces.
    _code, strings = scan(src)
    cbs_names = cbs.load_cbs_names()
    for content_start, content in strings:
        if "{{" not in content:
            continue
        for issue in cbs.validate(content, cbs_names):
            if issue.get("kind") != "name":
                continue
            line, col = _line_col(src, content_start + issue["offset"])
            findings.append({"file": rel_path, "line": line, "col": col,
                             "severity": issue["severity"], "code": "cbs",
                             "message": issue["message"]})

    return findings


def check_pack(pack_dir: str) -> List[Dict]:
    """Lint every src/*.lua in a pack. Returns findings sorted by file/line."""
    cfg = bundler.load_config(pack_dir)
    src_dir = os.path.join(pack_dir, cfg["src"])
    findings: List[Dict] = []
    for root, _dirs, files in os.walk(src_dir):
        for fn in sorted(files):
            if not fn.endswith(".lua"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, pack_dir).replace(os.sep, "/")
            with open(full, "r", encoding="utf-8") as fh:
                findings.extend(check_source(rel, fh.read()))
    findings.sort(key=lambda f: (f["file"], f["line"], f["col"]))
    return findings
