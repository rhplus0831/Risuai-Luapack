# Annotated source tree

A map of the codebase, focused on the directories you'll spend time in. For the
top-level layout see [`STRUCTURE.md`](../STRUCTURE.md).

---

## `src/`

| Path | Role |
|------|------|
| `App.svelte` | Conditional-render root — no router. `App.svelte:103-260` decides what mounts. |
| `LiteMain.svelte` | Embeddable "Lite" variant. |
| `main.ts` | Mounts App, calls `loadData()` + `initHotkey()`. |
| `preload.ts` | Polyfills/setup that must run before mount. |
| `styles.css` | Tailwind v4 theme tokens → `--risu-theme-*` CSS variables. |
| `types.d.ts`, `vite-env.d.ts` | Ambient types. |

### `src/lang/`

i18n JSON files. Languages: `en`, `ko`, `cn`, `zh-Hant`, `vi`, `de`, `es`.

### `src/etc/`

Static extras: `Airisu.webp`, `bg.jpg`, `airisu.cbs`, `o200k_base.json`
(tiktoken bpe), `patchNote.ts`, `send.mp3`, `docs/`.

### `src/test/`

Vitest entry (`runTest.ts`). Most tests live next to their subjects as
`*.test.ts`.

---

## `src/ts/` — business logic

### Root files

| File | Role | Key symbols |
|------|------|-------------|
| `bootstrap.ts` | App init: load DB, decode, migrate. | `loadData()`, `checkNewFormat()` |
| `globalApi.svelte.ts` | Save loop, BroadcastChannel, top-level API surface used by UI. | `saveDb()`, `getDbBackups()` |
| `stores.svelte.ts` | All Svelte 5 stores (`DBState`, `DynamicGUI`, `sideBarStore`, alerts, modals…). | listed in [ui.md](./ui.md) |
| `alert.ts` | Alert/confirm/input/wait promise wrappers around `alertStore`. | `alertNormal`, `alertConfirm`, `alertInput` |
| `cbs.ts` | Callback System — `{{name::args}}` template substitution. | `registerCBS`, `registerFunction` |
| `characterCards.ts` | Multi-format character card import/export. | `importCharacterCardSpec`, `exportCharacterCard` |
| `characters.ts` | Character CRUD helpers. | |
| `defaulthotkeys.ts`, `hotkey.ts` | Keyboard shortcut binding. | |
| `iris.ts` | Iris (settings/preset import-export?) — paired with `sionyw.ts`. | |
| `licenses.ts` | License screen content. | |
| `lite.ts` | Helpers for the Lite variant. | |
| `loadout.ts` | Named preference snapshots ("loadouts"). | |
| `mutex.ts` | Promise-based mutex used by storage and sync. | |
| `observer.svelte.ts` | Generic observer pattern. | |
| `parser.svelte.ts` | Top-level message parser (calls into `cbs.ts` + `parser/`). | |
| `persona.ts` | User persona model + PNG export/import. | `saveUserPersona`, `changeUserPersona` |
| `platform.ts` | Platform detection (`isTauri`, `isNodeServer`, `isMobile`). | |
| `plugins/` | Plugin engine — see below. | |
| `pngChunk.ts` | Read/write PNG tEXt chunks (character cards). | `PngChunk.read`, `PngChunk.write` |
| `polyfill.ts` | Browser polyfills loaded by `preload.ts`. | |
| `realm.ts` | Realm (community hub) client. | `shareRealmCardData`, `openRealm` |
| `rpack/` | Risuai pack format. | |
| `setting/` | Setting-page state and helpers. | |
| `sionyw.ts` | Paired with `iris.ts`. | |
| `sourcemap.ts`, `sourcemap.test.ts` | Source-map utilities (used by stack-trace dialogs). | |
| `tokenizer.ts` | Token counting facade — chooses tiktoken / Claude / Llama3 etc. | `ChatTokenizer` |
| `update.ts` | In-app update check (Tauri & web). | |
| `util.ts`, `util/` | Generic utilities (hash, base64, RNG, …). | |
| `voice.ts` | Web Speech API wrapper for TTS. | |

### `src/ts/storage/`

Persistence layer. Detail: [storage.md](./storage.md).

