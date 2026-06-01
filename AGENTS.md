# AGENTS.md

Risuai-Luapack lets you author, validate, bundle, and test
[RisuAI](https://github.com/kwaroran/RisuAI) Lua scripts off-platform. An agent
in this repo is usually doing one of two things:

- **(A) Authoring a Risu Lua pack** — writing `.lua`, validating it, bundling to
  one string to paste into Risu.
- **(B) Developing luapack itself** — the emulator, bundler, linter, docs.

## Setup

- Python 3.11+. `pip install -r requirements.txt` (lupa, pytest).
- Windows, no toolchain: `powershell -ExecutionPolicy Bypass -File setup.ps1`,
  then use `.\luapack.cmd ...` instead of `python -m luapack ...`.
- Run the test suite: `python -m pytest -q` (keep it green).

## CLI (`python -m luapack <cmd>`)

| Command | Purpose |
|---------|---------|
| `new <dir>` | scaffold a pack |
| `check [dir] [--strict]` | validate: Lua compile + name lint + CBS syntax (no behavior) |
| `check-cbs "<str>"` | validate one CBS `{{...}}` template string |
| `build [dir]` | bundle `src/*.lua` -> `dist/bundle.lua` (paste into Risu) |
| `test [dir]` | run the pack's pytest tests |
| `sync-source [--ref main]` | refresh vendored Risu sources (pinned by default) |

## (A) Authoring a Risu Lua pack

1. **Read [docs/README.md](docs/README.md) first** — the index into the
   hand-authored reference for CBS (`docs/cbs/`), hooks (`docs/hooks/`), host
   APIs (`docs/api/`), and shared elements (`docs/element/`). It covers the host
   API, the `id` access-key convention, permission tiers, async/await, and CBS.
2. `luapack new mypack`; put code in `mypack/src/*.lua` and `require()` between
   modules. See `packs/example/` for the pattern (tests included).
3. Risu rules that bite if ignored:
   - **Event/button handlers must be GLOBAL functions** — Risu dispatches by
     global name. A top-level `function onStart(id)` inside a module stays
     global in the bundle, which is what you want. Don't wrap handlers in a
     module table.
   - Every host call takes the access-key **`id` as its first argument**.
   - **Low-level** APIs (LLM/request/similarity/image) need `lowLevelAccess`.
   - **Chat indices are 0-based.**
4. `luapack check mypack` (fix findings) -> `luapack build mypack` -> paste
   `mypack/dist/bundle.lua` into Risu's Lua trigger field.
5. Behavior-test with pytest via `luapack.testing.load` / `load_pack`
   (see `packs/example/tests/`).

## (B) Developing luapack

Layout:

- `luapack/emulator/` — lupa (Lua 5.4) runtime, host-API mocks, `RisuState`,
  the synchronous Promise shim + a verbatim copy of Risu's `luaCodeWrapper`
  (`lua_src.py`).
- `luapack/bundler.py` — multi-file pack -> single string.
- `luapack/cbs.py`, `luapack/lint.py` — CBS + Lua name validation.
- `luapack/vendored.py` — pinned Risu source paths, `RISU_REF`, and the
  `declareAPI`/helper parsers that feed lint, `sync-source`, and the drift guard.
- `luapack/testing.py`, `luapack/__main__.py`.
- `vendor/` — pinned RisuAI sources (`scriptings.ts`, `cbs.ts`) + rxi `json.lua`.
  **This is the source of truth** for the host API and CBS name lists.
- `tests/` — emulator, bundler, lint + the API-coverage drift guard.

## Conventions and gotchas (read before editing)

- **ASCII-only console output.** `print()` of non-ASCII (em-dash, `≤`, emoji)
  raises `UnicodeEncodeError` and crashes the CLI on cp949 (Korean) Windows
  consoles. Non-ASCII is fine in files written with `encoding="utf-8"` (e.g.
  the docs under `docs/`).
- **`vendor/*.ts` is pinned** to `vendored.RISU_REF` and committed. Don't
  hand-edit; refresh with `luapack sync-source`. The API/CBS name lists and
  lint all derive from it, so the tooling tracks Risu.
- **`docs/` is hand-authored** — source-grounded reference pages for CBS, hooks,
  APIs, and elements. Ground new pages in `Refer/Risuai`; keep `docs/README.md`
  in sync when you add or rename a page.
- **Drift guard** (`tests/test_api_coverage.py`) keeps the emulator in sync with
  the pinned Risu source. The CI `upstream-drift` job re-checks against latest
  Risu weekly.
- **Line endings:** `.gitattributes` enforces LF; vendored `.ts` must stay LF so
  `sync-source` is a byte no-op. `.cmd` stays CRLF.
- **License:** GPLv3 (matches RisuAI). See [NOTICE](NOTICE) for third-party
  attribution. Keep `print` output and new files compatible.

## Before committing

- `python -m pytest -q` is green.
- If you changed the emulator's host API or the wrapper, confirm the
  API-coverage drift guard (`tests/test_api_coverage.py`) still passes.
- If you changed Lua behavior, CBS, hooks, or the host API, update the matching
  pages under `docs/` (and `docs/README.md`).
- Never commit `bin/`, `dist/`, or `Refer/` (all gitignored).
