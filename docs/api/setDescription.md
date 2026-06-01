# API: `setDescription(id, desc)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setDescription', ...)`)

Sets the description (`desc`) of the currently selected character.

## Signature

```lua
setDescription(id, desc)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `desc` | string | The new character description. |

## Returns

Nothing.

**Throws** `Invalid data type` on a type-check failure, and `Character is a
group` if the selected character is a group chat (`char.type === 'group'`).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Writes the selected character's `desc` field and stores it back via
  `DBState.db.characters[selectedCharID]`.

## Example

```lua
function onStart(id)
    setDescription(id, 'A wandering knight, weary but kind.')
end
```

## See also

- [`getDescription`](getDescription.md) (read the description)
- [`setName`](setName.md), [`setCharacterFirstMessage`](setCharacterFirstMessage.md)
