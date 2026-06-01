# Element: Prompt toggles (`toggle_` globals)

- **Kind:** Element (data structure)
- **Source:** `Refer/Risuai/src/ts/util.ts` (`parseToggleSyntax`, `sidebarToggle`), `Refer/Risuai/src/lib/SideBars/Toggles.svelte` (sidebar UI + stored value format), `Refer/Risuai/src/ts/process/modules.ts` (`getModuleToggles`)

User-facing sidebar controls whose state is stored as `toggle_`-prefixed global
variables, readable from Lua.

## What it is

A prompt toggle is a sidebar control (checkbox, dropdown, text field) that
writes into [global variables](global-variables.md) under the key
`toggle_<key>`. Risu builds the sidebar from the concatenation of
`db.customPromptTemplateToggle` and every enabled module's `customModuleToggle`
text (`getModuleToggles()` joins them). Each non-blank line defines one row.

Lua reads a toggle's stored value with
`getGlobalVar(id, 'toggle_' .. key)` — there is no Lua setter (the user sets it
in the sidebar).

## Line syntax

Each line is split on `=` into `key=value=type=options`. The recognized forms:

| Line form | Control | Stored in `toggle_<key>` |
|-----------|---------|--------------------------|
| `key=Label` | checkbox | `"1"` (checked) or `"0"` (unchecked) |
| `key=Label=select=A,B,C` | dropdown | the **zero-based index** as a string (`"0"`, `"1"`, …) |
| `key=Label=text` | single-line text | the entered text |
| `key=Label=textarea` | multi-line text | the entered text |

Decorative rows create **no** stored variable (they only structure the sidebar).
They put the type marker in the third field, leaving `key` empty:

| Line form | Effect |
|-----------|--------|
| `=Section=group` … `==groupEnd` | starts / ends a collapsible group |
| `=Label=divider` | horizontal rule (optionally labelled) |
| `=Caption text=caption` | small caption text (requires a value) |

Notes verified against `parseToggleSyntax`:

- A checkbox line has no explicit type; it falls through to the default branch
  and stores its value only when both `key` and label are present.
- `select` options come from the comma-separated 4th field.
- `caption` rows are dropped unless they carry a value.

## Reading from Lua

```lua
-- key=Label  (checkbox)
if getGlobalVar(id, 'toggle_hardmode') == '1' then
    -- hard mode on
end

-- key=Label=select=Easy,Normal,Hard  (dropdown -> "0"/"1"/"2")
local idx = tonumber(getGlobalVar(id, 'toggle_difficulty')) or 0

-- key=Label=text
local nickname = getGlobalVar(id, 'toggle_nickname')
```

An unset toggle reads back as the string `"null"` (the global-variable fallback)
until the user first interacts with it, so test for `"1"` rather than assuming
`"0"`.

## Shape / fields

| Field | Source | Type |
|-------|--------|------|
| sidebar definition | `db.customPromptTemplateToggle` + module `customModuleToggle` | line-based text |
| stored value | `db.globalChatVariables['toggle_' .. key]` | string |

## Used by

- API: [`getGlobalVar`](../api/getGlobalVar.md)
- CBS: [`{{getglobalvar}}`](../cbs/variables/getglobalvar.md)

## See also

- Elements: [Global variables](global-variables.md), [Modules](modules.md)
- Index: [`docs/README.md`](../README.md)
