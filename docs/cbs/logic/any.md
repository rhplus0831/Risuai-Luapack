# CBS: `{{any::...}}`

- **Layer:** CBS function
- **Category:** logic
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`any`)

Logical OR across many values.

## Syntax

```text
{{any::a::b::c::...}}
{{any::["a","b","c"]}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | values | yes | Two or more boolean values, **or** a single JSON array of values. |

## Behavior

Returns `"1"` if **at least one** value is exactly the string `"1"`, otherwise
`"0"`. When more than one argument is supplied, the arguments themselves are the
list; when a single argument is supplied it is parsed as a JSON array and its
elements are the list. This is the multi-input form of [`{{or}}`](or.md).

## Example

```text
{{any::0::1::0}}
```

renders `1`.

## See also

- CBS: [`{{all}}`](all.md), [`{{or}}`](or.md), [`{{and}}`](and.md), [`{{not}}`](not.md)
