# API: `getCharacterLastMessage(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getCharacterLastMessage', ...)`)

Returns the data of the most recent char-role message in the chat.

## Signature

```lua
getCharacterLastMessage(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries **no key guard**. |

## Returns

`string` — the `data` of the last message whose `role` is `'char'`, found by
scanning the chat backward from the end. If the chat has **no** char message, it
falls back to the selected character's first message (`selchar.firstMessage`).
Returns `''` only when there is no active chat.

## Permission

Always available — the implementation never checks `id` against any permission
set. It works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — scans `chat.message` for the last
  entry with `role = 'char'`.

## Example

```lua
function onOutput(id)
    local last = getCharacterLastMessage(id)
    log(last)
end
```

## See also

- [`getUserLastMessage`](getUserLastMessage.md) (the last user message)
- [`getCharacterFirstMessage`](getCharacterFirstMessage.md) (the fallback value)
- CBS: [`{{previouscharchat}}`](../cbs/history/previouscharchat.md)
