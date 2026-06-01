# CBS: `{{unicodeencode::s::index}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** `unicode_encode`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`unicodeencode`)

Returns the UTF-16 code unit of a character in a string.

## Syntax

```text
{{unicodeencode::s::index}}
{{unicode_encode::s::index}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The source string. |
| 2 | `index` | no | Position of the character to read. Defaults to `0` (first character). |

## Behavior

Returns `s.charCodeAt(index)` as a string — the numeric code unit at the given
position. If `index` is omitted (falsy), position `0` is used; otherwise the
argument is coerced with `Number`. The value is a UTF-16 code unit, so
characters outside the Basic Multilingual Plane are split across two surrogate
units.

This is the inverse of [`{{unicodedecode}}`](unicodedecode.md).

## Example

```text
{{unicodeencode::A}}
```

renders `65`.

## See also

- CBS: [`{{unicodedecode}}`](unicodedecode.md), [`{{u}}`](u.md), [`{{ue}}`](ue.md)
