# CBS: `{{not::a}}`

- **Layer:** CBS function
- **Category:** logic
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`not`)

Logical NOT of a boolean value.

## Syntax

```text
{{not::a}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | A boolean, `"1"` or `"0"`. |

## Behavior

Returns `"0"` if `a` is exactly the string `"1"`, and `"1"` for any other value.
This inverts the boolean state: a true (`"1"`) becomes false (`"0"`), and
anything that is not `"1"` (including `"0"` and arbitrary text) becomes `"1"`.

## Example

```text
{{not::1}}
```

renders `0`.

## See also

- CBS: [`{{and}}`](and.md), [`{{or}}`](or.md), [`{{notequal}}`](notequal.md)
