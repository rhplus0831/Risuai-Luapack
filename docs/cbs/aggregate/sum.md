# CBS: `{{sum::...}}`

- **Layer:** CBS function
- **Category:** aggregate
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`sum`)

Adds up a set of numbers.

## Syntax

```text
{{sum::a::b::c::...}}
{{sum::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | values | yes | One or more numbers, **or** a single JSON array of values. |

## Behavior

When more than one argument is supplied, the arguments themselves are the list;
when a single argument is supplied it is parsed as a JSON array (`parseArray`)
and its elements are the list. Each value is coerced with `Number`; any value
that is `NaN` is treated as `0`. The coerced values are reduced with addition
starting from `0`, and the total is rendered as a string.

Non-numeric entries contribute `0` rather than aborting the sum.

## Example

```text
{{sum::1::2::3}}
```

renders `6`.

## See also

- CBS: [`{{average}}`](average.md), [`{{min}}`](min.md), [`{{max}}`](max.md)
