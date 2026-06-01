# CBS: `{{ruby::text::ruby}}`

- Layer: CBS function
- Category: format
- Aliases: `furigana`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`ruby`)

Renders ruby text (furigana) as HTML.

## Syntax

```text
{{ruby::text::ruby}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `text` | yes | The base text. |
| 2 | `ruby` | yes | The ruby (annotation) text shown above the base. |

## Behavior

Returns a `<ruby>` element of the form
`<ruby>text<rp> (</rp><rt>ruby</rt><rp>) </rp></ruby>`. The `<rt>` holds the
annotation; the `<rp>` fallback parentheses are shown by browsers that do not
support ruby rendering. This is the standard markup for East Asian furigana, e.g.
kanji with a reading above it.

## Example

```text
{{ruby::Tokyo::Tokyo}}
```

renders the base text with the annotation above it.

## See also

- CBS: [`{{tex}}`](tex.md), [`{{codeblock}}`](codeblock.md)
