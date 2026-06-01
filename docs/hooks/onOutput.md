# Hook: `onOutput` (mode `output`)

- Layer: Hook (event mode)
- Define: global `function onOutput(id)`
- Fires: after the model reply has been added to the chat
- Permission tier: Safe (plus low-level if the character has `lowLevelAccess`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (mode dispatch in `runScripted`)

`onOutput` runs once the assistant reply is present in the chat.

## When it fires

Risu invokes `onOutput` after the model reply has been added to the chat as
a `char` message. The reply is already stored, so any mutation you make here
changes the stored reply (and therefore the saved history).

Relative to the other entry points: [`onInput`](onInput.md) runs *before* the
user text is stored; [`onStart`](onStart.md) runs *after* it is stored but
*before* the request; `onOutput` runs *after* the reply is stored. See the
pipeline overview in [`docs/README.md`](../README.md).

`onOutput` is distinct from [`editOutput`](editOutput.md): `editOutput`
transforms the reply *string* as it is being stored and must return the new
text, while `onOutput` runs afterward and mutates the chat in place via the host
APIs.

## How to handle

Define a global function named `onOutput`. Risu dispatches by global name,
so it must not live inside a module table.

```lua
function onOutput(id)
    -- runs after the model reply is stored
end
```

## Receives

| Arg | Description |
|-----|-------------|
| `id` | The [access key](../element/access-key.md) for this run (safe tier; low-level too if `lowLevelAccess` is on). |

## Return value

Return `false` to stop the send (Risu sets `stopSending`). Any other return
value (including `nil`) is treated as success.

## Capabilities

- Can: read and mutate the stored reply ([`getChat`](../api/getChat.md),
  [`setChat`](../api/setChat.md), [`addChat`](../api/addChat.md)), read/write
  chat variables, read/write character fields, and call low-level APIs
  ([`LLM`](../api/LLM.md), [`request`](../api/request.md)) if the character
  has `lowLevelAccess`.
- Cannot: decorate the reply for display only — mutations here are
  persistent. To change how the reply *renders* without touching stored text,
  emit marker text here and convert it in [`editDisplay`](editDisplay.md) or an
  `editdisplay` Regex Script.

A common pattern is to append durable marker text that a display-layer script
later turns into HTML:

```lua
function onOutput(id)
    local last = getChat(id, -1)
    if last and last.role == 'char' then
        setChat(id, -1, last.data .. '\n[[status hp=' .. getChatVar(id, 'hp') .. ']]')
    end
end
```

## See also

- Hooks: [`onInput`](onInput.md), [`onStart`](onStart.md), [`editOutput`](editOutput.md), [`editDisplay`](editDisplay.md)
- API: [`setChat`](../api/setChat.md), [`addChat`](../api/addChat.md)
- Elements: [Access key & tiers](../element/access-key.md), [Chat message](../element/chat-message.md)
