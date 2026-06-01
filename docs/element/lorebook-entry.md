# Element: Lorebook entry

- **Kind:** Element (data structure)
- **Source:** `Refer/Risuai/src/ts/storage/database.svelte.ts` (`loreBook` interface), `Refer/Risuai/src/ts/process/scriptings.ts` (`getLoreBooksMain`, `upsertLocalLoreBook`, `loadLoreBooksMain`), `Refer/Risuai/src/ts/process/lorebook.svelte.ts` (decorator loader)

The structured world-info entry Risu activates into prompts, and how Lua reads
and writes it.

## Shape / fields

The database `loreBook` interface (fields most relevant to Lua):

| Field | Type | Description |
|-------|------|-------------|
| `comment` | string | Entry title / lookup name. `getLoreBooks` matches on this exactly. |
| `content` | string | The lore text (CBS is parsed before it reaches Lua via `getLoreBooks`). |
| `key` | string | Activation keys (comma-separated terms). |
| `secondkey` | string | Secondary keys; relevant when `selective` is set. |
| `insertorder` | number | Sort/insertion order among activated entries. |
| `alwaysActive` | boolean | When true, the entry is always inserted (a "constant"). |
| `selective` | boolean | Requires a `secondkey` match in addition to `key`. |
| `useRegex` | boolean | Treat `key` as a regular expression. |
| `mode` | `'multiple'\|'constant'\|'normal'\|'child'\|'folder'` | Entry mode. `upsertLocalLoreBook` writes `'normal'`. |
| `activationPercent?` | number | Optional activation probability. |
| `id?` | string | Optional stable id. |

## Three scopes

Lorebook entries come from three places, all visible to `getLoreBooks`:

1. **Chat-local**: `chat.localLore` (per current chat).
2. **Character**: `character.globalLore`.
3. **Module**: every enabled module's `lorebook` (`getModuleLorebooks()`).

## Reading: `getLoreBooks(id, search)`

`getLoreBooks` (wrapper over `getLoreBooksMain`) does an **exact `comment`
lookup** across all three scopes and returns every match as an array. It does
**not** run normal key-based activation. Each returned entry's `content` has
already been CBS-parsed in the selected-character context.

```lua
local entries = getLoreBooks(id, 'scene-state')
for _, e in ipairs(entries) do
    -- e.comment, e.content (CBS-parsed), e.key, ...
end
```

## Reading: `loadLoreBooks(id)`

[`loadLoreBooks`](../api/loadLoreBooks.md) (wrapper over `loadLoreBooksMain`,
**low-level, awaitable**) runs Risu's real activated-lore selection and returns
prompt-ready entries shaped `{ role, data }` (the host maps an `assistant` role
to `char`). The raw host call takes a `reserve` token budget; the high-level
wrapper passes none. It awaits internally.

## Writing: `upsertLocalLoreBook`

[`upsertLocalLoreBook`](../api/upsertLocalLoreBook.md) replaces any current-chat
local entry whose `comment` matches `name`, then pushes a fresh entry. Options:

| Option | Default | Maps to field |
|--------|---------|---------------|
| `alwaysActive` | `false` | `alwaysActive` |
| `insertOrder` | `100` | `insertorder` |
| `key` | `''` | `key` |
| `secondKey` | `''` | `secondkey` |
| `regex` | `false` | `useRegex` |

The new entry is written with `mode = 'normal'`, and **`selective` is set to
`true` whenever `secondKey` is non-empty** (`selective: !!secondKey`). Only
chat-local lore is writable from Lua — there is no Lua API to edit character or
module lore.

## Content decorators

Lorebook `content` may begin with `@@`-prefixed decorator lines, parsed by the
loader (`CCardLib.decorator.parse`). The decorator names the loader actually
handles (verified in `lorebook.svelte.ts`):

- Position / depth: `@@depth`, `@@reverse_depth`, `@@position`, `@@end`
- Scan: `@@scan_depth`
- Activation gating: `@@activate_only_after`, `@@activate_only_every`,
  `@@is_greeting`, `@@probability`, `@@activate`, `@@dont_activate`,
  `@@keep_activate_after_match`, `@@dont_activate_after_match`
- Keys / matching: `@@additional_keys`, `@@exclude_keys`, `@@exclude_keys_all`,
  `@@match_full_word`, `@@match_partial_word`
- Role: `@@role` (`user` | `assistant` | `system`)
- Recursion: `@@recursive`, `@@unrecursive`, `@@no_recursive_search`
- Priority: `@@priority`, `@@ignore_on_max_context`
- Injection: `@@inject_lore`, `@@inject_at`, `@@inject_replace`, `@@inject_prepend`
- Prompt control: `@@disable_ui_prompt` (`post_history_instructions` | `system_prompt`)

Decorators like `@@instruct_depth` / `@@reverse_instruct_depth` /
`@@instruct_scan_depth` and `@@is_user_icon` are recognized but treated as
no-ops (the instruct mode does not exist in Risu). Unknown decorators are
ignored.

## Used by

- APIs: [`getLoreBooks`](../api/getLoreBooks.md),
  [`loadLoreBooks`](../api/loadLoreBooks.md),
  [`upsertLocalLoreBook`](../api/upsertLocalLoreBook.md)
- Modules contribute lorebook scope — see [Modules](modules.md)

## See also

- Elements: [Modules](modules.md), [Access key & tiers](access-key.md),
  [Promise / await](promise-async.md)
- Index: [`docs/README.md`](../README.md)
