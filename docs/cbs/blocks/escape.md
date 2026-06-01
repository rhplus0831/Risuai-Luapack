# CBS: `{{#escape}} ... {{/escape}}`

- Layer: CBS block
- Category: blocks
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`#escape`, doc-only); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher` returning the `escape` type, and the `escape` case in `blockEndMatcher` calling `risuEscape`)

Escapes braces and parentheses in its body, treating the content as literal
text.

## Syntax

```text
{{#escape}} ... {{/escape}}
{{#escape::keep}} ... {{/escape}}
```

## Arguments

| Operator | Form | Meaning |
|----------|------|---------|
| `keep` | `#escape::keep` | preserve whitespace; without it, the body is trimmed |

## Behavior

The body is passed to `risuEscape`, which escapes curly braces and parentheses so
they are rendered literally rather than interpreted as CBS syntax. Without an
operator, the body is trimmed first (`p1Trimmed`); with the `keep` operator
(`#escape::keep`), the body is escaped as-is, preserving whitespace.

This is the block-level equivalent of the per-character
[escaped literal characters](../format/escaped-characters.md) helpers: use
`{{#escape}}` to make a whole region literal instead of escaping one character at
a time.

## Example

```text
{{#escape}}{{char}} and (parentheses) shown literally{{/escape}}
```

renders the inner text without expanding `{{char}}` or reinterpreting the
parentheses.

## See also

- Block: [`{{#puredisplay}}`](puredisplay.md), [`{{#pure}}`](pure.md)
- CBS: [escaped literal characters](../format/escaped-characters.md)
