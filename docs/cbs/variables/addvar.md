# CBS: `{{addvar::name::amount}}`

- Layer: CBS function
- Category: variables
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`addvar`)

Adds a number to a persistent chat variable.

## Syntax

```text
{{addvar::name::amount}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The chat-variable name to update. |
| 2 | `amount` | yes | The number to add to the current value. |

## Behavior

Reads the chat variable `name`, coerces both the stored value and `amount` to
numbers, adds them, and saves the sum back as a string. Because the current
value is read with `Number(...)`, an unset or non-numeric variable counts as
the JavaScript number it coerces to (e.g. unset reads as empty and becomes `0`).

Like [`{{setvar}}`](setvar.md), the write only takes effect when the parser
runs with `runVar` enabled. With `runVar` off the function returns `null` (no
write); in `rmVar` mode it is stripped to an empty string. On a successful write
it returns an empty string and emits nothing.

## Example

```text
{{setvar::counter::0}}{{addvar::counter::5}}{{getvar::counter}}
```

renders `5` (when `runVar` is on).

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{setvar}}`](setvar.md), [`{{getvar}}`](getvar.md), [`{{setdefaultvar}}`](setdefaultvar.md)
