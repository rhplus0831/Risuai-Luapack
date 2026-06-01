# CBS: `{{role}}`

- Layer: CBS function
- Category: context
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`role`)

Returns the role of the current message.

## Syntax

```text
{{role}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Resolves the role of the message being processed, in this order:

1. If the matcher's `cbsConditions.chatRole` is set, that value is returned.
2. Otherwise, if this is a first-message context (`cbsConditions.firstmsg`), it
   returns `char`.
3. Otherwise, if there is a message index (`chatID !== -1`), it returns that
   message's stored `role` (`user`, `char`, or `system`).
4. As a final fallback it returns the matcher's `role`, or the literal `null`
   if none is set.

Roles correspond to the stored [chat-message](../../element/chat-message.md)
shape, where `user` is the user and `char` is the character/assistant.

## Example

```text
{{#if {{? {{role}} == "user"}}}}(from you){{/if}}
```

## See also

- CBS: [`{{chatindex}}`](chatindex.md), [`{{isfirstmsg}}`](isfirstmsg.md)
- Element: [Chat message](../../element/chat-message.md)
