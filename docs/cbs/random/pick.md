# CBS: `{{pick::...}}`

- **Layer:** CBS function
- **Category:** random
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`pick`, via `randomPickImpl`)

Like [`{{random}}`](random.md), but the choice is hash-stable: it stays the same
across re-renders of the same message.

## Syntax

```text
{{pick}}
{{pick::a::b::c}}
{{pick::a,b,c}}
{{pick::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | choices | no | Nothing (returns a float), several arguments (pick one), or a single string/array (pick an element). |

## Behavior

Identical argument handling to [`{{random}}`](random.md) — no args returns a
float, one arg is treated as a JSON array (if bracketed) or a `:`/`,`-split list,
and multiple args are the list directly. The difference is the random source:
instead of `Math.random()`, `{{pick}}` uses `pickHashRand` seeded by the current
message count and the character id plus chat id.

Because the seed is derived from chat/character identity rather than wall-clock
randomness, the same message resolves to the **same** choice every time it is
re-parsed or re-rendered, whereas `{{random}}` re-rolls each parse. During
accurate tokenization the first element is chosen.

## Example

```text
{{pick::sunny::cloudy::rainy}}
```

renders one of the three, and keeps that value on re-render.

## See also

- CBS: [`{{random}}`](random.md) (re-rolls each parse), [`{{rollp}}`](rollp.md), [`{{hash}}`](hash.md)
