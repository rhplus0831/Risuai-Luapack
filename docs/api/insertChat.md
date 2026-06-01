# API: `insertChat(id, index, role, value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('insertChat', ...)`)

Inserts a new message at a given index, shifting later messages down.

## Signature

```lua
insertChat(id, index, role, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `index` | number | 0-based index at which to insert. |
| `role` | string | `"user"` stores a user message; **any other value becomes `"char"`** (same coercion as [`addChat`](addChat.md)). |
| `value` | string | The message text. `nil` is coerced to an empty string (`value ?? ''`). |

## Returns

Nothing.

## Behavior

The host runs `chat.message.splice(index, 0, { role, data })` — standard JS
`splice` insertion. The new message is placed *before* whatever currently sits
at `index`; existing messages from `index` onward shift down by one. A negative
`index` counts from the end; an index at or beyond the length appends. Indices
are 0-based.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — the inserted message uses the
  stored shape `{ role = 'user'|'char', data = '<string>' }`.

## Example

```lua
function onStart(id)
    insertChat(id, 0, 'system', 'Scene start.')   -- 'system' becomes 'char'
end
```

## See also

- [`addChat`](addChat.md) (append at the end), [`removeChat`](removeChat.md),
  [`setChat`](setChat.md), [`cutChat`](cutChat.md)
- Element: [Chat message](../element/chat-message.md)
