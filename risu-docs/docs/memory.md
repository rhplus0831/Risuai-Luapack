# Memory systems

Five memory subsystems coexist under `src/ts/process/memory/`. Only one runs
at a time per chat — `process/index.svelte.ts:1005-1072` picks the first match
in priority order.

---

## 1. Priority & dispatch

`process/index.svelte.ts:1005-1072`:

```
if (db.hanuraiEnable)        → hanuraiMemory()
else if (db.hypav2)          → hypaMemoryV2()
else if (db.hypaV3)          → hypaMemoryV3()
else if (db.supaMemory && db.supaModelType !== 'none')
                             → supaMemory()
```

All four return `{ currentTokens, chats, error?, memory? }`. The memory string
is injected as a system message labelled `"supaMemory"`.

---

## 2. Hypa — vector retrieval, no summarization

`memory/hypamemory.ts`.

- **Idea.** Embed past messages, retrieve the most-similar k via cosine
  similarity.
- **No summarization.** Stores raw text alongside embeddings.
- **Embeddings supported.** OpenAI (ada, 3-small, 3-large), Xenova local
  models via WASM/WebGPU (MiniLM, Nomic, BGE, multilingual), Voyage Context3
  (contextual — see §7 below).
- **API.** `HypaProcesser.addText()` (`:157-196`), `similaritySearch()`
  (`:198-201`), `similaritySearchScored()` (`:203-205`). Cache key:
  `text|model|suffix` keyed in localforage.
- **DB fields.** `hypaModel`, `hypaCustomSettings`, `supaMemoryKey`.
- **Pick this when.** Context window is generous and the chat isn't huge; or
  as a search-only supplement under Supa.

---

## 3. HypaV2 — summarized + chunked

`memory/hypav2.ts:335-669`.

- **Idea.** Greedy-batch the older chats, summarize each batch, keep the
  summaries + their split-paragraph chunks indexed for similarity search. The
  most recent few messages are kept untouched.
- **Data model.** `HypaV2Data` = `mainChunks[]` (id, text summary,
  `Set<chatMemo>`, `lastChatMemo`) + `chunks[]` (split paragraphs linked to
  mainChunk by id). Sets are serialised as arrays.
- **Summarizer.** Distilbart (transformers.js) or OpenAI legacy summarizers
  (`gpt-3.5-turbo-instruct`, `text-davinci-003`, `text-curie-001`).
- **Algorithm.** Accumulate messages until token size exceeds
  `db.hypaChunkSize` (default 3000), summarize the batch, split summary on
  `\n\n`, embed and store. Retrieval weights similarity scores by recency
  (last three chats descending).
- **DB fields.** `hypaAllocatedTokens` (default 3000), `hypaChunkSize` (3000),
  `supaMemoryPrompt`, `supaModelType`.
- **Per-chat state.** `room.hypaV2Data`.
- **Pick this when.** Long chats where you want compression *and* search but
  don't need preset tuning.

---

## 4. HypaV3 — multi-strategy with presets

`memory/hypav3.ts:118-1830`.

The most sophisticated. Budgets the memory token pool across four selection
strategies and supports parallel batch processing.

- **Data model.** `HypaV3Data` = `summaries[]` (text, `Set<chatMemo>`,
  `isImportant`, `categoryId`, `tags`). `metrics` tracks last-selected indices
  per category.
- **Selection strategies.**
  - **Important** — manually-flagged (`isImportant`).
  - **Recent** — tail of the summary list, weighted by availability.
  - **Similar** — embedding lookup with optional **similarity correction**
    (re-summarize the user's recent message before querying so it matches
    better against compressed summaries).
  - **Random** — fills unused token budget.
- **Token budget split.** `memoryTokensRatio × maxContext`, divided per the
  preset's (recent / similar / random) triplet. Important entries are added
  first.
- **Batches.** `maxChatsPerSummary` (default 6); reserves `queryChatCount`
  (default 3) recent chats from being summarized.
- **Experimental mode.** Collects every pending batch, runs them in parallel
  through `TaskRateLimiter` (`memory/taskRateLimiter.ts:20-189`).
