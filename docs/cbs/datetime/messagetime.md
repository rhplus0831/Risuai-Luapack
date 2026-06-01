# CBS: `{{messagetime}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** `message_time`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`messagetime`)

Returns the local time at which the current message was sent (HH:MM:SS).

## Syntax

```text
{{messagetime}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the `time` timestamp of the current message (the message at the current
[`{{chatindex}}`](../context/chatindex.md)) and returns it formatted with
`Date.toLocaleTimeString()`, i.e. the viewer's local time. Returns:

- `00:00:00` during accurate tokenization (`tokenizeAccurate`), so token counts
  stay stable.
- `[Cannot get time]` when there is no message context (`chatID === -1`).
- `[Cannot get time, message was sent in older version]` when the message has no
  stored `time` (messages from old Risu versions).

## Example

```text
Sent at: {{messagetime}}
```

## See also

- CBS: [`{{messagedate}}`](messagedate.md), [`{{time}}`](time.md), [`{{isotime}}`](isotime.md)
- Element: [Chat message](../../element/chat-message.md)
