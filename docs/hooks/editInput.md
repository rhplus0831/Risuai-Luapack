# Hook: `editInput` (mode `editInput`)

- **Layer:** Hook (edit listener)
- **Define:** `listenEdit('editInput', function(id, value, meta) ... return value end)`
- **Fires:** on the submitted user text, before it is stored as the user message
- **Permission tier:** Safe — **never** low-level (forced off for all edit listeners)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`callListenMain` in `luaCodeWrapper`; `runLuaEditTrigger`)

`editInput` transforms the text the user just submitted before Risu stores it.

## When it fires

`editInput` runs at the input stage, on the submitted user text, **before** that
text is stored as the user message. The string you return becomes the stored
message. It runs alongside `editinput` Regex Scripts; the Lua edit handlers run
first within that pipeline.

This is the companion to [`onInput`](onInput.md): `onInput` is an event hook for
side effects before the message lands, while `editInput` is the place to
actually rewrite the submitted text.

## How to handle

Register a handler with `listenEdit('editInput', fn)`. You may register
**multiple** handlers; they chain in registration order, each receiving the
previous handler's return value. Every handler **must `return` the value** —
forgetting `return` passes `nil` down the chain and blanks the stored text. If a
handler errors, Risu keeps the original content.

```lua
listenEdit('editInput', function(id, value, meta)
    -- value is the submitted user text (a string)
    return value
end)
```

## Receives

| Arg | Type | Description |
|-----|------|-------------|
| `id` | [access key](../element/access-key.md) | Safe tier. Low-level access is **forced off** here, even if the character has `lowLevelAccess`. |
| `value` | string | The submitted user text. |
| `meta` | table | Context Risu has for this run; may be empty. |

## Return value

**Return the transformed string.** Returning `nil` (or forgetting `return`)
blanks the stored user message. The returned string becomes the input to the
next `editInput` handler, and finally the stored user message.

## What you can / cannot do here

- **Can:** rewrite the user text (normalize whitespace, expand shorthand,
  prepend a tag), read chat variables, and write them with
  [`setChatVar`](../api/setChatVar.md)/`setState`.
- **Cannot:** use low-level APIs — the edit-trigger runner forces low-level off.
  The `value` is a **string**, not an array or the stored `{ role, data }`
  shape.

```lua
listenEdit('editInput', function(id, value, meta)
    return (value:gsub('^%s+', ''):gsub('%s+$', ''))
end)
```

## See also

- Hooks: [`onInput`](onInput.md), [`editOutput`](editOutput.md), [`editRequest`](editRequest.md), [`editDisplay`](editDisplay.md)
- Elements: [Access key & tiers](../element/access-key.md), [Chat variables](../element/chat-variables.md)
