# CBS: `{{char}}`

- **Layer:** CBS function
- **Category:** identity
- **Aliases:** `bot`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`char`)

Returns the display name (or nickname) of the current character/bot.

## Syntax

```text
{{char}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Resolves the name of the currently selected character. If the character has a
`nickname`, that is returned in preference to its `name`. For a **group chat**
the selected entry is a group, so the **group name** is returned instead of an
individual character name. In consistent-character mode (used during
tokenization/consistency passes) it returns the literal `"botname"`. If no
character is selected from the database, Risu falls back to the character passed
in the matcher argument (a string is returned as-is; otherwise its `name`).

The result is the raw name string and is not further CBS-parsed.

## Example

```text
{{char}} smiles at {{user}}.
```

## See also

- CBS: [`{{user}}`](user.md), [`{{personality}}`](personality.md), [`{{description}}`](description.md)
