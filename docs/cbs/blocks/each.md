# CBS: `{{#each ARRAY as V}} ... {{/each}}`

- Layer: CBS block
- Category: blocks
- Aliases: `:each`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`#each`, doc-only); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher` returning the `each` type, and the `each` handling in the block-end loop)

Iterates over a JSON array, rendering the body once per element. The current
element is read with [`{{slot::V}}`](slot.md).

## Syntax

```text
{{#each ARRAY as V}} ... {{slot::V}} ... {{/each}}
{{#each::keep ARRAY as V}} ... {{/each}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `ARRAY` | yes | A JSON array to iterate (parsed by the parser's `parseArray`). |
| 2 | `V` | yes | The slot name bound to the current element, introduced with `as`. |

The optional `keep` operator (`#each::keep ARRAY as V`) preserves whitespace in
the body instead of trimming it.

## Behavior

The parser splits on the last ` as ` to get the slot name `V` and parses the text
before it as the array. For each element it takes the rendered body and replaces
every `{{slot::V}}` with that element — strings are inserted as-is, non-strings
are `JSON.stringify`'d. The per-iteration outputs are concatenated. With `keep`,
the joined result is kept verbatim; otherwise it is trimmed.

A compatibility mode exists: if there is no ` as `, the parser splits on the last
space, using the trailing token as the slot name.

## Example

```text
{{#each ["red","green","blue"] as color}}- {{slot::color}}
{{/each}}
```

renders one bullet per color.

## See also

- Block: [`{{slot::name}}`](slot.md) (read the current element)
- Block: [`{{#when ...}}`](when.md)
