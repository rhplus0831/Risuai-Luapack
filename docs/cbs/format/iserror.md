# CBS: `{{iserror::s}}`

- **Layer:** CBS function
- **Category:** format
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`iserror`)

Tests whether a string looks like an error message.

## Syntax

```text
{{iserror::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to test. |

## Behavior

Lower-cases `s` and returns `"1"` if it starts with `"error:"`, otherwise `"0"`.
The match is case-insensitive (it lower-cases before comparing), so
`Error: failed`, `ERROR: x`, and `error: y` all return `"1"`. The colon is part
of the prefix — a string starting with just `error ` (no colon) returns `"0"`.

This is handy for branching on the result of a call that returns an `error:`
string on failure (for example, low-level request helpers).

## Example

```text
{{#when::var::lastResult}}{{iserror::{{getvar::lastResult}}}}{{/when}}
```

returns `"1"` when the stored result begins with `error:`.

## See also

- CBS: [`{{startswith}}`](../string/startswith.md), [`{{contains}}`](../string/contains.md)
- Block: [`{{#when ...}}`](../blocks/when.md)
