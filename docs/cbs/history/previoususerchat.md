# CBS: `{{previoususerchat}}`

- **Layer:** CBS function
- **Category:** history
- **Aliases:** `lastusermessage`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`previoususerchat`)

Returns the most recent user message.

## Syntax

```text
{{previoususerchat}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

When a specific message context is available (`chatID` is not `-1`), searches
backwards through the current chat from just before that position and returns
the `data` of the most recent message with role `user`. If no user message is
found, it falls back to the first message: the character's `firstMessage`, or
the selected alternate greeting when one is active (`chat.fmIndex`). When there
is no message context (`chatID` is `-1`), it returns an **empty string**.

## Example

```text
You said: {{previoususerchat}}
```

## See also

- CBS: [`{{previouscharchat}}`](previouscharchat.md), [`{{lastmessage}}`](lastmessage.md)
- Lua equivalent: [`getUserLastMessage`](../../api/getUserLastMessage.md)
