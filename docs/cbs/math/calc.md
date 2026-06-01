# CBS: `{{calc::expr}}`

- **Layer:** CBS function
- **Category:** math
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`calc`)

Evaluates a math expression and returns the result.

## Syntax

```text
{{calc::expr}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `expr` | yes | A math expression to evaluate. |

## Behavior

Passes `expr` to Risu's expression evaluator and returns the result as a string.
The evaluator supports the basic arithmetic operators (`+`, `-`, `*`, `/`) and
parentheses for grouping. It is a numeric evaluator, not full JavaScript, so it
handles arithmetic only.

For a terser inline form, the same evaluation is available through the
[`{{? expr}}` shorthand](../blocks/calc-shorthand.md).

## Example

```text
{{calc::2 + 2 * 3}}
```

renders `8`.

## See also

- CBS: [`{{round}}`](round.md), [`{{floor}}`](floor.md), [`{{ceil}}`](ceil.md), [`{{pow}}`](pow.md)
- Shorthand: [`{{? expr}}`](../blocks/calc-shorthand.md)
