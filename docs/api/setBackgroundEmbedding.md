# API: `setBackgroundEmbedding(id, data)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('setBackgroundEmbedding', ...)`)

Sets the selected character's background embedding HTML (`char.backgroundHTML`).

## Signature

```lua
setBackgroundEmbedding(id, data)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `data` | string | The new background HTML. A non-string value makes the call return `false` without writing. |

## Returns

`boolean` — `true` on success, `false` if `data` is not a string. When `id` is
not in `ScriptingSafeIds` the call no-ops and returns nothing (`nil`).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- [Background embedding](../element/background-embedding.md) — writes
  `DBState.db.characters[selectedCharID].backgroundHTML`.

## Example

```lua
function onStart(id)
    local ok = setBackgroundEmbedding(id, '<div style="background:#000"></div>')
    log(ok)   -- true
end
```

## See also

- [`getBackgroundEmbedding`](getBackgroundEmbedding.md) (read it)
- Element: [Background embedding](../element/background-embedding.md)
