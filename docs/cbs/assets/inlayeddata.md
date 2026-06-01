# CBS: `{{inlayeddata::id}}`

- **Layer:** CBS function (inlay token)
- **Category:** assets
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`parseInlayAssets`)

Renders an inlay-store asset by id, styled — and is included in the model
request.

## Syntax

```text
{{inlayeddata::id}}
```

## Behavior

`id` points at a blob in Risu's inlay storage. For display, the parser
(`parseInlayAssets`) renders it just like [`{{inlayed::id}}`](inlayed.md): media
HTML wrapped in a `risu-inlay-image` frame.

**Included in the model request (multimodal).** This is the multimodal form: when
[`LLM`](../../api/LLM.md) / [`axLLM`](../../api/axLLM.md) run with
`useMultimodal = true`, `inlayeddata` is the **only** inlay form attached for
**assistant** messages (and it also attaches for user/system messages). The token
text is stripped from the content and the referenced blob is attached as media.
Use this token when you want the model to *see* the image in an assistant turn.

## Example

```text
{{inlayeddata::abc123}}
```

## See also

- Full reference: [Inlay tokens](../../element/inlay-tokens.md)
- CBS: [`{{inlay::id}}`](inlay.md), [`{{inlayed::id}}`](inlayed.md)
- API: [`LLM`](../../api/LLM.md), [`axLLM`](../../api/axLLM.md)
