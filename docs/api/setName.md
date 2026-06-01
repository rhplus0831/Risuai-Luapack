# API: `setName(id, name)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setName', ...)`)

Sets the name of the currently selected character.

## Signature

```lua
setName(id, name)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `name` | string | The new character name. A non-string value **throws** `Invalid data type`. |

## Returns

Nothing.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners (which
hold only an edit-display key). Available from `onStart`/`onInput`/`onOutput`,
button/custom modes, and the request/input/output edit hooks. See
[access key & tiers](../element/access-key.md).

## Elements used

- None. Writes `DBState.db.characters[selectedCharID].name`.

## Example

```lua
function onStart(id)
    setName(id, 'Aria')
end
```

## See also

- [`getName`](getName.md) (read the name)
- [`setDescription`](setDescription.md), [`setCharacterFirstMessage`](setCharacterFirstMessage.md)
