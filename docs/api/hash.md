# API: `hash(id, value)`

- Layer: Host API (`declareAPI`)
- Permission tier: Always available (no key guard)
- Async: yes (returns a Promise — use `:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('hash', ...)`)

Hashes a string using Risu's `hasher`.

## Signature

```lua
hash(id, value):await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries no key guard. |
| `value` | string | The string to hash. It is UTF-8 encoded (`new TextEncoder().encode(value)`) before hashing. |

## Returns

A [Promise](../element/promise-async.md) that resolves to the hash of `value`.
Call inside an `async` handler and unwrap with `:await()`.

## Permission

Always available — the implementation never checks `id` against any permission
set, so it works from every mode (including [`editDisplay`](../hooks/editDisplay.md)
listeners). The `id` argument is passed for consistency. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — the call is awaitable.

## Example

```lua
onStart = async(function(id)
    local h = hash(id, getName(id)):await()
    log(h)
end)
```

## See also

- [`getTokens`](getTokens.md), [`sleep`](sleep.md) (other awaitable utilities)
- Element: [Promise / await](../element/promise-async.md)
