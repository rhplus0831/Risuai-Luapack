# CBS: `{{arraypop::array}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`arraypop`)

Returns a JSON array with its last element removed.

## Syntax

```text
{{arraypop::array}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b","c"]`). |

## Behavior

Parses `array` as JSON, removes the last element (JavaScript
`Array.prototype.pop`), and returns the remaining elements as a JSON array
string. The removed element is discarded, not returned. An empty or invalid
array yields `[]`.

This produces a **new** array string for use downstream; it does not write back
to any variable. To persist the result, pass it to
[`{{setvar}}`](../variables/setvar.md).

## Example

```text
{{arraypop::["a","b","c"]}}   -> ["a","b"]
```

## See also

- CBS: [`{{arrayshift}}`](arrayshift.md), [`{{arraypush}}`](arraypush.md)
- CBS: [`{{arraysplice}}`](arraysplice.md), [`{{arrayelement}}`](arrayelement.md)
