# CBS: `{{random::...}}`

- Layer: CBS function
- Category: random
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`random`, via `randomPickImpl`)

Returns a random number, or a random element chosen from its arguments.

## Syntax

```text
{{random}}
{{random::a::b::c}}
{{random::a,b,c}}
{{random::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | choices | no | Nothing (returns a float), several arguments (pick one), or a single string/array (pick an element). |

## Behavior

Backed by `Math.random()` (true per-call randomness):

- No arguments: returns the raw `Math.random()` value, a float in `[0, 1)`,
  as a string.
- One argument: if it starts with `[` and ends with `]` it is parsed as a
  JSON array; otherwise it is split on `:` or `,` into a list (use `\,` to keep a
  literal comma). A random element of that list is returned.
- Multiple arguments: the arguments themselves are the list, and a random one
  is returned.

The chosen element is returned as a string; objects/arrays are
`JSON.stringify`d. During accurate tokenization (`tokenizeAccurate`) the first
element is chosen deterministically instead of a random one.

`{{random}}` re-rolls on every parse, so the value changes each time the
message is re-rendered. For a value that stays stable across re-renders, use
[`{{pick}}`](pick.md).

## Example

```text
{{random::a,b,c}}
```

renders one of `a`, `b`, or `c`.

## See also

- CBS: [`{{pick}}`](pick.md) (hash-stable), [`{{randint}}`](randint.md), [`{{roll}}`](roll.md), [`{{hash}}`](hash.md)
