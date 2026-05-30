# Risuai-Luapack

Author, bundle, type-check, and **test** [RisuAI](https://github.com/kwaroran/RisuAI)
Lua scripts off-platform.

Risu runs character/trigger Lua as a single pasted string, in a sandboxed VM
with no compile feedback and no way to test behavior. Luapack fixes that:

- **Emulator** — reproduces Risu's Lua host environment in Python (via `lupa`,
  Lua 5.4, matching Risu's wasmoon VM): the `luaCodeWrapper` preamble, all ~50
  host functions, the three permission tiers, and the async `Promise`/`await`
  model — with mockable LLM / HTTP / image / similarity calls.
- **Bundler** — amalgamates a multi-file `src/*.lua` pack into the one string
  Risu accepts, with working `require`.
- **pytest harness** — write real behavioral tests against your script.
- **Generated API reference** — kept in sync with Risu's source.

## Install

### Windows — no system Python (recommended)

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

Downloads an embedded CPython plus `lupa` into `bin\python` (the lupa wheel
bundles Lua, so no compiler/MSVC is needed). Then drive everything through the
launcher:

```powershell
.\luapack.cmd build packs\example
.\luapack.cmd test  packs\example
```

`.\luapack.ps1` works too. Re-run `setup.ps1 -Force` to rebuild.

### Any OS — system Python

- Python 3.11+ (3.13 tested), then `pip install -r requirements.txt`
- Run with `python -m luapack ...`

## Quickstart

```sh
python -m luapack new mypack          # scaffold a pack
# edit mypack/src/main.lua ...
python -m luapack build mypack        # -> mypack/dist/bundle.lua (+ syntax check)
python -m luapack test  mypack        # run the pack's pytest tests
# paste mypack/dist/bundle.lua into Risu's Lua trigger field
```

Write tests like:

```python
from luapack.testing import load_pack

def test_greeting():
    emu = load_pack("mypack", char_name="Rika")
    emu.run_mode("start")
    assert [m.data for m in emu.state.messages] == ["Hello, Rika!"]
```

## Docs

- [docs/lua-guide.md](docs/lua-guide.md) — how Risu Lua works: entry points, the
  `id` key, permission tiers, state, async, bundling, testing.
- [docs/lua-api.md](docs/lua-api.md) — generated reference of every helper and
  host function. Regenerate with `python -m luapack docs`.

## Layout

```
luapack/            the Python package
  emulator/         lupa runtime, host API, RisuState
  bundler.py        multi-file pack -> single string
  docgen.py         API reference generator
  testing.py        load() / load_pack() test helpers
  __main__.py       CLI: new / build / check / test / docs
packs/example/      worked example pack
docs/               guide + generated reference
vendor/json.lua     rxi/json, byte-identical to Risu's
tests/              emulator, bundler, docgen, and drift tests
setup.ps1           build bin\python (embedded CPython + lupa)
luapack.cmd / .ps1  launchers that use bin\python
```

## How it stays correct

A vendored RisuAI checkout under `Refer/` is the source of truth. Tests parse it
and fail if the emulator or the docs fall behind:
`tests/test_api_coverage.py` (every declared host API is emulated) and
`tests/test_docgen.py` (the reference matches the source).
