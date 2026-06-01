# Risuai-Luapack

Risuai-Luapack is a local toolkit for building
[RisuAI](https://github.com/kwaroran/RisuAI) Lua packs. It lets you write a pack
as normal files, validate it before opening Risu, bundle it into the single Lua
string Risu accepts, and test behavior with pytest.

Use it when a Risu Lua trigger has grown past "one pasted script" and you want
source files, repeatable checks, and tests.

## What It Provides

- A pack scaffold with `luapack.toml`, `src/main.lua`, and a starter pytest.
- A bundler for multi-file Lua packs that preserves `require("module")` between
  files under `src/`.
- A checker for Lua syntax, Risu host/helper names, event handler names,
  `listenEdit` types, and CBS function names inside Lua strings.
- A `check-cbs` command for validating one complete `{{...}}` template.
- A Python emulator for behavior tests, including permission tiers, edit
  listeners, async/await wrappers, chat state, and mockable low-level calls.
- Reference docs for Risu hooks, host APIs, CBS functions, and shared runtime
  concepts under [`docs/`](docs/).

## Install

### Windows, Self-Contained

If you do not want to manage Python yourself, run:

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

This prepares `bin\python`, installs the Python dependencies, and makes the
launchers usable:

```powershell
.\luapack.cmd check packs\example
.\luapack.cmd build packs\example
.\luapack.cmd test  packs\example
```

`.\luapack.ps1` works the same way. Re-run `setup.ps1 -Force` to rebuild the
embedded Python runtime.

### System Python

Use Python 3.11 or newer:

```sh
python -m pip install -e ".[dev]"
python -m luapack check packs/example
```

If you prefer not to install the package in editable mode, run commands from the
repo root after `python -m pip install -r requirements.txt`.

## Quickstart

Create a new pack:

```sh
python -m luapack new packs/my-pack
```

Edit the generated Lua files, then run the normal loop:

```sh
python -m luapack check packs/my-pack --strict
python -m luapack build packs/my-pack
python -m luapack test  packs/my-pack
```

`build` writes `dist/bundle.lua` and `dist/bundle.lua.map.json` inside the pack.
Paste `dist/bundle.lua` into Risu's Lua trigger field.

On Windows with the self-contained setup, use `.\luapack.cmd` instead of
`python -m luapack`.

## Pack Layout

A pack is just a directory with a config file, Lua source, and optional tests:

```text
my-pack/
  luapack.toml
  src/
    main.lua
    utils.lua
  tests/
    test_main.py
  dist/
    bundle.lua
    bundle.lua.map.json
```

`luapack.toml` defaults to:

```toml
[pack]
name = "my-pack"
entry = "main"
src = "src"
out = "dist/bundle.lua"
low_level_access = false
```

The entry module is loaded last. Define Risu handlers as globals there, for
example `function onStart(id) ... end`, so Risu can dispatch them.

For a minimal working example, see [`packs/example/`](packs/example/).

## Command Reference

| Command | Purpose |
| --- | --- |
| `new <dir>` | Create a new pack skeleton. |
| `check [dir] [--strict]` | Validate Lua syntax, Risu names, handler names, `listenEdit` types, and CBS names in Lua strings. |
| `check-cbs "<str>"` | Validate one complete CBS template string, including brace balance. |
| `build [dir]` | Bundle `src/*.lua` into the configured output file and syntax-check the result. |
| `test [dir]` | Run pytest tests from the pack's `tests/` directory. |
| `sync-source [--ref <git-ref>]` | Refresh vendored Risu source files used by lint and drift tests. Mainly for maintainers. |

## Testing Packs

Tests load the real bundled pack and drive it through the emulator:

```python
from luapack.testing import load_pack


def test_greeting():
    emu = load_pack("packs/example", char_name="Rika")
    emu.run_mode("start")
    assert [m.data for m in emu.state.messages] == ["Hello, Rika!"]
```

The emulator exposes Risu-style state through `emu.state`, and low-level APIs
such as LLM, request, image generation, and similarity can be mocked through
`RisuState` fields.

## References

- [`docs/README.md`](docs/README.md) indexes the Risu Lua and CBS reference.
- [`docs/hooks/`](docs/hooks/) covers event and edit hooks.
- [`docs/api/`](docs/api/) covers Lua host APIs and wrapper helpers.
- [`docs/cbs/`](docs/cbs/) covers `{{...}}` Callback System functions.
- [`docs/element/`](docs/element/) covers shared runtime concepts and data
  shapes.

## Maintainer Notes

The checker and emulator are compared against vendored, pinned RisuAI source
files under [`vendor/`](vendor/). To inspect upstream drift:

```sh
python -m luapack sync-source --ref main
python -m pytest -q
```

The drift test fails if Risu declares a host API that the emulator does not
implement.

## License

Risuai-Luapack is licensed under the GNU GPLv3. See [`LICENSE`](LICENSE) and
[`NOTICE`](NOTICE).

Vendored sources include:

- `vendor/scriptings.ts` and parts of `luapack/emulator/lua_src.py` from
  [RisuAI](https://github.com/kwaroran/RisuAI), GPLv3.
- `vendor/json.lua` from rxi's [json.lua](https://github.com/rxi/json.lua), MIT.
