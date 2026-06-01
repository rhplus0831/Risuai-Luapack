# API: `getPersonaImageMain(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getPersonaImageMain', ...)`)

The **raw** host call behind [`getPersonaImage`](getPersonaImage.md). Loads the
current persona (user) icon into Risu's inlay store and returns an
[`{{inlayed::id}}`](../element/inlay-tokens.md) token, or `''`. The preamble
helper [`getPersonaImage`](getPersonaImage.md) simply awaits this; prefer it
unless you have a reason to call the raw form.

## Signature

```lua
getPersonaImageMain(id)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. No permission set is checked. |

## Returns

A Promise. After `:await()`, a string:

- `{{inlayed::<id>}}` when a persona icon exists.
- `''` if there is no persona icon, the inlay write fails, or any error is thrown.

## Permission

Always available — there is **no guard** on this call, so it works for any
access key regardless of tier (including from edit listeners). It is *not*
gated behind `lowLevelAccess`. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Inlay tokens](../element/inlay-tokens.md) — returns an `{{inlayed::id}}` token.

## Example

```lua
function onStart(id)
    local img = getPersonaImageMain(id):await()
    if img ~= '' then
        log(img)
    end
end
```

## See also

- Preamble helper: [`getPersonaImage`](getPersonaImage.md)
- Character image: [`getCharacterImageMain`](getCharacterImageMain.md)
- Elements: [Inlay tokens](../element/inlay-tokens.md),
  [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
