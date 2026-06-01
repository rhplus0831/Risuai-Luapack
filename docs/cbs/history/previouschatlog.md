# CBS: `{{previouschatlog::index}}`

- **Layer:** CBS function
- **Category:** history
- **Aliases:** `previous_chat_log`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`previouschatlog`)

Returns the content of the message at a given chat index.

## Syntax

```text
{{previouschatlog::index}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `index` | yes | 0-based index into the chat's message list. |

## Behavior

Returns the `data` (text content) of the message at the given **0-based** index
in the current chat. The argument is coerced to a number. If the index is out of
range (or no character/chat is selected), it returns the literal string
`"Out of range"`. The content is returned as stored and is not re-parsed.

## Example

```text
First reply: {{previouschatlog::0}}
Last message: {{previouschatlog::{{lastmessageid}}}}
```

## See also

- CBS: [`{{lastmessageid}}`](lastmessageid.md), [`{{lastmessage}}`](lastmessage.md), [`{{history}}`](history.md)
