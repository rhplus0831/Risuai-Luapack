# CBS: `{{lastmessageid}}`

- Layer: CBS function
- Category: history
- Aliases: `lastmessageindex`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`lastmessageid`)

Returns the 0-based index of the last message in the chat.

## Syntax

```text
{{lastmessageid}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the index of the last message in the current chat as a string, using
0-based indexing (`chat.message.length - 1`). Returns an empty string if
no character is selected. Use this with [`{{previouschatlog::index}}`](previouschatlog.md)
to read a specific message by index.

## Example

```text
{{previouschatlog::{{lastmessageid}}}}
```

## See also

- CBS: [`{{lastmessage}}`](lastmessage.md), [`{{previouschatlog}}`](previouschatlog.md)
