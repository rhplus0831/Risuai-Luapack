# Hook: `editRequest` (mode `editRequest`)

- Layer: Hook (edit listener)
- Define: `listenEdit('editRequest', function(id, value, meta) ... return value end)`
- Fires: after the outgoing prompt has been fully assembled (memory + lorebook), before it is sent to the model
- Permission tier: Safe — never low-level (forced off for all edit listeners)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`callListenMain` in `luaCodeWrapper`; `runLuaEditTrigger`)

`editRequest` lets you inspect or rewrite the final outgoing message array
without touching stored chat.

## When it fires

`editRequest` runs after Risu has assembled the full request — main prompt,
description, persona, examples, activated lorebooks, author note, chat history,
and memory — and before the request is dispatched to the model. The handler
receives the assembled outgoing message array and returns the version that
is actually sent. Because it edits only the request payload, the stored chat and
history are unaffected.

Relative to the other entry points: [`onStart`](onStart.md) mutates the stored
chat *before* assembly; `editRequest` rewrites the *assembled* request *after*
assembly. There is no Lua `editProcess` listener, even though Risu's regex
pipeline has an `editprocess` mode (`runLuaEditTrigger` returns that content
unchanged).

## How to handle

Register a handler with `listenEdit('editRequest', fn)`. You may register
multiple handlers; they chain in registration order, each receiving the
previous handler's return value. Every handler must `return` the value —
forgetting `return` passes `nil` down the chain and blanks the request. If a
handler errors, Risu keeps the original content.

```lua
listenEdit('editRequest', function(id, value, meta)
    -- value is the OpenAI-style outgoing message array
    return value
end)
```

## Receives

| Arg | Type | Description |
|-----|------|-------------|
| `id` | [access key](../element/access-key.md) | Safe tier. Low-level access is forced off here, even if the character has `lowLevelAccess`. |
| `value` | array | OpenAI-style message array: a list of `{ role = 'system'\|'user'\|'assistant', content = '<string>' }` items. |
| `meta` | table | Context Risu has for this run; may be empty. |

## Return value

Return the (possibly transformed) message array. Returning `nil` (or
forgetting `return`) blanks the outgoing request. The returned array becomes the
input to the next `editRequest` handler, and finally the request that is sent.

## Capabilities

- Can: read and rewrite the outgoing message array — append a system message,
  strip or reorder entries, edit `content`, inject a one-shot directive that
  affects only this request. Read chat variables and write them with
  [`setChatVar`](../api/setChatVar.md)/`setState`.
- Cannot: use low-level APIs ([`LLM`](../api/LLM.md),
  [`request`](../api/request.md), [`similarity`](../api/similarity.md)) — the
  edit-trigger runner forces low-level off. The value shape is the OpenAI-style
  `{ role, content }` array, not the stored chat shape `{ role, data }`.

```lua
listenEdit('editRequest', function(id, value, meta)
    table.insert(value, { role = 'system', content = 'Stay in character.' })
    return value
end)
```

To inspect or rewrite the request after memory has been assembled, this is the
right place — `onStart` only sees the chat before assembly.

## See also

- Hooks: [`editInput`](editInput.md), [`editOutput`](editOutput.md), [`editDisplay`](editDisplay.md), [`onStart`](onStart.md)
- Elements: [Access key & tiers](../element/access-key.md), [Chat message](../element/chat-message.md)
