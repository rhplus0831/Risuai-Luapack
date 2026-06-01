# Element: Inlay tokens (`{{inlay::}}`, `{{inlayed::}}`, `{{inlayeddata::}}`)

- Kind: Element (display token)
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseInlayAssets`), `Refer/Risuai/src/ts/process/scriptings.ts` (`generateImage`, `getCharacterImageMain`, `getPersonaImageMain`, the `useMultimodal` extractor in `LLMMain`/`axLLMMain`)

Tokens that reference files in Risu's inlay storage. They render as media for
display and can be attached as multimodal input to LLM calls — unlike
[asset display tokens](asset-tokens.md).

## What it is

An inlay token points at a blob in Risu's inlay store by id:

```text
{{inlay::<id>}}
{{inlayed::<id>}}
{{inlayeddata::<id>}}
```

Lua image APIs return these tokens:

- [`generateImage`](../api/generateImage.md) returns `{{inlay::<id>}}`.
- [`getCharacterImage`](../api/getCharacterImage.md) and
  [`getPersonaImage`](../api/getPersonaImage.md) return `{{inlayed::<id>}}`.

`{{inlayeddata::<id>}}` is not produced by a Lua getter directly, but it is
recognized everywhere inlay tokens are parsed. It is the only inlay form that
assistant messages attach as multimodal input.

## Display rendering

`parseInlayAssets` looks up each id's blob and replaces the token with HTML by
media type. `inlay` renders bare; `inlayed`/`inlayeddata` wrap in a
`<div class="risu-inlay-image">…</div>`:

| Blob type | Replacement (for `inlayed`/`inlayeddata`) |
|-----------|-------------------------------------------|
| image | `<div class="risu-inlay-image"><img src="blob:…"/></div>` |
| video | `<div class="risu-inlay-image"><video controls><source src="blob:…" type="video/mp4"></video></div>` |
| audio | `<div class="risu-inlay-image"><audio controls><source src="blob:…" type="audio/mpeg"></audio></div>` |

For `{{inlay::…}}` the wrapper `<div>` is omitted. With "hide all images" on,
image inlays render as empty.

## Multimodal extraction (`useMultimodal = true`)

When [`LLM`](../api/LLM.md) / [`axLLM`](../api/axLLM.md) run with
`useMultimodal = true`, each message's content is scanned with
`/{{(inlay|inlayed|inlayeddata)::(.+?)}}/g`. The matched token text is removed
from the content, the referenced blob is loaded with `getInlayAsset`, and it
is attached to the request as a `MultiModal` entry. Which tokens attach depends
on the message role:

| Message `role` | Tokens attached |
|----------------|-----------------|
| `assistant` | only `{{inlayeddata::…}}` |
| `user` / `system` (any non-assistant) | all three: `inlay`, `inlayed`, `inlayeddata` |

So for an assistant message, `{{inlay::…}}` and `{{inlayed::…}}` are *not*
attached (only `inlayeddata` is); for user/system messages every inlay form is
attached. Without `useMultimodal`, the tokens are left in the text as-is.

## Asset tokens vs. inlay tokens

[Asset display tokens](asset-tokens.md) (`{{img::}}`, `{{image::}}`, …) are
display-only and never attached to an LLM request. Inlay tokens are the bridge
for multimodal Lua LLM calls. Use the inlay tokens returned by `generateImage` /
`getCharacterImage` / `getPersonaImage` when you want the model to *see* the
image.

## Shape / fields

| Token | Produced by | Display wrapper | Assistant multimodal | User/system multimodal |
|-------|-------------|-----------------|----------------------|------------------------|
| `{{inlay::id}}` | `generateImage` | none | no | yes |
| `{{inlayed::id}}` | `getCharacterImage`, `getPersonaImage` | `risu-inlay-image` div | no | yes |
| `{{inlayeddata::id}}` | (recognized in text) | `risu-inlay-image` div | yes | yes |

## Used by

- APIs: [`generateImage`](../api/generateImage.md),
  [`getCharacterImage`](../api/getCharacterImage.md),
  [`getPersonaImage`](../api/getPersonaImage.md),
  [`LLM`](../api/LLM.md), [`axLLM`](../api/axLLM.md)
- CBS: [`{{inlay}}`](../cbs/assets/inlay.md), [`{{inlayed}}`](../cbs/assets/inlayed.md),
  [`{{inlayeddata}}`](../cbs/assets/inlayeddata.md)

## See also

- Elements: [Asset display tokens](asset-tokens.md), [Display HTML](display-html.md)
- Index: [`docs/README.md`](../README.md)
