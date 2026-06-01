# CBS: `{{tohex::num}}`

- Layer: CBS function
- Category: encoding
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`tohex`)

Converts a decimal number to its hexadecimal string.

## Syntax

```text
{{tohex::num}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `num` | yes | A base-10 number string. |

## Behavior

Parses the argument with `Number.parseInt(num)` (base 10, integer only) and
returns `.toString(16)` — the lowercase base-16 representation. This is the
inverse of [`{{fromhex}}`](fromhex.md). Note the input is parsed as an integer,
so any fractional part is dropped before conversion.

## Example

```text
{{tohex::255}}
```

renders `ff`.

## See also

- CBS: [`{{fromhex}}`](fromhex.md) (hex to decimal), [`{{unicodeencode}}`](unicodeencode.md)
