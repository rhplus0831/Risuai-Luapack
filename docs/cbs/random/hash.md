# CBS: `{{hash::s}}`

- **Layer:** CBS function
- **Category:** random
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`hash`)

Turns a string into a deterministic ~7-digit number.

## Syntax

```text
{{hash::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The input string to hash. |

## Behavior

Computes `pickHashRand(0, s)` (a value in `[0, 1)` derived from `s`), multiplies
by `10000000`, adds `1`, rounds to an integer with `toFixed(0)`, and left-pads to
at least 7 digits with zeros. The result is fully deterministic: the same input
always yields the same number, with no dependence on time or chat state. It is
handy as a stable seed-like value for consistent pseudo-randomization.

> **Not the Lua `hash` API.** This CBS function is a deterministic numeric
> stringifier evaluated by the template parser. The Lua host API
> [`hash(id, value)`](../../api/hash.md) is a different thing: it is an
> **awaitable** call into Risu's cryptographic-style `hasher` and returns that
> hasher's value, not a 7-digit number. Do not expect the two to agree.

## Example

```text
{{hash::hello}}
```

renders a fixed 7-digit number such as `1234567` (same every time for `hello`).

## See also

- CBS: [`{{pick}}`](pick.md), [`{{rollp}}`](rollp.md) (other hash-stable functions), [`{{random}}`](random.md)
- Lua API (different): [`hash`](../../api/hash.md)
