# CBS: `{{arraylength::array}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`arraylength`)

Returns the number of elements in a JSON array.

## Syntax

```text
{{arraylength::array}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b","c"]`). |

## Behavior

Parses `array` as JSON and returns its element count (`.length`) as a string.
Parsing is forgiving: if `array` is not valid JSON it is treated as an empty
array, so the result is `"0"` rather than an error. This is the array
counterpart of the string-character count [`{{length}}`](../string/length.md).

## Example

```text
{{arraylength::["a","b","c"]}}   -> 3
{{arraylength::not json}}        -> 0
```

## See also

- CBS: [`{{arrayelement}}`](arrayelement.md), [`{{makearray}}`](makearray.md)
- CBS: [`{{length}}`](../string/length.md)
