# API: `getName(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getName', ...)`)

Returns the name of the currently selected character.

## Signature

```lua
getName(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries **no key guard**. |

## Returns

`string` — `char.name` of the selected character (`db.characters[selectedCharID]`).

## Permission

Always available — the implementation reads the database directly and never
checks `id` against any permission set. It works from every mode, including
[`editDisplay`](../hooks/editDisplay.md) listeners. The `id` argument is still
passed for consistency with the rest of the host API; see
[access key & tiers](../element/access-key.md).

## Elements used

- None. Reads only the selected character's `name` field.

## Example

```lua
function onStart(id)
    log('Talking to ' .. getName(id))
end
```

## See also

- [`setName`](setName.md) (change the name)
- [`getPersonaName`](getPersonaName.md) (the user/persona name)
- [`getDescription`](getDescription.md), [`getCharacterFirstMessage`](getCharacterFirstMessage.md)
