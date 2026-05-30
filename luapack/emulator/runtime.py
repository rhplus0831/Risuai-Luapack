"""RisuEmulator - run a Risu Lua bundle under lupa with a mock host environment.

M1 scope: enough of the host API + permission tiers to prove the spine
(Promise/async bridge, edit-listener dispatch, JSON-marshalled LLM path). M2
extends the host surface to full parity. See ``state.py`` for the data model and
``lua_src.py`` for the Lua fragments assembled around the user's bundle.
"""
from __future__ import annotations

import hashlib
import json as _json
import os
import uuid
from typing import Any, Dict, List, Optional

from lupa import lua54

from . import lua_src
from .state import Message, RisuState

# Per-version lupa modules define their own exception classes; the top-level
# lupa.LuaError does NOT catch lupa.lua54.LuaSyntaxError. Use the lua54 ones.
LuaError = lua54.LuaError

_VENDOR_JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "vendor",
    "json.lua",
)

_EDIT_MODES = {"editRequest", "editDisplay", "editInput", "editOutput"}


class LuaSyntaxError(Exception):
    """Raised by compile_check for a bundle that does not parse."""


def _at(seq, index):
    """Array.prototype.at() semantics: 0-based, negatives count from the end."""
    i = int(index)
    if i < 0:
        i += len(seq)
    if 0 <= i < len(seq):
        return seq[i]
    return None


def _lua_get(tbl, key, default):
    """Read a field from a possibly-nil lupa table, with a Python default."""
    if tbl is None:
        return default
    try:
        v = tbl[key]
    except (KeyError, TypeError):
        v = None
    return default if v is None else v


def _lua_to_list(tbl) -> List[Any]:
    """Convert a 1-based lupa array table into a Python list."""
    if tbl is None:
        return []
    if isinstance(tbl, (list, tuple)):
        return list(tbl)
    out: List[Any] = []
    i = 1
    while True:
        try:
            v = tbl[i]
        except (KeyError, TypeError):
            break
        if v is None:
            break
        out.append(v)
        i += 1
    return out


