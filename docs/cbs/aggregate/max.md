# CBS: `{{max::...}}`

- Layer: CBS function
- Category: aggregate
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`max`)

Returns the largest of a set of numbers.

## Syntax

```text
{{max::a::b::c::...}}
{{max::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | values | yes | Two or more numbers, or a single JSON array of values. |

## Behavior

When more than one argument is supplied, the arguments themselves are the list;
when a single argument is supplied it is parsed as a JSON array (`parseArray`)
and its elements are the list. Each value is coerced with `Number`; any value
that is `NaN` is treated as `0`. The result is `Math.max(...)` over the coerced
values, rendered as a string.

Because non-numeric entries become `0`, a list of only negative numbers mixed
with a non-number can return `0`.

## Example

```text
{{max::5::2::8}}
```

renders `8`.

## See also

- CBS: [`{{min}}`](min.md), [`{{sum}}`](sum.md), [`{{average}}`](average.md)
