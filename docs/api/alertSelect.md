# API: `alertSelect(id, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: yes (returns a Promise — use `:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('alertSelect', ...)`)

Presents the user with a list of choices and resolves to the one they pick.

## Signature

```lua
alertSelect(id, value):await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string[] | A Lua array (table) of option strings to choose from. |

## Returns

A [Promise](../element/promise-async.md) that resolves to the user's chosen
option. Call inside an `async` handler and unwrap with `:await()`. When `id` is
not in `ScriptingSafeIds` the call no-ops and returns nothing.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. Available
from `onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — the call is awaitable.

## Example

```lua
onStart = async(function(id)
    local choice = alertSelect(id, {'Attack', 'Defend', 'Flee'}):await()
    alertNormal(id, 'You chose: ' .. tostring(choice))
end)
```

## See also

- [`alertInput`](alertInput.md), [`alertConfirm`](alertConfirm.md) (other awaitable prompts)
- [`alertNormal`](alertNormal.md), [`alertError`](alertError.md) (fire-and-forget)
- Element: [Promise / await](../element/promise-async.md)
