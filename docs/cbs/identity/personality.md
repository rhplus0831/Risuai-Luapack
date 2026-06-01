# CBS: `{{personality}}`

- Layer: CBS function
- Category: identity
- Aliases: `charpersona`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`personality`)

Returns the current character's personality field.

## Syntax

```text
{{personality}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the `personality` field of the active character (the one passed in the
matcher argument, otherwise the selected character) and returns it after running
it through Risu's chat parser, so any CBS templates inside the personality text
are expanded. For a group chat the character has type `group` and this
returns an empty string.

## Example

```text
Personality: {{personality}}
```

## See also

- CBS: [`{{description}}`](description.md), [`{{scenario}}`](scenario.md), [`{{exampledialogue}}`](exampledialogue.md)
