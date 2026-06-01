# Element: Chat variables (per-chat string state)

- Kind: Element (data structure)
- Source: `Refer/Risuai/src/ts/parser/chatVar.svelte.ts` (`getChatVar`, `setChatVar`), `Refer/Risuai/src/ts/process/scriptings.ts` (`getChatVar`/`setChatVar` declarations, `getState`/`setState` wrappers)

Persistent per-chat string variables, stored on the current chat and read with
a defined fallback chain.

## What it is

A chat variable is a named string saved on the current chat under
`chat.scriptstate['$' + key]`. Variables persist with the chat between sessions
and are scoped to that one chat (a different chat, or the same character's other
chat page, has its own `scriptstate`). All values are stored and returned as
strings.

Lua reads and writes them with [`getChatVar`](../api/getChatVar.md) and
[`setChatVar`](../api/setChatVar.md); CBS reads them with
[`{{getvar}}`](../cbs/variables/getvar.md).

## Read fallback order

`getChatVar(id, key)` resolves a value in this order, returning the first hit:

1. `chat.scriptstate['$' + key]` — the live per-chat value.
2. The selected character's `defaultVariables` (parsed key/value list).
3. The database `templateDefaultVariables` (parsed key/value list).
4. The literal string `"null"` when nothing matches.

So an *unset* chat variable reads back as the string `"null"` in Lua — not
`nil`, not `""`. (CBS `{{getvar}}` differs: an unset variable expands to an empty
string there.) Steps 2 and 3 are concatenated, so character defaults take
precedence over template defaults.

## Write

`setChatVar(id, key, value)` writes `value` to `chat.scriptstate['$' + key]`,
creating `scriptstate` if needed. It is the only chat-data mutation allowed
in the restricted `editDisplay` tier: its guard accepts a key in either
`ScriptingSafeIds` or `ScriptingEditDisplayIds`, where every other mutator
requires `ScriptingSafeIds` only. (Reads via `getChatVar` carry no guard.)

## The `getState` / `setState` helpers

For structured data, the Lua wrapper provides JSON helpers:

```lua
setState(id, name, value)   -- setChatVar(id, '__'..name, json.encode(value))
local v = getState(id, name) -- json.decode(getChatVar(id, '__'..name))
```

They prefix the variable name with `__` and JSON-encode/decode around the
string store, so you can keep tables, arrays, counters, and UI state. A
`getState` on an unset name decodes the fallback string `"null"` — i.e. JSON
`null` — yielding Lua `nil`.

## Shape / fields

| Concept | Storage key | Type |
|---------|-------------|------|
| plain chat variable `key` | `chat.scriptstate['$' .. key]` | string |
| `setState`/`getState` name | `chat.scriptstate['$__' .. name]` | JSON string |

## Used by

- APIs: [`getChatVar`](../api/getChatVar.md), [`setChatVar`](../api/setChatVar.md),
  and the `getState`/`setState` wrappers documented in
  [`setChatVar`](../api/setChatVar.md)
- CBS: [`{{getvar}}`](../cbs/variables/getvar.md),
  [`{{setvar}}`](../cbs/variables/setvar.md)
- Hooks: writable from any handler, including [`editDisplay`](../hooks/editDisplay.md)
  (the only chat write that tier permits)

## See also

- Elements: [Global variables](global-variables.md),
  [Access key & tiers](access-key.md)
- Index: [`docs/README.md`](../README.md)
