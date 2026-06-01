# CBS: `{{floor::n}}`

- Layer: CBS function
- Category: math
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`floor`)

Rounds a number down to the nearest integer.

## Syntax

```text
{{floor::n}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `n` | yes | The number to round down. |

## Behavior

Coerces `n` to a number, applies `Math.floor` (always rounds toward negative
infinity, so `-3.1` becomes `-4`), and returns the integer result as a string.

## Example

```text
{{floor::3.9}}
```

renders `3`.

## See also

- CBS: [`{{ceil}}`](ceil.md), [`{{round}}`](round.md), [`{{calc}}`](calc.md)
