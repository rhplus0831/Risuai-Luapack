# API: `listenEdit(type, func)`

- Layer: Preamble helper (defined in `luaCodeWrapper`, not `declareAPI`)
- Permission tier: N/A (registration only — the registered handler runs under the edit hook's key)
- Async: no (registration is synchronous; the handler may be `async`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper` -> `function listenEdit`)

Registers a chained edit-trigger handler for one of the four edit hooks.

## Signature

```lua
listenEdit(type, func)
```

Note: `listenEdit` does not take an access key — it is a registration helper,
not a host call. The `id` is delivered to your handler when it later runs.

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `type` | string | One of `'editRequest'`, `'editInput'`, `'editOutput'`, `'editDisplay'`. Any other value throws `Invalid type`. |
| `func` | function | Handler `function(id, value, meta)` that must return the transformed `value`. |

Handlers are stored per type and invoked in registration order; each
handler's return value becomes the `value` passed to the next (a chain). The
final return value is what Risu uses for that edit stage.

The handler arguments are:

| Arg | Description |
|-----|-------------|
| `id` | The [access key](../element/access-key.md) for this run. For `editRequest`/`editInput`/`editOutput` it is a safe key (low-level forced off); for `editDisplay` it is an edit-display key (chat-var writes only). |
| `value` | The content for this stage (e.g. the message array for `editRequest`, a string for the others). Decoded from JSON before the call. |
| `meta` | Hook metadata (decoded from JSON). |

## Returns

Nothing (registration). The registered handler must return the transformed
`value`; if it returns `nil`, that becomes the chained value.

## Permission

`listenEdit` itself performs no privileged action, so it needs no key. When the
handler runs, its `id` tier depends on the hook: edit listeners never receive
low-level access, and `editDisplay` handlers can only write chat variables. See
[access key & tiers](../element/access-key.md).

## Elements used

- None directly. The handler operates on the edit stage's `value`.

## Example

```lua
listenEdit('editOutput', function(id, value, meta)
    -- redact a word from the model's reply before it is stored
    return (value:gsub('secret', '[redacted]'))
end)
```

## See also

- Hooks: [`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md), [`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)
- Element: [Access key & tiers](../element/access-key.md)
