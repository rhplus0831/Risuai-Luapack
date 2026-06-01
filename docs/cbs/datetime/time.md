# CBS: `{{time}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`time`)

Returns the current local time.

## Syntax

```text
{{time}}
{{time::format::timestamp}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `format` | no | A date/time format string (same tokens as [`{{date}}`](date.md)). |
| 2 | `timestamp` | no | A unix timestamp in **milliseconds** to format instead of "now". Non-numeric values are treated as `0` (now). |

## Behavior

With **no arguments**, returns the current local clock as
`hours:minutes:seconds` using the raw `Date` getters, so the parts are **not
zero-padded** (e.g. `9:5:3`, not `09:05:03`).

`cbs.ts` registers two functions under the name `time`; the later registration
wins, so `{{time}}` also accepts the same arguments as
[`{{date}}`](date.md): with a `format` argument it formats the current time (or
the optional millisecond `timestamp`) through Risu's `dateTimeFormat`, which
supports tokens such as `HH`, `hh`, `mm`, `ss`, and `A`. Those formatted tokens
**are** zero-padded; only the no-argument form is unpadded.

## Example

```text
{{time}}                    -> 9:5:3
{{time::HH:mm:ss}}          -> 09:05:03
```

## See also

- CBS: [`{{date}}`](date.md), [`{{isotime}}`](isotime.md), [`{{unixtime}}`](unixtime.md)
