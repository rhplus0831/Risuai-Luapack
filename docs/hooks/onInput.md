# Hook: `onInput` (mode `input`)

- Layer: Hook (event mode)
- Define: global `function onInput(id)`
- Fires: when the user submits input, before that text is stored as the user message
- Permission tier: Safe (plus low-level if the character has `lowLevelAccess`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (mode dispatch in `runScripted`)

`onInput` runs at the very start of a send, the moment the user submits text.

## When it fires

Risu invokes `onInput` when the user submits input, before the submitted
text has been stored as a message in the chat. This is the earliest entry point
in the send pipeline.

Relative to the other entry points: `onInput` runs *before* the user text is
stored; [`onStart`](onStart.md) runs *after* it is stored but *before* the model
request; [`onOutput`](onOutput.md) runs *after* the reply is stored. See the
pipeline overview in [`docs/README.md`](../README.md).

Because the submitted text is not yet in the chat, you usually cannot read it
from `getChat` here. If you need to *rewrite* the text the user just typed,
register an [`editInput`](editInput.md) listener instead — that handler receives
the submitted string and returns the version Risu stores.

## How to handle

Define a global function named `onInput`. Risu dispatches by global name, so
it must not live inside a module table.

```lua
function onInput(id)
    -- runs before the submitted user text is stored
end
```

## Receives

| Arg | Description |
|-----|-------------|
| `id` | The [access key](../element/access-key.md) for this run (safe tier; low-level too if `lowLevelAccess` is on). |

## Return value

Return `false` to stop the send (Risu sets `stopSending`). Any other return
value (including `nil`) lets the send proceed.

## Capabilities

- Can: read/write chat variables, mutate the existing chat
  ([`addChat`](../api/addChat.md), [`setChat`](../api/setChat.md)), read/write
  character fields, and call low-level APIs ([`LLM`](../api/LLM.md),
  [`request`](../api/request.md)) if the character has `lowLevelAccess`.
- Cannot: see or modify the just-submitted text as a stored message — it has
  not been written yet. Rewriting the submitted text is the job of
  [`editInput`](editInput.md). Use `onInput` for side effects (gating the send,
  updating counters) that should run before the message lands.

```lua
function onInput(id)
    local turns = tonumber(getChatVar(id, 'turns') or '0') or 0
    setChatVar(id, 'turns', tostring(turns + 1))
end
```

## See also

- Hooks: [`onStart`](onStart.md), [`onOutput`](onOutput.md), [`editInput`](editInput.md)
- Elements: [Access key & tiers](../element/access-key.md), [Chat message](../element/chat-message.md)
