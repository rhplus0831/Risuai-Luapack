# CBS: `{{lorebook}}`

- Layer: CBS function
- Category: history
- Aliases: `worldinfo`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`lorebook`)

Returns all active lorebook entries as a JSON array.

## Syntax

```text
{{lorebook}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Collects the active lorebook (world info) entries and returns them as a JSON
array, where each element is a JSON-stringified entry object. The combined set
is the character lorebook (`globalLore`, empty for group chats), followed by
the chat-specific lorebook (`chat.localLore`), followed by the active module
lorebooks. Entries are returned as stored; their fields are not CBS-parsed here.

## Example

```text
{{lorebook}}
```

## See also

- Element: [Lorebook entry](../../element/lorebook-entry.md)
- CBS: [`{{history}}`](history.md)
