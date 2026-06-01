# API: `getState(id, name)`

- **Layer:** Preamble helper (wraps [`getChatVar`](getChatVar.md))
- **Permission tier:** Always available (inherits `getChatVar`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper`, `function getState`)

Reads a JSON-decoded "state" value stored in a `__`-prefixed chat variable.

## Signature

```lua
getState(id, name)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored (the underlying `getChatVar` has no permission check). |
| `name` | string | The state name. Stored under the chat variable `'__' .. name`. |

## Returns

Any JSON-decodable Lua value — `json.decode(getChatVar(id, '__' .. name))`.
A state that was never written reads back through `getChatVar` as the string
`"null"`, which `json.decode` turns into Lua `nil`. So an unset state is `nil`,
and you can round-trip tables, numbers, booleans, and strings via
[`setState`](setState.md).

## Permission

No guard — see [`getChatVar`](getChatVar.md) and
[access key & tiers](../element/access-key.md). Because it reads a plain chat
var, it works from every mode including [`editDisplay`](../hooks/editDisplay.md).

## Elements used

- [Chat variables](../element/chat-variables.md) — state is stored as a
  `__`-prefixed chat variable.

## Example

```lua
function onStart(id)
    local s = getState(id, 'inventory') or {}
    s.gold = (s.gold or 0) + 10
    setState(id, 'inventory', s)
end
```

## See also

- [`setState`](setState.md) (write), [`getChatVar`](getChatVar.md) (raw string
  read)
- Element: [Chat variables](../element/chat-variables.md)
