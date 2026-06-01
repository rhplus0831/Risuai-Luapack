# API: `loadLoreBooks(id)`

- Layer: Preamble helper (defined in `luaCodeWrapper`)
- Permission tier: Low-level (requires `lowLevelAccess`)
- Async: yes (`:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`function loadLoreBooks` in `luaCodeWrapper`, wrapping `declareAPI('loadLoreBooksMain', ...)`)

Runs Risu's real activated-lore selection and returns the prompt-ready entries,
decoded into a Lua array. Unlike [`getLoreBooks`](getLoreBooks.md) (an exact
`comment` lookup), this performs the actual activation Risu would use when
building a request. It is the preamble wrapper over the raw
[`loadLoreBooksMain`](loadLoreBooksMain.md): it awaits the host call and
`json.decode`s the result. The helper passes no reserve token budget.

## Signature

```lua
loadLoreBooks(id)   -- returns a Promise; call :await()
```

The preamble defines it as:

```lua
function loadLoreBooks(id)
    return json.decode(loadLoreBooksMain(id):await())
end
```

Note: the preamble call site does not pass a `reserve` argument, so the raw
host call receives `reserve = nil` (treated as no reserve budget).

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |

## Returns

A Promise. After `:await()`, a Lua array of activated entries shaped
`{ role = <string>, data = <string> }`, where `data` is the CBS-parsed prompt
text and `role` is the entry's role (an `assistant` role is mapped to `char`).
Entries whose parsed text is empty are skipped.

## Permission

Low-level tier — although `loadLoreBooks` itself is a preamble helper, the raw
[`loadLoreBooksMain`](loadLoreBooksMain.md) it calls no-ops unless `id` is in
`ScriptingLowLevelIds`, so this requires `lowLevelAccess`. That set is granted
only to safe-mode runs when the character/module has `lowLevelAccess`
enabled. It is never available to edit listeners
([`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md),
[`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)),
which run with low-level access forced off. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Lorebook entry](../element/lorebook-entry.md) — the activated entries come
  from Risu's lore selection; returned shape is `{ role, data }`.

## Example

```lua
function onStart(id)
    local actives = loadLoreBooks(id):await()
    for _, entry in ipairs(actives) do
        log(entry.role .. ': ' .. entry.data)
    end
end
```

## See also

- Raw host call: [`loadLoreBooksMain`](loadLoreBooksMain.md)
- Exact lookup: [`getLoreBooks`](getLoreBooks.md)
- Writing: [`upsertLocalLoreBook`](upsertLocalLoreBook.md)
- Elements: [Lorebook entry](../element/lorebook-entry.md),
  [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
