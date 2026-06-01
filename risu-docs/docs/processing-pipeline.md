# Chat processing pipeline

`src/ts/process/index.svelte.ts` is the main orchestrator. `sendChat()` is the
single entry point for "user just sent a message".

---

## 1. Stages of `sendChat()`

`index.svelte.ts:67` — `sendChat(chatProcessIndex = -1, arg)`.

1. **Pre-flight & group routing** (`:67-260`).
   For group chats, recurse per character. `groupOrder()` in
   `process/group.ts:52` ranks members by relevance to the latest user message.
2. **Prompt assembly** (`:315-768`).
   Build a structured object: `{ main, jailbreak, description, chats,
   lorebook, authorNote, globalNote, personaPrompt, … }`. If the active
   preset has a prompt template the order follows the card; otherwise the
   preset defaults apply.
3. **Memory injection** (`:1005-1072`).
   Pick one of `hanuraiMemory()`, `hypaMemoryV2()`, `hypaMemoryV3()`,
   `supaMemory()` based on `db` flags. The output is folded in as a system
   message labelled `"supaMemory"`. Detail: [memory.md](./memory.md).
4. **Tokenization** (`:310, 763-765`).
   `ChatTokenizer` from `src/ts/tokenizer.ts` counts every section. The
   token-budget loop (`db.maxContext`) drops/clips sections in priority order.
5. **Triggers — pre-request** (`:239-261, 825-835`).
   `runTrigger(char, 'start', …)` and `runTrigger(char, 'before_request', …)`.
   Triggers can mutate the prompt, call other LLMs, set variables, or abort.
6. **Inlays & multimodal** (`:838-950+`).
   Images/video/file attachments are wrapped per provider — see
   [requests.md](./requests.md).
7. **Request dispatch.**
   `requestChatData()` from `request/request.ts` — see [requests.md](./requests.md).
8. **Response collection.**
   Streaming flows to writable stores; `ChatBody.svelte` re-renders per chunk.
   Tool calls are extracted from XML tags (provider-dependent).
9. **Post-processing & triggers — output / display.**
   Output regex scripts run; then display regex scripts; then output triggers.
10. **Persistence.**
    The message lands in `db.characters[selectedCharID].chats[…]`, the save
    effect debounces, and the save loop writes
    `database/database.bin` — see [storage.md](./storage.md).

---

## 2. Status / UI stores

`index.svelte.ts:60-65`:

- `doingChat` — boolean writable, drives the "thinking" spinner.
- `chatProcessStage` — current stage label.
- `abortChat` — `AbortController` exposed to the UI Cancel button.
- `previewFormated`, `previewBody`, `requestTokenParts` — fuel the
  "Show me what would be sent" preview.

---

## 3. Prompt assembly detail

Default ordering (when no preset template overrides):

```
mainPrompt → description → personaPrompt → exampleMessages → lorebook (depth-bucketed)
            → authorNote → chats (windowed) → memory → jailbreak → globalNote
```

Each section is tokenized independently. The token-budget pass walks them in a
configurable priority and drops/clips until the sum fits `db.maxContext`.

Lorebook insertion respects decorator-driven positioning (`@@depth`,
`@@position`, `@@inject_at`) — see
[characters-and-lore.md](./characters-and-lore.md).

CBS variables (`{{char}}`, `{{user}}`, `{{getvar::x}}`, math/logic functions)
are expanded by `parser.svelte.ts` and the CBS registry in
`src/ts/cbs.ts` — see [scripting.md](./scripting.md).

---

## 4. Subsystems that hang off the pipeline

| Subsystem | File | Role at request time |
|-----------|------|----------------------|
| Prereroll | `prereroll.ts:1-29` | Walks reroll history per `genId` for redo/undo without re-calling APIs. |
| Group chat | `group.ts:52` | Decides which member of a group answers and in what order. |
| WebLLM | `webllm.ts:16-34` | In-browser inference via `@mlc-ai/web-llm`; lazy load, unload on switch. |
| Transformers.js | `transformers.ts:14-32` | On-device embeddings & captioning; caches via browser Cache or local assets. |
| Pyodide worker | `pyworker.ts` | Python sandbox for scripting & some helpers. |
| Inlays | `files/inlays.ts` | Multimodal attachments. |
| Multisend | `files/multisend.ts` | Send one message to multiple targets. |

---

## 5. Non-obvious behaviours

- **Streaming vs escape mode.** Streaming is disabled if escape-mode is active
  (`request.ts:212-214`), but a caller can force streaming on
  (`request.ts:460`).
- **Server-error retries.** 5xx errors retry aggressively with 1 s sleep;
  the `antiServerOverloads` flag reduces retry count (`request.ts:323-328`).
- **Cache markers (Anthropic).** Prompt-cache `cache_control` markers are
  injected per role in `reformater()` (`request.ts:402-406`) — see
  [requests.md](./requests.md).
- **Token overflow.** No graceful degradation if the assembled prompt exceeds
  `maxContext` after clipping — a truncated/malformed request may be sent.
- **Coldstorage.** `coldstorage.svelte.ts` archives old chats off the main DB.
- **Schema simplification.** `simplifySchema()` removes unnecessary nested
  properties before sending to APIs that don't tolerate large schemas.

---

## 6. Related docs

- [requests.md](./requests.md) — what happens *after* prompt assembly.
- [memory.md](./memory.md) — how `hypa*`/`supa*`/`hanurai` slot in.
- [scripting.md](./scripting.md) — CBS / regex / triggers / Lua-Py.
- [storage.md](./storage.md) — where the resulting chat lands.
