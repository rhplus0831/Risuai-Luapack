# CBS: `{{#if_pure cond}} ... {{/if_pure}}`

- **Layer:** CBS block (deprecated)
- **Category:** blocks
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`#if_pure`, doc-only, marked `deprecated`); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher`, the `p1.startsWith('#if')` branch returning the `ifpure` type)

Legacy conditional that preserves whitespace. **Deprecated** — use
[`{{#when::keep::cond}}`](when.md) instead.

## Syntax

```text
{{#if_pure cond}} ... {{/if_pure}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `cond` | yes | The condition. Truthy only when it is exactly `"true"` or `"1"`. |

## Behavior

Behaves like [`{{#if}}`](if.md) for the truth test (`"true"` or `"1"` keeps the
body, anything else removes it), but the kept body is returned **verbatim** —
`blockEndMatcher` returns `p1` unchanged for the `ifpure` type, so whitespace and
newlines inside the block are preserved rather than line-trimmed.

The construct is registered as **deprecated**: *"Due to limitations of adding
operators, #if_pure is deprecated and replaced with #when with keep operator. Use
#when::keep::condition instead."* New scripts should use
[`{{#when::keep::cond}}`](when.md).

## Example

```text
{{#if_pure 1}}
  indented, with blank line kept

{{/if_pure}}
```

## See also

- Block: [`{{#when ...}}`](when.md) (use `keep`), [`{{#if}}`](if.md)
- Block: [`{{#pure}}`](pure.md), [`{{#puredisplay}}`](puredisplay.md)
