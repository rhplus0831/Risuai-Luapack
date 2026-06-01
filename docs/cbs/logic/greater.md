# CBS: `{{greater::a::b}}`

- Layer: CBS function
- Category: logic
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`greater`)

Numeric "greater than" comparison.

## Syntax

```text
{{greater::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | Left operand. |
| 2 | `b` | yes | Right operand. |

## Behavior

Coerces both arguments to numbers and returns `"1"` if `a > b`, `"0"` otherwise.
Because the operands are converted with `Number(...)`, non-numeric values become
`NaN` and any comparison against `NaN` is false (`"0"`). For the inclusive form,
use [`{{greaterequal}}`](greaterequal.md).

## Example

```text
{{greater::10::5}}
```

renders `1`.

## See also

- CBS: [`{{less}}`](less.md), [`{{greaterequal}}`](greaterequal.md), [`{{lessequal}}`](lessequal.md), [`{{equal}}`](equal.md)
