# API: `removeChat(id, index)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('removeChat', ...)`)

Removes a single message from the chat.

## Signature

```lua
removeChat(id, index)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `index` | number | 0-based index of the message to remove. |

## Returns

Nothing.

## Behavior

The host runs `chat.message.splice(index, 1)` — standard JS `splice` semantics.
The element at `index` is removed and later messages shift down by one. A
negative `index` counts from the end. An out-of-range positive index removes
nothing. Indices are 0-based.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — removes one entry from the
  message array.

## Example

```lua
function onStart(id)
    removeChat(id, getChatLength(id) - 1)   -- drop the last message
end
```

## See also

- [`cutChat`](cutChat.md) (keep a range), [`insertChat`](insertChat.md) (add),
  [`setChat`](setChat.md) (edit text)
- Element: [Chat message](../element/chat-message.md)
