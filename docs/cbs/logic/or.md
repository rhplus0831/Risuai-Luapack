# CBS: `{{or::a::b}}`

- **Layer:** CBS function
- **Category:** logic
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`or`)

Logical OR of two boolean values.

## Syntax

```text
{{or::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | First boolean, `"1"` or `"0"`. |
| 2 | `b` | yes | Second boolean, `"1"` or `"0"`. |

## Behavior

Returns `"1"` if **either** `a` or `b` is exactly the string `"1"`, otherwise
`"0"`. Any value other than `"1"` is treated as false. The arguments are
typically the `"1"`/`"0"` results of comparison functions. For more than two
inputs, use [`{{any}}`](any.md).

## Example

```text
{{or::1::0}}
```

renders `1`.

## See also

- CBS: [`{{and}}`](and.md), [`{{not}}`](not.md), [`{{any}}`](any.md), [`{{all}}`](all.md)
