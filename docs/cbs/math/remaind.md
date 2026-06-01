# CBS: `{{remaind::a::b}}`

- Layer: CBS function
- Category: math
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`remaind`)

Returns the remainder of dividing one number by another (modulo).

## Syntax

```text
{{remaind::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | The dividend. |
| 2 | `b` | yes | The divisor. |

## Behavior

Coerces both arguments to numbers and returns `a % b` (the JavaScript remainder
operator) as a string. The result takes the sign of `a`. Dividing by `0`
yields `NaN`, which renders as the string `NaN`. Useful for cycles and wrapping
indices into a range.

## Example

```text
{{remaind::10::3}}
```

renders `1`.

## See also

- CBS: [`{{calc}}`](calc.md), [`{{pow}}`](pow.md), [`{{abs}}`](abs.md)
