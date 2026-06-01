# CBS: `{{arraypush::array::element}}`

- Layer: CBS function
- Category: array
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`arraypush`)

Returns a JSON array with one element appended to the end.

## Syntax

```text
{{arraypush::array::element}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b"]`). |
| 2 | `element` | yes | The value to append. Added as a string. |

## Behavior

Parses `array` as JSON, appends `element` (JavaScript `Array.prototype.push`),
and returns the result as a JSON array string. `element` is pushed as the raw
string it was given, so numbers and JSON fragments are stored as quoted strings,
not as numeric or nested-object values. An empty or invalid array is treated as
`[]`, so the result is a one-element array.

This produces a new array string for use downstream; it does not write back
to any variable. To persist the result, pass it to
[`{{setvar}}`](../variables/setvar.md).

## Example

```text
{{arraypush::["a","b"]::c}}   -> ["a","b","c"]
```

## See also

- CBS: [`{{arraypop}}`](arraypop.md), [`{{arrayshift}}`](arrayshift.md)
- CBS: [`{{arraysplice}}`](arraysplice.md), [`{{arrayassert}}`](arrayassert.md)
