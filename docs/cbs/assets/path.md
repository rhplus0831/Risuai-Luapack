# CBS: `{{path::name}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Expands to the bare URL/path of a named asset (no HTML tag).

## Syntax

```text
{{path::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets, and the token expands to the resolved asset URL/path `p`
as plain text — no `<img>`/`<video>` wrapper. This is identical to
[`{{raw::name}}`](raw.md); both are handled by the same branch. Useful inside
CSS `url(...)`. Resolves to an empty string when no asset matches, and is also
suppressed when "hide all images" is on.

## Example

```text
<div style="background-image:url({{path::wallpaper}})"></div>
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{raw::name}}`](raw.md), [`{{source::char}}`](source.md)
