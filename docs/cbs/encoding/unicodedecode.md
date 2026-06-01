# CBS: `{{unicodedecode::codepoint}}`

- Layer: CBS function
- Category: encoding
- Aliases: `unicode_decode`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`unicodedecode`)

Returns the character for a decimal code unit.

## Syntax

```text
{{unicodedecode::codepoint}}
{{unicode_decode::codepoint}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `codepoint` | yes | A decimal UTF-16 code unit. |

## Behavior

Coerces the argument with `Number` and returns
`String.fromCharCode(codepoint)` — the single character for that UTF-16 code
unit. This is the inverse of [`{{unicodeencode}}`](unicodeencode.md). For a hex
input instead of decimal, use [`{{u}}`](u.md).

Because it uses `fromCharCode`, the input is treated as a 16-bit code unit;
values above the BMP require a surrogate pair rather than a single call.

## Example

```text
{{unicodedecode::65}}
```

renders `A`.

## See also

- CBS: [`{{unicodeencode}}`](unicodeencode.md), [`{{u}}`](u.md) (hex input), [`{{ue}}`](ue.md)
