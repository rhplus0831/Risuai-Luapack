# API: `stopChat(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('stopChat', ...)`)

Halts the current send by setting the run's `stopSending` flag.

## Signature

```lua
stopChat(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |

## Returns

Nothing.

## Behavior

The host sets the run-local `stopSending = true`. When the script finishes,
`runScripted` returns this flag and Risu aborts the in-progress send (no model
request is dispatched). This is the imperative equivalent of returning `false`
from an entry point such as [`onStart`](../hooks/onStart.md) /
[`onInput`](../hooks/onInput.md) (which the host also turns into `stopSending`).
Use `stopChat` when you want to stop conditionally without ending the handler.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Access key & tiers](../element/access-key.md) — the safe-tier key gates this
  call.

## Example

```lua
function onStart(id)
    local last = getChat(id, -1)
    if last and last.data == '/stop' then
        stopChat(id)
    end
end
```

## See also

- Hooks that can stop a send by returning `false`:
  [`onStart`](../hooks/onStart.md), [`onInput`](../hooks/onInput.md),
  [`onOutput`](../hooks/onOutput.md)
- Element: [Access key & tiers](../element/access-key.md)
