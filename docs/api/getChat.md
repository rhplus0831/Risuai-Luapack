# API: `getChat(id, index)`

- **Layer:** Preamble helper (wraps [`getChatMain`](getChatMain.md))
- **Permission tier:** Always available (inherits `getChatMain`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper`, `function getChat`)

Returns one chat message as a decoded Lua table `{role, data, time}`.

## Signature

```lua
getChat(id, index)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored (the underlying `getChatMain` has no permission check). |
| `index` | number | 0-based message index. Negative values count from the end like JS `Array.at`; `getChat(id, -1)` returns the last message. |

## Returns

A Lua **table** `{ role = 'user'|'char', data = '<string>', time = <number> }`.
This is a thin wrapper: the helper calls `getChatMain(id, index)` and runs
`json.decode` on the result. For an out-of-range index the raw call returns the
JSON string `null`, so the helper returns Lua `nil` — always guard with
`if msg then ...`.

## Permission

No guard — see [`getChatMain`](getChatMain.md) and
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — the `{ role, data, time }` shape
  this helper produces.

## Example

```lua
function onStart(id)
    local last = getChat(id, -1)
    if last and last.role == 'user' then
        setChat(id, -1, last.data .. ' (edited)')
    end
end
```

## See also

- [`getChatMain`](getChatMain.md) (raw form), [`getFullChat`](getFullChat.md),
  [`setChat`](setChat.md), [`getChatLength`](getChatLength.md)
- Element: [Chat message](../element/chat-message.md)
