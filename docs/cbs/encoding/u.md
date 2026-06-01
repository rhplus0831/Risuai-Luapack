# CBS: `{{u::hex}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** `unicodedecodefromhex`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`u`)

Returns the character for a **hexadecimal** code unit.

## Syntax

```text
{{u::hex}}
{{unicodedecodefromhex::hex}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `hex` | yes | A UTF-16 code unit written in base 16 (for example `41`). |

## Behavior

Parses the argument as base 16 (`parseInt(hex, 16)`) and returns
`String.fromCharCode(...)` for that value — the single character at that code
unit. It is the hex-input counterpart of
[`{{unicodedecode}}`](unicodedecode.md), which takes a decimal code unit.

## Example

```text
{{u::41}}
```

renders `A`.

## See also

- CBS: [`{{ue}}`](ue.md) (identical behavior), [`{{unicodedecode}}`](unicodedecode.md) (decimal input), [`{{unicodeencode}}`](unicodeencode.md)
