# CBS: `{{abs::n}}`

- **Layer:** CBS function
- **Category:** math
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`abs`)

Returns the absolute value of a number.

## Syntax

```text
{{abs::n}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `n` | yes | The number to take the absolute value of. |

## Behavior

Coerces `n` to a number, applies `Math.abs` (drops the sign so the result is
non-negative), and returns it as a string.

## Example

```text
{{abs::-5}}
```

renders `5`.

## See also

- CBS: [`{{round}}`](round.md), [`{{remaind}}`](remaind.md), [`{{calc}}`](calc.md)
