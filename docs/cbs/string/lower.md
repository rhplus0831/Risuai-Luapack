# CBS: `{{lower::s}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`lower`)

Converts a string to lowercase.

## Syntax

```text
{{lower::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to lowercase. |

## Behavior

Returns `s` lowercased using the locale-aware JavaScript
`String.prototype.toLocaleLowerCase`, so international characters are handled
according to locale rules rather than a plain ASCII fold.

## Example

```text
{{lower::Hello WORLD}}   -> hello world
```

## See also

- CBS: [`{{upper}}`](upper.md), [`{{capitalize}}`](capitalize.md)
- CBS: [`{{trim}}`](trim.md)
