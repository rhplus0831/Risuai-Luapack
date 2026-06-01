# CBS: `{{all::...}}`

- Layer: CBS function
- Category: logic
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`all`)

Logical AND across many values.

## Syntax

```text
{{all::a::b::c::...}}
{{all::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | values | yes | Two or more boolean values, or a single JSON array of values. |

## Behavior

Returns `"1"` only if every value is exactly the string `"1"`, otherwise
`"0"`. When more than one argument is supplied, the arguments themselves are the
list; when a single argument is supplied it is parsed as a JSON array and its
elements are the list. Any element other than `"1"` makes the result `"0"`. This
is the multi-input form of [`{{and}}`](and.md).

## Example

```text
{{all::1::1::1}}
```

renders `1`.

## See also

- CBS: [`{{any}}`](any.md), [`{{and}}`](and.md), [`{{or}}`](or.md), [`{{not}}`](not.md)
