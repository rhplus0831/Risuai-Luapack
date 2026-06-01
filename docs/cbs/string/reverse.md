# CBS: `{{reverse::s}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`reverse`)

Reverses the input string.

## Syntax

```text
{{reverse::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to reverse. |

## Behavior

Returns the input reversed by code point: `[...str].reverse().join('')`. Because
it spreads the string into an array of Unicode code points before reversing,
surrogate-pair characters (e.g. emoji) are preserved as whole characters rather
than being torn apart, but combining-mark sequences are still reversed
code-point by code-point.

Note that this function reverses the entire inner content of the call, not a
single parsed argument; supply one value as shown.

## Example

```text
{{reverse::hello}}   -> olleh
```

## See also

- CBS: [`{{upper}}`](upper.md), [`{{lower}}`](lower.md)
- CBS: [`{{length}}`](length.md)