| File | Role |
|------|------|
| `database.svelte.ts` | Central `Database` interface + `DBState` rune. |
| `risuSave.ts` | Block-based binary save format (msgpackr + gzip). |
| `autoStorage.ts` | Backend picker (Account / OPFS / Node / LocalForage). |
| `accountStorage.ts` | Remote sync via `/api/account/{read,write}`. |
| `opfsStorage.ts` | Origin Private File System backend. |
| `nodeStorage.ts` | Self-host proxy backend (ECDSA JWT). |
| `persistant.ts` | `navigator.storage.persist()` requests. |
| `defaultPrompts.ts` | Built-in preset / prompt defaults. |
| `exportAsDataset.ts` | Export chats as training dataset. |

### `src/ts/process/`

Chat orchestration & everything that runs *during* a turn.

| Path | Role |
|------|------|
| `index.svelte.ts` | `sendChat()` — main pipeline (prompt → tokenize → trigger → request). |
| `prompt.ts` | Prompt assembly helpers. |
| `group.ts` | Group chat ordering (`groupOrder()`). |
| `prereroll.ts` | Reroll history per message id. |
| `exampleMessages.ts` | Example-message handling. |
| `request/` | Provider request layer — see [requests.md](./requests.md). |
| `models/` | NAI, Ooba, local model wrappers. |
| `memory/` | Hypa / HypaV2 / HypaV3 / Supa / Hanurai. See [memory.md](./memory.md). |
| `templates/` | Jinja-like chat templates + JSON schema extraction. |
| `mcp/` | Model Context Protocol — see [mcp.md](./mcp.md). |
| `files/` | Inlays (multimodal attachments), multisend. |
| `embedding/` | Supplementary embedding helpers (additional info retrieval). |
| `dynamicutils/` | Hot-path utilities. |
| `lorebook.svelte.ts` | Lorebook activation. See [characters-and-lore.md](./characters-and-lore.md). |
| `scriptings.ts` | Lua/Python sandbox. See [scripting.md](./scripting.md). |
| `scripts.ts` | Regex script engine. |
| `triggers.ts` | Trigger evaluation. |
| `command.ts` | Slash commands. |
| `modules.ts` | RisuModule loading. |
| `infunctions.ts` | Built-in functions called from triggers/scripts. |
| `stableDiff.ts` | Stable Diffusion integration. |
| `tts.ts`, `ttsHooks.ts`, `ttsHooks.test.ts` | TTS pipeline + plugin hooks. |
| `transformers.ts` | HuggingFace Transformers.js wrapper. |
| `webllm.ts` | WebLLM in-browser inference. |
| `pyworker.ts` | Pyodide worker management. |
| `coldstorage.svelte.ts` | "Cold storage" archiving of chats to disk. |
| `inlayScreen.ts` | Inlay rendering helpers. |
| `processzip.ts` | Zip processing (CharX). |
| `stringlize.ts` | Stringify helpers for prompts. |

### `src/ts/plugins/`

Plugin engine. Detail: [plugins.md](./plugins.md) (internals) and
[`../plugins.md`](../plugins.md) (author guide).

| Path | Role |
|------|------|
| `plugins.svelte.ts` | Plugin import, transpile, validate, V2 loader. |
| `pluginSafeClass.ts` | `SafeLocalStorage`, `SafeIdbFactory`, `SafeDocument`. |
| `pluginSafety.ts` | acorn-based AST safety check + rewrite. |
| `apiV3/factory.ts` | Iframe sandbox host (postMessage RPC). |
| `apiV3/v3.svelte.ts` | V3 API surface, permissions, UI registration. |
| `apiV3/transpiler.ts` | TS → JS via sucrase. |
| `apiV3/developMode.ts` | Hot-reload from a local file. |
| `apiV3/risuai.d.ts` | Type surface plugins consume. |
| `migrationGuide.md` | V2 → V3 author migration notes. |

### `src/ts/model/`

Model registry. Detail: [models.md](./models.md).

| File | Role |
|------|------|
| `modellist.ts` | `LLMModels[]` master list. |
| `modelGrid.ts` | UI model picker grid data. |
| `types.ts` | `LLMModel`, `LLMProvider`, `LLMFormat`, `LLMFlags`, tokenizer enum. |
| `providers/{openai,anthropic,google,nanogpt}.ts` | Provider-specific model lists. |
| `ooba.ts`, `ollama.ts`, `openrouter.ts`, `nanogpt.ts` | Provider clients. |

