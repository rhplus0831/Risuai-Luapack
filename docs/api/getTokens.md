# API: `getTokens(id, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: yes (returns a Promise — use `:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getTokens', ...)`)

Returns the token count of a string using Risu's active tokenizer.

## Signature

```lua
getTokens(id, value):await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `value` | string | The text to tokenize. |

## Returns

A [Promise](../element/promise-async.md) that resolves to the token count
(`number`) from `tokenize(value)`. Call inside an `async` handler and unwrap with
`:await()`. When `id` is not in `ScriptingSafeIds` the call no-ops and returns
nothing.

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
    local n = getTokens(id, getCharacterLastMessage(id)):await()
    log('last reply tokens: ' .. tostring(n))
end)
```

## See also

- [`hash`](hash.md), [`sleep`](sleep.md) (other awaitable utilities)
- Element: [Promise / await](../element/promise-async.md)
