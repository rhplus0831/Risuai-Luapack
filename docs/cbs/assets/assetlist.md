# CBS: `{{assetlist}}`

- **Layer:** CBS function
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`assetlist`)

Returns a JSON array of the current character's additional asset names.

## Syntax

```text
{{assetlist}}
```

## Arguments

This token takes no arguments.

## Behavior

Reads the selected character's `additionalAssets` and returns a JSON array
(`makeArray`) of the **first element of each entry** — the asset name only, not
the path or extension. `additionalAssets` is stored as `[name, path, ext]`
triples, so the result is `["sword","map",...]`.

Returns an empty string when there is no selected character or when the
character is a `group`.

These names are the ones you pass to the asset display tokens such as
[`{{img::name}}`](img.md), [`{{image::name}}`](image.md), and
[`{{asset::name}}`](asset.md).

## Example

```text
Assets: {{assetlist}}
```

## See also

- CBS: [`{{emotionlist}}`](emotionlist.md), [`{{chardisplayasset}}`](chardisplayasset.md), [`{{moduleassetlist::namespace}}`](moduleassetlist.md)
- Element: [Asset display tokens](../../element/asset-tokens.md)
