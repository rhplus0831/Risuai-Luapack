# API: `alertConfirm(id, value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** yes (returns a Promise — use `:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('alertConfirm', ...)`)

Asks the user a yes/no question and resolves to a boolean.

## Signature

```lua
alertConfirm(id, value):await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string | The confirmation message shown to the user. |

## Returns

A [Promise](../element/promise-async.md) that resolves to a `boolean`: `true` if
the user confirmed, `false` otherwise (the host maps the raw result via
`res ? true : false`). Call inside an `async` handler and unwrap with `:await()`.
When `id` is not in `ScriptingSafeIds` the call no-ops and returns nothing.

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
    local ok = alertConfirm(id, 'Reset the chat?'):await()
    if ok then
        cutChat(id, 0, 0)
    end
end)
```

## See also

- [`alertInput`](alertInput.md), [`alertSelect`](alertSelect.md) (other awaitable prompts)
- [`alertNormal`](alertNormal.md), [`alertError`](alertError.md) (fire-and-forget)
- Element: [Promise / await](../element/promise-async.md)
