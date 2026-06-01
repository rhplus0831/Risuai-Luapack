# CBS: `{{mainprompt}}`

- Layer: CBS function
- Category: prompts
- Aliases: `systemprompt`, `main_prompt`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`mainprompt`)

Returns the main system prompt.

## Syntax

```text
{{mainprompt}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the global main system prompt (`db.mainPrompt`) that provides the base
instructions to the AI model, after running it through Risu's chat parser, so
any CBS templates inside it are expanded.

## Example

```text
{{mainprompt}}
```

## See also

- CBS: [`{{jb}}`](jb.md), [`{{globalnote}}`](globalnote.md), [`{{authornote}}`](authornote.md)
