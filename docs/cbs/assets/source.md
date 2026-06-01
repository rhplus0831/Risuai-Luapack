# CBS: `{{source::char}}` / `{{source::user}}`

- Layer: CBS function (display token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseAdditionalAssets`)

Expands to the character or user profile image URL/path (bare, no HTML tag).

## Syntax

```text
{{source::char}}
{{source::user}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `char` \| `user` | yes | `char` selects the current character image; `user` selects the active user icon. |

## Behavior

Unlike the other asset tokens, `source` does not look up the asset library. The
parser marks the spot and, in a second pass, substitutes:

- `char` -> the selected character's image URL/path (`getFileSrc(chara.image)`),
- `user` -> the active user-icon URL/path (`getFileSrc(getUserIcon())`).

Either resolves to an empty string when the corresponding image is unset. The
result is a bare path, so it is suitable for CSS `url(...)` or feeding into other
HTML.

## Example

```text
<img src="{{source::char}}" />
```

## See also

- Full reference: [Asset display tokens](../../element/asset-tokens.md)
- CBS: [`{{raw::name}}`](raw.md), [`{{path::name}}`](path.md)
