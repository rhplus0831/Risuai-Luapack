# CBS: `{{arraysplice::array::index::deleteCount::element}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`arraysplice`)

Removes and/or inserts elements at an index and returns the modified array.

## Syntax

```text
{{arraysplice::array::index::deleteCount::element}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b","c"]`). |
| 2 | `index` | yes | 0-based start index for the splice. |
| 3 | `deleteCount` | yes | Number of elements to remove starting at `index`. |
| 4 | `element` | yes | The value to insert at `index` (inserted as a string). |

## Behavior

Parses `array` as JSON, then calls JavaScript
`Array.prototype.splice(index, deleteCount, element)`: it removes `deleteCount`
elements starting at `index` and inserts `element` at that position. The
modified array is returned as a JSON array string.

All four arguments are passed positionally and the call always inserts the
single `element`; there is no form that deletes without inserting through this
CBS. `index` and `deleteCount` are coerced with `Number`. `element` is inserted
as the raw string it was given.

This produces a **new** array string for use downstream; it does not write back
to any variable. To persist the result, pass it to
[`{{setvar}}`](../variables/setvar.md).

## Example

```text
{{arraysplice::["a","b","c"]::1::1::x}}   -> ["a","x","c"]
```

## See also

- CBS: [`{{arraypush}}`](arraypush.md), [`{{arrayassert}}`](arrayassert.md)
- CBS: [`{{arrayshift}}`](arrayshift.md), [`{{arraypop}}`](arraypop.md)
