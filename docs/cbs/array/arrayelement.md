# CBS: `{{arrayelement::array::index}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`arrayelement`)

Returns the element at a given index of a JSON array.

## Syntax

```text
{{arrayelement::array::index}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b","c"]`). |
| 2 | `index` | yes | 0-based index. Negative values count from the end. |

## Behavior

Parses `array` as JSON and returns the element at `index` using JavaScript
`Array.prototype.at`, so the index is **0-based** and a negative `index` counts
back from the end (`-1` is the last element). If the index is out of bounds the
result is the literal string `"null"`. If the selected element is itself an
object or array it is re-serialized with `JSON.stringify`; otherwise it is
coerced to a string.

Invalid JSON for `array` is treated as an empty array, so any index returns
`"null"`.

## Example

```text
{{arrayelement::["a","b","c"]::1}}    -> b
{{arrayelement::["a","b","c"]::-1}}   -> c
{{arrayelement::["a","b","c"]::9}}    -> null
```

## See also

- CBS: [`{{arraylength}}`](arraylength.md), [`{{makearray}}`](makearray.md)
- CBS: [`{{arraypush}}`](arraypush.md), [`{{arraysplice}}`](arraysplice.md)
