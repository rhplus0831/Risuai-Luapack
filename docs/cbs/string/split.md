# CBS: `{{split::s::delim}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`split`)

Splits a string on a delimiter and returns the parts as a JSON array.

## Syntax

```text
{{split::s::delim}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to split. |
| 2 | `delim` | yes | The delimiter to split on. |

## Behavior

Returns a JSON array string built from `s.split(delim)` (JavaScript
`String.prototype.split`). Each piece between delimiters becomes one element, in
order; consecutive delimiters produce empty-string elements. The result is a
**JSON array string** (e.g. `["a","b"]`), the same representation consumed by the
array CBS functions such as [`{{arrayelement}}`](../array/arrayelement.md) and
[`{{arraylength}}`](../array/arraylength.md).

`{{split}}` is the inverse of [`{{join}}`](../array/join.md): splitting on a
delimiter and joining the result with the same delimiter reproduces the
original string.

## Example

```text
{{split::apple,banana,cherry::,}}   -> ["apple","banana","cherry"]
```

## See also

- CBS: [`{{join}}`](../array/join.md), [`{{spread}}`](../array/spread.md)
- CBS: [`{{arraylength}}`](../array/arraylength.md), [`{{arrayelement}}`](../array/arrayelement.md)
- CBS: [`{{replace}}`](replace.md)
