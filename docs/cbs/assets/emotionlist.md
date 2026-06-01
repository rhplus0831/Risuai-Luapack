# CBS: `{{emotionlist}}`

- **Layer:** CBS function
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`emotionlist`)

Returns a JSON array of the current character's emotion image names.

## Syntax

```text
{{emotionlist}}
```

## Arguments

This token takes no arguments.

## Behavior

Reads the selected character's `emotionImages` and returns a JSON array
(`makeArray`) containing only the **first element of each entry** — the emotion
name — never the image path or data. `emotionImages` is stored as `[name, path]`
pairs, so the result is `["happy","sad",...]`.

Returns an empty string when there is no selected character, and an empty array
(`[]`) when the character has no emotion images.

The names returned here are exactly those you reference with the
[`{{emotion::name}}`](emotion.md) display token.

## Example

```text
Available emotions: {{emotionlist}}
```

## See also

- CBS: [`{{emotion::name}}`](emotion.md), [`{{assetlist}}`](assetlist.md), [`{{chardisplayasset}}`](chardisplayasset.md)
- Element: [Asset display tokens](../../element/asset-tokens.md)
