# CBS: `{{raw::name}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Expands to the bare URL/path of a named asset (no HTML tag).

## Syntax

```text
{{raw::name}}
```

## Behavior

`name` resolves against the selected character's `additionalAssets` plus
enabled-module assets, and the token expands to the resolved asset URL/path `p`
as plain text. It shares the exact same branch as [`{{path::name}}`](path.md) —
both just return `p`. Useful inside CSS `url(...)`. Resolves to an empty string
when no asset matches, and is also suppressed when "hide all images" is on.

## Example

```text
<div style="background-image:url({{raw::wallpaper}})"></div>
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{path::name}}`](path.md), [`{{source::char}}`](source.md)
