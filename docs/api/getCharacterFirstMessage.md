# API: `getCharacterFirstMessage(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getCharacterFirstMessage', ...)`)

Returns the selected character's first/greeting message (`char.firstMessage`).

## Signature

```lua
getCharacterFirstMessage(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries **no key guard**. |

## Returns

`string` — `char.firstMessage` of the selected character. This is the primary
greeting only; alternate greetings are not exposed here.

## Permission

Always available — the implementation reads the database directly and never
checks `id` against any permission set. It works from every mode, including
[`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- None. Reads the selected character's `firstMessage` field.

## Example

```lua
function onStart(id)
    local greeting = getCharacterFirstMessage(id)
    log(greeting)
end
```

## See also

- [`setCharacterFirstMessage`](setCharacterFirstMessage.md) (change it)
- [`getCharacterLastMessage`](getCharacterLastMessage.md) (falls back to this when no char message exists)
- [`getName`](getName.md), [`getDescription`](getDescription.md)
