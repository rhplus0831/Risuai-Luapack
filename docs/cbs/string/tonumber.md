# CBS: `{{tonumber::s}}`

- Layer: CBS function
- Category: string
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`tonumber`)

Strips everything except digits and decimal points from a string.

## Syntax

```text
{{tonumber::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to filter. |

## Behavior

Walks `s` character by character and keeps only the characters that are digits
(a single character that is not `NaN` when passed to `Number`) and the literal
`.`; every other character is dropped. The kept characters are concatenated, in
their original order, and returned as a string.

This is a filter, not a numeric parse: it does not evaluate or normalize the
result. A string containing several separated numbers or multiple `.` characters
will keep all of the digits and dots, so the output is not guaranteed to be a
valid number (e.g. `{{tonumber::1.2.3}}` -> `1.2.3`). For arithmetic, feed the
result into [`{{calc}}`](../math/calc.md).

## Example

```text
{{tonumber::abc123.45def}}   -> 123.45
```

## See also

- CBS: [`{{calc}}`](../math/calc.md), [`{{round}}`](../math/round.md)
- CBS: [`{{replace}}`](replace.md)
