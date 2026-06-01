# CBS: `{{setdefaultvar::name::value}}`

- Layer: CBS function
- Category: variables
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`setdefaultvar`)

Sets a chat variable only if it is not already set.

## Syntax

```text
{{setdefaultvar::name::value}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The chat-variable name to initialize. |
| 2 | `value` | yes | The default value to store when unset. |

## Behavior

Writes `value` to the chat variable `name` only when the variable does not
already have a value (the existing value is falsy: unset or empty). If `name`
already holds a non-empty value, nothing is written and the existing value is
kept. This makes it the idiomatic way to seed a default once.

Like [`{{setvar}}`](setvar.md), the write only takes effect when the parser
runs with `runVar` enabled. With `runVar` off the function returns `null` (no
write); in `rmVar` mode it is stripped to an empty string. On a successful pass
it returns an empty string and emits nothing.

## Example

```text
{{setdefaultvar::hp::100}}{{getvar::hp}}
```

sets `hp` to `100` only the first time, then renders the current value.

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{setvar}}`](setvar.md), [`{{addvar}}`](addvar.md), [`{{getvar}}`](getvar.md)
