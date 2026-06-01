# Element: Global variables (read-only from Lua)

- Kind: Element (data structure)
- Source: `Refer/Risuai/src/ts/parser/chatVar.svelte.ts` (`getGlobalChatVar`), `Refer/Risuai/src/ts/process/scriptings.ts` (`getGlobalVar` declaration)

Cross-chat string variables stored in the database, readable from Lua but not
writable.

## What it is

A global variable is a named string kept in `db.globalChatVariables[key]`.
Unlike [chat variables](chat-variables.md), globals are shared across all chats
and characters. Lua reads one with [`getGlobalVar`](../api/getGlobalVar.md):

```lua
local mode = getGlobalVar(id, 'difficulty')
```

`getGlobalChatVar(key)` returns `db.globalChatVariables[key]`, or the literal
string `"null"` when the key is absent. So an unset global reads back as the
string `"null"` in Lua (not `nil`, not `""`).

## No Lua setter

There is no Lua host API to write a global variable. Risu declares only
`getGlobalVar`; there is no `setGlobalVar`. Globals are written by the user
through Risu's UI (notably the prompt-toggle sidebar) and by CBS. If a Lua
script needs writable persistent state, use [chat variables](chat-variables.md)
(`setChatVar` / `setState`) instead.

## Prompt toggles live here

Risu's custom prompt toggles are global variables whose keys are prefixed
`toggle_`. A checkbox toggle named `hardmode` stores its state in
`db.globalChatVariables['toggle_hardmode']` (`"1"` or `"0"`), and Lua reads it
with `getGlobalVar(id, 'toggle_hardmode')`. See [Prompt toggles](prompt-toggles.md)
for the full toggle syntax and stored-value formats.

## Shape / fields

| Concept | Storage | Type | Lua access |
|---------|---------|------|------------|
| global variable `key` | `db.globalChatVariables[key]` | string | read only (`getGlobalVar`) |
| prompt toggle | `db.globalChatVariables['toggle_' .. key]` | string | read only |

## Used by

- API: [`getGlobalVar`](../api/getGlobalVar.md)
- CBS: [`{{getglobalvar}}`](../cbs/variables/getglobalvar.md)

## See also

- Elements: [Chat variables](chat-variables.md), [Prompt toggles](prompt-toggles.md)
- Index: [`docs/README.md`](../README.md)
