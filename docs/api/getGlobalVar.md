# API: `getGlobalVar(id, key)`

- Layer: Host API (`declareAPI`)
- Permission tier: Always available (no guard)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getGlobalVar', ...)`)

Reads a global chat variable shared across all chats.

## Signature

```lua
getGlobalVar(id, key)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Ignored by this call (no permission check). |
| `key` | string | The global-variable name to read. |

## Returns

A string. The host delegates to Risu's `getGlobalChatVar(key)`, which looks
up `db.globalChatVariables[key]`. A name with no stored value reads back as the
literal string `"null"` (not Lua `nil`). Custom prompt toggles are stored under
the key `toggle_<key>`, so a toggle named `mature` is read with
`getGlobalVar(id, 'toggle_mature')`.

## Permission

This call carries no guard — it works with any `id`, including the restricted
edit-display key. See [access key & tiers](../element/access-key.md). There is
no Lua setter for global variables in this API surface.

## Elements used

- [Global variables](../element/global-variables.md) — the global store this
  getter reads from.
- [Prompt toggles](../element/prompt-toggles.md) — custom toggles surface here
  under the `toggle_<key>` naming.

## Example

```lua
function onStart(id)
    if getGlobalVar(id, 'toggle_mature') == '1' then
        -- toggle is on
    end
end
```

## See also

- [`getChatVar`](getChatVar.md) (chat scope)
- Elements: [Global variables](../element/global-variables.md),
  [Prompt toggles](../element/prompt-toggles.md)
