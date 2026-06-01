# API: `getLoreBooks(id, search)`

- **Layer:** Preamble helper (defined in `luaCodeWrapper`)
- **Permission tier:** Always available
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`function getLoreBooks` in `luaCodeWrapper`, wrapping `declareAPI('getLoreBooksMain', ...)`)

Finds lorebook entries whose `comment` **exactly** matches `search`, across all
three lore scopes, and returns them as a Lua array. This is the preamble wrapper
over [`getLoreBooksMain`](getLoreBooksMain.md): it calls the raw function and
`json.decode`s the result for you.

## Signature

```lua
getLoreBooks(id, search)
```

The preamble defines it as:

```lua
function getLoreBooks(id, search)
    return json.decode(getLoreBooksMain(id, search))
end
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. No permission set is checked. |
| `search` | string | The `comment` to match. Matching is **exact** (not key-based activation). |

## Returns

A Lua array of matching [lorebook entries](../element/lorebook-entry.md). Each
entry is the stored `loreBook` shape (`comment`, `content`, `key`, `secondkey`,
`insertorder`, …) with its `content` already **CBS-parsed** in the
selected-character context. Entries are gathered from, in order:

1. Chat-local lore (`chat.localLore`).
2. Character-global lore (`character.globalLore`).
3. Enabled-module lore (`getModuleLorebooks()`).

If the selected character is not of type `character` (e.g. a group), the raw
call returns nothing.

## Permission

Always available — the underlying `getLoreBooksMain` carries **no guard**, so it
works for any access key regardless of tier (including from edit listeners). It
is *not* gated behind `lowLevelAccess`. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Lorebook entry](../element/lorebook-entry.md) — the returned entries use the
  database `loreBook` shape; `content` is CBS-parsed.

## Example

```lua
function onStart(id)
    local entries = getLoreBooks(id, 'scene-state')
    for _, e in ipairs(entries) do
        log(e.content)
    end
end
```

## See also

- Raw host call: [`getLoreBooksMain`](getLoreBooksMain.md)
- Activated lore: [`loadLoreBooks`](loadLoreBooks.md)
- Writing: [`upsertLocalLoreBook`](upsertLocalLoreBook.md)
- Element: [Lorebook entry](../element/lorebook-entry.md)
