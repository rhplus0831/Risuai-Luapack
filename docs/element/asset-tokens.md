# Element: Asset display tokens (`{{img::}}`, `{{video::}}`, …)

- Kind: Element (display token)
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`assetRegex`, `parseAdditionalAssets`)

Tokens the display parser expands into image/video/audio/background HTML when it
renders chat text and background embedding. These are display helpers, not
multimodal attachments — contrast [inlay tokens](inlay-tokens.md).

## What it is

When Risu renders a message (or background HTML), `parseAdditionalAssets` scans
for `{{type::name}}` tokens matching:

```text
/{{(raw|path|img|image|video|audio|bgm|bg|emotion|asset|video-img|source)::(.+?)}}/gms
```

`name` is matched case-insensitively against the selected character's
`additionalAssets` plus enabled-module assets (a fuzzy closest-match is used if
there is no exact hit, unless legacy media-finding is on). Emotion tokens use
the character's `emotionImages`. A token that resolves to nothing expands to an
empty string.

You can emit these tokens from Lua (e.g. via `setChat`, `setBackgroundEmbedding`,
or an `editDisplay` listener); Risu expands them at display time.

## Tokens and the HTML they emit

`p` below is the resolved asset URL/path; widths reflect the user's `assetWidth`
setting.

| Token | Emits (verified from `parseAdditionalAssets`) |
|-------|-----------------------------------------------|
| `{{raw::name}}` | the bare path `p` (no tag — useful in CSS `url(...)`) |
| `{{path::name}}` | the bare path `p` (same as `raw`) |
| `{{img::name}}` | `<img src="p" alt="p" style="…"/>` |
| `{{image::name}}` | `<div class="risu-inlay-image"><img src="p" alt="p" style="…"/></div>` |
| `{{video::name}}` | `<video controls autoplay loop><source src="p" type="video/mp4"></video>` |
| `{{video-img::name}}` | `<video autoplay muted loop><source src="p" type="video/mp4"></video>` |
| `{{audio::name}}` | `<audio controls autoplay loop><source src="p" type="audio/mpeg"></audio>` |
| `{{asset::name}}` | `<video …>` if the asset extension is a video type, else `<img …>` |
| `{{bg::name}}` | a full-size background `<div style="…background:…url(p)…">` — only in background mode; expands to empty in normal chat |
| `{{bgm::name}}` | `<div risu-ctrl="bgm___auto___p" style="display:none;"></div>` (hidden BGM control) |
| `{{emotion::name}}` | `<img src="…" alt="…" style="…"/>` from `emotionImages` |
| `{{source::char}}` | the selected character image URL/path (bare) |
| `{{source::user}}` | the active user-icon URL/path (bare) |

`bg` is gated on `mode === 'back'`; the others render in both normal chat and
background mode. When the user enables "hide all images", the image-bearing
tokens (`img`, `image`, `emotion`, `asset`, `bg`, `raw`, `path`) expand to
empty.

## Not multimodal

These tokens produce HTML for the screen only. They are not attached to
LLM/`axLLM` requests, even with `useMultimodal=true`. For multimodal attachments
use [inlay tokens](inlay-tokens.md) (`{{inlay::}}` / `{{inlayed::}}` /
`{{inlayeddata::}}`), which Risu can strip from text and attach as media.

## Shape / fields

| Concept | Source | Notes |
|---------|--------|-------|
| asset library | character `additionalAssets` + module assets | `[name, path, ext]` triples |
| emotion library | character `emotionImages` | `[name, path]` pairs |

## Used by

- Elements: surfaced through [Display HTML](display-html.md) rendering and
  [Background embedding](background-embedding.md) (background mode)
- Modules contribute the asset library — see [Modules](modules.md)

## See also

- Elements: [Inlay tokens](inlay-tokens.md), [Display HTML](display-html.md),
  [Background embedding](background-embedding.md)
- Index: [`docs/README.md`](../README.md)
