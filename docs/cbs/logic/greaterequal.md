# CBS: `{{greaterequal::a::b}}`

- Layer: CBS function
- Category: logic
- Aliases: `greater_equal`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`greaterequal`)

Numeric "greater than or equal to" comparison.

## Syntax

```text
{{greaterequal::a::b}}
{{greater_equal::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | Left operand. |
| 2 | `b` | yes | Right operand. |

## Behavior

Coerces both arguments to numbers and returns `"1"` if `a >= b`, `"0"`
otherwise. Because the operands are converted with `Number(...)`, non-numeric
values become `NaN` and any comparison against `NaN` is false (`"0"`). This is
the inclusive form of [`{{greater}}`](greater.md).

## Example

```text
{{greaterequal::10::10}}
```

renders `1`.

## See also

- CBS: [`{{greater}}`](greater.md), [`{{lessequal}}`](lessequal.md), [`{{less}}`](less.md), [`{{equal}}`](equal.md)