class RisuEmulator:
    def __init__(self, state: Optional[RisuState] = None):
        self.state = state or RisuState()
        self._stop = False
        # Permission tiers, mirroring ScriptingSafeIds / EditDisplay / LowLevel.
        self._safe: set = set()
        self._editdisplay: set = set()
        self._lowlevel: set = set()

        self.lua = lua54.LuaRuntime(
            encoding="utf-8",
            source_encoding="utf-8",
            unpack_returned_tuples=False,
        )
        self._dispatch = None
        self._loaded_bundle: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Static syntax check (fast, no execution, no host env)
    # ------------------------------------------------------------------ #
    @staticmethod
    def compile_check(bundle: str) -> None:
        """Compile the bundle for syntax only. Raises LuaSyntaxError on failure."""
        rt = lua54.LuaRuntime(encoding="utf-8", source_encoding="utf-8")
        try:
            rt.compile(bundle, name="bundle")
        except LuaError as exc:  # lua54.LuaError covers lua54.LuaSyntaxError
            raise LuaSyntaxError(str(exc)) from exc

    # ------------------------------------------------------------------ #
    # Load a bundle into the live environment
    # ------------------------------------------------------------------ #
    def load(self, bundle: str) -> None:
        g = self.lua.globals()

        # 1. Inject host API (sync host fns under their real names; async host
        #    fns as __mock_<name>, wrapped into Promises by the prelude).
        for name, fn in self._sync_host().items():
            g[name] = fn
        for name, fn in self._async_mocks().items():
            g["__mock_" + name] = fn

        # 2. Preload the identical json.lua so `require 'json'` matches Risu.
        with open(_VENDOR_JSON, "r", encoding="utf-8") as fh:
            json_src = fh.read()
        g["__json_chunk"] = self.lua.compile(json_src, name="json.lua")

        # 3. Prelude (Promise/throw/json preload/async wrappers).
        self.lua.execute(lua_src.PRELUDE)

        # 4. Risu wrapper + user bundle.
        self.lua.execute(lua_src.build_wrapped(bundle))

        # 5. Mode dispatcher.
        self.lua.execute(lua_src.DISPATCHER)

        self._dispatch = g["__luapack_dispatch"]
        self._loaded_bundle = bundle

    # ------------------------------------------------------------------ #
    # Drive a single entry point
    # ------------------------------------------------------------------ #
    def run_mode(
        self,
        mode: str,
        data: Any = None,
        meta: Any = None,
        low_level: bool = False,
    ) -> Dict[str, Any]:
        if self._dispatch is None:
            raise RuntimeError("load() a bundle before run_mode()")

        self._stop = False
        acc = uuid.uuid4().hex
        if mode == "editDisplay":
            self._editdisplay.add(acc)
        else:
            self._safe.add(acc)
            if low_level:
                self._lowlevel.add(acc)

        if mode in _EDIT_MODES:
            data_arg = _json.dumps(data)
            meta_arg = _json.dumps(meta if meta is not None else {})
        elif mode == "onButtonClick":
            data_arg = "" if data is None else str(data)
            meta_arg = ""
        else:
            data_arg, meta_arg = "", ""

        error = None
        try:
            res = self._dispatch(mode, acc, data_arg, meta_arg)
        except LuaError as exc:
            # Risu wraps mode dispatch in try/catch and logs; a script error
            # leaves the result undefined rather than crashing the host.
            res = None
            error = str(exc)
            self.state.last_error = error
        finally:
            self._safe.discard(acc)
            self._editdisplay.discard(acc)
            self._lowlevel.discard(acc)

        if error is None and mode in _EDIT_MODES and isinstance(res, str):
            res = _json.loads(res)

        return {
            "res": res,
            "stop": (res is False) or self._stop,
            "error": error,
            "chat": [m.to_dict() for m in self.state.messages],
        }

    # ------------------------------------------------------------------ #
    # Host API - synchronous functions (real names, take id first)
    # ------------------------------------------------------------------ #
    def _can_write(self, id_: str) -> bool:
        return id_ in self._safe or id_ in self._editdisplay

    def _is_safe(self, id_: str) -> bool:
        return id_ in self._safe

    def _sync_host(self) -> Dict[str, Any]:
        s = self.state

        def getChatVar(id_, key):
            return s.chat_vars.get(key, "")

        def setChatVar(id_, key, value):
            if not self._can_write(id_):
                return
            s.chat_vars[key] = value if value is not None else ""

        def getGlobalVar(id_, key):
            return s.global_vars.get(key, "")

        def stopChat(id_):
            if self._is_safe(id_):
                self._stop = True

        def alertNormal(id_, value):
            if self._is_safe(id_):
                s.alerts.append({"type": "normal", "value": value})

        def alertError(id_, value):
            if self._is_safe(id_):
                s.alerts.append({"type": "error", "value": value})

        def getChatLength(id_):
            return len(s.messages)

        def getChatMain(id_, index):
            m = _at(s.messages, index)
            return _json.dumps(None) if m is None else _json.dumps(m.to_dict())

        def getFullChatMain(id_):
            return _json.dumps([m.to_dict() for m in s.messages])

        def setFullChatMain(id_, value):
            if not self._is_safe(id_):
                return
            arr = _json.loads(value)
            s.messages = [Message(role=v["role"], data=v.get("data", "")) for v in arr]

        def setChat(id_, index, value):
            if not self._is_safe(id_):
                return
            m = _at(s.messages, index)
            if m is not None:
                m.data = value if value is not None else ""

        def setChatRole(id_, index, value):
            if not self._is_safe(id_):
                return
            m = _at(s.messages, index)
            if m is not None:
                m.role = "user" if value == "user" else "char"

        def cutChat(id_, start, end):
            if not self._is_safe(id_):
                return
            s.messages = s.messages[int(start):int(end)]

        def removeChat(id_, index):
            if not self._is_safe(id_):
                return
            i = int(index)
            if 0 <= i < len(s.messages):
                s.messages.pop(i)

        def addChat(id_, role, value):
            if not self._is_safe(id_):
                return
            s.messages.append(
                Message(role="user" if role == "user" else "char",
                        data=value if value is not None else "")
            )

        def insertChat(id_, index, role, value):
            if not self._is_safe(id_):
                return
            s.messages.insert(
                int(index),
                Message(role="user" if role == "user" else "char",
                        data=value if value is not None else ""),
            )

        def logMain(value):
            s.logs.append(_json.loads(value))

        def getName(id_):
            return s.char_name

        def setName(id_, name):
            if self._is_safe(id_):
                s.char_name = name

        def getDescription(id_):
            if self._is_safe(id_):
                return s.char_desc

        def setDescription(id_, desc):
            if self._is_safe(id_):
                s.char_desc = desc

        def getCharacterFirstMessage(id_):
            return s.char_first_message

        def getPersonaName(id_):
            return s.persona_name

        def getPersonaDescription(id_):
            return s.persona_desc

        def getAuthorsNote(id_):
            return s.note

        def getCharacterLastMessage(id_):
            for m in reversed(s.messages):
                if m.role == "char":
                    return m.data
            return s.char_first_message

        def getUserLastMessage(id_):
            for m in reversed(s.messages):
                if m.role == "user":
                    return m.data
            return ""

        def cbs(value):
            # TODO: emulate risuChatParser. For now, pass through unchanged.
            return value

        def setCharacterFirstMessage(id_, data):
            if not self._is_safe(id_):
                return False
            s.char_first_message = data
            return True

        def getBackgroundEmbedding(id_):
            if self._is_safe(id_):
                return s.background_html

        def setBackgroundEmbedding(id_, data):
            if not self._is_safe(id_):
                return False
            s.background_html = data
            return True

        def reloadDisplay(id_):
            if self._is_safe(id_):
                s.reload_display_count += 1

        def reloadChat(id_, index):
            if self._is_safe(id_):
                s.reloaded_chats.append(int(index))

        def getLoreBooksMain(id_, search):
            found = []
            for source in (s.local_lore, s.global_lore, s.module_lore):
                for b in source:
                    if b.get("comment") == search:
                        # content would be risuChatParser-expanded in Risu.
                        found.append({**b, "content": b.get("content", "")})
            return _json.dumps(found)

        def upsertLocalLoreBook(id_, name, content, options=None):
            if not self._is_safe(id_):
                return
            second = _lua_get(options, "secondKey", "")
            s.local_lore = [b for b in s.local_lore if b.get("comment") != name]
            s.local_lore.append({
                "alwaysActive": bool(_lua_get(options, "alwaysActive", False)),
                "comment": name,
                "content": content,
                "insertorder": _lua_get(options, "insertOrder", 100),
                "mode": "normal",
                "key": _lua_get(options, "key", ""),
                "secondkey": second,
                "selective": bool(second),
                "useRegex": bool(_lua_get(options, "regex", False)),
            })

        return {
            "setCharacterFirstMessage": setCharacterFirstMessage,
            "getBackgroundEmbedding": getBackgroundEmbedding,
            "setBackgroundEmbedding": setBackgroundEmbedding,
            "reloadDisplay": reloadDisplay,
            "reloadChat": reloadChat,
            "getLoreBooksMain": getLoreBooksMain,
            "upsertLocalLoreBook": upsertLocalLoreBook,
            "getChatVar": getChatVar,
            "setChatVar": setChatVar,
            "getGlobalVar": getGlobalVar,
            "stopChat": stopChat,
            "alertNormal": alertNormal,
            "alertError": alertError,
            "getChatLength": getChatLength,
            "getChatMain": getChatMain,
            "getFullChatMain": getFullChatMain,
            "setFullChatMain": setFullChatMain,
            "setChat": setChat,
            "setChatRole": setChatRole,
            "cutChat": cutChat,
            "removeChat": removeChat,
            "addChat": addChat,
            "insertChat": insertChat,
            "logMain": logMain,
            "getName": getName,
            "setName": setName,
            "getDescription": getDescription,
            "setDescription": setDescription,
            "getCharacterFirstMessage": getCharacterFirstMessage,
            "getPersonaName": getPersonaName,
            "getPersonaDescription": getPersonaDescription,
            "getAuthorsNote": getAuthorsNote,
            "getCharacterLastMessage": getCharacterLastMessage,
            "getUserLastMessage": getUserLastMessage,
            "cbs": cbs,
        }

    # ------------------------------------------------------------------ #
    # Host API - async functions (exposed as __mock_<name>, wrapped in Lua)
    # ------------------------------------------------------------------ #
    def _async_mocks(self) -> Dict[str, Any]:
        s = self.state

        def _llm(id_, prompt_json, kind):
            if id_ not in self._lowlevel:
                return None  # -> Promise.resolve(nil); script errors, as in Risu
            s.llm_calls.append({"kind": kind, "prompt": _json.loads(prompt_json)})
            resp = s.mock_llm
            if callable(resp):
                resp = resp(prompt_json, kind)
            return _json.dumps(resp)

        def LLMMain(id_, prompt_json, use_mm=False, opts_json=""):
            return _llm(id_, prompt_json, "model")

        def axLLMMain(id_, prompt_json, use_mm=False, opts_json=""):
            return _llm(id_, prompt_json, "otherAx")

        def simpleLLM(id_, prompt):
            if id_ not in self._lowlevel:
                return None
            return s.mock_llm if not callable(s.mock_llm) else s.mock_llm(prompt, "simple")

        def sleep(id_, ms):
            return True  # no real delay in the emulator

        def getTokens(id_, value):
            # Cheap deterministic stand-in for the real tokenizer.
            return len(str(value).split())

        def alertInput(id_, value):
            if not self._is_safe(id_):
                return None
            s.alerts.append({"type": "input", "value": value})
            return s.input_responses.pop(0) if s.input_responses else ""

        def alertConfirm(id_, value):
            if not self._is_safe(id_):
                return None
            s.alerts.append({"type": "confirm", "value": value})
            return s.confirm_responses.pop(0) if s.confirm_responses else False

        def alertSelect(id_, values):
            if not self._is_safe(id_):
                return None
            opts = _lua_to_list(values)
            s.alerts.append({"type": "select", "value": opts})
            return s.select_responses.pop(0) if s.select_responses else 0

        def similarity(id_, source, values):
            if id_ not in self._lowlevel:
                return None
            vals = _lua_to_list(values)
            if callable(s.mock_similarity):
                result = list(s.mock_similarity(source, vals))
            elif s.mock_similarity is not None:
                result = list(s.mock_similarity)
            else:
                result = vals  # echo input when no mock configured
            return self.lua.table_from(result)

        def request(id_, url):
            if id_ not in self._lowlevel:
                return None
            s.request_calls.append(url)
            if len(url) > 120:
                return _json.dumps({"status": 413, "data": "URL to large. max is 120 characters"})
            if not url.startswith("https://"):
                return _json.dumps({"status": 400, "data": "Only https requests are allowed"})
            for burl in ("https://realm.risuai.net", "https://risuai.net", "https://risuai.xyz"):
                if url.startswith(burl):
                    return _json.dumps({"status": 400, "data": "request to " + url + " is not allowed"})
            mock = s.mock_http
            if callable(mock):
                resp = mock(url)
            elif isinstance(mock, dict) and "status" in mock:
                resp = mock  # flat default applied to every URL
            elif isinstance(mock, dict):
                resp = mock.get(url, {"status": 404, "data": ""})  # url -> response map
            else:
                resp = {"status": 200, "data": mock}
            return _json.dumps(resp)

        def generateImage(id_, value, neg_value=""):
            if id_ not in self._lowlevel:
                return None
            s.image_calls.append({"prompt": value, "negative": neg_value})
            return s.mock_image

        def getCharacterImageMain(id_):
            return s.char_image_inlay

        def getPersonaImageMain(id_):
            return s.persona_image_inlay

        def hash_(id_, value):
            return hashlib.sha256(str(value).encode("utf-8")).hexdigest()

        def loadLoreBooksMain(id_, reserve):
            if id_ not in self._lowlevel:
                return None
            return _json.dumps(list(s.mock_loaded_lorebooks))

        return {
            "LLMMain": LLMMain,
            "axLLMMain": axLLMMain,
            "simpleLLM": simpleLLM,
            "sleep": sleep,
            "getTokens": getTokens,
            "alertInput": alertInput,
            "alertConfirm": alertConfirm,
            "alertSelect": alertSelect,
            "similarity": similarity,
            "request": request,
            "generateImage": generateImage,
            "getCharacterImageMain": getCharacterImageMain,
            "getPersonaImageMain": getPersonaImageMain,
            "hash": hash_,
            "loadLoreBooksMain": loadLoreBooksMain,
        }
