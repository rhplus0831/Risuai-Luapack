# API: `getPersonaName(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getPersonaName', ...)`)

Returns the active user/persona name (`getUserName()`).

## Signature

```lua
getPersonaName(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries **no key guard**. |

## Returns

`string` — the current user/persona display name, as resolved by Risu's
`getUserName()`.

## Permission

Always available — the implementation never checks `id` against any permission
set. It works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Reads the active persona's name.

## Example

```lua
function onStart(id)
    log('User is ' .. getPersonaName(id))
end
```

## See also

- [`getPersonaDescription`](getPersonaDescription.md) (the persona prompt)
- [`getName`](getName.md) (the character name)
