# API: `setCharacterFirstMessage(id, data)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setCharacterFirstMessage', ...)`)

Sets the selected character's first/greeting message (`char.firstMessage`).

## Signature

```lua
setCharacterFirstMessage(id, data)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `data` | string | The new first message. A non-string value makes the call return `false` without writing. |

## Returns

`boolean` — `true` on success, `false` if `data` is not a string. When `id` is
not in `ScriptingSafeIds` the call no-ops and returns nothing (`nil`).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Writes the selected character's `firstMessage` field and stores it back
  via `DBState.db.characters[selectedCharID]`.

## Example

```lua
function onStart(id)
    local ok = setCharacterFirstMessage(id, 'Welcome back, traveler.')
    log(ok)   -- true
end
```

## See also

- [`getCharacterFirstMessage`](getCharacterFirstMessage.md) (read it)
- [`setName`](setName.md), [`setDescription`](setDescription.md)
