# CBS: `{{upper::s}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`upper`)

Converts a string to uppercase.

## Syntax

```text
{{upper::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to uppercase. |

## Behavior

Returns `s` uppercased using the locale-aware JavaScript
`String.prototype.toLocaleUpperCase`, so international characters are handled
according to locale rules rather than a plain ASCII fold.

## Example

```text
{{upper::Hello world}}   -> HELLO WORLD
```

## See also

- CBS: [`{{lower}}`](lower.md), [`{{capitalize}}`](capitalize.md)
- CBS: [`{{trim}}`](trim.md)
