# CBS: `{{roll::XdY}}`

- Layer: CBS function
- Category: random
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`roll`)

Rolls dice (true random) with sensible defaults and returns the sum.

## Syntax

```text
{{roll::XdY}}
{{roll::Y}}
{{roll}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `XdY` | no | Dice notation `XdY`, or a bare number of sides `Y`. Omitted means 1d6. |

## Behavior

With no argument the function returns `"1"`. Otherwise the argument is split
on `d`:

- Two parts (`X`d`Y`): `X` defaults to `1` if blank, `Y` defaults to `6` if
  blank.
- One part (`Y` only, no `d`): `X` stays `1` and `Y` is that number.

Both are coerced with `Number`; if either is `NaN`, or `X < 1`, or `Y < 1`, the
function returns the literal string `"NaN"`. Otherwise it rolls `X` dice, each
`Math.floor(Math.random() * Y) + 1`, sums them, and returns the total.

Rolling uses `Math.random()` (true random), so it re-rolls on each parse. For a
hash-stable equivalent that stays the same across re-renders, use
[`{{rollp}}`](rollp.md).

## Example

```text
{{roll::2d6}}
```

renders a number from 2 to 12. `{{roll::20}}` rolls 1d20, and `{{roll}}` returns
`1`.

## See also

- CBS: [`{{rollp}}`](rollp.md) (hash-stable), [`{{dice}}`](dice.md) (no defaults), [`{{randint}}`](randint.md)
