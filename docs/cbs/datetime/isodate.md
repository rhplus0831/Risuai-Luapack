# CBS: `{{isodate}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`isodate`)

Returns the current UTC date (YYYY-MM-DD).

## Syntax

```text
{{isodate}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the current UTC date as `year-month-day` using `getUTCFullYear()`,
`getUTCMonth() + 1` and `getUTCDate()`. The month is **not zero-padded** (the
getters are used directly), so e.g. June 5 is `2026-6-5`, not `2026-06-05`. Use
this for timezone-independent dates; for the viewer's local date use
[`{{messagedate}}`](messagedate.md) (per-message) or [`{{date}}`](date.md).

## Example

```text
UTC date: {{isodate}}
```

## See also

- CBS: [`{{isotime}}`](isotime.md), [`{{date}}`](date.md), [`{{messagedate}}`](messagedate.md)
