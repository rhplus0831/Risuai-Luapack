# Architecture — End-to-end runtime flow

This is the one-page tour of how Risuai actually runs, from a cold page load to
"the AI replies in the chat". Each step cites the file you should open if you
need the details.

---

## 1. Boot

1. `src/main.ts` mounts `App.svelte` and calls `loadData()` / `initHotkey()`.
2. `src/ts/bootstrap.ts:54-267` loads the persistent database.
   - Tauri: read `AppData/database/database.bin` via `@tauri-apps/plugin-fs`.
   - Web: read from `forageStorage` (which internally picks one of the auto-storage backends).
   - Decode via `RisuSaveDecoder` (`src/ts/storage/risuSave.ts:425-621`).
   - On corruption, iterate up to 20 timestamped backups.
3. `setDatabase(decoded)` populates the reactive `DBState` rune
   (`src/ts/storage/database.svelte.ts`).
4. Migrations run (`bootstrap.ts:333-505`): assign missing `chaId` UUIDs,
   normalize asset paths, drop expired trashed characters.

Storage backend picking and save format detail: [storage.md](./storage.md).

---

## 2. UI assembly

1. `App.svelte:103-260` is the conditional-render root. There is no router —
   stores in `src/ts/stores.svelte.ts` decide what mounts.
2. Responsive split: `DynamicGUI` (≤1024 px) collapses the sidebar into an
   overlay. `MobileGUI` swaps in the `MobileBody` layout.
3. Theme variant (`db.theme`): `classic`, `waifu`, `waifuMobile` —
   `ChatScreens/ChatScreen.svelte:35-80`.
4. CSS variables: `src/styles.css` maps Tailwind v4 tokens to `--risu-theme-*`
   variables. `src/ts/gui/colorscheme.ts` writes them onto
   `document.documentElement` whenever the user changes a colour scheme.

UI deep dive: [ui.md](./ui.md).

---

## 3. User sends a message

The path through `src/ts/process/index.svelte.ts:67` (`sendChat()`):

1. **Stage 1 — Prompt assembly** (`index.svelte.ts:315-768`).
   For group chats, recurse per character (`group.ts:52` decides order). Build
   `{ main, jailbreak, description, chats, … }`. If the active preset has a
   prompt template the order follows the card; else the preset defaults apply.
2. **Stage 2 — Token counting** via `ChatTokenizer`. Per-section budgeting
   respects `db.maxContext`.
3. **Stage 3 — Triggers** (`triggers.ts:1058`): `start` and `before_request`
   hooks may inject system prompts, run LLMs, mutate variables.
4. **Memory** is folded in between stages 1 and 3
   (`index.svelte.ts:1005-1072`):
   - `hanuraiEnable` → `hanuraiMemory()` (recent-query retrieval)
   - `hypav2` → `hypaMemoryV2()` (summaries + chunks)
   - `hypaV3` → `hypaMemoryV3()` (multi-ratio selection with presets)
   - else → `supaMemory()` (string-based summaries, optional hypa augment)

Memory architecture: [memory.md](./memory.md). Scripting/triggers: [scripting.md](./scripting.md).

---

## 4. Request dispatch

`src/ts/process/request/request.ts`:

1. `requestChatData()` (`:205`) wraps the call with fallback chain
   (`db.fallbackModels`), retry loop, character-set banning, blank-response
   recovery.
2. `requestChatDataMain()` (`:434`) routes by `LLMFormat` to:
   - `requestOpenAI()` — `request/openAI/requests.ts:41`
   - `requestClaude()` — `request/anthropic.ts:71`
   - `requestGoogleCloudVertex()` — `request/google.ts:44`
   - `requestOllama()`, `requestNovelAI()`, etc.
3. `reformater()` (`request.ts:347-431`) enforces per-model constraints:
   system-message consolidation, role alternation, user-first ordering.

Provider routing details: [requests.md](./requests.md).
Model registry & capability flags: [models.md](./models.md).

---

## 5. Streaming back

- Streaming responses are forwarded via writable stores so `ChatBody` updates
  message-by-message.
- Tool calls are extracted from XML tags (`request/openAI/requests.ts:47-80`).
- The final assistant message lands in `db.characters[selectedCharID].chats[…]`
  and triggers the save effect chain.

---

## 6. Persistence

`src/ts/globalApi.svelte.ts:291-485`:

1. A Svelte `$effect.root` watches `selectedCharID`, presets, modules, plugins,
   and settings.
2. On change, debounced ~500 ms, `RisuSaveEncoder.set(db, changeTracker)`
   produces a granular diff.
3. Write `database/database.bin` + a timestamped backup. Keep last 20
   (`globalApi.svelte.ts:492-528`).
4. `BroadcastChannel('risu-db')` prevents concurrent tabs from clobbering.
5. If account sync is on, `accountStorage.ts:18-182` posts to
   `/api/account/write` (last-write-wins, no merge).

Detail: [storage.md](./storage.md).

---

## 7. Cross-cutting subsystems on every turn

These run as side-channels alongside the main pipeline:

- **Plugins** — V2 plugins run in main thread with `getSafeGlobalThis()`; V3
  plugins run inside an iframe with a postMessage RPC bridge
  (`src/ts/plugins/apiV3/factory.ts`). They can register hooks, custom
  providers, UI buttons, and MCP modules.
  See [plugins.md](./plugins.md).
- **MCP** — `src/ts/process/mcp/mcp.ts` exposes built-in servers (dice,
  filesystem, googlesearch, graphmem, aiaccess, risuaccess) and external ones.
  Tools are JSON-RPC 2.0 over HTTP/SSE.
  See [mcp.md](./mcp.md).
- **Translation** — `src/ts/translator/translator.ts:39` is the entry point;
  providers: LLM, DeepL, DeepLX, Bergamot offline, Google.
  See [translation.md](./translation.md).
- **TTS / image gen** — `src/ts/process/tts.ts:80` and
  `src/ts/process/stableDiff.ts:12`. See [integrations.md](./integrations.md).
- **Sync / Realm / Drive** — peer-to-peer via PeerJS
  (`src/ts/sync/multiuser.ts`), character sharing via Realm (`src/ts/realm.ts`),
  Google Drive + Risuai-hub backups (`src/ts/drive/`).
  See [sync-and-realm.md](./sync-and-realm.md).

---

## 8. Native & server side

When running as a Tauri desktop app, the Rust side of `src-tauri/src/main.rs`
exposes commands the frontend invokes via `@tauri-apps/api`:

- `native_request`, `streamed_fetch` — bypass browser CORS for AI API calls
- `oauth_login` — OAuth2 PKCE with deep-link callback (`risuailocal://`)
- `install_python`, `run_py_server` — manage the embedded FastAPI + llama-cpp
  server on port 10026 for local inference
- `check_auth` — gate file access on disk

When running as a self-hosted server, the same frontend bundle is served by
`server/node/server.cjs` (Express + WS, port 6001, ECDSA JWT auth) which proxies
the same outbound calls server-side.

See [tauri.md](./tauri.md) and [self-hosting.md](./self-hosting.md).
