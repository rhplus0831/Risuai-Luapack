# CBS: `{{ue::hex}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** `unicodeencodefromhex`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`ue`)

Returns the character for a hexadecimal code unit. Despite the "encode" name,
its behavior is **identical** to [`{{u}}`](u.md) (a *decode*).

## Syntax

```text
{{ue::hex}}
{{unicodeencodefromhex::hex}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `hex` | yes | A UTF-16 code unit written in base 16 (for example `41`). |

## Behavior

In the source `ue`'s callback is exactly the same as `u`'s:
`String.fromCharCode(parseInt(hex, 16))`. It parses the hex argument and returns
the matching character. It does **not** convert a character to hex — the name
notwithstanding, it decodes a hex code unit to a character just like
[`{{u}}`](u.md).

To go the other way (character to a numeric code unit) use
[`{{unicodeencode}}`](unicodeencode.md), then [`{{tohex}}`](tohex.md) if you want
the result in hex.

## Example

```text
{{ue::41}}
```

renders `A` (same as `{{u::41}}`).

## See also

- CBS: [`{{u}}`](u.md) (identical), [`{{unicodeencode}}`](unicodeencode.md), [`{{tohex}}`](tohex.md)
