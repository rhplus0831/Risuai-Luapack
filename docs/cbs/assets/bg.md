# CBS: `{{bg::name}}`

- **Layer:** CBS function (display token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Renders a full-size background div from a named asset — only in background mode.

## Syntax

```text
{{bg::name}}
```

## Behavior

Gated on the parser running in background mode (`mode === 'back'`). When in
background mode it emits a cover-sized div:

```html
<div style="width:100%;height:100%;background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),url(p); background-size: cover;"></div>
```

where `p` is the resolved asset URL/path. In normal chat it expands to an empty
string. Also resolves to empty when no asset matches or when "hide all images"
is on.

## Example

```text
{{bg::room}}
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- Element: [Background embedding](../../element/background-embedding.md)
- CBS: [`{{video-img::name}}`](video-img.md), [`{{bgm::name}}`](bgm.md)
