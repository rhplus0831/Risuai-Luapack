# Hook: `onStart` (mode `start`)

- **Layer:** Hook (event mode)
- **Define:** global `function onStart(id)`
- **Fires:** after the user message is stored, before the chat history is built into the model request
- **Permission tier:** Safe (plus low-level if the character has `lowLevelAccess`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (mode dispatch in `runScripted`)

## When it fires

`onStart` runs once per send, at the start of request assembly. By this point
the latest **user message has already been stored** in the chat, but Risu has
not yet assembled the prompt (description, persona, lorebooks, history, …) or
sent anything to the model. Mutating chat here therefore changes the upcoming
request.

Relative to the other entry points: `onInput` runs *before* the user text is
stored; `onStart` runs *after* it is stored but *before* the request; `onOutput`
runs *after* the reply is stored. See the pipeline overview in
[`docs/README.md`](../README.md).

## How to handle

Define a **global** function named `onStart`. Risu dispatches by global name, so
it must not live inside a module table.

```lua
function onStart(id)
    -- runs before the model request is sent
end
```

## Receives

| Arg | Description |
|-----|-------------|
| `id` | The [access key](../element/access-key.md) for this run (safe tier; low-level too if `lowLevelAccess` is on). |

## Return value

Return `false` to **stop the send** (Risu sets `stopSending`). Any other return
value (including `nil`) lets the send proceed.

## What you can / cannot do here

- **Can:** read and mutate chat ([`addChat`](../api/addChat.md),
  [`setChat`](../api/setChat.md), [`cutChat`](../api/cutChat.md)), read/write chat
  variables, read/write character fields ([`setName`](../api/setName.md),
  [`setBackgroundEmbedding`](../api/setBackgroundEmbedding.md)), and call
  low-level APIs ([`LLM`](../api/LLM.md), [`request`](../api/request.md)) **if**
  the character has `lowLevelAccess`.
- **Cannot:** rewrite the outgoing message array as a structured transform — that
  is the job of [`editRequest`](../hooks/editRequest.md). `onStart` mutates the
  stored chat; `editRequest` mutates only the request payload.

A common pattern is to prepend a one-shot directive to the last user message so
it affects only the next request (but note this mutates stored chat):

```lua
function onStart(id)
    local last = getChat(id, -1)
    if last and last.role == 'user' then
        setChat(id, -1, '<AD>Describe the scene slowly.</AD>\n\n' .. last.data)
    end
end
```

## See also

- Hooks: [`onInput`](onInput.md), [`onOutput`](onOutput.md), [`editRequest`](editRequest.md)
- Elements: [Access key & tiers](../element/access-key.md), [Chat message](../element/chat-message.md)
