# CBS: `{{#if cond}} ... {{/if}}`

- Layer: CBS block (deprecated)
- Category: blocks
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`#if`, doc-only, marked `deprecated`); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher`, the `p1.startsWith('#if')` branch)

Legacy conditional block. Deprecated — use [`{{#when}}`](when.md) instead.

## Syntax

```text
{{#if cond}} ... {{/if}}
```

The condition follows after a space; the parser reads it with
`p1.split(' ', 2)`.

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `cond` | yes | The condition. Truthy only when it is exactly `"true"` or `"1"`. |

## Behavior

If `cond` is exactly `"true"` or `"1"`, the body is parsed and emitted (block
type `parse`, which trims each line); any other value removes the body (type
`ignore`). There is no `{{:else}}` branch.

The construct is registered as deprecated: *"Due to limitations of adding
operators, #if is deprecated and replaced with #when. Use #when instead."* Its
replacement, [`{{#when}}`](when.md), supports operators, an else clause, and
configurable whitespace handling. New scripts should use `{{#when}}`.

## Example

```text
{{#if {{getvar::ready}}}}Go!{{/if}}
```

renders `Go!` only when the `ready` variable expands to `1` or `true`.

## See also

- Block: [`{{#when ...}}`](when.md) (replacement), [`{{#if_pure}}`](if-pure.md)
