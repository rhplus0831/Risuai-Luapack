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
| `docs` | regenerate `docs/lua-api.md` from the vendored Risu source |
| `sync-source [--ref main]` | refresh vendored Risu sources (pinned by default) |

## (A) Authoring a Risu Lua pack

1. **Read [docs/lua-guide.md](docs-refer/lua-guide.md) and
   [docs/lua-api.md](docs-refer/lua-api.md) first.** They cover the host API, the `id`
   access-key convention, permission tiers, async/await, and CBS.
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
- `luapack/docgen.py` — generates `docs/lua-api.md` from the vendored source.
- `luapack/testing.py`, `luapack/__main__.py`.
- `vendor/` — pinned RisuAI sources (`scriptings.ts`, `cbs.ts`) + rxi `json.lua`.
  **This is the source of truth** for the host API and CBS name lists.
- `tests/` — emulator, bundler, lint, docgen + drift guards.

## Conventions and gotchas (read before editing)

- **ASCII-only console output.** `print()` of non-ASCII (em-dash, `≤`, emoji)
  raises `UnicodeEncodeError` and crashes the CLI on cp949 (Korean) Windows
  consoles. Non-ASCII is fine in files written with `encoding="utf-8"` (e.g.
  generated docs).
- **`vendor/*.ts` is pinned** to `docgen.RISU_REF` and committed. Don't
  hand-edit; refresh with `luapack sync-source`. The API/CBS name lists, docs,
  and lint all derive from it, so the tooling tracks Risu.
- **`docs/lua-api.md` is generated** — never hand-edit; run `luapack docs`. A
  drift test fails if it's stale.
- **Drift guards** (`tests/test_api_coverage.py`, `tests/test_docgen.py`) keep
  the emulator and docs in sync with the pinned Risu source. The CI
  `upstream-drift` job re-checks against latest Risu weekly.
- **Line endings:** `.gitattributes` enforces LF; vendored `.ts` must stay LF so
  `sync-source` is a byte no-op. `.cmd` stays CRLF.
- **License:** GPLv3 (matches RisuAI). See [NOTICE](NOTICE) for third-party
  attribution. Keep `print` output and new files compatible.

## Before committing

- `python -m pytest -q` is green.
- If you changed the emulator's host API or the wrapper, run `luapack docs` and
  confirm the drift tests pass.
- Never commit `bin/`, `dist/`, or `Refer/` (all gitignored).
