# CBS: `{{endswith::s::sub}}`

- Layer: CBS function
- Category: string
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`endswith`)

Tests whether a string ends with a given substring.

## Syntax

```text
{{endswith::s::sub}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to test. |
| 2 | `sub` | yes | The suffix to look for. |

## Behavior

Returns `"1"` if `s` ends with `sub`, `"0"` otherwise. The check is the literal
JavaScript `String.prototype.endsWith`, so it is case-sensitive and matches
bytes exactly. An empty `sub` always yields `"1"`.

The result is the same `"1"`/`"0"` shape used by the comparison and logic CBS
functions, so it composes directly with [`{{and}}`](../logic/and.md),
[`{{not}}`](../logic/not.md), and `{{#if}}` blocks.

## Example

```text
{{endswith::Hello World::World}}   -> 1
{{endswith::Hello World::world}}   -> 0
```

## See also

- CBS: [`{{startswith}}`](startswith.md), [`{{contains}}`](contains.md)
- CBS: [`{{equal}}`](../logic/equal.md)
