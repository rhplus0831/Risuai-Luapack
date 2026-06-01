# CBS: `{{getglobalvar::name}}`

- **Layer:** CBS function
- **Category:** variables
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`getglobalvar`)

Reads a global chat variable, shared across all chats and characters.

## Syntax

```text
{{getglobalvar::name}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The global-variable name to read. |

## Behavior

Looks up the global chat variable `name` and returns its value as a string.
Global variables are shared across every chat and character, unlike the
per-chat store read by [`{{getvar}}`](getvar.md). This is the same value Lua
reads with [`getGlobalVar`](../../api/getGlobalVar.md). If `name` is not set, the
function returns an empty string.

`{{getglobalvar}}` only **reads**; there is no CBS counterpart that writes a
global variable.

## Example

```text
Theme: {{getglobalvar::ui_theme}}
```

## See also

- Element: [Global variables](../../element/global-variables.md)
- CBS: [`{{getvar}}`](getvar.md), [`{{tempvar}}`](tempvar.md)
- Lua equivalent: [`getGlobalVar`](../../api/getGlobalVar.md)
