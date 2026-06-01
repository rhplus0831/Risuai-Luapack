# CBS: `{{fromhex::hex}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`fromhex`)

Converts a hexadecimal string to its decimal value.

## Syntax

```text
{{fromhex::hex}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `hex` | yes | A base-16 number string (for example `FF`). |

## Behavior

Returns `Number.parseInt(hex, 16)` as a string — the base-10 value of the
base-16 input. Parsing is case-insensitive for the hex digits and follows
`parseInt` rules (leading valid digits are read, trailing garbage is ignored).
This is the inverse of [`{{tohex}}`](tohex.md).

## Example

```text
{{fromhex::FF}}
```

renders `255`.

## See also

- CBS: [`{{tohex}}`](tohex.md) (decimal to hex), [`{{u}}`](u.md)
