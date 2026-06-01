# CBS: `{{comment::text}}`

- **Layer:** CBS function
- **Category:** format
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`comment`)

Renders a visible, styled comment block.

## Syntax

```text
{{comment::text}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `text` | yes | The comment text to show. |

## Behavior

When the parser is running in **display** mode (`matcherArg.displaying`), returns
`<div class="risu-comment">text</div>` — a styled comment div visible in the chat
UI. When **not** displaying (for example, while building the model request),
returns an empty string, so the comment is shown to the user but never sent to
the model.

This is the *visible* counterpart to the hidden comment
[`{{// ...}}`](../blocks/comment-block.md), whose content is removed entirely and
appears nowhere.

## Example

```text
{{comment::Author note: this scene is optional.}}
```

shows a styled note in the chat but adds nothing to the prompt.

## See also

- Block: [`{{// comment}}`](../blocks/comment-block.md) (hidden comment)
- CBS: [`{{codeblock}}`](codeblock.md)
