# CBS: `{{randint::min::max}}`

- **Layer:** CBS function
- **Category:** random
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`randint`)

Returns a random integer in an inclusive range.

## Syntax

```text
{{randint::min::max}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `min` | yes | Lower bound (inclusive). |
| 2 | `max` | yes | Upper bound (inclusive). |

## Behavior

Coerces both arguments with `Number`. If either is `NaN`, the function returns
the literal string `"NaN"`. Otherwise it returns
`Math.floor(Math.random() * (max - min + 1)) + min` as a string — a uniformly
random integer in `[min, max]`, both ends included.

This uses `Math.random()`, so the value is true random and re-rolls on each
parse. There is no clamping or ordering: if `min > max` the `(max - min + 1)`
term is non-positive and the result is not meaningful.

## Example

```text
{{randint::1::10}}
```

renders an integer from 1 to 10.

## See also

- CBS: [`{{random}}`](random.md), [`{{dice}}`](dice.md), [`{{roll}}`](roll.md)
