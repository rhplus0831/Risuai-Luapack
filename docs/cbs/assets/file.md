# CBS: `{{file::name::base64}}`

- Layer: CBS function
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`file`)

Renders a filename chip in display mode, or decodes embedded base64 content
otherwise.

## Syntax

```text
{{file::name::base64}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The filename to show in display mode. |
| 2 | `base64` | yes | Base64-encoded file contents, decoded outside display mode. |

## Behavior

Branches on whether the parser is rendering for display (`matcherArg.displaying`):

- Display mode: returns a filename chip
  `<br><div class="risu-file">name</div><br>` — only the `name` is shown, the
  base64 payload is not.
- Otherwise (e.g. prompt building): decodes the second argument from base64
  and returns it as UTF-8 text (`Buffer.from(base64, 'base64').toString('utf-8')`).

This lets a single token carry a file's text into the model request while
showing only a compact filename in the chat UI.

## Example

```text
{{file::notes.txt::SGVsbG8gd29ybGQ=}}
```

## See also

- CBS: [`{{button::text::trigger}}`](button.md)
- Element: [Display HTML](../../element/display-html.md)
