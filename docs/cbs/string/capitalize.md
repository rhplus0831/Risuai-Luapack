# CBS: `{{capitalize::s}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`capitalize`)

Capitalizes the first character of a string.

## Syntax

```text
{{capitalize::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to capitalize. |

## Behavior

Returns `s` with its first character upper-cased and the remainder left
unchanged: `s.charAt(0).toUpperCase() + s.slice(1)`. Only the very first
character is affected, so this is sentence-case, not title-case. If `s` is empty
the result is empty.

To change the case of the whole string, use [`{{upper}}`](upper.md) or
[`{{lower}}`](lower.md).

## Example

```text
{{capitalize::hello world}}   -> Hello world
```

## See also

- CBS: [`{{upper}}`](upper.md), [`{{lower}}`](lower.md)
- CBS: [`{{trim}}`](trim.md)
