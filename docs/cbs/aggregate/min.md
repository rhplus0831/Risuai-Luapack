# CBS: `{{min::...}}`

- Layer: CBS function
- Category: aggregate
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`min`)

Returns the smallest of a set of numbers.

## Syntax

```text
{{min::a::b::c::...}}
{{min::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | values | yes | Two or more numbers, or a single JSON array of values. |

## Behavior

When more than one argument is supplied, the arguments themselves are the list;
when a single argument is supplied it is parsed as a JSON array (`parseArray`)
and its elements are the list. Each value is coerced with `Number`; any value
that is `NaN` is treated as `0`. The result is `Math.min(...)` over the coerced
values, rendered as a string.

Because non-numeric entries become `0`, a stray non-number can pull the minimum
down to `0`.

## Example

```text
{{min::5::2::8}}
```

renders `2`.

## See also

- CBS: [`{{max}}`](max.md), [`{{sum}}`](sum.md), [`{{average}}`](average.md)
