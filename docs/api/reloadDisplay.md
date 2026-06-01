# API: `reloadDisplay(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('reloadDisplay', ...)`)

Requests a refresh of the whole chat display / GUI.

## Signature

```lua
reloadDisplay(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |

## Returns

Nothing.

## Behavior

The host bumps an internal pointer (`ReloadGUIPointer`), which Risu observes to
re-render the display. Use it after mutating chat or character data so the UI
reflects the change. To re-render a single message instead of the whole view,
use [`reloadChat`](reloadChat.md).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners (which
already run as part of the render pipeline). See
[access key & tiers](../element/access-key.md).

## Elements used

- [Display HTML](../element/display-html.md) — controls what the refresh
  re-renders.

## Example

```lua
function onButtonClick(id, data)
    setName(id, 'New Name')
    reloadDisplay(id)
end
```

## See also

- [`reloadChat`](reloadChat.md) (one message), [`setName`](setName.md),
  [`setBackgroundEmbedding`](setBackgroundEmbedding.md)
- Hook: [`editDisplay`](../hooks/editDisplay.md)
