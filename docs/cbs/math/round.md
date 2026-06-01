# CBS: `{{round::n}}`

- Layer: CBS function
- Category: math
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`round`)

Rounds a number to the nearest integer.

## Syntax

```text
{{round::n}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `n` | yes | The number to round. |

## Behavior

Coerces `n` to a number, applies `Math.round` (standard half-up rounding, so
`.5` rounds toward positive infinity), and returns the integer result as a
string.

## Example

```text
{{round::3.7}}
```

renders `4`.

## See also

- CBS: [`{{floor}}`](floor.md), [`{{ceil}}`](ceil.md), [`{{fixnum}}`](fixnum.md), [`{{calc}}`](calc.md)
