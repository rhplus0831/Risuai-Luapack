# CBS: `{{:else}}`

- Layer: CBS block (clause)
- Category: blocks
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`:else`, doc-only); handled in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockEndMatcher`, the `newif` / `newif-falsy` cases)

The else clause inside a [`{{#when}}`](when.md) block.

## Syntax

```text
{{#when condition}} ... {{:else}} ... {{/when}}
```

## Arguments

None — `{{:else}}` is a marker, not a function with arguments.

## Behavior

Splits a `{{#when}}` body into a truthy part (before `{{:else}}`) and a falsy part
(after it). When the condition is truthy, only the part before `{{:else}}` is
kept; when falsy, only the part after it is kept.

Placement rules from the parser:

- It works in both single-line and multi-line `{{#when}}` blocks.
- In a multi-line block, `{{:else}}` must sit on its own line with no other
  text (the parser finds the line whose trimmed content equals exactly
  `{{:else}}`).
- It does not work when the `{{#when}}` uses the `legacy` operator, because
  that path falls back to the old `{{#if}}` handling, which has no else branch.

`{{:else}}` is only meaningful inside a `{{#when}}` block; on its own it has no
effect.

## Example

```text
{{#when::var::loggedin}}Welcome back.{{:else}}Please log in.{{/when}}
```

## See also

- Block: [`{{#when ...}}`](when.md)
- Block: [`{{#if}}`](if.md) (deprecated; has no else clause)
