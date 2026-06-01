# API: `getPersonaImage(id)`

- **Layer:** Preamble helper (defined in `luaCodeWrapper`)
- **Permission tier:** Always available
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`function getPersonaImage` in `luaCodeWrapper`, wrapping `declareAPI('getPersonaImageMain', ...)`)

Returns the current persona (user) icon as an
[`{{inlayed::id}}`](../element/inlay-tokens.md) token, or an empty string if
there is no usable icon. A thin preamble wrapper that awaits the raw
[`getPersonaImageMain`](getPersonaImageMain.md).

## Signature

```lua
getPersonaImage(id)   -- returns a Promise; call :await()
```

The preamble defines it as:

```lua
function getPersonaImage(id)
    return getPersonaImageMain(id):await()
end
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. No permission set is checked. |

## Returns

A Promise. After `:await()`, a string:

- `{{inlayed::<id>}}` if a persona icon exists (loaded into the inlay store).
- `''` if there is no persona icon, the inlay write fails, or any error is thrown.

## Permission

Always available — the underlying `getPersonaImageMain` carries **no guard**, so
it works for any access key regardless of tier (including from edit listeners).
It is *not* gated behind `lowLevelAccess`. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Inlay tokens](../element/inlay-tokens.md) — returns an `{{inlayed::id}}`
  token (renders wrapped in a `risu-inlay-image` div).

## Example

```lua
function onStart(id)
    local img = getPersonaImage(id):await()
    if img ~= '' then
        addChat(id, 'user', img)
    end
end
```

## See also

- Raw host call: [`getPersonaImageMain`](getPersonaImageMain.md)
- Character image: [`getCharacterImage`](getCharacterImage.md)
- Elements: [Inlay tokens](../element/inlay-tokens.md),
  [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
