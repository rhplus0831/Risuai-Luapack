# CBS: `{{inlay::id}}`

- Layer: CBS function (inlay token)
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseInlayAssets`)

Renders an inlay-store asset by id, unstyled. Display only.

## Syntax

```text
{{inlay::id}}
```

## Behavior

`id` points at a blob in Risu's inlay storage. The display parser
(`parseInlayAssets`) replaces the token with `<img>`/`<video>`/`<audio>` HTML
according to the blob's media type — and for `inlay` the media is emitted
bare, with no surrounding `risu-inlay-image` wrapper (contrast
[`{{inlayed::id}}`](inlayed.md)).

[`generateImage`](../../api/generateImage.md) returns this token form.

Not included in the model request. `inlay` is display-only: for an assistant
message it is never attached as multimodal input, and only attaches for
user/system messages when `useMultimodal` is on. For a token that is always part
of the request, use [`{{inlayeddata::id}}`](inlayeddata.md).

## Example

```text
{{inlay::abc123}}
```

## See also

- Full reference: [Inlay tokens](../../element/inlay-tokens.md)
- CBS: [`{{inlayed::id}}`](inlayed.md), [`{{inlayeddata::id}}`](inlayeddata.md)
- API: [`generateImage`](../../api/generateImage.md)
