"""Generate the Lua API reference from Risu's source, so it can't silently drift.

Parses ``declareAPI('name', (params) => { ...guards... })`` out of
``scriptings.ts`` for the host-function table (name, params, permission tier),
and ``function name(params)`` out of the vendored ``luaCodeWrapper`` for the
high-level helpers. The async/await classification comes from the emulator's
``ASYNC_HOST_NAMES`` (authoritative: some host fns return Promises without the
``async`` keyword). Curated one-line descriptions live in ``DESCRIPTIONS``.

``python -m luapack docs`` writes ``docs/lua-api.md``; ``tests/test_docgen.py``
fails if the committed file is stale.
"""
from __future__ import annotations

import os
import re
from typing import Dict, List

from .emulator import lua_src

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The RisuAI commit the emulator and docs are validated against. `luapack
# sync-source` fetches scriptings.ts at this ref by default; bump it to
# deliberately re-check against newer Risu (see CI's upstream-drift job).
RISU_REF = "fc7811d548784deb6db2f6946a19a5b2d7fe50be"

# Source of truth for the API surface: vendored, pinned copies of Risu's
# scriptings.ts (host API) and cbs.ts (CBS function names). Committed (GPLv3,
# like luapack) so docs/lint/drift work on a fresh clone. Refresh with
# `python -m luapack sync-source`.
DEFAULT_SCRIPTINGS = os.path.join(_REPO_ROOT, "vendor", "scriptings.ts")
DEFAULT_CBS = os.path.join(_REPO_ROOT, "vendor", "cbs.ts")

# Risu files fetched by sync-source. `sentinel` rejects a non-source 200 body.
VENDORED_SOURCES = [
    {"raw": "src/ts/process/scriptings.ts", "dest": DEFAULT_SCRIPTINGS, "sentinel": "declareAPI("},
    {"raw": "src/ts/cbs.ts", "dest": DEFAULT_CBS, "sentinel": "registerFunction("},
]

# Entry-point modes (hand-encoded: small, semantic, rarely changes).
MODES = [
    ("start", "function onStart(id)", "before the model request is sent", "`false` stops sending"),
    ("input", "function onInput(id)", "user input is submitted", "`false` stops sending"),
    ("output", "function onOutput(id)", "the model reply arrives", "`false` stops sending"),
    ("onButtonClick", "function onButtonClick(id, data)", "a chat button is clicked", "value"),
    ("editRequest", "listenEdit('editRequest', fn)", "the outgoing request is built", "transformed message array"),
    ("editInput", "listenEdit('editInput', fn)", "user input is processed", "transformed text"),
    ("editOutput", "listenEdit('editOutput', fn)", "the model reply is processed", "transformed text"),
    ("editDisplay", "listenEdit('editDisplay', fn)", "text is rendered (restricted edit-display tier)", "transformed text"),
    ("<custom>", "function <name>(id)", "run with mode='<name>'", "value (`false` stops sending)"),
]