### `src/ts/translator/`

| File | Role |
|------|------|
| `translator.ts` | Main entry + provider dispatch + cache. |
| `presets.ts` | LLM-translator presets (encrypted `.risutl`). |
| `presets.test.ts` | Tests. |
| `bergamotTranslator.ts` | Mozilla offline translator (lazy-loaded WASM). |

### `src/ts/sync/`, `src/ts/drive/`

| File | Role |
|------|------|
| `sync/multiuser.ts` | PeerJS multiuser chat sync. |
| `drive/drive.ts` | Google Drive OAuth + backup. |
| `drive/accounter.ts` | Risuai-hub account backups. |
| `drive/backuplocal.ts` | Local file backup with `LocalWriter`. |

### `src/ts/gui/`

| File | Role |
|------|------|
| `colorscheme.ts` | Color-scheme presets + applier. |
| `guisize.ts` | Responsive size computation. |
| `animation.ts` | `--risu-animation-speed` sync. |
| `tooltip.ts` | Tippy.js wrapper. |
| `highlight.ts` | CSS Highlight API for CBS syntax. |
| `branches.ts` | Chat branch tree visualization. |
| `longtouch.ts` | Long-press detection on mobile. |
| `codearea/` | CodeMirror/Monaco area helpers. |

### `src/ts/horde/`, `src/ts/network/`, `src/ts/parser/`, `src/ts/media/`, `src/ts/3d/`, `src/ts/kei/`

Smaller subsystems: AI Horde client, network helpers, the parser folder used by
`parser.svelte.ts`, media-related helpers, three.js bits, Kei cloud client.

---

## `src/lib/` — Svelte components

| Path | Role |
|------|------|
| `ChatScreens/` | Chat surface — `Chat.svelte`, `ChatScreen.svelte`, `ChatBody.svelte`, `Message.svelte`, `EmotionBox.svelte`, … |
| `UI/` | Cross-cutting components: `MainMenu.svelte`, `ModelGrid.svelte`, popup buttons, `Title.svelte`, `3DLoader.svelte`. |
| `UI/GUI/` | Form inputs (`TextInput`, `NumberInput`, `SelectInput`, `CheckInput`, `ColorInput`, `SliderInput`, `SegmentedControl`). |
| `UI/NewGUI/` | Newer-style form inputs. |
| `UI/Realm/` | Realm hub (browse, upload, popup, license). |
| `Setting/` | Settings panel — `Settings.svelte`, `SettingRenderer.svelte`, `Pages/`, `Wrappers/`. |
| `SideBars/` | `Sidebar.svelte`, `Scripts/`, `LoreBook/`, `CharConfig`, `DevTool`. |
| `Others/` | Modals & overlays — `AlertComp`, `PluginAlertModal`, `HypaV3Modal`, `BookmarkList`, `MonacoEditor`, `LoadoutModal`, etc. |
| `Mobile/` | `MobileHeader`, `MobileBody`, `MobileFooter`, `MobileCharacters`. |
| `Playground/` | Tester pages — chat, embedding, tokenizer, regex, jinja, image gen, MCP, parser, etc. |
| `LiteUI/` | Components specific to the Lite variant. |
| `VisualNovel/` | Visual-novel mode UI. |

---

## `src-tauri/`

| Path | Role |
|------|------|
| `Cargo.toml`, `tauri.conf.json`, `build.rs` | Tauri config. |
| `src/main.rs` | Rust commands & event handling. |
| `src-python/main.py` | FastAPI + llama-cpp local-inference server. |
| `capabilities/` | Tauri permission scopes (FS, HTTP, shell). |
| `icons/`, `gen/` | App icons & generated bindings. |

Detail: [tauri.md](./tauri.md).

---

## `server/`

| Path | Role |
|------|------|
| `node/server.cjs` | Production Express + WS server. |
| `node/readme.md` | Node server docs. |
| `node/ssl/` | (Optional) TLS certs. |
| `hono/` | WIP Hono router. `cf.ts` (Workers), `node.ts` (Node), `bun.ts` (Bun). |

Detail: [self-hosting.md](./self-hosting.md).
