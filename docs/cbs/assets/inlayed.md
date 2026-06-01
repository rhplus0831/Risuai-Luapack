# CBS: `{{inlayed::id}}`

- **Layer:** CBS function (inlay token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseInlayAssets`)

Renders an inlay-store asset by id, styled. Display only.

## Syntax

```text
{{inlayed::id}}
```

## Behavior

`id` points at a blob in Risu's inlay storage. The display parser
(`parseInlayAssets`) replaces the token with media HTML wrapped in a styled
frame, e.g. `<div class="risu-inlay-image"><img src="blob:..."/></div>`
(contrast the bare [`{{inlay::id}}`](inlay.md)).

This is the token form returned by
[`getCharacterImage`](../../api/getCharacterImage.md) and
[`getPersonaImage`](../../api/getPersonaImage.md).

**Not included in the model request.** Like `inlay`, it is display-only: for an
assistant message it is never attached as multimodal input, and only attaches
for user/system messages when `useMultimodal` is on. For a token that is always
part of the request, use [`{{inlayeddata::id}}`](inlayeddata.md).

## Example

```text
{{inlayed::abc123}}
```

## See also

- Full reference: [Inlay tokens](../../element/inlay-tokens.md)
- CBS: [`{{inlay::id}}`](inlay.md), [`{{inlayeddata::id}}`](inlayeddata.md)
- API: [`getCharacterImage`](../../api/getCharacterImage.md), [`getPersonaImage`](../../api/getPersonaImage.md)
