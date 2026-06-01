# API: `setChatRole(id, index, value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setChatRole', ...)`)

Changes the role of the message at a given index.

## Signature

```lua
setChatRole(id, index, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `index` | number | 0-based message index. Resolved with JS `Array.at`, so negative values count from the end (`-1` is the last message). |
| `value` | string | `"user"` sets a user message; **any other value becomes `"char"`**. |

## Returns

Nothing.

## Behavior

The host looks up `chat.message.at(index)` and, **only if a message exists
there**, sets `message.role = value === 'user' ? 'user' : 'char'`. If the index
is out of range the call is a silent **no-op**. Only the role changes; the text
(`data`) is untouched (use [`setChat`](setChat.md) for that).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — mutates the `role` field of one
  message.

## Example

```lua
function onStart(id)
    setChatRole(id, -1, 'char')   -- reclassify the last message
end
```

## See also

- [`setChat`](setChat.md) (change text), [`getChat`](getChat.md),
  [`addChat`](addChat.md), [`insertChat`](insertChat.md)
- Element: [Chat message](../element/chat-message.md)
