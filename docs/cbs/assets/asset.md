# CBS: `{{asset::name}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders a character/module asset as an image or a video, chosen by file
extension.

## Syntax

```text
{{asset::name}}
```

## Behavior

`name` is matched (case-insensitively) against the selected character's
`additionalAssets` plus enabled-module assets. The display parser emits:

- a muted looping `<video><source src="p" type="video/mp4"></video>` if the
  resolved asset's extension is a video type, or
- `<img src="p" alt="p" style="..."/>` otherwise.

`p` is the resolved asset URL/path. Resolves to an empty string when no asset
matches or when "hide all images" is on.

## Example

```text
{{asset::map}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{img::name}}`](img.md), [`{{video::name}}`](video.md), [`{{assetlist}}`](assetlist.md)
