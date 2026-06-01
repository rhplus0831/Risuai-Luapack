# CBS: `{{bgm::name}}`

- **Layer:** CBS function (display token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Emits a hidden background-music control element.

## Syntax

```text
{{bgm::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets. The display parser emits a hidden control div:

```html
<div risu-ctrl="bgm___auto___p" style="display:none;"></div>
```

where `p` is the resolved asset URL/path. The element is not visible; Risu uses
the `risu-ctrl` attribute to drive BGM playback. Resolves to an empty string
when no asset matches.

## Example

```text
{{bgm::ambient}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{audio::name}}`](audio.md), [`{{bg::name}}`](bg.md)
