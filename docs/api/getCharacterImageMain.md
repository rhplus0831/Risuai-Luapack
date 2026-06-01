# API: `getCharacterImageMain(id)`

- Layer: Host API (`declareAPI`)
- Permission tier: Always available
- Async: yes (`:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getCharacterImageMain', ...)`)

The raw host call behind [`getCharacterImage`](getCharacterImage.md). Loads
the selected character's image into Risu's inlay store and returns an
[`{{inlayed::id}}`](../element/inlay-tokens.md) token, or `''`. The preamble
helper [`getCharacterImage`](getCharacterImage.md) simply awaits this; prefer it
unless you have a reason to call the raw form.

## Signature

```lua
getCharacterImageMain(id)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. No permission set is checked. |

## Returns

A Promise. After `:await()`, a string:

- `{{inlayed::<id>}}` when the selected character has a usable image.
- `''` if the selected index is out of range, the character is a group, has no
  image, the inlay write fails, or any error is thrown.

## Permission

Always available — there is no guard on this call, so it works for any
access key regardless of tier (including from edit listeners). It is *not*
gated behind `lowLevelAccess`. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Inlay tokens](../element/inlay-tokens.md) — returns an `{{inlayed::id}}` token.

## Example

```lua
function onStart(id)
    local img = getCharacterImageMain(id):await()
    if img ~= '' then
        log(img)
    end
end
```

## See also

- Preamble helper: [`getCharacterImage`](getCharacterImage.md)
- Persona image: [`getPersonaImageMain`](getPersonaImageMain.md)
- Elements: [Inlay tokens](../element/inlay-tokens.md),
  [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
