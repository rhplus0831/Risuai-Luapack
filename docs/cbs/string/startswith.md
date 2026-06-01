# CBS: `{{startswith::s::sub}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`startswith`)

Tests whether a string begins with a given substring.

## Syntax

```text
{{startswith::s::sub}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to test. |
| 2 | `sub` | yes | The prefix to look for. |

## Behavior

Returns `"1"` if `s` starts with `sub`, `"0"` otherwise. The check is the literal
JavaScript `String.prototype.startsWith`, so it is **case-sensitive** and matches
bytes exactly. An empty `sub` always yields `"1"`.

The result is the same `"1"`/`"0"` shape used by the comparison and logic CBS
functions, so it composes directly with [`{{and}}`](../logic/and.md),
[`{{not}}`](../logic/not.md), and `{{#if}}` blocks.

## Example

```text
{{startswith::Hello World::Hello}}   -> 1
{{startswith::Hello World::hello}}   -> 0
```

## See also

- CBS: [`{{endswith}}`](endswith.md), [`{{contains}}`](contains.md)
- CBS: [`{{equal}}`](../logic/equal.md)
