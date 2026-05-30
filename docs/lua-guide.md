# Risu Lua scripting guide

How Risu's Lua scripting actually works, and how to build/test a pack with
luapack. For the exhaustive function list see [lua-api.md](./lua-api.md).

## The model

Risu lets a character/trigger run Lua. You paste **one Lua string**; Risu wraps
it in a fixed preamble (`luaCodeWrapper`) that defines helpers (`json`, `LLM`,
`getState`, `listenEdit`, …) and injects ~50 host functions, then runs your code
at the bottom. Your script's job is to define **handlers** (`onStart`,
`onOutput`, edit listeners, …) that Risu calls at the right moment.

luapack reproduces that whole environment in Python (via `lupa`, Lua 5.4 — the
same version as Risu's wasmoon VM) so you can compile- and behavior-check a
script off-platform, and it bundles multiple `.lua` files into the single string
Risu wants.

## Entry points

Risu runs your script in a **mode** and calls the matching handler:

```lua
function onStart(id)    -- chat begins
    addChat(id, 'char', 'Hello!')
end

function onOutput(id)   -- model reply arrived
    -- return false to stop the message being sent
end

listenEdit('editOutput', function(id, value, meta)
    return value:gsub('badword', '****')   -- MUST return the new value
end)
```

- `onStart` / `onInput` / `onOutput` — return `false` to halt sending.
- `onButtonClick(id, data)` — a chat button was clicked; `data` is its payload.
- `listenEdit('editRequest'|'editInput'|'editOutput'|'editDisplay', fn)` — a
  transform: it **receives** the current value and **returns** the new one.
  `editDisplay` runs in a read-only tier (see below).

Full mode table: [lua-api.md#entry-points](./lua-api.md#entry-points).

## The `id` access key (the #1 gotcha)

Every host call takes an opaque `id` as its **first argument** — the access key
Risu passes to your handler. You must thread it through:

```lua
function onStart(id)
    local hp = getChatVar(id, 'hp')   -- correct: id first
    setChatVar(id, 'hp', '100')
end
```

The `id` is what carries your permission tier. Calling a host function with the
wrong/missing id silently no-ops (or errors). Always pass the `id` your handler
received.

## Permission tiers

The `id` belongs to one of three tiers; host functions check it:

| Tier | Granted to | Can do |
|------|-----------|--------|
| **Always** | every script | reads (`getChatVar`, `getName`, …) |
| **Safe** | normal triggers | modify chat/character (`addChat`, `setName`, …) |
| **Edit-display** | `editDisplay` listeners | chat-var writes only, no chat mutation |
| **Low-level** | scripts with `lowLevelAccess` | `LLM`, `request`, `similarity`, `generateImage`, … |

**Low-level** functions (anything that hits the network/model) only work if the
character/trigger has `lowLevelAccess` enabled in Risu. Declare it in your
`luapack.toml` (`low_level_access = true`) as a reminder — and remember to flip
it on in Risu itself. In tests, grant it per call:
`emu.run_mode('output', low_level=True)`.

## State: chat vars vs `getState`/`setState`

- `getChatVar(id, key)` / `setChatVar(id, key, value)` store **strings**.
- `getState(id, name)` / `setState(id, name, value)` store **any JSON value** —
  they `json.encode`/`json.decode` for you and prefix the key with `__`:

```lua
setState(id, 'inventory', { 'sword', 'shield' })   -- stored at __inventory
local items = getState(id, 'inventory')            -- back to a Lua table
```

`getState` on a name that was never set will error (it decodes an empty string),
so initialise before reading.

## Async / `await`

Risu's VM injects a `Promise`. Functions that hit the model/network/disk return
a promise you must `:await()`:

```lua
local res = LLMMain(id, json.encode(prompt), false, '{}'):await()
```

In practice, **use the helpers** — `LLM`, `axLLM`, `loadLoreBooks`,
`getCharacterImage` await and JSON-decode for you:

```lua
local out = LLM(id, { { role = 'user', content = 'Summarise.' } })
-- out = { success = true, result = '...' }
```

Functions tagged _(await)_ in the reference are the promise-returning ones.

## Reserved globals — don't shadow these

The preamble already defines these; redefining them breaks your script:
`json`, `log`, `getState`, `setState`, `getChat`, `getFullChat`, `setFullChat`,
`getLoreBooks`, `loadLoreBooks`, `LLM`, `axLLM`, `getCharacterImage`,
`getPersonaImage`, `listenEdit`, `async`, plus every host function in the
reference. Your own handler names (`onStart`, `onOutput`, …) are expected to be
global — that's how Risu finds them.

## Other gotchas

- **Chat indices are 0-based.** `getChat(id, 0)` is the first message — they map
  straight to a JS array, unusual for Lua.
- **`request` is restricted:** HTTPS only, URL ≤ 120 chars, 5 calls/minute,
  some hosts banned. It returns a JSON string `{status, data}` — decode it.
- **Edit listeners must return a value.** Forgetting `return` blanks the text.

## Multi-file packs

Split code into `src/*.lua` and pull modules in with `require`:

```lua
-- src/main.lua
local utils = require('utils')        -- resolves to src/utils.lua
function onStart(id) addChat(id, 'char', utils.greeting(getName(id))) end
```
```lua
-- src/utils.lua
local M = {}
function M.greeting(n) return 'Hello, ' .. n .. '!' end
return M
```

`python -m luapack build` amalgamates these into `dist/bundle.lua` — the single
string you paste into Risu. `require('utils')` resolves to the bundled module;
unknown names (like `'json'`) fall through to Risu's own `require`. Your entry
module runs last so its `function onStart` stays global.

## Testing

Write pytest tests; drive the emulator like Risu would.

```python
from luapack.testing import load, load_pack

def test_inline():
    emu = load("function onStart(id) setChatVar(id,'x','1') end")
    emu.run_mode("start")
    assert emu.state.chat_vars["x"] == "1"

def test_a_pack():
    emu = load_pack("packs/example", char_name="Rika")
    out = emu.run_mode("editOutput", data="hi")
    assert out["res"] == "[hi]"
```

Seed state with kwargs (`char_name=`, …) or a `RisuState`. Mock the external
calls (`state.mock_llm`, `state.mock_http`, `state.input_responses`, …) and read
back what happened (`state.messages`, `state.chat_vars`, `state.llm_calls`,
`state.alerts`). `run_mode` returns `{res, stop, error, chat}`.

Scaffold a fresh pack with `python -m luapack new <dir>`.

## CLI summary

```
python -m luapack new   <dir>      scaffold a pack
python -m luapack check [dir]      validate: Lua compile + name lint + CBS syntax
python -m luapack check-cbs "..."  validate a single CBS template string
python -m luapack build [dir]      src/*.lua -> dist/bundle.lua (+ syntax check)
python -m luapack test  [dir]      run the pack's pytest tests
python -m luapack docs             regenerate docs/lua-api.md from Risu source
python -m luapack sync-source      refresh vendored Risu sources (pinned)
```

## Static validation (`check`)

`luapack check` is fast, static, and runs no behavior. It reports:

- **Lua syntax** — per file, with line numbers.
- **Name typos** — calls to host APIs that are one edit away from a real name
  (`setChatVarr` → `setChatVar`), misspelled/miscased handlers (`onOuput`,
  `onstart` — which silently never fire), invalid `listenEdit` types, and
  shadowing of reserved globals (`function json(...)`).
- **CBS** — every `{{...}}` in a string literal is checked for balanced/nested
  braces and known function names (`{{getvarr}}` → did you mean `{{getvar}}`).

Errors fail the command; likely-but-not-certain issues are warnings (use
`--strict` to fail on those too). The API and CBS name lists come from the
pinned Risu sources, so the lint tracks Risu like the docs do.
