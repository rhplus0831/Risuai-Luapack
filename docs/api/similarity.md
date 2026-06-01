# API: `similarity(id, source, value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Low-level (requires `lowLevelAccess`)
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('similarity', ...)`)

Embedding-based similarity search. The candidate strings in `value` are embedded
with the configured embedding model (via `HypaProcesser`), then ranked against
the embedded `source` query. Returns the candidates sorted by similarity to
`source`.

## Signature

```lua
similarity(id, source, value)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `source` | string | The query string to compare candidates against. |
| `value` | array of strings | The candidate texts to embed and rank. |

## Returns

A Promise resolving to the result of `HypaProcesser.similaritySearch(source)`:
the candidate entries ordered by similarity to `source` (most similar first).

## Permission

Low-level tier — the call no-ops unless `id` is in `ScriptingLowLevelIds`,
granted only to safe-mode runs **when the character/module has `lowLevelAccess`
enabled**. It is **never** available to edit listeners
([`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md),
[`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)),
which run with low-level access forced off. See
[access key & permission tiers](../element/access-key.md).

Note: embedding the candidates calls the embedding model, so this can be slow
and may incur cost depending on the configured embedding provider.

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.

## Example

```lua
function onStart(id)
    local ranked = similarity(id, 'How do I save progress?', {
        'Press F5 to save.',
        'The weather is nice.',
        'Use the save menu in settings.',
    }):await()
    -- ranked is ordered most-similar first
end
```

## See also

- Elements: [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
- Other low-level calls: [`request`](request.md), [`simpleLLM`](simpleLLM.md)
