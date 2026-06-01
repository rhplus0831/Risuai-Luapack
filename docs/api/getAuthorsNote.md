# API: `getAuthorsNote(id)`

- Layer: Host API (`declareAPI`)
- Permission tier: Always available (no key guard)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getAuthorsNote', ...)`)

Returns the current chat's author's note (`chat.note`).

## Signature

```lua
getAuthorsNote(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries no key guard. |

## Returns

`string` — `chat.note` of the active chat, or `''` when the chat has no note
(`ScriptingEngineState.chat?.note ?? ''`).

## Permission

Always available — the implementation never checks `id` against any permission
set. It works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Reads the active chat's `note` field.

## Example

```lua
function onStart(id)
    local note = getAuthorsNote(id)
    if note ~= '' then
        log(note)
    end
end
```

## See also

- [`getCharacterLastMessage`](getCharacterLastMessage.md), [`getUserLastMessage`](getUserLastMessage.md)
- Element: [Chat message](../element/chat-message.md)
