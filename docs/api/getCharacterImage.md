# API: `getCharacterImage(id)`

- **Layer:** Preamble helper (defined in `luaCodeWrapper`)
- **Permission tier:** Always available
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`function getCharacterImage` in `luaCodeWrapper`, wrapping `declareAPI('getCharacterImageMain', ...)`)

Returns the selected character's image as an
[`{{inlayed::id}}`](../element/inlay-tokens.md) token, or an empty string if
there is no usable image. This is a thin preamble wrapper that just awaits the
raw [`getCharacterImageMain`](getCharacterImageMain.md).

## Signature

```lua
getCharacterImage(id)   -- returns a Promise; call :await()
```

The preamble defines it as:

```lua
function getCharacterImage(id)
    return getCharacterImageMain(id):await()
end
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. No permission set is checked. |

## Returns

A Promise. After `:await()`, a string:

- `{{inlayed::<id>}}` if the character has a usable image (the image is loaded
  into the inlay store and a token is returned).
- `''` for a group character, a character with no image, or on any error.

## Permission

Always available — the underlying `getCharacterImageMain` carries **no guard**,
so it works for any access key regardless of tier (including from edit
listeners). Despite producing an image, it is *not* gated behind
`lowLevelAccess`. See [access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Inlay tokens](../element/inlay-tokens.md) — returns an `{{inlayed::id}}`
  token (renders wrapped in a `risu-inlay-image` div).

## Example

```lua
function onStart(id)
    local img = getCharacterImage(id):await()
    if img ~= '' then
        addChat(id, 'char', img)
    end
end
```

## See also

- Raw host call: [`getCharacterImageMain`](getCharacterImageMain.md)
- Persona image: [`getPersonaImage`](getPersonaImage.md)
- Generation: [`generateImage`](generateImage.md)
- Elements: [Inlay tokens](../element/inlay-tokens.md),
  [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
