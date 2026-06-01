# Model registry & capability flags

`src/ts/model/` holds the metadata: which models exist, which provider runs
them, which API format they speak, and what capabilities they expose. The
request layer (`src/ts/process/request/`) consumes this metadata to dispatch
properly — see [requests.md](./requests.md).

---

## 1. Core type

`src/ts/model/types.ts:102` defines `LLMModel`:

```ts
interface LLMModel {
  id: string                // canonical identifier (used in db.aiModel)
  name: string              // display name
  provider: LLMProvider     // who hosts it
  format: LLMFormat         // wire protocol family
  flags: LLMFlags           // bitmask of capabilities
  parameters: string[]      // tunable param names (temperature, top_p, …)
  tokenizer: Tokenizer      // which tokenizer to count against
  // … additional fields per category
}
```

- `LLMProvider` (`types.ts:32-50`) — `OpenAI`, `Anthropic`, `GoogleCloud`,
  `AWS`, `Ollama`, `WebLLM`, `Horde`, …
- `LLMFormat` (`types.ts:53-78`) — `OpenAICompatible`, `Anthropic`,
  `AWSBedrockClaude`, `VertexAIGemini`, … — what the dispatcher routes on.
- `LLMFlags` (`types.ts:3-29`) — bitmask: `hasImageInput`, `hasStreaming`,
  `claudeThinking`, `geminiThinking`, `deepSeekThinkingOutput`,
  `supportsCachePoints`, etc.
- `Tokenizer` (`types.ts:81-99`) — enum: tiktoken o200k_base, Claude,
  Llama3, Gemma, Mistral, … 16 entries total.

---

## 2. Master list

`src/ts/model/modellist.ts:43` exports `LLMModels[]` — the union of:

- Hard-coded OpenAI / Anthropic / Google / AWS Bedrock / DeepInfra models
  (one constant per family in `model/providers/*.ts`).
- Dynamic Ollama / OpenRouter / Ooba models discovered at runtime.
- User-added `db.customModels`.

`getModelInfo(id)` returns the entry for an id — used by
`request.ts:440` and by `index.svelte.ts:31` for token-budget math.

---

## 3. Per-provider model files

| File | Models |
|------|--------|
| `model/providers/openai.ts` | GPT-3.5 / GPT-4 / GPT-4o / GPT-5 family, embeddings, audio. |
| `model/providers/anthropic.ts` | Claude 3 / 3.5 / 4 family + Opus 4.7 (1M ctx). |
| `model/providers/google.ts` | Gemini 1.5 / 2.0 / 2.5 / 3 family + Vertex AI. |
| `model/providers/nanogpt.ts` | NanoGPT-hosted models. |

---

## 4. Provider clients

These are runtime clients for providers that aren't fully baked into the
generic OpenAI-compatible dispatcher:

| File | Role |
|------|------|
| `model/ooba.ts` | Text Generation WebUI / oobabooga. |
| `model/ollama.ts` | Ollama (local). |
| `model/openrouter.ts` | OpenRouter (catalog + routing). |
| `model/nanogpt.ts` | NanoGPT account/billing helpers. |

---

## 5. Model picker UI

`model/modelGrid.ts` produces the data for `lib/UI/ModelGrid.svelte` (the grid
picker shown in settings). `lib/UI/ModelList.svelte` is the flat-list
alternative. NanoGPT has dedicated UI (`NanoGPTDashboard.svelte`,
`NanoGPTProviderPicker.svelte`).

---

## 6. Tokenizers

Token counting is centralized in `src/ts/tokenizer.ts` (`ChatTokenizer`).
`Tokenizer` enum entries in `types.ts:81-99` map to specific implementations:

- tiktoken via `@dqbd/tiktoken` (encodings shipped in `src/etc/o200k_base.json`).
- Claude: in-house tokenizer.
- Llama3 / Gemma / Mistral / etc.: WASM via `@huggingface/transformers` or
  `@mlc-ai/web-tokenizers`.

The pipeline calls `ChatTokenizer.tokenize(text)` per section
(`process/index.svelte.ts:310`) for budgeting.

---

## 7. Custom / reverse-proxy models

- **Custom model.** A user can add an entry in `db.customModels` with a
  chosen format. It joins `LLMModels` via the dynamic union
  (`request.ts:473-477`).
- **Reverse proxy.** Per-model proxy URL parsed in `request/shared.ts:34-64`.
- **Additional params.** `request/additionalParams.ts` parses a JSON snippet
  the user supplies and merges it onto the outgoing payload.

---

## 8. Capability flag cheat-sheet

| Flag | Effect on the request layer |
|------|-----------------------------|
| `hasStreaming` | Allow SSE streaming. |
| `hasImageInput` | Accept image attachments (multimodal). |
| `supportsCachePoints` | Inject Anthropic prompt-cache markers. |
| `claudeThinking` / `geminiThinking` | Enable thinking-token paths. |
| `deepSeekThinkingOutput` | Parse DeepSeek `<think>` tags. |
| `alterUserAssistantRoles` | Force role alternation in `reformater()`. |
| `noSystemMessages` | Fold system → first user. |

Many more flags exist; the enum is the source of truth.

---

## 9. Related docs

- [requests.md](./requests.md) — how the dispatcher uses this metadata.
- [processing-pipeline.md](./processing-pipeline.md) — token counting upstream.
