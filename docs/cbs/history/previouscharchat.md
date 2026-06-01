# CBS: `{{previouscharchat}}`

- Layer: CBS function
- Category: history
- Aliases: `lastcharmessage`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`previouscharchat`)

Returns the most recent character message, falling back to the greeting.

## Syntax

```text
{{previouscharchat}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Searches backwards through the current chat from the current message position
(or from the last message when there is no specific message context) and returns
the `data` of the most recent message with role `char`. If no character message
is found, it falls back to the first message: the character's `firstMessage`, or
the selected alternate greeting when one is active (`chat.fmIndex`).

## Example

```text
Last thing {{char}} said: {{previouscharchat}}
```

## See also

- CBS: [`{{previoususerchat}}`](previoususerchat.md), [`{{lastmessage}}`](lastmessage.md)
- Lua equivalent: [`getCharacterLastMessage`](../../api/getCharacterLastMessage.md)
