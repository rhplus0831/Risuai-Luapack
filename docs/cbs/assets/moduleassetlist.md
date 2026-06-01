# CBS: `{{moduleassetlist::namespace}}`

- Layer: CBS function
- Category: assets
- Aliases: `module_assetlist`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`moduleassetlist`)

Returns a JSON array of a module's asset names.

## Syntax

```text
{{moduleassetlist::namespace}}
{{module_assetlist::namespace}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `namespace` | yes | The `namespace` of an enabled module. |

## Behavior

Searches the enabled modules (`getModules()`) for the one whose `namespace`
equals the first argument. If no module matches, it returns an empty string.

Otherwise it returns a JSON array (`makeArray`) of that module's `assets`, using
only the first element of each entry — the asset name. Module assets are
stored as `[name, path, ...]`, so the result is `["icon","frame",...]`.

Module assets are part of the same asset library that the display tokens resolve
against, so these names work with tokens like [`{{img::name}}`](img.md) and
[`{{asset::name}}`](asset.md) when the module is enabled.

## Example

```text
Module assets: {{moduleassetlist::my-ui-module}}
```

## See also

- CBS: [`{{assetlist}}`](assetlist.md), [`{{chardisplayasset}}`](chardisplayasset.md)
- Element: [Modules](../../element/modules.md), [Asset display tokens](../../element/asset-tokens.md)
