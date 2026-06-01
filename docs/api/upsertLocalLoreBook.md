# API: `upsertLocalLoreBook(id, name, content, options)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('upsertLocalLoreBook', ...)`)

Creates or replaces a current-chat local lorebook entry, keyed by its
`comment` (`name`). Any existing chat-local entry with the same `comment` is
removed first, then a fresh entry is pushed. Only chat-local lore is writable
from Lua — there is no API to edit character-global or module lore.

## Signature

```lua
upsertLocalLoreBook(id, name, content, options)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `name` | string | The entry's `comment` (title / lookup key). Replaces any existing chat-local entry with the same `comment`. |
| `content` | string | The lore text stored verbatim in `content`. |
| `options` | table | Optional settings: `alwaysActive`, `insertOrder`, `key`, `secondKey`, and `regex`. |

`options` fields:

| Option | Type | Default | Maps to field |
|--------|------|---------|---------------|
| `alwaysActive` | boolean | `false` | `alwaysActive` |
| `insertOrder` | number | `100` | `insertorder` |
| `key` | string | `''` | `key` |
| `secondKey` | string | `''` | `secondkey` |
| `regex` | boolean | `false` | `useRegex` |

The new entry is always written with `mode = 'normal'`, and `selective` is set
to `true` whenever `secondKey` is non-empty (the source uses
`selective: !!secondKey`). A selective entry requires both `key` and `secondKey`
to match before it activates.

## Returns

Nothing. If the selected character is not of type `character`, the call no-ops.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners (which
hold only an edit-display key). Available from `onStart`/`onInput`/`onOutput`,
button/custom modes, and the request/input/output edit hooks. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Lorebook entry](../element/lorebook-entry.md) — writes a `loreBook`-shaped
  entry into the current chat's `localLore`.

## Example

```lua
function onStart(id)
    upsertLocalLoreBook(id, 'scene-state', 'It is raining in the city.', {
        alwaysActive = true,
        insertOrder = 50,
    })

    -- a selective entry: secondKey makes it selective
    upsertLocalLoreBook(id, 'secret', 'The vault code is 4729.', {
        key = 'vault',
        secondKey = 'code',
    })
end
```

## See also

- Reading: [`getLoreBooks`](getLoreBooks.md), [`loadLoreBooks`](loadLoreBooks.md)
- Element: [Lorebook entry](../element/lorebook-entry.md)
- [Access key & tiers](../element/access-key.md)
