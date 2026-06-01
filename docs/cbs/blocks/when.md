# CBS: `{{#when ...}} ... {{/when}}`

- **Layer:** CBS block
- **Category:** blocks
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`#when`, doc-only); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`blockStartMatcher`, the `p1.startsWith('#when')` branch, and `blockEndMatcher` for the `newif` / `newif-falsy` types)

The current conditional block: renders its body only when the condition is
truthy. Replaces the deprecated [`{{#if}}`](if.md).

## Syntax

```text
{{#when condition}} ... {{/when}}
{{#when::OPERANDS::OPERATORS}} ... {{:else}} ... {{/when}}
```

A bare condition may be given after a space (`#when condition`) or as a single
`::` argument (`#when::condition`). With operators, operands and operators are
all `::`-separated.

## Arguments

A value is **truthy** only when it is exactly `"true"` or `"1"`; everything else
is falsy. Operators are applied from the right (the parser pops operands/operators
off the end), reducing the statement to a single truthy/falsy result.

| Operator | Form | Meaning |
|----------|------|---------|
| `and` | `A::and::B` | both A and B are truthy |
| `or` | `A::or::B` | at least one of A, B is truthy |
| `is` | `A::is::B` | A equals B (string compare) |
| `isnot` | `A::isnot::B` | A does not equal B |
| `>` | `A::>::B` | A greater than B (numeric) |
| `<` | `A::<::B` | A less than B (numeric) |
| `>=` | `A::>=::B` | A greater than or equal to B (numeric) |
| `<=` | `A::<=::B` | A less than or equal to B (numeric) |
| `not` | `not::A` | negates A |
| `var` | `var::A` | true if chat variable `A` is truthy |
| `vis` | `A::vis::B` | true if chat variable `A` equals literal `B` |
| `visnot` | `A::visnot::B` | true if chat variable `A` does not equal `B` |
| `toggle` | `toggle::name` | true if toggle `name` is enabled |
| `tis` | `A::tis::B` | true if toggle `A` equals literal `B` |
| `tisnot` | `A::tisnot::B` | true if toggle `A` does not equal `B` |
| `keep` | `keep::A` | render the body without trimming whitespace |
| `legacy` | `legacy::A` | use the old `{{#if}}`-style whitespace handling |

Operators can be combined, e.g. `{{#when::keep::not::condition}}` or
`{{#when::condition1::and::condition2}}`. The numeric comparisons use
`parseFloat`; `var`/`vis`/`visnot` read chat variables; `toggle`/`tis`/`tisnot`
read the global variable `toggle_<name>`.

Note on operand order for comparisons: the parser pops the right operand first,
so `A::>::B` is evaluated as `parseFloat(A) > parseFloat(B)` reading left to
right as written.

## Behavior

If the reduced condition is truthy, the block body is emitted; otherwise it is
removed. An optional [`{{:else}}`](else.md) clause supplies the alternative body
for the falsy case. By default leading/trailing blank lines are trimmed; the
`keep` operator preserves whitespace, and `legacy` reverts to the older
`{{#if}}` whitespace rules.

## Example

```text
{{#when::var::hp::>::0}}You are alive.{{:else}}You have fallen.{{/when}}
```

## See also

- Block: [`{{:else}}`](else.md), [`{{#if}}`](if.md) (deprecated predecessor)
- Element: [Prompt toggles](../../element/prompt-toggles.md), [Chat variables](../../element/chat-variables.md)
