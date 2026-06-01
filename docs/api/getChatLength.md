# API: `getChatLength(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getChatLength', ...)`)

Returns the number of messages currently in the chat.

## Signature

```lua
getChatLength(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored by this call (no permission check). |

## Returns

A **number** — `chat.message.length`. Because chat indices are **0-based**, the
last message is at index `length - 1` (or, more conveniently, index `-1` with
the [`getChat`](getChat.md) / [`setChat`](setChat.md) negative-index support).

## Permission

This call carries **no guard** — it works with any `id`, including the restricted
edit-display key. See [access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — counts entries in the message
  array.

## Example

```lua
function onStart(id)
    local n = getChatLength(id)
    log('messages so far: ' .. n)
end
```

## See also

- [`getChat`](getChat.md), [`getFullChat`](getFullChat.md),
  [`addChat`](addChat.md)
- Element: [Chat message](../element/chat-message.md)
