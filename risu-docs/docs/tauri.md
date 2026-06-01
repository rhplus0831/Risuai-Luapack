# Tauri desktop backend

The desktop app wraps the same Svelte 5 frontend in a Tauri 2 shell with a
Rust backend (`src-tauri/src/main.rs`) and an embedded Python helper
(`src-tauri/src-python/`) for local LLM inference.

---

## 1. Tauri version & config

- Tauri **2.9.5** (`src-tauri/Cargo.toml:15-35`).
- Identifier `co.aiclient.risu` (`tauri.conf.json:30-32`).
- Plugins enabled: `http`, `shell`, `fs`, `os`, `process`, `updater`,
  `deep-link`, `dialog`.
- Build inputs: `pnpm tauribuild` (Vite without sourcemap) → `tauri build`.

---

## 2. Capabilities

`src-tauri/capabilities/desktop.json:1-15` declares the permissions exposed
to the frontend:

- `updater:default` — auto-update via GitHub releases + public-key signature.
- `process:default`, `shell:default` — subprocess management.
- `http:default` — unrestricted HTTPS via Rust `reqwest` (the CORS-bypass
  story).
- `deep-link:default` — custom protocol `risuailocal://` for OAuth callbacks.
- `fs` scope: `$APPDATA` and `/data/**`; asset protocol enabled.

---

## 3. Commands exposed to the frontend

`src-tauri/src/main.rs:589-601`:

| Command | Purpose |
|---------|---------|
| `greet(name)` | Smoke test. |
| `native_request(url, body, header, method)` | Raw HTTP via reqwest (GET/POST, base64 body). |
| `streamed_fetch(id, url, headers, body, method, timeout_secs)` | Streaming HTTP; emits `streamed_fetch` Tauri events per chunk. |
| `check_auth(fpath, auth)` | Validate an auth token file (≤1000 bytes). |
| `check_requirements_local()` | Confirm Python + Git on PATH. |
| `install_python(path)` | Download Python 3.11.7 embeddable (Windows only — `main.rs:241-246`). |
| `install_pip(path)` | Bootstrap pip via `get-pip.py`. |
| `post_py_install(path)` | Uncomment `import site` in `python311._pth`. |
| `install_py_dependencies(path, dependency)` | `pip install` a package. |
| `run_py_server(handle, py_path)` | Spawn `uvicorn` on port 10026 (`main.rs:407-429`). |
| `oauth_login(app)` | OAuth2 PKCE flow with deep-link callback (`main.rs:126-184`). |

---

## 4. Embedded Python — local inference

`src-tauri/src-python/main.py:1-126` is a FastAPI service that owns a
`llama-cpp` instance. It listens on port **8912** (standalone) or **10026**
(spawned from Tauri).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/llamacpp` | POST | Stream inference (temperature, top-p, penalties …). Requires `x_risu_auth` header. |
| `/llamacpp/tokenize` | POST | Tokenize against the loaded model. |
| `/` , `/auth` | GET | Debug — return the key-file path. |

Auth is a UUID written to `src-tauri/key.txt` (`main.py:14-21`). CORS allows
any origin (the host process is the client).

---

## 5. File associations & bundling

`tauri.conf.json:17-28`:

- Resources: `src-python/*` bundled into the app.
- File associations: `.risum` (modules), `.risup` (presets), `.charx`
  (CharX cards). Open-with launches Risuai.
- Targets: `deb`, `rpm`, `appimage`, `nsis`, `app`, `dmg`.
- Auto-update artifacts generated; the verifier public key is hardcoded.

---

## 6. Why this matters to the frontend

The frontend calls these commands via `@tauri-apps/api`. Key uses:

- **`streamed_fetch`** — used by `src/ts/process/request/` to bypass browser
  CORS for AI providers. The streaming events flow through a Tauri event
  listener that pushes into the same writable stores the chat UI consumes.
- **`oauth_login`** — the desktop OAuth path. Web uses a popup; Tauri uses
  the deep-link callback (`risuailocal://`).
- **`install_python` & `run_py_server`** — wire up local inference. The
  frontend treats the local server as a provider in `db.aiModel`.

---

## 7. Related docs

- [requests.md](./requests.md) — the consumer of `streamed_fetch`.
- [self-hosting.md](./self-hosting.md) — the server-side equivalent of these
  transport commands.
- [build-and-test.md](./build-and-test.md) — `pnpm tauribuild`, codesigning,
  release workflow.
