# API: `alertError(id, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('alertError', ...)`)

Shows an error alert to the user.

## Signature

```lua
alertError(id, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string | The error message to display. |

## Returns

Nothing. Fire-and-forget; it does not wait for the user (`alertError(value)`).

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Drives Risu's alert UI (error styling).

## Example

```lua
function onStart(id)
    if getChatLength(id) == 0 then
        alertError(id, 'No messages yet.')
    end
end
```

## See also

- [`alertNormal`](alertNormal.md) (info variant)
- [`alertInput`](alertInput.md), [`alertSelect`](alertSelect.md), [`alertConfirm`](alertConfirm.md) (awaitable prompts)
