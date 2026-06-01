# CBS: `{{join::array::sep}}`

- Layer: CBS function
- Category: array
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`join`)

Joins the elements of a JSON array into one string with a separator.

## Syntax

```text
{{join::array::sep}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["apple","banana"]`). |
| 2 | `sep` | yes | The separator placed between elements. |

## Behavior

Parses `array` as JSON and returns its elements joined with `sep` (JavaScript
`Array.prototype.join`). Invalid JSON is treated as an empty array, which joins
to an empty string. A one-element array returns that element with no separator.

`{{join}}` is the inverse of [`{{split}}`](../string/split.md): splitting a
string on a delimiter and joining the pieces with the same delimiter reproduces
the original. To join with the fixed `::` separator used for spreading into
another CBS call's arguments, use [`{{spread}}`](spread.md) instead.

## Example

```text
{{join::["apple","banana"]::, }}   -> apple, banana
```

## See also

- CBS: [`{{split}}`](../string/split.md), [`{{spread}}`](spread.md)
- CBS: [`{{makearray}}`](makearray.md), [`{{arrayelement}}`](arrayelement.md)
