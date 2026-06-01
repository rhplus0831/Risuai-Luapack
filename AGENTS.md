# AGENTS.md

Risuai-Luapack lets agents author, validate, bundle, and behavior-test
[RisuAI](https://github.com/kwaroran/RisuAI) Lua packs outside Risu. Use this
guide when working on a pack with `luapack`.

## Start with the references

- Read [docs/README.md](docs/README.md) before using a hook, host API, CBS
  function, or shared runtime concept. It links to one page per item under
  `docs/hooks/`, `docs/api/`, `docs/cbs/`, and `docs/element/`.
- Use [packs/example/](packs/example/) as the minimal pack pattern: Lua code in
  `src/*.lua`, `require()` between modules, and pytest tests under `tests/`.
- When a detail matters, prefer the specific reference page over memory. The
  docs cover access keys, permission tiers, async/await, CBS parsing, chat
  message shapes, and hook timing.

## CLI

Use the available luapack launcher for the workspace. The command surface is:

| Command | Purpose |
|---------|---------|
| `new <dir>` | Scaffold a pack with `luapack.toml`, `src/main.lua`, and a starter test. |
| `check [dir] [--strict]` | Validate Lua syntax, Risu host/helper names, handler names, `listenEdit` types, and CBS function names inside Lua strings. |
| `check-cbs "<str>"` | Validate one complete CBS `{{...}}` template string, including brace balance. |
| `build [dir]` | Bundle `src/*.lua` into `dist/bundle.lua` and syntax-check the bundled output. |
| `test [dir]` | Run the pack's pytest tests. |

## Pack workflow

1. Create or inspect the pack's `luapack.toml`. The defaults are `src/` for
   source files, `main` as the entry module, and `dist/bundle.lua` as output.
2. Put pack code in `src/*.lua`. The entry module is loaded last, so global
   handlers defined there are visible to Risu.
3. Run `luapack check <pack>` and fix findings before building.
4. Run `luapack build <pack>` and paste the generated `dist/bundle.lua` into
   Risu's Lua trigger field.
5. Add behavior tests with `luapack.testing.load` or `load_pack`, then run
   `luapack test <pack>`.

## Risu Lua rules to keep in mind

- Event and button handlers must be global functions. Risu dispatches by global
  name, so define handlers like `function onStart(id)` rather than hiding them
  inside a module table.
- Most host API calls take the access key `id` as their first argument. Check
  the API page for exceptions such as `cbs(value)` and `log(value)`.
- Low-level APIs such as LLM, request, similarity, and image generation require
  `low_level_access = true` in `luapack.toml` and low-level access enabled for
  the character or trigger inside Risu.
- Chat indices are 0-based.
- Edit listeners are registered with `listenEdit(type, func)`, where `type` is
  `editInput`, `editOutput`, `editRequest`, or `editDisplay`.
- Some host calls are asynchronous in Risu. Use the documented `async()` /
  `await` pattern from [docs/element/promise-async.md](docs/element/promise-async.md)
  when a referenced API page says a call returns a promise.

## Testing packs

- Tests should drive the pack through the emulator, not by calling helper
  functions in isolation when hook behavior matters.
- Load the pack with `luapack.testing.load_pack`, set up state through the
  emulator helpers, then call modes such as `emu.run_mode("start")` or
  `emu.run_mode("editOutput", data="...")`.
- Mock low-level calls in tests when a pack uses LLM, request, image, or
  similarity APIs.
