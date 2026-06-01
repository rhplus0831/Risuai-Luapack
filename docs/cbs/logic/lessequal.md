# CBS: `{{lessequal::a::b}}`

- **Layer:** CBS function
- **Category:** logic
- **Aliases:** `less_equal`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`lessequal`)

Numeric "less than or equal to" comparison.

## Syntax

```text
{{lessequal::a::b}}
{{less_equal::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | Left operand. |
| 2 | `b` | yes | Right operand. |

## Behavior

Coerces both arguments to numbers and returns `"1"` if `a <= b`, `"0"`
otherwise. Because the operands are converted with `Number(...)`, non-numeric
values become `NaN` and any comparison against `NaN` is false (`"0"`). This is
the inclusive form of [`{{less}}`](less.md).

## Example

```text
{{lessequal::5::5}}
```

renders `1`.

## See also

- CBS: [`{{less}}`](less.md), [`{{greaterequal}}`](greaterequal.md), [`{{greater}}`](greater.md), [`{{equal}}`](equal.md)
