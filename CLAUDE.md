# CLAUDE.md

Project guidance lives in @AGENTS.md — read it for setup, the CLI, how to author
a Risu Lua pack, the repo layout, and conventions.

Highest-impact reminders:

- Run `python -m pytest -q` before finishing a change; keep it green.
- **All CLI `print()` output must be ASCII** — non-ASCII crashes cp949 (Korean)
  Windows consoles. Non-ASCII is fine in UTF-8 files.
- `docs/` is hand-authored, source-grounded reference (CBS, hooks, APIs,
  elements); `docs/README.md` is the index. Ground it in `Refer/Risuai`.
- `vendor/*.ts` is pinned to `vendored.RISU_REF` — refresh with
  `python -m luapack sync-source`, never hand-edit.
- Risu dispatches Lua handlers by GLOBAL name; keep event/button handlers global.
