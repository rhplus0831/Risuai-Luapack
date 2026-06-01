# CBS: `{{lastmessage}}`

- Layer: CBS function
- Category: history
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`lastmessage`)

Returns the content of the last message in the chat, regardless of role.

## Syntax

```text
{{lastmessage}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the `data` (text content) of the last message in the current chat,
whether that message is from the user or the character. Returns an empty
string if no character is selected. Unlike
[`{{previouscharchat}}`](previouscharchat.md), it does not search by role and
does not fall back to the greeting.

## Example

```text
Last message: {{lastmessage}}
```

## See also

- CBS: [`{{lastmessageid}}`](lastmessageid.md), [`{{previouscharchat}}`](previouscharchat.md), [`{{previoususerchat}}`](previoususerchat.md)
