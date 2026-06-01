# Build, test, CI/CD

Reference for the build pipeline, the test setup, and the GitHub workflows.

---

## 1. Build commands (`package.json:10-21`)

| Command | What it does |
|---------|--------------|
| `pnpm dev` | Vite dev server on `0.0.0.0:5174` (strict port). |
| `pnpm build` | Production web build → `dist/` (sourcemap on). |
| `pnpm tauribuild` | Vite build for Tauri (no sourcemap flag). |
| `pnpm buildsite` | Same as `build` but explicit `--outDir dist`. |
| `pnpm preview` | Vite preview server for `dist/`. |
| `pnpm check` | `svelte-check --tsconfig ./tsconfig.json` — type check. |
| `pnpm test` | Vitest run. |
| `pnpm tauri` | Tauri CLI passthrough (build/dev/updater). |
| `pnpm runserver` | Node self-host server on port 6001. |
| `pnpm hono:build` | Vite build + `server/hono/src/utils/postbuild.js`. |
| `pnpm sync` / `pnpm electron` | Legacy Electron sync scripts. |

Engines: `node ^20.19.0 || >=22.12.0`, `pnpm`.

---

## 2. Vite (`vite.config.ts:1-66`)

- Plugins: `@sveltejs/vite-plugin-svelte`, `@tailwindcss/vite`,
  `vite-plugin-wasm`, `@rollup/plugin-strip` (strip console in prod).
- Dev: `host: 0.0.0.0`, `port: 5174`, `strictPort: true`.
- Build: oxc minification, conditional sourcemap, `chunkSizeWarningLimit: 2000`.
- Env prefixes: `VITE_*` and `TAURI_*`.
- Alias: `src` → `/src`.

WASM modules (`@huggingface/transformers`, `@mlc-ai/web-llm`,
`@mlc-ai/web-tokenizers`, `wasmoon`, `pyodide`, etc.) are handled by
`vite-plugin-wasm`.

---

## 3. TypeScript (`tsconfig.json:1-35`)

- `target: es2023`, `module: es2022`.
- `strict: false`, `skipLibCheck: true`.
- Bundler module resolution, `isolatedModules: true`.
- `noEmit: true` — Vite owns transpilation.

`tsconfig.node.json` covers `vite.config.ts` and friends.

---

## 4. Tests (`vitest.config.ts:1-18`)

- Runner: Vitest.
- Env: `happy-dom`.
- Setup: `vitest.setup.ts` (KaTeX stub, `safeStructuredClone` polyfill).
- Svelte support: `@sveltejs/vite-plugin-svelte`.
- Tests are colocated as `*.test.ts` (e.g.
  `src/ts/process/ttsHooks.test.ts`, `src/ts/translator/presets.test.ts`,
  `src/ts/sourcemap.test.ts`).
- One entry test: `src/test/runTest.ts`.

There is no comprehensive test suite — type safety is the primary
correctness gate. Treat `pnpm check` as the CI must-pass.

---

## 5. Build outputs

| Output | Location |
|--------|----------|
| Web bundle | `dist/` |
| Tauri native binaries | `src-tauri/target/release/` |
| Tauri installers | NSIS / DMG / APP / DEB / RPM / AppImage |
| Node server | uses `dist/` directly |

---

## 6. CI/CD — `.github/workflows/`

### `docker-build.yml`

- Trigger: push to `main`, tags `v*`.
- Multi-platform: `linux/amd64`, `linux/arm64` via buildx.
- Publishes to GHCR: `ghcr.io/kwaroran/risuai:{shortsha,version}`.
- Login uses `GITHUB_TOKEN`.

### `github-actions-builder.yml`

- Trigger: push to `production` branch.
- Matrix: macOS (ARM64 + Intel), Ubuntu (x86_64), Windows (x86_64).
- Steps: checkout → Node 24 → pnpm → Rust stable → Linux deps → Tauri
  action.
- Secrets: `TAURI_PRIVATE_KEY`, `TAURI_KEY_PASSWORD` (code signing).
- Output: GitHub Releases (drafts), version replacement built-in.
- Env: `VITE_RISU_LEGAL_CONFIGURED=TRUE`.

### `codeql.yml`

CodeQL static analysis (standard JavaScript/TypeScript pack).

### `mod.yml`

Module-related automation (likely auto-update of the public module catalog).

---

## 7. Capacitor (mobile) — prepared, not used

`capacitor.config.ts:1-13` is set up — `appId: "co.aiclient.risu"`,
`webDir: "dist"`, `androidScheme: 'https'` — but **there are no Capacitor
build scripts in `package.json`** and **no mobile workflows**. Treat
Capacitor as a placeholder for future iOS/Android builds, not as part of the
current shipping pipeline.

---

## 8. Quick reference

```bash
# Develop web
pnpm dev

# Develop desktop
pnpm tauri dev

# Type check
pnpm check

# Web release
pnpm build && ls dist

# Desktop release
pnpm tauri build

# Server (local self-host)
pnpm runserver           # http://localhost:6001

# Hono build (WIP)
pnpm hono:build
```

---

## 9. Related docs

- [tauri.md](./tauri.md) — what `pnpm tauri build` actually packages.
- [self-hosting.md](./self-hosting.md) — what `pnpm runserver` exposes.
- [storage.md](./storage.md) — where built-app data lives at runtime.
