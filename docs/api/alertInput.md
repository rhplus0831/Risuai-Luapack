# API: `alertInput(id, value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** yes (returns a Promise — use `:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('alertInput', ...)`)

Prompts the user for a line of text and resolves to what they typed.

## Signature

```lua
alertInput(id, value):await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string | The prompt label/message shown above the input box. |

## Returns

A [Promise](../element/promise-async.md) that resolves to the entered `string`
(or `null`/`nil` if the user dismisses the prompt). Call inside an `async`
handler and unwrap with `:await()`. When `id` is not in `ScriptingSafeIds` the
call no-ops and returns nothing.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — the call is awaitable.

## Example

```lua
onStart = async(function(id)
    local name = alertInput(id, 'What is your name?'):await()
    if name then
        alertNormal(id, 'Hello, ' .. name)
    end
end)
```

## See also

- [`alertSelect`](alertSelect.md), [`alertConfirm`](alertConfirm.md) (other awaitable prompts)
- [`alertNormal`](alertNormal.md), [`alertError`](alertError.md) (fire-and-forget)
- Element: [Promise / await](../element/promise-async.md)
