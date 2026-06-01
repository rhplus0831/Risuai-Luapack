# CBS: `{{#pure}} ... {{/pure}}`

- Layer: CBS block (deprecated)
- Category: blocks
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`#pure`, doc-only, marked `deprecated`); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher` returning the `pure` type)

Legacy raw block: renders its contents without CBS processing. Deprecated —
use [`{{#puredisplay}}`](puredisplay.md) instead.

## Syntax

```text
{{#pure}} ... {{/pure}}
```

## Arguments

None.

## Behavior

The parser marks the block as `pure`, so the body is not processed as CBS — any
`{{...}}` inside is left as literal text. `blockEndMatcher` returns the trimmed
body for the `pure` type.

The construct is registered as deprecated: *"Due to reparsing issue, #pure is
deprecated and replaced with #puredisplay. Use #puredisplay instead."* The
replacement [`{{#puredisplay}}`](puredisplay.md) additionally escapes the braces
on the way out so they cannot be re-parsed by a later pass.

## Example

```text
{{#pure}}This {{char}} is shown literally.{{/pure}}
```

renders the inner text without expanding `{{char}}`.

## See also

- Block: [`{{#puredisplay}}`](puredisplay.md) (replacement), [`{{#escape}}`](escape.md)
