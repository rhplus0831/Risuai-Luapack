# CBS: `{{unixtime}}`

- Layer: CBS function
- Category: datetime
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`unixtime`)

Returns the current unix time in seconds.

## Syntax

```text
{{unixtime}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Takes the current time (`new Date()`), divides its millisecond value by 1000 and
returns the result as an integer string via `.toFixed(0)`. The value is the
number of whole seconds since the unix epoch. Unlike
[`{{messageunixtimearray}}`](messageunixtimearray.md) (which reports message
times in milliseconds), this is in seconds.

## Example

```text
Generated at unix {{unixtime}}.
```

## See also

- CBS: [`{{time}}`](time.md), [`{{isotime}}`](isotime.md), [`{{date}}`](date.md)
