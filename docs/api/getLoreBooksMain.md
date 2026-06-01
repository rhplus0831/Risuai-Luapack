# API: `getLoreBooksMain(id, search)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getLoreBooksMain', ...)`)

The **raw** host call behind [`getLoreBooks`](getLoreBooks.md): same exact
`comment` lookup across the three lore scopes, but returns a **JSON string**
rather than a decoded table. Prefer the [`getLoreBooks`](getLoreBooks.md)
preamble helper, which decodes for you.

## Signature

```lua
getLoreBooksMain(id, search)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. No permission set is checked. |
| `search` | string | The `comment` to match exactly. |

## Returns

A **JSON string** encoding an array of matching
[lorebook entries](../element/lorebook-entry.md), each with `content` already
CBS-parsed in the selected-character context. Decode it with `json.decode`. If
the selected character is not of type `character`, the call returns nothing
(`nil`). Scopes searched, in order: chat-local lore, character-global lore,
enabled-module lore.

## Permission

Always available — there is **no guard** on this call, so it works for any
access key regardless of tier (including from edit listeners). It is *not*
gated behind `lowLevelAccess`. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Lorebook entry](../element/lorebook-entry.md) — the encoded entries use the
  database `loreBook` shape; `content` is CBS-parsed.

## Example

```lua
function onStart(id)
    local entries = json.decode(getLoreBooksMain(id, 'scene-state'))
    for _, e in ipairs(entries) do
        log(e.content)
    end
end
```

## See also

- Preamble helper: [`getLoreBooks`](getLoreBooks.md)
- Activated lore: [`loadLoreBooksMain`](loadLoreBooksMain.md)
- Writing: [`upsertLocalLoreBook`](upsertLocalLoreBook.md)
- Element: [Lorebook entry](../element/lorebook-entry.md)
