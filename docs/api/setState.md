# API: `setState(id, name, value)`

- **Layer:** Preamble helper (wraps [`setChatVar`](setChatVar.md))
- **Permission tier:** Safe or edit-display (inherits `setChatVar`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper`, `function setState`)

Writes a JSON-encoded "state" value into a `__`-prefixed chat variable.

## Signature

```lua
setState(id, name, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds` **or** `ScriptingEditDisplayIds` (checked by the underlying `setChatVar`). |
| `name` | string | The state name. Stored under the chat variable `'__' .. name`. |
| `value` | any | Any JSON-encodable Lua value (table, number, boolean, string). |

## Returns

Nothing.

## Behavior

This is a thin wrapper: the helper calls
`setChatVar(id, '__' .. name, json.encode(value))`. Because it routes through
`setChatVar`, it accepts **either** the safe tier or the edit-display tier, so it
works from an [`editDisplay`](../hooks/editDisplay.md) listener as well as the
normal modes. Read it back with [`getState`](getState.md).

## Permission

Safe-or-edit-display — no-ops unless `id` is in `ScriptingSafeIds` or
`ScriptingEditDisplayIds`. See [access key & tiers](../element/access-key.md).

## Elements used

- [Chat variables](../element/chat-variables.md) — state is stored as a
  `__`-prefixed chat variable.

## Example

```lua
function onOutput(id)
    setState(id, 'flags', { greeted = true, count = 3 })
end
```

## See also

- [`getState`](getState.md) (read), [`setChatVar`](setChatVar.md) (raw string
  write)
- Element: [Chat variables](../element/chat-variables.md)
