# API: `setChatVar(id, key, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe or edit-display
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setChatVar', ...)`)

Writes a persistent chat variable.

## Signature

```lua
setChatVar(id, key, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds` or `ScriptingEditDisplayIds`. |
| `key` | string | The chat-variable name to write. |
| `value` | string | The value to store. Persisted in the chat's `scriptstate`. |

## Returns

Nothing.

## Permission

Unusually for a mutating call, `setChatVar` accepts either tier: the guard
is `ScriptingSafeIds.has(id) || ScriptingEditDisplayIds.has(id)`. It is therefore
the one write available from an [`editDisplay`](../hooks/editDisplay.md)
listener, which holds only the restricted edit-display key and cannot mutate
chat or character data. It of course also works from every safe-tier mode. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat variables](../element/chat-variables.md) — the chat-scoped store this
  writes into.

## Example

```lua
function onOutput(id)
    setChatVar(id, 'turns', tostring(getChatLength(id)))
end
```

## See also

- [`getChatVar`](getChatVar.md) (read), [`setState`](setState.md)
  (JSON-encoded wrapper)
- Element: [Chat variables](../element/chat-variables.md)
- CBS equivalent: [`{{getvar::name}}`](../cbs/variables/getvar.md) (read side)
