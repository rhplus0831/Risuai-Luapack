# API: `getFullChat(id)`

- **Layer:** Preamble helper (wraps [`getFullChatMain`](getFullChatMain.md))
- **Permission tier:** Always available (inherits `getFullChatMain`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper`, `function getFullChat`)

Returns the whole chat as a decoded Lua array of `{role, data, time}` tables.

## Signature

```lua
getFullChat(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored (the underlying `getFullChatMain` has no permission check). |

## Returns

A Lua **array** (1-based table) of
`{ role = 'user'|'char', data = '<string>', time = <number> }` entries, in chat
order. This is a thin wrapper: the helper calls `getFullChatMain(id)` and runs
`json.decode` on the result. Note the array itself is 1-based in Lua, but the
underlying message **indices** used by [`getChat`](getChat.md) /
[`setChat`](setChat.md) are 0-based.

## Permission

No guard — see [`getFullChatMain`](getFullChatMain.md) and
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — each element uses the
  `{ role, data, time }` shape.

## Example

```lua
function onOutput(id)
    local all = getFullChat(id)
    for _, msg in ipairs(all) do
        log(msg.role .. ': ' .. msg.data)
    end
end
```

## See also

- [`getFullChatMain`](getFullChatMain.md) (raw form), [`getChat`](getChat.md),
  [`setFullChat`](setFullChat.md), [`getChatLength`](getChatLength.md)
- Element: [Chat message](../element/chat-message.md)
