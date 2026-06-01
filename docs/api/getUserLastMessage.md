# API: `getUserLastMessage(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getUserLastMessage', ...)`)

Returns the data of the most recent user-role message in the chat.

## Signature

```lua
getUserLastMessage(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries **no key guard**. |

## Returns

`string` — the `data` of the last message whose `role` is `'user'`, found by
scanning the chat backward from the end. Returns `''` if there is no user
message (and `''` when there is no active chat). Unlike
[`getCharacterLastMessage`](getCharacterLastMessage.md), there is no first-message
fallback.

## Permission

Always available — the implementation never checks `id` against any permission
set. It works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — scans `chat.message` for the last
  entry with `role = 'user'`.

## Example

```lua
function onStart(id)
    local lastUser = getUserLastMessage(id)
    log(lastUser)
end
```

## See also

- [`getCharacterLastMessage`](getCharacterLastMessage.md) (the last char message)
- Element: [Chat message](../element/chat-message.md)
