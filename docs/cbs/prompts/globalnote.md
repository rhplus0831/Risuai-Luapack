# CBS: `{{globalnote}}`

- Layer: CBS function
- Category: prompts
- Aliases: `systemnote`, `ujb`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`globalnote`)

Returns the global note (also called the system note).

## Syntax

```text
{{globalnote}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the global note (`db.globalNote`), also referred to as the system note
or `ujb`, which is appended to prompts. The text is run through Risu's chat
parser, so any CBS templates inside it are expanded.

## Example

```text
{{globalnote}}
```

## See also

- CBS: [`{{mainprompt}}`](mainprompt.md), [`{{jb}}`](jb.md), [`{{authornote}}`](authornote.md)
