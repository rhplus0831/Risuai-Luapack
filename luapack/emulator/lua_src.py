"""Lua source fragments used to reconstruct Risu's Lua environment under lupa.

Three pieces are assembled around the user's bundle, in order:

1. ``PRELUDE``    - ambient globals that *wasmoon* injects but lupa does not
                    (``Promise``, ``throw``) plus the ``json`` module preload and
                    Lua wrappers for the async host functions.
2. ``WRAPPER``    - a byte-faithful copy of ``luaCodeWrapper`` from Risu's
                    ``src/ts/process/scriptings.ts``. The user bundle is spliced
                    in where ``USERCODE_SENTINEL`` sits.
3. ``DISPATCHER`` - mirrors the ``switch(mode)`` entry-point dispatch in
                    ``runScripted`` so Python can drive a single mode call.

The WRAPPER must stay in sync with Risu's source; the emulator-coverage test
(``tests/test_api_coverage.py``) diffs it against the vendored ``scriptings.ts``.
"""

# --- async host functions -------------------------------------------------
# Every Risu host function declared with `async` in scriptings.ts returns a JS
# Promise under wasmoon, which Lua code `:await()`s. lupa host callables return
# values synchronously, so we expose the Python mock as `__mock_<name>` and wrap
# it in a Lua function that returns `Promise.resolve(...)`, restoring `:await()`.
ASYNC_HOST_NAMES = [
    "getTokens",
    "sleep",
    "similarity",
    "request",
    "generateImage",
    "getCharacterImageMain",
    "getPersonaImageMain",
    "hash",
    "LLMMain",
    "simpleLLM",
    "axLLMMain",
    "loadLoreBooksMain",
    "alertInput",
    "alertSelect",
    "alertConfirm",
]

USERCODE_SENTINEL = "--[[ __LUAPACK_USERCODE__ ]]"

# Built from ASYNC_HOST_NAMES at module load (kept as a literal list in Lua).
_ASYNC_NAMES_LUA = "{ " + ", ".join("'%s'" % n for n in ASYNC_HOST_NAMES) + " }"

PRELUDE = (
    """
-- luapack emulator prelude -------------------------------------------------
-- Reproduce the ambient globals that wasmoon injects into Risu's Lua VM.

-- `throw` is used by luaCodeWrapper but is not standard Lua; wasmoon provides
-- it. `error` with level 2 is a faithful-enough stand-in for the emulator.
function throw(msg)
    error(msg, 2)
end

-- Minimal synchronous Promise that matches the surface luaCodeWrapper uses:
--   Promise.create(executor) / Promise.resolve(v) / p:await() / p:finally(fn)
-- Because every host mock resolves synchronously, settle happens inline; the
-- coroutine dance inside `async()` therefore completes without real suspension.
Promise = {}
Promise.__index = Promise

function Promise.create(executor)
    local self = setmetatable({ _state = 'pending', _value = nil, _cbs = {} }, Promise)
    local function settle(state, v)
        if self._state ~= 'pending' then
            return
        end
        self._state = state
        self._value = v
        local cbs = self._cbs
        self._cbs = {}
        for _, f in ipairs(cbs) do
            f()
        end
    end
    local resolve = function(v) settle('fulfilled', v) end
    local reject = function(v) settle('rejected', v) end
    local ok, err = pcall(executor, resolve, reject)
    if not ok then
        reject(err)
    end
    return self
end

function Promise.resolve(v)
    -- Identity for existing promises: luaCodeWrapper relies on
    -- `result == Promise.resolve(result)` to detect a thenable.
    if type(v) == 'table' and getmetatable(v) == Promise then
        return v
    end
    return Promise.create(function(res) res(v) end)
end

function Promise.reject(v)
    return Promise.create(function(_, rej) rej(v) end)
end

function Promise:finally(fn)
    if self._state == 'pending' then
        self._cbs[#self._cbs + 1] = fn
    else
        fn()
    end
    return self
end

function Promise:await()
    if self._state == 'pending' then
        error('luapack: await() on a pending Promise -- the emulator requires synchronous mocks')
    end
    if self._state == 'rejected' then
        error(self._value)
    end
    return self._value
end

-- `json` is mounted by Risu via LuaFactory.mountFile; we preload the identical
-- module so `require 'json'` inside luaCodeWrapper resolves the same way.
package.preload['json'] = __json_chunk

-- Wrap each async host function so Lua `:await()` keeps working.
local __async_names = """
    + _ASYNC_NAMES_LUA
    + """
for _, name in ipairs(__async_names) do
    _G[name] = function(...)
        local mock = _G['__mock_' .. name]
        if mock == nil then
            return Promise.resolve(nil)
        end
        return Promise.resolve(mock(...))
    end
end
"""
)

