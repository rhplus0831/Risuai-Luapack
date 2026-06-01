# CBS: `{{and::a::b}}`

- **Layer:** CBS function
- **Category:** logic
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`and`)

Logical AND of two boolean values.

## Syntax

```text
{{and::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | First boolean, `"1"` or `"0"`. |
| 2 | `b` | yes | Second boolean, `"1"` or `"0"`. |

## Behavior

Returns `"1"` only if **both** `a` and `b` are exactly the string `"1"`,
otherwise `"0"`. Any value other than `"1"` is treated as false. The arguments
are typically the `"1"`/`"0"` results of comparison functions like
[`{{equal}}`](equal.md) or [`{{greater}}`](greater.md). For more than two
inputs, use [`{{all}}`](all.md).

## Example

```text
{{and::1::1}}
```

renders `1`.

## See also

- CBS: [`{{or}}`](or.md), [`{{not}}`](not.md), [`{{all}}`](all.md), [`{{any}}`](any.md)
