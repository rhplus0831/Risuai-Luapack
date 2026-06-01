# CBS: `{{fixnum::n::decimals}}`

- Layer: CBS function
- Category: math
- Aliases: `fixnumber`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`fixnum`)

Formats a number to a fixed number of decimal places.

## Syntax

```text
{{fixnum::n::decimals}}
{{fixnumber::n::decimals}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `n` | yes | The number to format. |
| 2 | `decimals` | yes | How many digits to keep after the decimal point. |

## Behavior

Coerces both arguments to numbers and returns `n.toFixed(decimals)`. The value
is rounded to the requested number of decimal places and always rendered with
exactly that many digits (padding with zeros if needed), so the result is a
fixed-width decimal string. Unlike [`{{round}}`](round.md), the result is not
truncated to an integer.

## Example

```text
{{fixnum::3.14159::2}}
```

renders `3.14`.

## See also

- CBS: [`{{round}}`](round.md), [`{{floor}}`](floor.md), [`{{ceil}}`](ceil.md), [`{{calc}}`](calc.md)
