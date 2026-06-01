# CBS: `{{spread::array}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`spread`)

Joins a JSON array with `::` so it can be spread into another CBS call's
arguments.

## Syntax

```text
{{spread::array}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string (e.g. `["a","b","c"]`). |

## Behavior

Parses `array` as JSON and joins its elements with the literal separator `::`
(JavaScript `(parseArray(array)).join('::')`). It is a specialized
[`{{join}}`](join.md) whose separator is fixed to `::`. Invalid JSON is treated
as an empty array and yields an empty string.

Because CBS splits a function's arguments on `::`, the output of `{{spread}}` can
be embedded inside another call so the array elements become **separate
arguments**. For example, building an array and spreading it lets a variadic
function such as [`{{makearray}}`](makearray.md) receive each element
individually. (Whether the surrounding parser re-splits the result depends on
how the enclosing template is evaluated.)

## Example

```text
{{spread::["a","b","c"]}}   -> a::b::c
```

## See also

- CBS: [`{{join}}`](join.md), [`{{split}}`](../string/split.md)
- CBS: [`{{makearray}}`](makearray.md), [`{{range}}`](range.md)
