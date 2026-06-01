# CBS: `{{video::name}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders a video player with controls.

## Syntax

```text
{{video::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets. The display parser emits

```html
<video controls autoplay loop><source src="p" type="video/mp4"></video>
```

where `p` is the resolved asset URL/path. Resolves to an empty string when no
asset matches.

## Example

```text
{{video::intro}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{video-img::name}}`](video-img.md), [`{{asset::name}}`](asset.md)
