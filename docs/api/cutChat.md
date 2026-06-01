# API: `cutChat(id, start, end)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('cutChat', ...)`)

Trims the chat to a contiguous range of messages.

## Signature

```lua
cutChat(id, start, end)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `start` | number | 0-based start index (inclusive). |
| `end` | number | 0-based end index (exclusive). |

## Returns

Nothing.

## Behavior

The host runs `chat.message = chat.message.slice(start, end)`, so it keeps the
half-open range `[start, end)` — `start` is kept, `end` is not. JS `slice`
semantics apply: indices clamp to the array bounds and negative values count
from the end. Omitting/over-shooting `end` keeps through the last message. The
message indices are 0-based.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — replaces the message array with a
  slice of itself.

## Example

```lua
function onStart(id)
    -- keep only the last 10 messages
    local n = getChatLength(id)
    cutChat(id, math.max(0, n - 10), n)
end
```

## See also

- [`removeChat`](removeChat.md) (drop one message),
  [`setFullChat`](setFullChat.md) (replace all), [`getChatLength`](getChatLength.md)
- Element: [Chat message](../element/chat-message.md)