# --- WRAPPER: verbatim from scriptings.ts luaCodeWrapper -------------------
# The WRAPPER string below is a verbatim copy of `luaCodeWrapper` from RisuAI
# (src/ts/process/scriptings.ts), Copyright (C) Kwaroran, licensed GPLv3.
# Source: https://github.com/kwaroran/RisuAI  (see NOTICE).
# Keep in sync with vendor/scriptings.ts, pinned at vendored.RISU_REF.
WRAPPER = (
    """
json = require 'json'

function getChat(id, index)
    return json.decode(getChatMain(id, index))
end

function getFullChat(id)
    return json.decode(getFullChatMain(id))
end

function setFullChat(id, value)
    setFullChatMain(id, json.encode(value))
end

function log(value)
    logMain(json.encode(value))
end

function getLoreBooks(id, search)
    return json.decode(getLoreBooksMain(id, search))
end


function loadLoreBooks(id)
    return json.decode(loadLoreBooksMain(id):await())
end

function LLM(id, prompt, useMultimodal, options)
    useMultimodal = useMultimodal or false
    options = options or {}
    return json.decode(LLMMain(id, json.encode(prompt), useMultimodal, json.encode(options)):await())
end

function axLLM(id, prompt, useMultimodal, options)
    useMultimodal = useMultimodal or false
    options = options or {}
    return json.decode(axLLMMain(id, json.encode(prompt), useMultimodal, json.encode(options)):await())
end

function getCharacterImage(id)
    return getCharacterImageMain(id):await()
end

function getPersonaImage(id)
    return getPersonaImageMain(id):await()
end

local editRequestFuncs = {}
local editDisplayFuncs = {}
local editInputFuncs = {}
local editOutputFuncs = {}

function listenEdit(type, func)
    if type == 'editRequest' then
        editRequestFuncs[#editRequestFuncs + 1] = func
        return
    end

    if type == 'editDisplay' then
        editDisplayFuncs[#editDisplayFuncs + 1] = func
        return
    end

    if type == 'editInput' then
        editInputFuncs[#editInputFuncs + 1] = func
        return
    end

    if type == 'editOutput' then
        editOutputFuncs[#editOutputFuncs + 1] = func
        return
    end

    throw('Invalid type')
end

function getState(id, name)
    local escapedName = "__"..name
    return json.decode(getChatVar(id, escapedName))
end

function setState(id, name, value)
    local escapedName = "__"..name
    setChatVar(id, escapedName, json.encode(value))
end

function async(callback)
    return function(...)
        local co = coroutine.create(callback)
        local safe, result = coroutine.resume(co, ...)

        return Promise.create(function(resolve, reject)
            local checkresult
            local step = function()
                if coroutine.status(co) == "dead" then
                    local send = safe and resolve or reject
                    return send(result)
                end

                safe, result = coroutine.resume(co)
                checkresult()
            end

            checkresult = function()
                if safe and result == Promise.resolve(result) then
                    result:finally(step)
                else
                    step()
                end
            end

            checkresult()
        end)
    end
end

callListenMain = async(function(type, id, value, meta)
    local realValue = json.decode(value)
    local realMeta = json.decode(meta)

    if type == 'editRequest' then
        for _, func in ipairs(editRequestFuncs) do
            realValue = func(id, realValue, realMeta)
        end
    end

    if type == 'editDisplay' then
        for _, func in ipairs(editDisplayFuncs) do
            realValue = func(id, realValue, realMeta)
        end
    end

    if type == 'editInput' then
        for _, func in ipairs(editInputFuncs) do
            realValue = func(id, realValue, realMeta)
        end
    end

    if type == 'editOutput' then
        for _, func in ipairs(editOutputFuncs) do
            realValue = func(id, realValue, realMeta)
        end
    end

    return json.encode(realValue)
end)

"""
    + USERCODE_SENTINEL
    + "\n"
)

# --- DISPATCHER: mirrors runScripted's switch(mode) -----------------------
DISPATCHER = """
-- Drives a single entry-point call, mirroring runScripted in scriptings.ts.
-- Edit modes return a JSON string (caller json.loads it); other modes return
-- the handler's raw value (false => stopSending).
function __luapack_dispatch(mode, id, data, meta)
    if mode == 'input' then
        if onInput ~= nil then return onInput(id) end
    elseif mode == 'output' then
        if onOutput ~= nil then return onOutput(id) end
    elseif mode == 'start' then
        if onStart ~= nil then return onStart(id) end
    elseif mode == 'onButtonClick' then
        if onButtonClick ~= nil then return onButtonClick(id, data) end
    elseif mode == 'editRequest' or mode == 'editDisplay'
        or mode == 'editInput' or mode == 'editOutput' then
        local r = callListenMain(mode, id, data, meta)
        if type(r) == 'table' and r.await ~= nil then
            return r:await()
        end
        return r
    else
        local f = _G[mode]
        if f ~= nil then return f(id) end
    end
    return nil
end
"""


def build_wrapped(bundle: str) -> str:
    """Splice a user bundle into the Risu wrapper (no prelude/dispatcher)."""
    return WRAPPER.replace(USERCODE_SENTINEL, bundle)
