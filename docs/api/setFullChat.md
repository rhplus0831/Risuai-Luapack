# API: `setFullChat(id, value)`

- **Layer:** Preamble helper (wraps [`setFullChatMain`](setFullChatMain.md))
- **Permission tier:** Safe (inherits `setFullChatMain`; blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper`, `function setFullChat`)

Replaces the entire chat from a Lua array of `{role, data}` tables.

## Signature

```lua
setFullChat(id, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds` (checked by the underlying `setFullChatMain`). |
| `value` | table | A Lua array (1-based) of `{ role = '...', data = '...' }` message tables. |

## Returns

Nothing.

## Behavior

This is a thin wrapper: the helper calls `setFullChatMain(id, json.encode(value))`.
The host then rebuilds `chat.message` keeping **only** `role` and `data` per
message (any `time` or other field is dropped). Roles are stored as-is by the
JSON round-trip; supply `'user'` or `'char'` (the host does not re-coerce here,
so an unexpected role string is stored verbatim).

## Permission

Safe tier — no-ops unless `id` is in `ScriptingSafeIds`, so it is **not**
available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — only `role` and `data` are kept.

## Example

```lua
function onStart(id)
    setFullChat(id, {
        { role = 'char', data = 'Welcome back.' },
        { role = 'user', data = 'Hi!' },
    })
end
```

## See also

- [`setFullChatMain`](setFullChatMain.md) (raw form),
  [`getFullChat`](getFullChat.md), [`setChat`](setChat.md),
  [`cutChat`](cutChat.md)
- Element: [Chat message](../element/chat-message.md)
