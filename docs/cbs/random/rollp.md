# CBS: `{{rollp::XdY}}`

- Layer: CBS function
- Category: random
- Aliases: `rollpick`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`rollp`)

Like [`{{roll}}`](roll.md), but hash-stable: the same message rolls the same
result across re-renders.

## Syntax

```text
{{rollp::XdY}}
{{rollp::Y}}
{{rollp}}
{{rollpick::XdY}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `XdY` | no | Dice notation `XdY`, or a bare number of sides `Y`. Omitted means 1d6. |

## Behavior

Argument parsing matches [`{{roll}}`](roll.md): no argument returns `"1"`; the
argument is split on `d` with `X` defaulting to `1` and `Y` to `6`; a `NaN`
count/sides or a value `< 1` returns the literal string `"NaN"`.

The difference is the random source. Each of the `X` dice is rolled with
`pickHashRand` seeded by the current message count (offset by `i * 15` for the
`i`-th die) plus the character id and chat id, rather than `Math.random()`. The
seed therefore depends on chat/character identity, so the same message yields the
same total every time it is re-parsed or re-rendered — the deterministic
counterpart to `{{roll}}`.

## Example

```text
{{rollp::2d6}}
```

renders a number from 2 to 12, stable across re-renders.

## See also

- CBS: [`{{roll}}`](roll.md) (true random), [`{{pick}}`](pick.md), [`{{hash}}`](hash.md)
