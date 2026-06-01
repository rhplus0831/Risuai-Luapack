# CBS: `{{exampledialogue}}`

- **Layer:** CBS function
- **Category:** identity
- **Aliases:** `examplemessage`, `example_dialogue`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`exampledialogue`)

Returns the current character's example dialogue/messages.

## Syntax

```text
{{exampledialogue}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the `exampleMessage` field of the active character (the one passed in the
matcher argument, otherwise the selected character) and returns it after running
it through Risu's chat parser, so any CBS templates inside the example messages
are expanded. For a **group chat** the character has type `group` and this
returns an **empty string**.

## Example

```text
Example dialogue:
{{exampledialogue}}
```

## See also

- CBS: [`{{personality}}`](personality.md), [`{{description}}`](description.md), [`{{scenario}}`](scenario.md)
