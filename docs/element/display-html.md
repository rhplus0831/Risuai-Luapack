# Element: Display HTML (sanitization & chat buttons)

- **Kind:** Element (runtime concept)
- **Source:** `Refer/Risuai/src/ts/parser/parser.svelte.ts` (`trimMarkdown`, the DOMPurify hooks, `parseThoughtsAndTools`, `decodeStyle`/`decodeStyleRule`), `Refer/Risuai/src/lib/ChatScreens/Chat.svelte` (`handleButtonTriggerWithin`)

How Risu sanitizes the HTML it renders for chat / display output, and the custom
attributes that turn markup into clickable triggers.

## Sanitization

Rendered chat and display HTML is passed through **DOMPurify** (`trimMarkdown`).
On top of the defaults, Risu allows extra tags and attributes:

- **Allowed tags** (`ADD_TAGS`): `iframe`, `style`, `risu-style`, `x-em`, and
  the MathML set (`annotation`, `semantics`, `mrow`, `mi`, `mo`, `mn`, `msup`,
  `msub`, `mfrac`, `msqrt`).
- **Allowed attributes** (`ADD_ATTR`): `allow`, `allowfullscreen`,
  `frameborder`, `scrolling`, and the Risu custom attrs `risu-ctrl`, `risu-btn`,
  `risu-trigger`, `risu-mark`, `risu-id`, plus `x-hl-lang` / `x-hl-text`.

Sanitizer rules worth knowing:

- **iframes** are kept only when `src` starts with
  `https://www.youtube.com/embed/`; any other iframe is removed.
- **`<a href>`** to `http(s)` gets `target="_blank"`; other hrefs are stripped.
- **`blob:` media `src`** on `IMG`/`SOURCE`/`VIDEO`/`AUDIO`/`STYLE` is force-kept
  (so inlay/asset blobs survive).
- **"Hide all images"** rewrites external `<img>` and `background-image:` URLs.

## `x-risu-` class prefix

Every `class` value (except `hljs*` and already-prefixed `x-risu-*`) is rewritten
with an `x-risu-` prefix during sanitization. So `class="button-default"`
renders as `class="x-risu-button-default"`. The same applies inside `<style>`:
class selectors are prefixed with `x-risu-` **and** scoped under `.chattext`
(`.button-default { … }` becomes `.chattext .x-risu-button-default { … }`). Write
your CSS and your markup against the *unprefixed* names; Risu handles both sides.

## `<Thoughts>` blocks

`parseThoughtsAndTools` rewrites a `<Thoughts>…</Thoughts>` region (nesting
aware) into a collapsible details block:

```html
<details><summary>…</summary>…</details>
```

(`<tool_call>…</tool_call>` is likewise rendered as a small
`x-risu-tool-call` notice.)

## Chat buttons (triggers)

Two custom attributes turn an element into a clickable trigger. `Chat.svelte`'s
click handler walks up to the closest `[risu-trigger], [risu-btn]` and dispatches:

| Attribute(s) | Dispatches to |
|--------------|---------------|
| `risu-trigger="name"` (optionally with `risu-id="..."`) | `runTrigger(char, 'manual', { manualName, triggerId })` — a **manual trigger** by name |
| `risu-btn="event"` | `runLuaButtonTrigger(char, event)` — runs the Lua [`onButtonClick`](../hooks/onButtonClick.md) handler with `event` as its data argument |

Note the distinction: the CBS [`{{button::Text::cmd}}`](../cbs/assets/button.md)
helper emits `<button class="button-default" risu-trigger="cmd">…</button>`,
which fires a **manual trigger** named `cmd` (handled by a global Lua function
`cmd(id)` when the manual trigger runs Lua). To target the dedicated
`onButtonClick` Lua entry point instead, emit your own element with a `risu-btn`
attribute, e.g.:

```html
<button class="my-btn" risu-btn="open_menu">Open</button>
```

After a trigger runs, Risu applies the returned chat and reloads the message.

## Used by

- Hooks: [`editDisplay`](../hooks/editDisplay.md) (its return value is rendered
  through this sanitizer), [`onButtonClick`](../hooks/onButtonClick.md)
  (`risu-btn` target)
- Elements: [Background embedding](background-embedding.md) uses the same
  sanitizer/scoping; [Asset display tokens](asset-tokens.md) and
  [Inlay tokens](inlay-tokens.md) produce HTML that flows through here

## See also

- Elements: [Background embedding](background-embedding.md),
  [Regex Script](regex-script.md), [Inlay tokens](inlay-tokens.md)
- CBS: [`{{button}}`](../cbs/assets/button.md)
- Index: [`docs/README.md`](../README.md)
