# CBS: `{{less::a::b}}`

- Layer: CBS function
- Category: logic
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`less`)

Numeric "less than" comparison.

## Syntax

```text
{{less::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | Left operand. |
| 2 | `b` | yes | Right operand. |

## Behavior

Coerces both arguments to numbers and returns `"1"` if `a < b`, `"0"` otherwise.
Because the operands are converted with `Number(...)`, non-numeric values become
`NaN` and any comparison against `NaN` is false (`"0"`). For the inclusive form,
use [`{{lessequal}}`](lessequal.md).

## Example

```text
{{less::5::10}}
```

renders `1`.

## See also

- CBS: [`{{greater}}`](greater.md), [`{{lessequal}}`](lessequal.md), [`{{greaterequal}}`](greaterequal.md), [`{{equal}}`](equal.md)
