# CBS: `{{video-img::name}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders a muted, looping video — background-style, no controls.

## Syntax

```text
{{video-img::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets. The display parser emits

```html
<video autoplay muted loop><source src="p" type="video/mp4"></video>
```

where `p` is the resolved asset URL/path. Unlike [`{{video::name}}`](video.md)
there are no controls and the audio is muted, so it behaves like an animated
image. Resolves to an empty string when no asset matches.

## Example

```text
{{video-img::rain}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{video::name}}`](video.md), [`{{asset::name}}`](asset.md)
