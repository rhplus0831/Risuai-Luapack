# CBS: `{{tex::latex}}`

- **Layer:** CBS function
- **Category:** format
- **Aliases:** `latex`, `katex`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`tex`)

Wraps an expression as display-mode LaTeX/KaTeX math.

## Syntax

```text
{{tex::latex}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `latex` | yes | The LaTeX/KaTeX math source. |

## Behavior

Returns the input wrapped in double dollar signs: `$$<latex>$$`. This is the
display-math delimiter Risu's renderer hands to KaTeX, so the expression renders
as a centered math block in the chat.

The argument is emitted verbatim between the delimiters — no escaping is done, so
characters that CBS treats specially (such as `:` or `}`) must be produced with
the literal-character helpers (see
[escaped literal characters](escaped-characters.md)) if they appear in the
formula.

## Example

```text
{{tex::E = mc^2}}
```

renders the equation as display math.

## See also

- CBS: [`{{codeblock}}`](codeblock.md), [`{{ruby}}`](ruby.md)
- CBS: [escaped literal characters](escaped-characters.md)
