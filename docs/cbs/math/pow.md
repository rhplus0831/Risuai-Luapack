# CBS: `{{pow::base::exp}}`

- Layer: CBS function
- Category: math
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`pow`)

Raises a number to a power.

## Syntax

```text
{{pow::base::exp}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `base` | yes | The base number. |
| 2 | `exp` | yes | The exponent. |

## Behavior

Coerces both arguments to numbers and returns `Math.pow(base, exp)` (`base`
raised to `exp`) as a string. Fractional and negative exponents are supported
through the underlying `Math.pow`.

## Example

```text
{{pow::2::3}}
```

renders `8`.

## See also

- CBS: [`{{calc}}`](calc.md), [`{{remaind}}`](remaind.md), [`{{abs}}`](abs.md)
