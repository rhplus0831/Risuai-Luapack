# API: `loadLoreBooksMain(id, reserve)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Low-level (requires `lowLevelAccess`)
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('loadLoreBooksMain', ...)`)

The **raw** activated-lore loader behind [`loadLoreBooks`](loadLoreBooks.md).
Runs Risu's real lore activation and returns a JSON array of prompt-ready
entries, honoring a caller-supplied `reserve` token budget. Prefer the
[`loadLoreBooks`](loadLoreBooks.md) preamble helper, which awaits and decodes
for you (but passes no reserve).

## Signature

```lua
loadLoreBooksMain(id, reserve)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `reserve` | number | Tokens to reserve from the context budget. Entries are added until cumulative tokens would exceed `maxContext - reserve`. The preamble helper passes none. |

## Returns

A Promise resolving to a **JSON string** encoding an array of
`{ "role": <string>, "data": <string> }` entries, where `data` is CBS-parsed
prompt text and an `assistant` role is mapped to `char`. Decode it with
`json.decode`. Entries are accumulated in order until adding the next would push
the running token total past `maxContext - reserve`; if `maxContext - reserve`
is negative the result is an empty array. If the selected character is not of
type `character`, the call returns nothing (`nil`).

## Permission

Low-level tier — the call no-ops unless `id` is in `ScriptingLowLevelIds`,
granted only to safe-mode runs **when the character/module has `lowLevelAccess`
enabled**. It is **never** available to edit listeners
([`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md),
[`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)),
which run with low-level access forced off. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Lorebook entry](../element/lorebook-entry.md) — the encoded entries are the
  activated prompt-ready form `{ role, data }`.

## Example

```lua
function onStart(id)
    -- reserve 2000 tokens of context for the rest of the prompt
    local actives = json.decode(loadLoreBooksMain(id, 2000):await())
    for _, entry in ipairs(actives) do
        log(entry.role .. ': ' .. entry.data)
    end
end
```

## See also

- Preamble helper: [`loadLoreBooks`](loadLoreBooks.md)
- Exact lookup: [`getLoreBooksMain`](getLoreBooksMain.md)
- Writing: [`upsertLocalLoreBook`](upsertLocalLoreBook.md)
- Element: [Lorebook entry](../element/lorebook-entry.md)
