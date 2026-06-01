# CBS: `{{description}}`

- Layer: CBS function
- Category: identity
- Aliases: `chardesc`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`description`)

Returns the current character's description field.

## Syntax

```text
{{description}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the `desc` (description) field of the active character (the one passed in
the matcher argument, otherwise the selected character) and returns it after
running it through Risu's chat parser, so any CBS templates inside the
description are expanded. For a group chat the character has type `group` and
this returns an empty string.

## Example

```text
Description: {{description}}
```

## See also

- CBS: [`{{personality}}`](personality.md), [`{{scenario}}`](scenario.md)
- Lua equivalent: [`getDescription`](../../api/getDescription.md)
