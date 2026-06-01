# CBS: `{{messageidleduration}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** `message_idle_duration`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`messageidleduration`)

Returns the elapsed time between the current user message and the previous user
message (HH:MM:SS).

## Syntax

```text
{{messageidleduration}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Starting at the current message index, scans backwards to find the two most
recent messages whose `role` is `user`, then returns the difference of their
`time` timestamps formatted as `H:MM:SS` (hours unpadded, minutes and seconds
zero-padded). Returns:

- `00:00:00` during accurate tokenization (`tokenizeAccurate`).
- `[Cannot get time]` when there is no message context (`chatID === -1`).
- `[No user message found]` if no user message exists at or before the current
  index.
- `[No previous user message found]` if only one user message is found.
- `[Cannot get time, message was sent in older version]` (or `... previous
  message ...`) when either user message has no stored `time`.

## Example

```text
Time since your last message: {{messageidleduration}}
```

## See also

- CBS: [`{{idleduration}}`](idleduration.md), [`{{messagetime}}`](messagetime.md)
- Element: [Chat message](../../element/chat-message.md)
