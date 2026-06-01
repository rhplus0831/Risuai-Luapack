# Risuai — Project Structure & Documentation Index

Source-of-truth: **the code under `src/`, `src-tauri/`, and `server/`**. The files in this folder
distill what is in the source; when in doubt, read the cited file at the cited line.

This index is for AI agents and contributors that need to navigate a large codebase
without reading every file. Every section here points to a dedicated page in
[`docs/`](./docs/) with file:line citations back to the source.

---

## 1. What Risuai is

A cross-platform AI chat application. The same Svelte 5 + TypeScript codebase
ships as:

- a web app (Vite static site, `pnpm build`)
- a desktop app (Tauri 2 + Rust, `pnpm tauribuild`)
- a self-hosted server (Node Express, `pnpm runserver`; or Hono WIP)
- a Docker image (`docker-compose.yml`, GHCR `ghcr.io/kwaroran/risuai`)

User-facing feature surface is summarised in [README.md](./README.md); plugin
authoring is in [plugins.md](./plugins.md). This document and `docs/` describe
the *internals*.

---

## 2. Top-level layout

```
risuai/
├── src/                     Svelte 5 + TypeScript frontend (the bulk of the app)
│   ├── App.svelte           Root component — conditional render of all screens
│   ├── LiteMain.svelte      "Lite" embeddable variant
│   ├── main.ts              Entry: mounts App.svelte, calls bootstrap
│   ├── preload.ts           Pre-mount polyfills/setup
│   ├── styles.css           Tailwind v4 theme & --risu-theme-* CSS variables
│   ├── ts/                  All non-component code (storage, process, plugins, …)
│   ├── lib/                 Svelte components (ChatScreens, UI, Setting, …)
│   ├── lang/                i18n (en, ko, cn, zh-Hant, vi, de, es)
│   ├── etc/                 Static extras (sounds, fonts, patch notes)
│   └── test/                Vitest entry
├── src-tauri/               Tauri desktop backend
│   ├── src/main.rs          Rust commands (HTTP proxy, OAuth, Python launcher)
│   └── src-python/          Embedded FastAPI + llama-cpp server (local inference)
├── server/
│   ├── node/server.cjs      Production Node/Express self-host server
│   └── hono/                WIP Hono router (Node/Bun/Workers targets)
├── public/                  Static assets served at /
├── resources/               Application resources
├── .github/workflows/       CI/CD (Docker, Tauri release builder)
├── Dockerfile, docker-compose.yml
├── package.json, vite.config.ts, vitest.config.ts, tsconfig.json
└── capacitor.config.ts      Prepared for mobile but not currently wired
```

The deeply-nested `src/ts/` and `src/lib/` trees are mapped out in
[docs/source-tree.md](./docs/source-tree.md).

---

## 3. Reading order for new contributors / agents

If you are an agent landing here cold, read in this order:

1. **[docs/architecture.md](./docs/architecture.md)** — runtime flow from page load
   to "AI replies in the chat" (one page, end-to-end).
2. **[docs/source-tree.md](./docs/source-tree.md)** — annotated tree of `src/ts`
   and `src/lib` so you know where things live.
3. The specific subsystem doc for the task at hand (see index below).
4. The cited source files. **Always confirm before recommending — files move.**

---

## 4. Subsystem documentation index

| Area | Doc | Source roots |
|------|-----|--------------|
| End-to-end runtime flow | [docs/architecture.md](./docs/architecture.md) | `src/App.svelte`, `src/main.ts`, `src/ts/bootstrap.ts` |
| Annotated source tree | [docs/source-tree.md](./docs/source-tree.md) | `src/`, `src-tauri/`, `server/` |
| Storage & save format | [docs/storage.md](./docs/storage.md) | `src/ts/storage/`, `src/ts/bootstrap.ts`, `src/ts/globalApi.svelte.ts` |
| Chat orchestration | [docs/processing-pipeline.md](./docs/processing-pipeline.md) | `src/ts/process/index.svelte.ts`, `src/ts/process/prompt.ts`, `src/ts/process/group.ts` |
| AI provider request layer | [docs/requests.md](./docs/requests.md) | `src/ts/process/request/` |
| Model registry & capability flags | [docs/models.md](./docs/models.md) | `src/ts/model/` |
| Memory systems (Hypa/Supa/Hanurai) | [docs/memory.md](./docs/memory.md) | `src/ts/process/memory/` |
| Plugin internals (apiV3 sandbox) | [docs/plugins.md](./docs/plugins.md) | `src/ts/plugins/` |
| UI architecture & theming | [docs/ui.md](./docs/ui.md) | `src/App.svelte`, `src/lib/`, `src/ts/gui/`, `src/ts/stores.svelte.ts` |
| CBS, regex scripts, triggers, Lua/Py | [docs/scripting.md](./docs/scripting.md) | `src/ts/cbs.ts`, `src/ts/process/scriptings.ts`, `triggers.ts`, `scripts.ts`, `command.ts` |
| Character cards, lorebook, personas | [docs/characters-and-lore.md](./docs/characters-and-lore.md) | `src/ts/characterCards.ts`, `src/ts/process/lorebook.svelte.ts`, `src/ts/persona.ts`, `src/ts/pngChunk.ts` |
| Translation | [docs/translation.md](./docs/translation.md) | `src/ts/translator/` |
| MCP (Model Context Protocol) | [docs/mcp.md](./docs/mcp.md) | `src/ts/process/mcp/` |
| Sync, Realm, Drive backup | [docs/sync-and-realm.md](./docs/sync-and-realm.md) | `src/ts/sync/`, `src/ts/drive/`, `src/ts/realm.ts`, `src/lib/UI/Realm/` |
| TTS & image gen integrations | [docs/integrations.md](./docs/integrations.md) | `src/ts/process/tts.ts`, `src/ts/process/stableDiff.ts`, `src/ts/voice.ts` |
| Tauri desktop backend & Python server | [docs/tauri.md](./docs/tauri.md) | `src-tauri/` |
| Self-hosting (Node, Hono, Docker) | [docs/self-hosting.md](./docs/self-hosting.md) | `server/`, `Dockerfile` |
| Build, test, CI/CD | [docs/build-and-test.md](./docs/build-and-test.md) | `package.json`, `vite.config.ts`, `vitest.config.ts`, `.github/workflows/` |

---

## 5. Conventions for these docs

- **Citations use `file:line`** so you can jump in your editor or grep precisely.
  Line numbers drift; if a citation doesn't match anymore, search nearby for the
  cited symbol and update the doc.
- **No code duplication.** These docs describe *what* and *where*, not *how to
  reimplement*. Open the source when you need the implementation.
- **Two plugin docs.** [`plugins.md`](./plugins.md) at the root is for *plugin
  authors*. [`docs/plugins.md`](./docs/plugins.md) is for *host-side
  contributors*. They cover different surfaces.
- **AGENTS.md** remains the short orientation page for AI assistants — it
  links here for depth.

---

## 6. Build & run quick reference

```bash
pnpm install
pnpm dev               # Vite dev server, port 5174
pnpm tauri dev         # Tauri desktop dev
pnpm build             # Web build → dist/
pnpm tauribuild        # Tauri-targeted web build (no sourcemap suppressed)
pnpm tauri build       # Native installers (NSIS, DMG, DEB, RPM, AppImage)
pnpm check             # svelte-check type-check (TypeScript + Svelte)
pnpm test              # Vitest
pnpm runserver         # Node self-host server on port 6001
pnpm hono:build        # Hono server build (WIP)
```

Full pipeline detail in [docs/build-and-test.md](./docs/build-and-test.md).
