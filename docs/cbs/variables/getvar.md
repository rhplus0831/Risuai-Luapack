# CBS: `{{getvar::name}}`

- Layer: CBS function
- Category: variables
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`getvar`)

Returns the value of a persistent chat variable.

## Syntax

```text
{{getvar::name}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The chat-variable name to read. |

## Behavior

Looks up the chat variable `name` and returns its current value as a string. The
value is the same one Lua reads with [`getChatVar`](../../api/getChatVar.md):
Risu first checks the chat's `scriptstate`, then the character's
`defaultVariables`, then the template default variables. Unlike the Lua getter,
an unset CBS variable expands to an empty string here.

`{{getvar}}` only reads. Writing is done by [`{{setvar}}`](setvar.md),
[`{{addvar}}`](addvar.md), and [`{{setdefaultvar}}`](setdefaultvar.md), which
only take effect when the parser runs with `runVar` enabled.

## Example

```text
HP: {{getvar::hp}} / {{getvar::maxhp}}
```

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{setvar}}`](setvar.md), [`{{tempvar}}`](tempvar.md), [`{{getglobalvar}}`](getglobalvar.md)
- Lua equivalent: [`getChatVar`](../../api/getChatVar.md)
