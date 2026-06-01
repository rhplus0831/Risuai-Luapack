# CBS: `{{isotime}}`

- Layer: CBS function
- Category: datetime
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`isotime`)

Returns the current UTC time (HH:MM:SS).

## Syntax

```text
{{isotime}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the current time in UTC using the `getUTCHours()`, `getUTCMinutes()` and
`getUTCSeconds()` getters, joined as `hours:minutes:seconds`. Because the raw
getters are used, the components are not zero-padded despite the
"HH:MM:SS" shorthand (e.g. `7:4:9`). Use this for timezone-independent
timestamps; for the viewer's local clock use [`{{time}}`](time.md).

## Example

```text
UTC now: {{isotime}}
```

## See also

- CBS: [`{{isodate}}`](isodate.md), [`{{time}}`](time.md), [`{{unixtime}}`](unixtime.md)
