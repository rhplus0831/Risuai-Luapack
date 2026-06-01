# CBS: `{{messagedate}}`

- **Layer:** CBS function
- **Category:** datetime
- **Aliases:** `message_date`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`messagedate`)

Returns the local date on which the current message was sent.

## Syntax

```text
{{messagedate}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the `time` timestamp of the current message (the message at the current
[`{{chatindex}}`](../context/chatindex.md)) and returns it formatted with
`Date.toLocaleDateString()`, i.e. the viewer's local date. Returns:

- `00:00:00` during accurate tokenization (`tokenizeAccurate`).
- `[Cannot get time]` when there is no message context (`chatID === -1`).
- `[Cannot get time, message was sent in older version]` when the message has no
  stored `time`.

## Example

```text
Sent on: {{messagedate}}
```

## See also

- CBS: [`{{messagetime}}`](messagetime.md), [`{{isodate}}`](isodate.md), [`{{date}}`](date.md)
- Element: [Chat message](../../element/chat-message.md)
