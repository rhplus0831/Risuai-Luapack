# API: `alertNormal(id, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('alertNormal', ...)`)

Shows an informational alert/toast to the user.

## Signature

```lua
alertNormal(id, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string | The message to display. |

## Returns

Nothing. Fire-and-forget; it does not wait for the user (`alertNormal(value)`).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Drives Risu's alert UI.

## Example

```lua
function onStart(id)
    alertNormal(id, 'Script loaded.')
end
```

## See also

- [`alertError`](alertError.md) (error variant)
- [`alertInput`](alertInput.md), [`alertSelect`](alertSelect.md), [`alertConfirm`](alertConfirm.md) (awaitable prompts)
