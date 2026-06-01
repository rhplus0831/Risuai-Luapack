# API: `sleep(id, time)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: yes (returns a Promise — use `:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('sleep', ...)`)

Pauses the handler for a given number of milliseconds.

## Signature

```lua
sleep(id, time):await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `time` | number | Delay in milliseconds before the promise resolves. |

## Returns

A [Promise](../element/promise-async.md) that resolves to `true` after `time`
milliseconds (the host uses `setTimeout`). Call inside an `async` handler and
unwrap with `:await()`. When `id` is not in `ScriptingSafeIds` the call no-ops
and returns nothing.

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
    alertNormal(id, 'Thinking...')
    sleep(id, 1000):await()   -- wait 1 second
    alertNormal(id, 'Done.')
end)
```

## See also

- [`hash`](hash.md), [`getTokens`](getTokens.md) (other awaitable utilities)
- Element: [Promise / await](../element/promise-async.md)
