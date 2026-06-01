# Hook: `editOutput` (mode `editOutput`)

- **Layer:** Hook (edit listener)
- **Define:** `listenEdit('editOutput', function(id, value, meta) ... return value end)`
- **Fires:** on the model reply text, before/while it is stored as the assistant message
- **Permission tier:** Safe — **never** low-level (forced off for all edit listeners)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`callListenMain` in `luaCodeWrapper`; `runLuaEditTrigger`)

`editOutput` transforms the model reply text before it becomes the stored
assistant message.

## When it fires

`editOutput` runs at the output stage, on the model reply text, before/while it
is stored as the `char` message. The string you return becomes the stored reply.
It runs alongside `editoutput` Regex Scripts; the Lua edit handlers run first
within that pipeline.

This is the companion to [`onOutput`](onOutput.md): `editOutput` rewrites the
reply *string* as it is stored, while `onOutput` is an event hook that runs
afterward and mutates the already-stored chat in place.

## How to handle

Register a handler with `listenEdit('editOutput', fn)`. You may register
**multiple** handlers; they chain in registration order, each receiving the
previous handler's return value. Every handler **must `return` the value** —
forgetting `return` passes `nil` down the chain and blanks the stored reply. If a
handler errors, Risu keeps the original content.

```lua
listenEdit('editOutput', function(id, value, meta)
    -- value is the model reply text (a string)
    return value
end)
```

## Receives

| Arg | Type | Description |
|-----|------|-------------|
| `id` | [access key](../element/access-key.md) | Safe tier. Low-level access is **forced off** here, even if the character has `lowLevelAccess`. |
| `value` | string | The model reply text. |
| `meta` | table | Context Risu has for this run; may be empty. |

## Return value

**Return the transformed string.** Returning `nil` (or forgetting `return`)
blanks the stored reply. The returned string becomes the input to the next
`editOutput` handler, and finally the stored assistant message.

## What you can / cannot do here

- **Can:** rewrite the reply text (strip a banned phrase, fix formatting, append
  a marker), read chat variables, and write them with
  [`setChatVar`](../api/setChatVar.md)/`setState`.
- **Cannot:** use low-level APIs — the edit-trigger runner forces low-level off.
  The `value` is a **string**, not the stored `{ role, data }` shape. To decorate
  the reply for display only (without changing stored text), use
  [`editDisplay`](editDisplay.md) or an `editdisplay` Regex Script instead.

```lua
listenEdit('editOutput', function(id, value, meta)
    return value:gsub('%s+$', '')
end)
```

## See also

- Hooks: [`onOutput`](onOutput.md), [`editInput`](editInput.md), [`editRequest`](editRequest.md), [`editDisplay`](editDisplay.md)
- Elements: [Access key & tiers](../element/access-key.md), [Chat message](../element/chat-message.md)
