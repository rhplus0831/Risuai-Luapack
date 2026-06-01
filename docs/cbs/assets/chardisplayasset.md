# CBS: `{{chardisplayasset}}`

- **Layer:** CBS function
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`chardisplayasset`)

Returns a JSON array of the character's display asset names, filtered by the
prebuilt-asset exclusion settings.

## Syntax

```text
{{chardisplayasset}}
```

## Arguments

This token takes no arguments.

## Behavior

Like [`{{assetlist}}`](assetlist.md), this reads the selected character's
`additionalAssets`, but it is gated on the character's display configuration:

- If `prebuiltAssetCommand` is **not** set, it returns an empty array (`[]`).
- Otherwise it filters out every asset whose **path** (`f[1]`) appears in the
  character's `prebuiltAssetExclude` list, then returns a JSON array
  (`makeArray`) of the remaining asset **names** (`f[0]`).

The result is the subset of asset names intended for display, with excluded
assets removed.

## Example

```text
Display assets: {{chardisplayasset}}
```

## See also

- CBS: [`{{assetlist}}`](assetlist.md), [`{{emotionlist}}`](emotionlist.md)
- Element: [Asset display tokens](../../element/asset-tokens.md)
