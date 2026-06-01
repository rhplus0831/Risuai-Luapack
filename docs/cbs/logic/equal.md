# CBS: `{{equal::a::b}}`

- Layer: CBS function
- Category: logic
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`equal`)

Tests two values for exact string equality.

## Syntax

```text
{{equal::a::b}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `a` | yes | First value. |
| 2 | `b` | yes | Second value. |

## Behavior

Compares `a` and `b` with strict string equality (`===`) and returns `"1"` if
they are identical, `"0"` otherwise. The comparison is on the raw strings, so it
is case-sensitive and does not coerce numbers (e.g. `1` and `1.0` are not
equal). For the inverse, use [`{{notequal}}`](notequal.md).

## Example

```text
{{equal::yes::yes}}
```

renders `1`.

## See also

- CBS: [`{{notequal}}`](notequal.md), [`{{greater}}`](greater.md), [`{{less}}`](less.md), [`{{and}}`](and.md)
