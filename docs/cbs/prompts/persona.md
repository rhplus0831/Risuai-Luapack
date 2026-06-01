# CBS: `{{persona}}`

- **Layer:** CBS function
- **Category:** prompts
- **Aliases:** `userpersona`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`persona`)

Returns the user persona prompt text.

## Syntax

```text
{{persona}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the active user persona prompt (Risu's `getPersonaPrompt()`) -- the
user's character description/personality -- after running it through Risu's chat
parser, so any CBS templates inside the persona text are expanded.

## Example

```text
About the user: {{persona}}
```

## See also

- CBS: [`{{user}}`](../identity/user.md), [`{{mainprompt}}`](mainprompt.md)
- Lua equivalent: [`getPersonaDescription`](../../api/getPersonaDescription.md)
