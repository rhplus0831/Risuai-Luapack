# Translation

Multi-provider translation with caching, HTML traversal, and character-scoped
prompts. Source: `src/ts/translator/`.

---

## 1. Entry points

- `translate(text, reverse)` — `translator.ts:39` — the public API. Uses an
  in-memory cache.
- `runTranslator(text, reverse, from, target, exarg)` — `:57` — provider
  dispatch.
- `translateHTML(html, reverse, charArg, chatID, regenerate)` — `:257` —
  recursive DOM walk with chunking for large pages.
- `getCurrentTranslatorPreset()` — `:35` — loads the active preset from the
  database.
- `LLMCacheStorage` — `:29` — localforage instance dedicated to LLM
  translation results.

---

## 2. Providers

`translator.ts:121-241` dispatches by `db.translator` to:

| Provider | Branch | Notes |
|----------|--------|-------|
| **LLM** | `:123-126` | Uses `requestChatData()` with a preset's system prompt; result is cached in `LLMCacheStorage`. |
| **DeepL** | `:127-145` | Free or pro endpoints; auth token from `db.deeplOptions`. |
| **DeepLX** | `:147-179` | Self-hosted reverse proxy; URL & bearer token configurable. |
| **Bergamot** | `:180-187` | Mozilla Firefox Translations, offline, lazy WASM (`bergamotTranslator.ts`); supports HTML mode. |
| **Google Translate** | `:188-241` | Fallback via `translate.googleapis.com`; experimental HTML scraping path. |

---

## 3. LLM translator presets

`src/ts/translator/presets.ts`.

Each preset is stored encrypted as a `.risutl` file:

```ts
interface TranslatorPreset {
  name: string
  prompt: string          // system prompt template (CBS-expanded)
  maxResponse: number
}
```

State synced via the `TranslatorPresetStateLike` interface (`presets.ts:6-169`).
Presets can be exported / imported through the UI.

Tests: `presets.test.ts`.

---

## 4. HTML translation

`translateHTML()` walks the DOM, batches text nodes, and chunks them to the
provider's limits (`translator.ts:257-498`). Cache keys include the HTML hash
so re-translating an unchanged page is a no-op.

For the offline Bergamot path, the HTML chunking strategy is different — the
engine accepts HTML directly and preserves tags.

---

## 5. Caching

- **In-memory** — `translator.ts:39` keeps a Map per-session.
- **Persistent (LLM)** — `LLMCacheStorage` in localforage
  (`translator.ts:576-618`). Keyed by `text|prompt-hash|model|preset`.
- Bypass via `regenerate: true` parameter.

---

## 6. Where translation is invoked

Most commonly:

- The chat UI per-message translate button (`lib/ChatScreens/Message.svelte`).
- The `editdisplay` regex/triggers path can translate output before display
  (when `db.autoTranslate` is on).
- The user-input translate path applies before sending.
- The Playground translation page (`lib/Playground/PlaygroundTranslation.svelte`).

---

## 7. Related docs

- [requests.md](./requests.md) — the LLM translator reuses the request layer.
- [processing-pipeline.md](./processing-pipeline.md) — auto-translate hooks
  into output/display regex.
