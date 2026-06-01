# CBS: `{{idleduration}}`

- Layer: CBS function
- Category: datetime
- Aliases: `idle_duration`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`idleduration`)

Returns the time elapsed since the last message in the chat (HH:MM:SS).

## Syntax

```text
{{idleduration}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Takes the last message in the current chat (any role) and returns the
difference between the current time (`new Date()`) and that message's `time`,
formatted as `H:MM:SS` (hours unpadded, minutes and seconds zero-padded).
Because it is measured against "now", the result grows the longer the chat sits
idle. Returns:

- `00:00:00` during accurate tokenization (`tokenizeAccurate`).
- `00:00:00` when the chat has no messages.
- `[Cannot get time, message was sent in older version]` when the last message
  has no stored `time`.

Unlike [`{{messageidleduration}}`](messageidleduration.md), which compares two
user messages, this measures from the very last message to the present moment.

## Example

```text
You have been away for {{idleduration}}.
```

## See also

- CBS: [`{{messageidleduration}}`](messageidleduration.md), [`{{unixtime}}`](unixtime.md)
- Element: [Chat message](../../element/chat-message.md)
