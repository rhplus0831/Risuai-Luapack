# API: `setChat(id, index, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setChat', ...)`)

Replaces the text of the message at a given index.

## Signature

```lua
setChat(id, index, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `index` | number | 0-based message index. Resolved with JS `Array.at`, so negative values count from the end (`-1` is the last message). |
| `value` | string | The replacement text. `nil` is coerced to an empty string (`value ?? ''`). |

## Returns

Nothing.

## Behavior

The host looks up `chat.message.at(index)` and, only if a message exists
there, sets `message.data = value ?? ''`. If the index is out of range the
call is a silent no-op — it does not insert or extend the array. Only the
message text (`data`) changes; the role is untouched (use
[`setChatRole`](setChatRole.md) for that).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — mutates the `data` field of one
  message.

## Example

```lua
function onStart(id)
    local last = getChat(id, -1)
    if last then
        setChat(id, -1, last.data .. '\n\n(directive applied)')
    end
end
```

## See also

- [`setChatRole`](setChatRole.md) (change role), [`getChat`](getChat.md),
  [`addChat`](addChat.md), [`insertChat`](insertChat.md),
  [`removeChat`](removeChat.md)
- Element: [Chat message](../element/chat-message.md)
