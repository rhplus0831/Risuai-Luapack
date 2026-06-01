# CBS: `{{settempvar::name::value}}`

- Layer: CBS function
- Category: variables
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`settempvar`)

Sets a temporary variable that lives only during the current parse.

## Syntax

```text
{{settempvar::name::value}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The temporary-variable name to write. |
| 2 | `value` | yes | The value to store. |

## Behavior

Stores `value` under `name` in the parse-local variable table and always
returns an empty string, so the function emits nothing into the rendered text.
The table is created fresh each parse and discarded when the parse finishes, so
the value never persists between sends or across separate template strings.

Unlike [`{{setvar}}`](setvar.md), this write is unconditional: it does not depend
on `runVar` and is not saved to the chat. Read it back with
[`{{tempvar}}`](tempvar.md).

## Example

```text
{{settempvar::count::3}}You have {{tempvar::count}} items.
```

renders `You have 3 items.`

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{tempvar}}`](tempvar.md), [`{{setvar}}`](setvar.md)
