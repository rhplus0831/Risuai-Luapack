# CBS: `{{img::name}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders a bare inline image.

## Syntax

```text
{{img::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets. The display parser emits an unstyled `<img>` (no
surrounding frame):

```html
<img src="p" alt="p" style="..."/>
```

where `p` is the resolved asset URL/path; the inline `style` only carries the
user's `assetWidth` setting. Contrast [`{{image::name}}`](image.md), which wraps
the image in a `risu-inlay-image` frame. Resolves to an empty string when no
asset matches or when "hide all images" is on.

## Example

```text
{{img::icon}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{image::name}}`](image.md), [`{{asset::name}}`](asset.md)
