# API: `setFullChatMain(id, value)`

- Layer: Host API (`declareAPI`) — raw form of [`setFullChat`](setFullChat.md)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setFullChatMain', ...)`)

Replaces the entire chat message array from a JSON string. This is the raw
host call; in Lua prefer the [`setFullChat`](setFullChat.md) preamble helper,
which JSON-encodes for you.

## Signature

```lua
setFullChatMain(id, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string | A JSON string encoding an array of message objects. |

## Returns

Nothing.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Behavior

The host runs `JSON.parse(value)` and rebuilds `chat.message` by mapping each
element to only `{ role, data }` — any other fields (such as `time`) are
dropped. Pass an array whose elements carry at least `role` and `data`.
Malformed JSON will throw inside the host.

## Elements used

- [Chat message](../element/chat-message.md) — only `role` and `data` survive
  the rebuild.

## Example

```lua
function onStart(id)
    -- prefer setFullChat; this shows the raw form
    setFullChatMain(id, '[{"role":"char","data":"Reset."}]')
end
```

## See also

- [`setFullChat`](setFullChat.md) (encoded helper — prefer this),
  [`getFullChatMain`](getFullChatMain.md), [`setChat`](setChat.md),
  [`cutChat`](cutChat.md)
- Element: [Chat message](../element/chat-message.md)
