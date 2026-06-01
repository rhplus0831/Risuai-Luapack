# CBS: `{{dice::XdY}}`

- **Layer:** CBS function
- **Category:** random
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`dice`)

Rolls dice in `XdY` notation and returns the sum.

## Syntax

```text
{{dice::XdY}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `XdY` | yes | Standard dice notation: `X` dice of `Y` sides (for example `2d6`). |

## Behavior

Splits the argument on the letter `d` into `X` (count) and `Y` (sides), coercing
both with `Number`. If either is `NaN`, the function returns the literal string
`"NaN"`. Otherwise it rolls `X` dice, each `Math.floor(Math.random() * Y) + 1`
(an integer in `[1, Y]`), sums them, and returns the total as a string.

Rolling uses `Math.random()`, so the result is true random and re-rolls on each
parse. Unlike [`{{roll}}`](roll.md) there is **no** default — the notation must
contain a `d`, and a missing count or sides coerces to `NaN`.

## Example

```text
{{dice::2d6}}
```

renders a number from 2 to 12.

## See also

- CBS: [`{{roll}}`](roll.md) (defaults to 1d6), [`{{rollp}}`](rollp.md) (hash-stable), [`{{randint}}`](randint.md)
