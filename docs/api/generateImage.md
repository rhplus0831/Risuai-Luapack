# API: `generateImage(id, value, negValue)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Low-level (requires `lowLevelAccess`)
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('generateImage', ...)`)

Generates an AI image from a prompt (and optional negative prompt), stores it in
Risu's inlay store, and returns an [`{{inlay::id}}`](../element/inlay-tokens.md)
token you can drop into chat text or feed back into a multimodal LLM call.

## Signature

```lua
generateImage(id, value, negValue)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `value` | string | The image prompt. |
| `negValue` | string | Optional (default `''`). The negative prompt. |

## Returns

A Promise. After `:await()`, a string:

- On success, an [inlay token](../element/inlay-tokens.md) `{{inlay::<id>}}`.
- On failure, the string `'Error: Image generation failed'`.

## Permission

Low-level tier — the call no-ops unless `id` is in `ScriptingLowLevelIds`,
granted only to safe-mode runs **when the character/module has `lowLevelAccess`
enabled**. It is **never** available to edit listeners
([`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md),
[`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)),
which run with low-level access forced off. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Inlay tokens](../element/inlay-tokens.md) — the return value is an
  `{{inlay::id}}` token; it renders as the image when placed in displayed text,
  and attaches as multimodal input to user/system messages in
  [`LLM`](LLM.md)/[`axLLM`](axLLM.md) when `useMultimodal = true`.

## Example

```lua
function onOutput(id)
    local token = generateImage(id, 'a cozy cabin in the snow', 'blurry, text'):await()
    if token ~= 'Error: Image generation failed' then
        addChat(id, 'char', token)
    end
end
```

## See also

- Image getters: [`getCharacterImage`](getCharacterImage.md),
  [`getPersonaImage`](getPersonaImage.md)
- Elements: [Inlay tokens](../element/inlay-tokens.md),
  [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
