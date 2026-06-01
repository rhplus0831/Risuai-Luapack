# CBS: `{{? expression}}`

- **Layer:** CBS function (inline shorthand)
- **Category:** blocks
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`?`, doc-only entry); evaluated in `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`matcher`, the `p1.startsWith('? ')` branch) via `calcString` in `Refer/Risuai/src/ts/process/infunctions.ts`

Inline calculator: evaluates a math expression and returns the result.

## Syntax

```text
{{? expression}}
```

Note the space after `?` — the parser dispatches this form by matching the
literal prefix `"? "`.

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `expression` | yes | The expression to evaluate. Everything after `"? "`. |

## Behavior

The parser strips the leading `? ` and passes the rest to `calcString`, returning
the numeric result as a string. `calcString` handles parentheses for grouping by
recursing on each `(...)` group and evaluating the rest in RPN.

Supported operators (per the registered description): `+`, `-`, `*`, `/`, `%`
(modulo), `^` (exponentiation), and the comparisons `<`, `>`, `<=`, `>=`, `==`,
`!=`. It is a numeric evaluator, not full JavaScript.

This is the terse inline form of [`{{calc::expr}}`](../math/calc.md); both route
through the same `calcString` evaluator.

## Example

```text
{{? (2*3)+4}}
```

renders `10`.

## See also

- CBS: [`{{calc::expr}}`](../math/calc.md) (the `::`-argument form)
- CBS: [`{{round}}`](../math/round.md), [`{{floor}}`](../math/floor.md)