# Curated one-liners. Functions without an entry just show their signature.
DESCRIPTIONS: Dict[str, str] = {
    # helpers (luaCodeWrapper)
    "getState": "Read a JSON-decoded state value (chat var, `__`-prefixed).",
    "setState": "Write a JSON-encoded state value (chat var, `__`-prefixed).",
    "getChat": "Get one chat message as a table `{role, data, time}` (0-based; negative indexes work like JS `Array.at`).",
    "getFullChat": "Get the whole chat as an array of `{role, data, time}`.",
    "setFullChat": "Replace the whole chat from an array of `{role, data}`.",
    "log": "Print a value to the dev console (JSON-encoded).",
    "getLoreBooks": "Find lorebook entries whose comment matches `search`.",
    "loadLoreBooks": "Load activated lorebooks and JSON-decode them (low-level, no reserve argument).",
    "LLM": "Run a sub-request against the main model (low-level); roles accept `system`/`sys`, `user`, `assistant`/`bot`/`char`.",
    "axLLM": "Run a sub-request against the auxiliary model (low-level); same prompt/options shape as `LLM`.",
    "getCharacterImage": "Return `{{inlayed::...}}` for the character image, or an empty string. Awaitable.",
    "getPersonaImage": "Return `{{inlayed::...}}` for the persona image, or an empty string. Awaitable.",
    "listenEdit": "Register a chained edit-trigger handler (editRequest/Input/Output/Display).",
    # host functions
    "getChatVar": "Read a chat variable (string).",
    "setChatVar": "Write a chat variable.",
    "getGlobalVar": "Read a global chat variable.",
    "stopChat": "Stop the current send.",
    "addChat": "Append a message (role `user`; any other role becomes `char`).",
    "insertChat": "Insert a message with JS `splice` semantics.",
    "removeChat": "Remove the message at an index with JS `splice` semantics.",
    "cutChat": "Keep only messages in `[start, end)`.",
    "setChat": "Replace the text of the message at an index.",
    "setChatRole": "Set role to `user`; any other value becomes `char`.",
    "getChatLength": "Number of messages.",
    "getName": "Character name.",
    "setName": "Set the character name.",
    "getDescription": "Character description.",
    "setDescription": "Set the character description.",
    "getCharacterFirstMessage": "Character's first message.",
    "setCharacterFirstMessage": "Set the character's first message.",
    "getPersonaName": "Persona (user) name.",
    "getPersonaDescription": "Persona (user) description, CBS-parsed.",
    "getAuthorsNote": "Author's note for the chat.",
    "getCharacterLastMessage": "Most recent character message.",
    "getUserLastMessage": "Most recent user message.",
    "getBackgroundEmbedding": "Character background HTML.",
    "setBackgroundEmbedding": "Set the character background HTML.",
    "upsertLocalLoreBook": "Create/replace a local lorebook entry.",
    "alertNormal": "Show an info alert.",
    "alertError": "Show an error alert.",
    "alertInput": "Prompt for text input. Awaitable.",
    "alertSelect": "Prompt to pick from options. Awaitable.",
    "alertConfirm": "Ask a yes/no question. Awaitable.",
    "request": "HTTPS GET (<=120 chars; current Risu code allows 6/min before 429; low-level); returns a JSON string. Awaitable.",
    "similarity": "Embedding similarity search (low-level). Awaitable.",
    "generateImage": "Generate an image and return `{{inlay::...}}` (low-level). Awaitable.",
    "hash": "Hash a string. Awaitable.",
    "getTokens": "Token count of a string. Awaitable.",
    "sleep": "Wait N milliseconds. Awaitable.",
    "cbs": "Expand a CBS `{{...}}` template string; variable-writing CBS does not run through this helper.",
    "simpleLLM": "One-shot user-prompt model call (low-level); returns `{success, result}`. Awaitable.",
    "reloadDisplay": "Trigger a display refresh.",
    "reloadChat": "Trigger a re-render of one message.",
    # raw *Main host calls — prefer the matching helper above
    "getChatMain": "Raw `getChat` (returns a JSON string).",
    "getFullChatMain": "Raw `getFullChat` (returns a JSON string).",
    "setFullChatMain": "Raw `setFullChat` (takes a JSON string).",
    "logMain": "Raw `log` (takes a JSON string).",
    "getLoreBooksMain": "Raw `getLoreBooks` (returns a JSON string).",
    "loadLoreBooksMain": "Raw `loadLoreBooks` with a reserve budget (returns a JSON string).",
    "getCharacterImageMain": "Raw `getCharacterImage`.",
    "getPersonaImageMain": "Raw `getPersonaImage`.",
    "LLMMain": "Raw `LLM` (JSON in, JSON out).",
    "axLLMMain": "Raw `axLLM` (JSON in, JSON out).",
}

