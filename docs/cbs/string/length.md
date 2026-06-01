# CBS: `{{length::s}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`length`)

Returns the character count of a string.

## Syntax

```text
{{length::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to measure. |

## Behavior

Returns `s.length` (JavaScript `String.prototype.length`) as a string. This
counts every UTF-16 code unit, including spaces and punctuation. Note that
characters outside the Basic Multilingual Plane (e.g. many emoji) are counted as
two code units, so this is a code-unit count, not a grapheme count.

To count the elements of a JSON array instead of the characters of a string, use
[`{{arraylength}}`](../array/arraylength.md).

## Example

```text
{{length::Hello}}   -> 5
```

## See also

- CBS: [`{{trim}}`](trim.md), [`{{reverse}}`](reverse.md)
- CBS: [`{{arraylength}}`](../array/arraylength.md)
