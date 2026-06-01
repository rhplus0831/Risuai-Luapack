# CBS: `{{contains::s::sub}}`

- **Layer:** CBS function
- **Category:** string
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`contains`)

Tests whether a substring appears anywhere within a string.

## Syntax

```text
{{contains::s::sub}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to search. |
| 2 | `sub` | yes | The substring to look for. |

## Behavior

Returns `"1"` if `sub` occurs anywhere in `s`, `"0"` otherwise. The check is the
literal JavaScript `String.prototype.includes`, so it is **case-sensitive** and
matches bytes exactly. An empty `sub` always yields `"1"`.

Unlike [`{{startswith}}`](startswith.md) / [`{{endswith}}`](endswith.md), the
match may be in the middle of `s`. The `"1"`/`"0"` result composes with
[`{{and}}`](../logic/and.md), [`{{not}}`](../logic/not.md), and `{{#if}}` blocks.

## Example

```text
{{contains::Hello World::lo Wo}}   -> 1
{{contains::Hello World::xyz}}     -> 0
```

## See also

- CBS: [`{{startswith}}`](startswith.md), [`{{endswith}}`](endswith.md)
- CBS: [`{{replace}}`](replace.md)