_TIER_LABEL = {
    "any": "Always available",
    "safe": "Safe — modifies chat/character (blocked in edit-display tier)",
    "safe-or-editdisplay": "Safe or edit-display",
    "low-level": "Low-level — requires `lowLevelAccess`",
}
_TIER_ORDER = ["any", "safe", "safe-or-editdisplay", "low-level"]

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
    helpers = []
    for m in re.finditer(r"function\s+(\w+)\s*\(([^)]*)\)", wrapper_src):
        name = m.group(1)
        if name in _HELPER_DENYLIST:
            continue
        helpers.append({"name": name, "params": _clean_params(m.group(2))})
    return helpers


def _row(name: str, params: str, is_async: bool) -> str:
    sig = f"`{name}({params})`"
    tag = " _(await)_" if is_async else ""
    desc = DESCRIPTIONS.get(name, "")
    return f"| {sig}{tag} | {desc} |"


def generate(scriptings_src: str, wrapper_src: str, async_names) -> str:
    async_set = set(async_names)
    apis = parse_host_apis(scriptings_src)
    helpers = parse_helpers(wrapper_src)

    out = []
    out.append("# Risu Lua API Reference")
    out.append("")
    out.append("> API surface generated from `scriptings.ts` by "
               "`python -m luapack docs`; descriptions and entry-point "
               "summaries are curated — do not edit by hand.")
    out.append("> Concepts, gotchas, and how-to are in [lua-guide.md](./lua-guide.md).")
    out.append("")
    out.append("Functions tagged _(await)_ return a promise; call `:await()` "
               "(the `LLM`/`axLLM`/`loadLoreBooks` helpers await and "
               "JSON-decode for you; image helpers await and return inlay "
               "strings).")
    out.append("")

    out.append("## Entry points")
    out.append("")
    out.append("Define the global / register the listener; Risu calls it per mode.")
    out.append("")
    out.append("| Mode | You define | Fires when | Returns |")
    out.append("|------|-----------|-----------|---------|")
    for mode, define, when, ret in MODES:
        out.append(f"| `{mode}` | `{define}` | {when} | {ret} |")
    out.append("")
    out.append("Notes: `listenEdit` handlers are chained in registration order. "
               "`editDisplay` uses a restricted edit-display key: it can write "
               "chat vars, but cannot mutate chat or character data. "
               "Edit listeners never receive low-level access.")
    out.append("")

    out.append("## Helpers")
    out.append("")
    out.append("Provided by Risu's preamble. Prefer these over the raw `*Main` "
               "host calls when they handle JSON for you; `log`, `cbs`, and "
               "image helpers are exceptions that return or pass plain values.")
    out.append("")
    out.append("| Helper | What it does |")
    out.append("|--------|--------------|")
    for h in sorted(helpers, key=lambda x: x["name"]):
        out.append(_row(h["name"], h["params"], h["name"] in async_set))
    out.append("")

    out.append("## Host functions")
    out.append("")
    out.append("Injected globals. Most calls take the access-key `id` as their "
               "first argument (exceptions include `cbs` and `logMain`; see "
               "the guide). Grouped by permission tier.")
    out.append("")
    for tier in _TIER_ORDER:
        group = [a for a in apis if a["tier"] == tier]
        if not group:
            continue
        out.append(f"### {_TIER_LABEL[tier]}")
        out.append("")
        out.append("| Function | What it does |")
        out.append("|----------|--------------|")
        for a in sorted(group, key=lambda x: x["name"]):
            out.append(_row(a["name"], a["params"], a["name"] in async_set))
        out.append("")

    return "\n".join(out).rstrip("\n") + "\n"


def generate_from_repo(scriptings_path: str = DEFAULT_SCRIPTINGS) -> str:
    with open(scriptings_path, "r", encoding="utf-8") as fh:
        scriptings_src = fh.read()
    return generate(scriptings_src, lua_src.WRAPPER, lua_src.ASYNC_HOST_NAMES)
