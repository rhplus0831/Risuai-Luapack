# CBS: `{{average::...}}`

- Layer: CBS function
- Category: aggregate
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`average`)

Returns the arithmetic mean of a set of numbers.

## Syntax

```text
{{average::a::b::c::...}}
{{average::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | values | yes | One or more numbers, or a single JSON array of values. |

## Behavior

When more than one argument is supplied, the arguments themselves are the list;
when a single argument is supplied it is parsed as a JSON array (`parseArray`)
and its elements are the list. Each value is coerced with `Number`; any value
that is `NaN` is treated as `0`. The function sums the coerced values and divides
by the count of list entries (`val.length`), rendering the result as a
string.

Note the divisor is the number of entries, including any that were coerced to
`0`, so non-numeric entries lower the average without being dropped. With a
single non-array argument the list has length 1.

## Example

```text
{{average::2::4::6}}
```

renders `4`.

## See also

- CBS: [`{{sum}}`](sum.md), [`{{min}}`](min.md), [`{{max}}`](max.md)
