# CBS: `{{setvar::name::value}}`

- Layer: CBS function
- Category: variables
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`setvar`)

Sets a persistent chat variable.

## Syntax

```text
{{setvar::name::value}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The chat-variable name to write. |
| 2 | `value` | yes | The value to store. |

## Behavior

Writes `value` to the chat variable `name`. Chat variables are saved with the
chat and persist between sessions, the same store
[`{{getvar}}`](getvar.md) reads and Lua reaches with
[`setChatVar`](../../api/setChatVar.md).

The write only takes effect when the parser runs with `runVar` enabled. When
`runVar` is off the function returns `null` (no replacement and no write); when
the parser runs in `rmVar` mode the call is stripped to an empty string without
writing. On a successful write it returns an empty string, so it emits nothing
into the rendered text.

## Example

```text
{{setvar::hp::100}}
```

sets `hp` to `100` (when `runVar` is on) and renders nothing.

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{getvar}}`](getvar.md), [`{{addvar}}`](addvar.md), [`{{setdefaultvar}}`](setdefaultvar.md)
- Lua equivalent: [`setChatVar`](../../api/setChatVar.md)
