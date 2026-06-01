# CBS: `{{arrayassert::array::index::value}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`arrayassert`)

Ensures a given index exists in a JSON array, extending it if necessary.

## Syntax

```text
{{arrayassert::array::index::value}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a"]`). |
| 2 | `index` | yes | 0-based index that must exist. |
| 3 | `value` | yes | The value to place at `index` if it is out of bounds. |

## Behavior

Parses `array` as JSON. If `index` is **greater than or equal to** the current
length (i.e. the index does not yet exist), it sets that index to `value`,
extending the array. Any positions between the old end and `index` become empty
(`null` when serialized to JSON). If `index` is already within bounds, the array
is returned unchanged — existing elements are **not** overwritten.

This mirrors the dictionary helper `objectassert` (alias `dictassert`), which
sets a key only if it is missing; `arrayassert` is the array-index equivalent.

This produces a **new** array string for use downstream; it does not write back
to any variable. To persist the result, pass it to
[`{{setvar}}`](../variables/setvar.md).

## Example

```text
{{arrayassert::["a"]::5::b}}   -> ["a",null,null,null,null,"b"]
{{arrayassert::["a","b"]::1::x}}   -> ["a","b"]   (index 1 already exists)
```

## See also

- CBS: [`{{arraysplice}}`](arraysplice.md), [`{{arraypush}}`](arraypush.md)
- CBS: [`{{arrayelement}}`](arrayelement.md), [`{{makearray}}`](makearray.md)
