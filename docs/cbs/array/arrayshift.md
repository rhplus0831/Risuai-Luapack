# CBS: `{{arrayshift::array}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`arrayshift`)

Returns a JSON array with its first element removed.

## Syntax

```text
{{arrayshift::array}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b","c"]`). |

## Behavior

Parses `array` as JSON, removes the first element (JavaScript
`Array.prototype.shift`), and returns the remaining elements as a JSON array
string. The removed element is discarded, not returned. An empty or invalid
array yields `[]`.

This produces a **new** array string for use downstream; it does not write back
to any variable. To persist the result, pass it to
[`{{setvar}}`](../variables/setvar.md).

## Example

```text
{{arrayshift::["a","b","c"]}}   -> ["b","c"]
```

## See also

- CBS: [`{{arraypop}}`](arraypop.md), [`{{arraypush}}`](arraypush.md)
- CBS: [`{{arraysplice}}`](arraysplice.md), [`{{arrayelement}}`](arrayelement.md)
