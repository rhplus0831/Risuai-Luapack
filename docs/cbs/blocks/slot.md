# CBS: `{{slot::name}}`

- **Layer:** CBS function (block slot)
- **Category:** blocks
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`slot`, doc-only); substituted in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (the `each` block handling, which `replaceAll`s `{{slot::<name>}}`)

The current loop/block slot value, used inside [`{{#each}}`](each.md).

## Syntax

```text
{{slot::name}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The slot name introduced by the enclosing block (e.g. the `V` in `{{#each ARRAY as V}}`). |

## Behavior

`{{slot}}` is a `doc_only` construct — it is not evaluated by a normal callback.
Instead, the enclosing [`{{#each}}`](each.md) block performs a textual
`replaceAll` of `{{slot::<name>}}` with the current element on each iteration:
string elements are inserted as-is, non-string elements are `JSON.stringify`'d.

It only has meaning inside a block that binds a slot of that name. Outside such a
block there is nothing to substitute, so it is left untouched / yields nothing
useful.

## Example

```text
{{#each ["a","b"] as letter}}[{{slot::letter}}]{{/each}}
```

renders `[a][b]`.

## See also

- Block: [`{{#each ARRAY as V}}`](each.md)
