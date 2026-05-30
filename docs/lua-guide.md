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
function onStart(id)    -- before the model request is sent
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
  `editDisplay` runs in a restricted tier (see below).
- Custom functions are called when Risu runs Lua with a custom mode. This is
  how manual trigger buttons commonly reach functions such as `OpenMenu(id)`.

You may register multiple `listenEdit` handlers for the same type. They run in
registration order, each receiving the previous handler's return value. Keep the
shape the same: strings for `editInput`, `editOutput`, and `editDisplay`;
OpenAI-style `{role, content}` message arrays for `editRequest`. If an edit
listener errors, Risu catches it and leaves the original content unchanged.

Full mode table: [lua-api.md#entry-points](./lua-api.md#entry-points).

## Chat buttons

Risu chat text is rendered as sanitized HTML. To put a clickable button in a
message, insert a normal HTML `<button>` tag into the chat text. Risu listens
for two button attributes:

- `risu-trigger="TriggerName"` runs a normal Risu manual trigger by name. Lua
  trigger scripts are also run with mode set to `TriggerName`, so a global
  function with the same name can handle the click.
- `risu-btn="payload"` runs Lua button scripts in `onButtonClick(id, data)`;
  `data` is the attribute value.
- `risu-id="some-id"` is passed to CBS as `{{trigger_id}}` for a
  `risu-trigger` click. It is not passed as the Lua `id`; the Lua `id` is still
  the access key.

Use `class="button-default"` if you want the built-in Risu button styling. Risu
prefixes chat CSS classes internally, so this becomes the styled
`x-risu-button-default` class at display time.

Buttons only fire in non-group chats. If an element has both `risu-trigger` and
`risu-btn`, `risu-trigger` wins and `onButtonClick` is not called.

There are two common Lua patterns:

- Use `risu-btn` when every button should enter one central
  `onButtonClick(id, data)` handler and dispatch on the payload.
- Use `risu-trigger` when the button should run a named manual trigger. Risu
  also gives every Lua trigger script a chance to handle that same name as a
  custom mode. This is the pattern used by scripts that define handlers such as
  `btnToggleVN(id)` and render a button with `risu-trigger="btnToggleVN"`.

```lua
function onStart(id)
    addChat(id, 'char',
        'Choose: <button class="button-default" risu-btn="inspect">Inspect</button>')
end

function onButtonClick(id, data)
    if data == 'inspect' then
        addChat(id, 'char', 'You clicked Inspect.')
    end
end
```

To run a named manual trigger instead, use `risu-trigger`:

```lua
addChat(id, 'char',
    '<button class="button-default" risu-trigger="OpenMenu">Open menu</button>')
```

For the global-function style, the trigger name and function name must match:

```lua
function btnToggleVN(id)
    local mode = getChatVar(id, 'uiVnMode')
    setChatVar(id, 'uiVnMode', mode == 'ON' and 'OFF' or 'ON')
    reloadDisplay(id)
end

-- Render this in chat/display HTML:
-- <button class="button-default" risu-trigger="btnToggleVN">VN</button>
```

Risu's CBS `{{button::Text::TriggerName}}` helper emits this same
`risu-trigger` HTML.

## The `id` access key (the #1 gotcha)

Most host calls take an opaque `id` as their **first argument** — the access key
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

The main exceptions are helpers that do not use the access key: `log(value)`,
raw `logMain(value)`, and `cbs(value)`.

## Permission tiers

The `id` belongs to one of three tiers; host functions check it:

| Tier | Granted to | Can do |
|------|-----------|--------|
| **Always** | every script | reads (`getChatVar`, `getName`, …) |
| **Safe** | normal triggers and edit listeners except `editDisplay` | modify chat/character (`addChat`, `setName`, …) |
| **Edit-display** | `editDisplay` listeners | chat-var writes only, no chat mutation |
| **Low-level** | scripts with `lowLevelAccess` | `LLM`, `request`, `similarity`, `generateImage`, … |

**Low-level** functions (anything that hits the network/model) only work if the
character/trigger has `lowLevelAccess` enabled in Risu. Declare it in your
`luapack.toml` (`low_level_access = true`) as a reminder — and remember to flip
it on in Risu itself. In tests, grant it per call:
`emu.run_mode('output', low_level=True)`.

Edit listeners never receive low-level access in Risu, even if the character or
module has `lowLevelAccess` enabled. Use normal/manual/output handlers for LLM,
network, image, similarity, and lore-loading calls.

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

## CBS from Lua

Use `cbs("Hello, {{user}}")` to expand a CBS template string from Lua. It runs
Risu's chat parser in the current character context.

CBS names are forgiving: they are lowercased and spaces, underscores, and
hyphens are ignored, so `{{trigger_id}}` and `{{triggerid}}` resolve to the same
function. Arguments normally split on `::`; single `:` also works when there is
no `::` in the call. Unknown CBS functions are preserved literally, and
recursive CBS expansion stops at 20 nested calls.

Two shorthands are worth knowing:

```text
{{? 2 + 2 * 3}}        -> calculator expression
<user>, <char>, <bot>  -> rewritten as {{user}}, {{char}}, {{bot}}
```

Lua `cbs()` is for expansion, not side effects. Variable-writing CBS functions
such as `{{setvar}}` and `{{addvar}}` require Risu's parser to run with
`runVar=true`, and the Lua helper does not pass that flag.

## Async / `await`

Risu's VM injects a `Promise`. Functions that hit the model/network/disk return
a promise you must `:await()`:

```lua
local res = LLMMain(id, json.encode(prompt), false, '{}'):await()
```

In practice, **use the helpers**. `LLM`, `axLLM`, and `loadLoreBooks` await and
JSON-decode for you:

```lua
local out = LLM(id, { { role = 'user', content = 'Summarise.' } })
-- out = { success = true, result = '...' }
```

`getCharacterImage` and `getPersonaImage` await for you and return raw
`{{inlayed::...}}` strings (or an empty string), not JSON.

Functions tagged _(await)_ in the reference are the promise-returning ones.

`LLM` and `axLLM` expect an array of `{ role, content }` tables. Risu maps
`system`/`sys` to system, `user` to user, and `assistant`/`bot`/`char` to the
assistant role. Pass `true` as the third argument to enable multimodal inlay
extraction; pass `{ streaming = true }` as the fourth argument to force
streaming and receive the collected final text.

`simpleLLM(id, prompt):await()` is the raw host shortcut for a one-message user
prompt and returns a result object directly. `request(id, url):await()` returns
a JSON string, so decode it with `json.decode`.

## Reserved globals — don't shadow these

The preamble already defines these; redefining them breaks your script:
`json`, `log`, `getState`, `setState`, `getChat`, `getFullChat`, `setFullChat`,
`getLoreBooks`, `loadLoreBooks`, `LLM`, `axLLM`, `getCharacterImage`,
`getPersonaImage`, `listenEdit`, `async`, plus every host function in the
reference. Your own handler names (`onStart`, `onOutput`, …) are expected to be
global — that's how Risu finds them.

## Other gotchas

- **Chat indices are 0-based.** `getChat(id, 0)` is the first message — they map
  straight to a JS array, unusual for Lua. Negative indices follow
  JavaScript's `Array.at`: `getChat(id, -1)` reads the last message.
- **Chat mutation uses JavaScript array semantics.** `cutChat(start, end)` keeps
  `[start, end)`, while `insertChat` and `removeChat` use JS `splice`. Message
  roles are only `user` or `char`; any other role passed to `addChat`,
  `insertChat`, or `setChatRole` becomes `char`.
- **`request` is restricted:** HTTPS only, URL ≤ 120 chars, Risu's current code
  allows 6 calls/minute before returning 429, and some hosts are banned. It
  returns a JSON string `{status, data}` — decode it. The luapack emulator
  models the URL/host restrictions but not the rate limit.
- **Edit listeners must return a value.** Forgetting `return` blanks the text.
- **There is no Lua `editprocess` listener.** Risu's regex/script pipeline has
  an `editprocess` mode, but Lua edit hooks only map `editinput`, `editoutput`,
  and `editdisplay` to `editInput`, `editOutput`, and `editDisplay`; the model
  request array hook is `editRequest`.
- **Edit listener `meta` carries context when Risu has it.** For the regex
  pipeline this includes `index`, the chat message index being processed.

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

Good pack tests usually cover the paths Risu makes easy to miss: button payloads
and manual trigger names, low-level APIs both allowed and denied, `editRequest`
array transforms, `editDisplay` restrictions, CBS expansion, and edge chat
indices such as `0` and `-1`.

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
- **CBS** — function names inside Lua string literals are checked for known CBS
  names (`{{getvarr}}` → did you mean `{{getvar}}`). Lua strings are often
  concatenated CBS fragments, so full brace/balance validation is reserved for
  complete strings passed to `check-cbs`.

Errors fail the command; likely-but-not-certain issues are warnings (use
`--strict` to fail on those too). The API and CBS name lists come from the
pinned Risu sources, so the lint tracks Risu like the docs do.
