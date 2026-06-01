# Audio & image integrations

Two side integrations that turn chat content into other media: text-to-speech
(TTS) and image generation (Stable Diffusion).

---

## 1. TTS pipeline

`src/ts/process/tts.ts` + `src/ts/process/ttsHooks.ts`.

### Entry — `sayTTS(character, text)` `tts.ts:80`

1. Extract speakable text. If `character.ttsReadOnlyQuoted` is on, keep only
   text inside quotes/brackets.
2. Pick the engine:
   - **VITS** — character-specific voice models. `runVITS(text, voiceId)`
     calls a transformers.js VITS encoder.
   - **WebTTS** — `src/ts/voice.ts` wraps `window.speechSynthesis`.
   - **Cloud / Risuai TTS** — provider clients per `db.ttsProvider`.
3. Run the pre/post hook pipeline.
4. Play the resulting `AudioBuffer`.

### Hook pipeline — `ttsHooks.ts`

`tts.ts:31-66`:

- `getTTSPreprocessors()` — pre-encode (e.g. translate to target language,
  text normalisation).
- `getTTSPostprocessors()` — post-synthesis (audio format conversion,
  effects).

Each hook is given a fresh `Uint8Array`/`ArrayBuffer` slice per invocation
so detached-buffer errors don't bubble. Plugins can register hooks via the
V3 API (`apiV3/v3.svelte.ts` — TTS hook registration entries).

### Voice files

Character cards can embed VITS voice files in `chara-ext-asset_voice_*` PNG
chunks (`characterCards.ts` import path; `backuplocal.ts:50-56` for backup).
The `character.vits` field carries voice model references.

Tests live in `ttsHooks.test.ts`.

---

## 2. Image generation (Stable Diffusion)

`src/ts/process/stableDiff.ts`.

### Orchestrator — `stableDiff(currentChar, prompt)` `:12`

1. Build a visual prompt from chat context (sub-LLM call shaped by the
   user's image-prompt template).
2. Call `generateAIImage()` with the result.

### Generator — `generateAIImage(genPrompt, currentChar, neg, returnSdData)` `:64`

Routes by `db.sdProvider`:

- **WebUI** (`:67`) — Local Stable Diffusion WebUI at `db.webUiUrl`,
  endpoint `/sdapi/v1/txt2img`.
- **Kei cloud** — `keiServerURL` for remote inference (Risuai-hosted).
- **NovelAI image** — gated by API key.

Config knobs in the DB:

- `db.sdProvider`
- `db.sdConfig.width` / `db.sdConfig.height`
- `db.sdSteps`
- `db.sdCFG`
- Sampler and other provider-specific fields.

### How it's invoked

- From a trigger (`runLLMImage` effect).
- From a Lua/Python script (`generateImage(prompt, neg)`).
- From the Playground (`lib/Playground/PlaygroundImageGen.svelte`).

---

## 3. Voice (Web Speech API)

`src/ts/voice.ts` is the WebTTS wrapper used when no other engine is
configured. It enumerates `speechSynthesis.getVoices()` and lets the user pick
in Settings → Display / Accessibility.

---

## 4. Related docs

- [plugins.md](./plugins.md) — plugins can register TTS hooks and custom
  providers.
- [scripting.md](./scripting.md) — Lua/Python expose `generateImage` and
  TTS calls.
