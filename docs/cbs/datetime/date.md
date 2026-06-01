# CBS: `{{date::format::timestamp}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** `datetimeformat`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`date`)

Formats a date/time with a custom format string.

## Syntax

```text
{{date}}
{{date::format}}
{{date::format::timestamp}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `format` | no | A format string (see tokens below). With no arguments at all, a default date is returned instead. |
| 2 | `timestamp` | no | A unix timestamp in **milliseconds** to format instead of "now". Non-numeric values fall back to the current time. |

## Behavior

With **no arguments**, returns the current local date as `year-month-day`
(`YYYY-M-D`, month and day **not** zero-padded), e.g. `2026-6-5`.

With a `format` argument, the string is passed to Risu's `dateTimeFormat` helper
along with the optional `timestamp` (converted from milliseconds to seconds
internally). The format is applied to the current time, or to `timestamp` if
provided. A leading `:` in the format is stripped, and formats longer than 300
characters return an empty string. Supported tokens (from
`parser.svelte.ts`):

| Token | Meaning |
|-------|---------|
| `YYYY` / `YY` | full / 2-digit year |
| `MMMM` / `MMM` / `MM` | month long / short / 2-digit |
| `DDDD` / `DD` | day-of-year / 2-digit day-of-month |
| `dddd` / `ddd` | weekday long / short |
| `HH` / `hh` | 24-hour / 12-hour (zero-padded) |
| `mm` / `ss` | minutes / seconds (zero-padded) |
| `A` | `AM` / `PM` |
| `X` / `x` | unix seconds / unix milliseconds |

`{{datetimeformat::...}}` is an exact alias.

## Example

```text
{{date}}                              -> 2026-6-5
{{date::YYYY-MM-DD}}                  -> 2026-06-05
{{date::HH:mm:ss::1717200000000}}     -> formats that timestamp
```

## See also

- CBS: [`{{time}}`](time.md), [`{{isodate}}`](isodate.md), [`{{unixtime}}`](unixtime.md)
