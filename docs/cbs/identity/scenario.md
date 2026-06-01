# CBS: `{{scenario}}`

- **Layer:** CBS function
- **Category:** identity
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`scenario`)

Returns the current character's scenario field.

## Syntax

```text
{{scenario}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the `scenario` field of the active character (the one passed in the
matcher argument, otherwise the selected character) and returns it after running
it through Risu's chat parser, so any CBS templates inside the scenario are
expanded. For a **group chat** the character has type `group` and this returns an
**empty string**.

## Example

```text
Scenario: {{scenario}}
```

## See also

- CBS: [`{{description}}`](description.md), [`{{personality}}`](personality.md)