- **Presets.** `db.hypaV3Presets[]` + `db.hypaV3PresetId`. A preset carries:
  `summarizationModel`, `summarizationPrompt`, `reSummarizationPrompt`,
  `memoryTokensRatio`, `extraSummarizationRatio`, `maxChatsPerSummary`,
  ratio triplet, `enableSimilarityCorrection`, `preserveOrphanedMemory`,
  `queryChatCount`, rate-limit tuples.
- **UI.** `src/lib/Others/HypaV3Modal.svelte` lets users edit summaries,
  toggle importance, manage categories & tags. `HypaV3Progress.svelte` shows
  in-flight progress.
- **Per-chat state.** `room.hypaV3Data`.
- **Pick this when.** Very long chats *and* you're willing to tune presets.

---

## 5. Supa — legacy summarization

`memory/supaMemory.ts:12-428`.

- **Idea.** Maintain a single rolling string of summaries — no embeddings.
- **Storage format.** `id\nsummary`. In hybrid mode (`asHyper`) you get
  `HypaData[]` of `(id, supa string, hypa string[])` so each Supa entry also
  carries a few raw chunks for keyword-grounded recall.
- **Algorithm.** Greedy chunking up to `db.maxSupaChunkSize` (~1000). On
  overflow, re-summarize the summary. If even that overflows, shrink chunk
  size by 0.7×.
- **DB fields.** `supaMemoryData`, `supaMemoryPrompt`, `supaModelType`
  (`distilbart` | `curie` | `instruct35` | `davinci003` | `subModel`),
  `maxSupaChunkSize`, `removePunctuationHypa`.
- **Per-chat state.** `room.supaMemoryData`.
- **Pick this when.** Simplest option, lightweight, can be combined with Hypa
  via `db.hypaMemory + asHyper`.

---

## 6. Hanurai — ephemeral recent-query search

`memory/hanuraiMemory.ts:9-103`.

- **Idea.** No persisted memory at all. On each turn, embed the most recent
  `maxRecentChatQuery` (4) messages, search them against the full history,
  weight matches by recency, inject the result.
- **Embedding cue.** Prefix documents `search_document:`, queries
  `search_query:`.
- **DB fields.** `hanuraiEnable`, `hanuraiSplit`, `hanuraiTokens` (default
  1000).
- **Pick this when.** You want context-aware retrieval but don't want any
  state.

---

## 7. Supporting infrastructure

### TaskRateLimiter — `memory/taskRateLimiter.ts:20-189`

Wraps async tasks with rate + concurrency limits.

- `executeTask<T>()` — single task.
- `executeBatch<T>()` — parallel batch, collected results.
- `cancelPendingTasks()` — abort.
- Config: `tasksPerMinute` (default 20), `maxConcurrentTasks` (default 5),
  `failFast` (default true).
- Used by HypaV3 experimental mode (`hypav3.ts:384-416`) and `HypaProcessorV2`.

### ContextualEmbedding — `memory/contextualEmbedding.ts:1-134`

Pluggable contextual-embedding provider. Voyage Context3 is the implementation
shipped (model `voyage-context-3`, endpoint
`https://api.voyageai.com/v1/contextualizedembeddings`).

- `embedDocumentGroups(groups: string[][])` — embed mutually-contextual
  groups.
- `embedQueries(queries: string[])` — retrieval queries.
- Cache key includes a context hash so same-group docs share a key.

### embedding/addinfo — `embedding/addinfo.ts`

Supplementary: at chat start, retrieves additional character info via
similarity against the first 4 chat messages.

---

## 8. Choosing a system

| If you want… | Use |
|--------------|-----|
| No state, just relevant recent recall | **Hanurai** |
| Simple rolling summary | **Supa** |
| Rolling summary + retrieval over its chunks | **HypaV2** |
| Fine-grained, multi-strategy retrieval with knobs | **HypaV3** |
| Embedding-only retrieval over raw text | **Hypa** (or Supa + `asHyper`) |
