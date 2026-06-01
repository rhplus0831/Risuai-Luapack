# API: `getChatVar(id, key)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getChatVar', ...)`)

Reads the current value of a persistent chat variable as a string.

## Signature

```lua
getChatVar(id, key)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored by this call (no permission check). |
| `key` | string | The chat-variable name to read. |

## Returns

A **string**. The host delegates to Risu's `getChatVar(key)`, which resolves the
value by checking, in order: the chat's `scriptstate`, the character's
`defaultVariables`, then the template default variables. A variable that was
never set anywhere reads back as the literal string `"null"` (not Lua `nil`).
This `"null"` fallback is what [`getState`](getState.md) relies on to decode a
missing value to Lua `nil`.

## Permission

This call carries **no guard** — it works with any `id`, including the restricted
edit-display key. See [access key & tiers](../element/access-key.md). Writing a
chat variable does require a tier; use [`setChatVar`](setChatVar.md).

## Elements used

- [Chat variables](../element/chat-variables.md) — the storage and fallback
  chain this getter reads from.

## Example

```lua
function onStart(id)
    local hp = getChatVar(id, 'hp')
    if hp == 'null' then
        setChatVar(id, 'hp', '100')   -- requires safe/editDisplay tier
    end
end
```

## See also

- [`setChatVar`](setChatVar.md) (write), [`getGlobalVar`](getGlobalVar.md)
  (global scope), [`getState`](getState.md) (JSON-decoded wrapper)
- CBS equivalent: [`{{getvar::name}}`](../cbs/variables/getvar.md)
- Element: [Chat variables](../element/chat-variables.md)
