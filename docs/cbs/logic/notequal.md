# CBS: `{{notequal::a::b}}`

- Layer: CBS function
- Category: logic
- Aliases: `not_equal`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`notequal`)

Tests two values for string inequality.

## Syntax

```text
{{notequal::a::b}}
{{not_equal::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | First value. |
| 2 | `b` | yes | Second value. |

## Behavior

Compares `a` and `b` with strict string inequality (`!==`) and returns `"1"` if
they differ, `"0"` if they are identical. The comparison is on the raw strings,
so it is case-sensitive and does not coerce numbers. This is the inverse of
[`{{equal}}`](equal.md).

## Example

```text
{{notequal::yes::no}}
```

renders `1`.

## See also

- CBS: [`{{equal}}`](equal.md), [`{{not}}`](not.md), [`{{greater}}`](greater.md), [`{{less}}`](less.md)
