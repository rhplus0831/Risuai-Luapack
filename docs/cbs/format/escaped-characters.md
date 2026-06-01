# CBS: escaped literal characters

- Layer: CBS function (family)
- Category: format
- Aliases: see the table below
- Source: `Refer/Risuai/src/ts/cbs.ts` (`decbo`, `decbc`, `bo`, `bc`, `displayescapedbracketopen`, `displayescapedbracketclose`, `displayescapedanglebracketopen`, `displayescapedanglebracketclose`, `displayescapedcolon`, `displayescapedsemicolon`)

A family of zero-argument CBS functions that emit characters which *display* as
`{`, `}`, `{{`, `}}`, `(`, `)`, `<`, `>`, `:`, or `;` but are not re-parsed as
CBS / HTML syntax.

## Syntax

```text
{{decbo}}      {{decbc}}
{{bo}}         {{bc}}
{{(}}          {{)}}
{{<}}          {{>}}
{{:}}          {{;}}
```

(Any alias from the table may be used; punctuation aliases like `{{(}}` are valid
names too.)

## Arguments

None — every member of this family is argument-free.

## Behavior

Each function returns a character from the Unicode Private Use Area (e.g. ``
for `{`). Risu's renderer shows these PUA characters as the corresponding literal
glyph, but because they are not the real `{`, `}`, `:`, `<`, etc., a later parsing
pass does not mistake them for CBS argument separators, CBS braces, or HTML
tags. This is how you put a literal brace, colon, parenthesis, or angle bracket
into output without it being interpreted.

Names are matched case-insensitively with spaces/underscores/hyphens ignored, and
each maps to the displayed character shown below.

| Canonical name | Aliases | Displays as |
|----------------|---------|-------------|
| `decbo` | `displayescapedcurlybracketopen` | `{` |
| `decbc` | `displayescapedcurlybracketclose` | `}` |
| `bo` | `ddecbo`, `doubledisplayescapedcurlybracketopen` | `{{` |
| `bc` | `ddecbc`, `doubledisplayescapedcurlybracketclose` | `}}` |
| `displayescapedbracketopen` | `debo`, `(` | `(` |
| `displayescapedbracketclose` | `debc`, `)` | `)` |
| `displayescapedanglebracketopen` | `deabo`, `<` | `<` |
| `displayescapedanglebracketclose` | `deabc`, `>` | `>` |
| `displayescapedcolon` | `dec`, `:` | `:` |
| `displayescapedsemicolon` | `;` | `;` |

## Example

```text
{{bo}}getvar::hp{{bc}}
```

displays the literal text `{{getvar::hp}}` instead of evaluating it.

## See also

- Block: [`{{#escape}} ... {{/escape}}`](../blocks/escape.md) (escape a whole region)
- CBS: [`{{codeblock}}`](codeblock.md), [`{{comment}}`](comment.md)
