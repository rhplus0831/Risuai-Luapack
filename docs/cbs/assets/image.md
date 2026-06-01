# CBS: `{{image::name}}`

- **Layer:** CBS function (display token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders a framed image block.

## Syntax

```text
{{image::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets. The display parser emits an image wrapped in a styled
inlay frame:

```html
<div class="risu-inlay-image"><img src="p" alt="p" style="..."/></div>
```

where `p` is the resolved asset URL/path. Contrast [`{{img::name}}`](img.md),
which emits a bare unstyled `<img>`. Resolves to an empty string when no asset
matches or when "hide all images" is on.

## Example

```text
{{image::portrait}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{img::name}}`](img.md), [`{{asset::name}}`](asset.md)
