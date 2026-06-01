# CBS: `{{user}}`

- Layer: CBS function
- Category: identity
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`user`)

Returns the active user/persona name.

## Syntax

```text
{{user}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the current user's name as set in user/persona settings (Risu's
`getUserName()`). In consistent-character mode (tokenization/consistency passes)
it returns the literal `"username"` instead.

The result is the raw name string and is not further CBS-parsed.

## Example

```text
Hello {{user}}, I'm {{char}}.
```

## See also

- CBS: [`{{char}}`](char.md), [`{{persona}}`](../prompts/persona.md)
- Lua equivalent: [`getPersonaName`](../../api/getPersonaName.md)
