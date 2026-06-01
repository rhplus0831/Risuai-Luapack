# CBS: `{{messageunixtimearray}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** `message_unixtime_array`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`messageunixtimearray`)

Returns every message timestamp in the current chat as a JSON array.

## Syntax

```text
{{messageunixtimearray}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Maps over every message in the current chat and emits its `time` value (a unix
timestamp in **milliseconds**) as a JSON array built with Risu's `makeArray`
helper. Messages that have no stored `time` (sent in older Risu versions) appear
as `0`. The order matches the chat's message order, so element index `i`
corresponds to message index `i`.

## Example

```text
{{messageunixtimearray}}
```

Produces something like `["1717200000000","1717200042000","0"]`.

## See also

- CBS: [`{{messagetime}}`](messagetime.md), [`{{unixtime}}`](unixtime.md)
- Element: [Chat message](../../element/chat-message.md)
