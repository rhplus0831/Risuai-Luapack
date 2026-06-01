# CBS: `{{ceil::n}}`

- Layer: CBS function
- Category: math
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`ceil`)

Rounds a number up to the nearest integer.

## Syntax

```text
{{ceil::n}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `n` | yes | The number to round up. |

## Behavior

Coerces `n` to a number, applies `Math.ceil` (always rounds toward positive
infinity, so `-3.9` becomes `-3`), and returns the integer result as a string.

## Example

```text
{{ceil::3.1}}
```

renders `4`.

## See also

- CBS: [`{{floor}}`](floor.md), [`{{round}}`](round.md), [`{{calc}}`](calc.md)
