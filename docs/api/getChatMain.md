# API: `getChatMain(id, index)`

- **Layer:** Host API (`declareAPI`) — raw form of [`getChat`](getChat.md)
- **Permission tier:** Always available (no guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getChatMain', ...)`)

Returns one chat message as a **JSON string**. This is the raw host call; in Lua
prefer the [`getChat`](getChat.md) preamble helper, which decodes the JSON for
you.

## Signature

```lua
getChatMain(id, index)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored by this call (no permission check). |
| `index` | number | 0-based message index. Resolved with JS `Array.at`, so negative values count from the end (`-1` is the last message). |

## Returns

A **JSON string**. When a message exists at `index`, it is
`JSON.stringify({ role, data, time })` where `time` falls back to `0`. When the
index is out of range, the host returns `JSON.stringify(null)` — the four
characters `null`. Decode with `json.decode` (the helper does this and yields
Lua `nil` for the out-of-range case).

## Permission

This call carries **no guard** — it works with any `id`, including the restricted
edit-display key. See [access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — describes the
  `{ role, data, time }` shape.

## Example

```lua
function onOutput(id)
    local raw = getChatMain(id, -1)   -- JSON string
    local msg = json.decode(raw)      -- or just use getChat(id, -1)
end
```

## See also

- [`getChat`](getChat.md) (decoded helper — prefer this),
  [`getFullChatMain`](getFullChatMain.md), [`getChatLength`](getChatLength.md)
- Element: [Chat message](../element/chat-message.md)
