# CBS: `{{emotion::name}}`

- **Layer:** CBS function (display token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders an emotion image for the current character.

## Syntax

```text
{{emotion::name}}
```

## Behavior

`name` is looked up (case-insensitively) in the selected character's
`emotionImages` (not the general asset library). The display parser emits

```html
<img src="p" alt="p" style="..."/>
```

where `p` is the resolved emotion-image path. Resolves to an empty string when
no emotion matches or when "hide all images" is on.

Names come from [`{{emotionlist}}`](emotionlist.md).

## Example

```text
{{emotion::happy}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{emotionlist}}`](emotionlist.md), [`{{img::name}}`](img.md)
