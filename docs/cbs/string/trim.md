# CBS: `{{trim::s}}`

- Layer: CBS function
- Category: string
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`trim`)

Strips leading and trailing whitespace from a string.

## Syntax

```text
{{trim::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to trim. |

## Behavior

Returns `s` with leading and trailing whitespace removed, using the literal
JavaScript `String.prototype.trim`. Whitespace inside the string is left
untouched; only the outer edges are stripped. "Whitespace" follows the
JavaScript definition (spaces, tabs, newlines, and other Unicode whitespace).

## Example

```text
{{trim::  hello world  }}   -> hello world
```

## See also

- CBS: [`{{replace}}`](replace.md), [`{{length}}`](length.md)
- CBS: [`{{lower}}`](lower.md), [`{{upper}}`](upper.md)
