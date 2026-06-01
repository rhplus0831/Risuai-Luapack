# CBS: `{{#puredisplay}} ... {{/puredisplay}}`

- **Layer:** CBS block
- **Category:** blocks
- **Aliases:** none (the parser also accepts `#pure_display`)
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`#puredisplay`, doc-only); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher` returning the `pure-display` type, and the `pure-display` handling in the parse loop)

Renders content without CBS processing, escaping the braces so a later pass
cannot re-parse them.

## Syntax

```text
{{#puredisplay}} ... {{/puredisplay}}
```

The parser recognizes both `#puredisplay` and `#pure_display`.

## Arguments

None.

## Behavior

The body is treated as raw (block type `pure-display`): inner `{{...}}` is not
expanded. On the way out the parser additionally escapes the braces — `{{` becomes
`\{\{` and `}}` becomes `\}\}` — so that even if the output is parsed again, the
content stays literal. This fixes the re-parsing issue that affected the
deprecated [`{{#pure}}`](pure.md).

Use it to display raw HTML or literal CBS syntax in the chat.

## Example

```text
{{#puredisplay}}{{getvar::hp}} stays as literal text{{/puredisplay}}
```

shows `{{getvar::hp}}` verbatim instead of expanding it.

## See also

- Block: [`{{#pure}}`](pure.md) (deprecated predecessor), [`{{#escape}}`](escape.md)
- CBS: [escaped literal characters](../format/escaped-characters.md)
