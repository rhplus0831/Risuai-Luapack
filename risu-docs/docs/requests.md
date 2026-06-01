# AI provider request layer

Everything under `src/ts/process/request/` and the per-provider clients in
`src/ts/model/` that talk to AI APIs. Inputs come from the chat pipeline
(see [processing-pipeline.md](./processing-pipeline.md)); outputs are messages
plus optional tool calls.

---

## 1. Entry points

- `requestChatData(arg)` — `request/request.ts:205` — public wrapper with
  fallback chain, retry loop, blank-response recovery, character-set banning,
  and `before_request` trigger emission.
- `requestChatDataMain(arg, model)` — `request/request.ts:434` — dispatches by
  `LLMFormat` to one of the provider-specific request functions.

---

## 2. Format → implementation routing

`request.ts:434-527` switches on `model.format`:

| `LLMFormat` | Dispatcher |
|-------------|-----------|
| `OpenAICompatible` (and variants) | `requestOpenAI()` — `request/openAI/requests.ts:41` |
| `Anthropic`, `AWSBedrockClaude` | `requestClaude()` — `request/anthropic.ts:71` |
| `Google`, `VertexAIGemini` | `requestGoogleCloudVertex()` — `request/google.ts:44` |
| `Ollama` | `requestOllama()` — `request.ts:512` |
| `NovelAI` | `requestNovelAI()` — `request.ts:497` |
| Custom / proxy | additional branches in `request.ts:467-477` |

Provider-specific quirks live inside each dispatcher. See per-provider
sections below.

---

## 3. Retry, fallback, recovery

`requestChatData` (`request.ts:205-345`):

- **Fallback models.** `db.fallbackModels` is walked in order if the primary
  returns an unrecoverable error.
- **Retry loop.** `db.requestRetrys` (`:331`) bounds attempts. 5xx errors get a
  1 s sleep and aggressive retry; `db.antiServerOverloads` reduces retry count.
- **Blank-response detection.** If the assistant message comes back empty,
  the loop retries up to a limit (`:309-313`).
- **Character-set banning.** Unwanted Unicode ranges trigger a retry
  (`:291-307`).
- **`before_request` trigger.** Fires before every dispatch
  (`:239-242`); a trigger can abort or rewrite the call.

---

## 4. Message reformatting

`reformater()` — `request.ts:347-431` — enforces per-model constraints
*after* the chat pipeline has assembled the prompt:

- Consolidate / drop system messages for models that don't allow them
  (`:354-372`).
- Force role alternation (user / assistant / user / …) where the API
  requires it (`:375-415`).
- Make the first non-system message a user message (`:417-424`).
- Inject Anthropic `cache_control` markers per role for prompt caching
  (`:402-406`).

---

## 5. Provider notes

### OpenAI-compatible (`request/openAI/`)

- Streaming via SSE; tool calls are extracted from XML or `tool_calls`
  depending on flag.
- JSON mode and structured outputs supported via `response_format`.
- `simplifySchema()` strips unsupported JSON-schema fields before sending.

### Anthropic (`request/anthropic.ts`)

- Streaming + non-streaming.
- `cache_control: { type: 'ephemeral' }` injected per role for prompt caching.
- Vision: images attached as `image` content blocks.
- Thinking tokens supported when `LLMFlags.claudeThinking` is set.

### Google / Vertex AI (`request/google.ts`)

- Gemini API + Vertex AI variants.
- `tools[].function_declarations` for function calling.
- Safety settings & system instruction handled separately from `contents`.
- Thinking-token support gated by `LLMFlags.geminiThinking`.

### Additional clients

- `request/additionalParams.ts` parses user-supplied JSON parameters and
  merges them onto the outgoing payload.
- `request/shared.ts` holds reverse-proxy URL parsing
  (`request.ts:467-472`), custom-header construction, and other helpers.
- `request/tests/` contains the few unit tests for this surface area.

---

## 6. Transport — bypassing CORS

- **Tauri:** calls go through `native_request` or `streamed_fetch` in
  `src-tauri/src/main.rs` so the browser CORS layer doesn't apply.
- **Node server:** the equivalent `/streamed_fetch` endpoint in
  `server/node/server.cjs` proxies streaming responses with heartbeats.
- **Web standalone:** uses standard `fetch`. Some providers require a
  reverse proxy URL configured in settings.

---

## 7. Notable corners

- **Tool-call chaining.** OpenAI requests parse tool calls from streaming
  XML/`tool_calls` and can chain tool → response → tool inside one turn
  (`openAI/requests.ts:47-80`).
- **Streaming-forced override.** A caller can pass `forceStream: true` to
  override `db.streaming` (`request.ts:460`).
- **Custom models.** `db.customModels` lets users add a model entry that
  routes through a chosen format (`request.ts:473-477`).
- **MCP tools** are exposed to providers that support function calling — see
  [mcp.md](./mcp.md).

---

## 8. Related docs

- [models.md](./models.md) — the metadata that feeds the dispatcher.
- [processing-pipeline.md](./processing-pipeline.md) — how the prompt arrives.
- [tauri.md](./tauri.md) / [self-hosting.md](./self-hosting.md) — the
  transport layer when not running pure-web.
