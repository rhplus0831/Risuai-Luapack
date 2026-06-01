# CBS: `{{history}}` / `{{history::role}}`

- Layer: CBS function
- Category: history
- Aliases: `messages`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`history`)

Returns the chat history as a JSON array.

## Syntax

```text
{{history}}
{{history::role}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `role` | no | The literal word `role`. When present, each item is prefixed with `role: `. |

## Behavior

With no arguments, returns a JSON array of full message objects. The first
message (the character's `firstMessage`, or the selected alternate greeting when
`chat.fmIndex` is set) is prepended to the chat's messages, and each object's
`data` is run through Risu's chat parser before serialization.

When called with the literal `role` argument, returns a JSON array of strings
instead: each message is rendered as `role: data` (the message's role, then a
colon and space, then its content). In this form the first message/greeting is
not prepended -- only `chat.message` entries are included, and their data is
returned as stored (not re-parsed).

## Example

```text
{{history}}
{{history::role}}
```

## See also

- Element: [Chat message](../../element/chat-message.md)
- CBS: [`{{userhistory}}`](userhistory.md), [`{{charhistory}}`](charhistory.md), [`{{previouschatlog}}`](previouschatlog.md)
