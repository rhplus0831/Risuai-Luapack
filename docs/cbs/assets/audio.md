# CBS: `{{audio::name}}`

- **Layer:** CBS function (display token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders an audio player for a named asset.

## Syntax

```text
{{audio::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets. The display parser emits

```html
<audio controls autoplay loop><source src="p" type="audio/mpeg"></audio>
```

where `p` is the resolved asset URL/path. Resolves to an empty string when no
asset matches.

## Example

```text
{{audio::theme}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{bgm::name}}`](bgm.md), [`{{video::name}}`](video.md)
