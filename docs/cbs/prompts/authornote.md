# CBS: `{{authornote}}`

- Layer: CBS function
- Category: prompts
- Aliases: `author_note`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`authornote`)

Returns the chat's author's note.

## Syntax

```text
{{authornote}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the author's note for the current chat (`chat.note`). If the chat has no
custom note, it falls back to the `defaultText` of the first `authornote` entry
in the prompt template (`db.promptTemplate`). If neither exists, it returns an
empty string. The resolved text is run through Risu's chat parser, so any CBS
templates inside it are expanded.

## Example

```text
[Author's note: {{authornote}}]
```

## See also

- CBS: [`{{globalnote}}`](globalnote.md), [`{{mainprompt}}`](mainprompt.md)
- Lua equivalent: [`getAuthorsNote`](../../api/getAuthorsNote.md)
