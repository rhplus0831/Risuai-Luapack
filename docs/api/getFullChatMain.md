# API: `getFullChatMain(id)`

- **Layer:** Host API (`declareAPI`) — raw form of [`getFullChat`](getFullChat.md)
- **Permission tier:** Always available (no guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getFullChatMain', ...)`)

Returns the whole chat as a **JSON string**: an array of message objects. This
is the raw host call; in Lua prefer the [`getFullChat`](getFullChat.md) preamble
helper, which decodes the JSON for you.

## Signature

```lua
getFullChatMain(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored by this call (no permission check). |

## Returns

A **JSON string** — `JSON.stringify` of `chat.message` mapped to
`{ role, data, time }` per message, with `time` falling back to `0`. Decode with
`json.decode` (the helper does this for you).

## Permission

This call carries **no guard** — it works with any `id`, including the restricted
edit-display key. See [access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — each array element uses the
  `{ role, data, time }` shape.

## Example

```lua
function onOutput(id)
    local raw = getFullChatMain(id)   -- JSON string
    local all = json.decode(raw)      -- or just use getFullChat(id)
end
```

## See also

- [`getFullChat`](getFullChat.md) (decoded helper — prefer this),
  [`getChatMain`](getChatMain.md), [`setFullChatMain`](setFullChatMain.md)
- Element: [Chat message](../element/chat-message.md)
