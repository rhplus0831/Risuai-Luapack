"""luapack CLI: build / check / test / new.

    python -m luapack build [pack_dir]   # bundle src/ -> dist/bundle.lua (+ compile)
    python -m luapack check [pack_dir]   # bundle in memory + syntax check
    python -m luapack test  [pack_dir]   # run the pack's pytest tests
    python -m luapack new   <pack_dir>   # scaffold a new pack
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

from . import bundler
from .emulator import LuaSyntaxError, RisuEmulator

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_TOML_TMPL = """[pack]
name = "{name}"
entry = "main"
src = "src"
out = "dist/bundle.lua"
# Set true if the script calls low-level APIs (LLM, request, similarity, ...).
# You must also enable low-level access for the character/trigger inside Risu.
low_level_access = false
"""

_MAIN_TMPL = """-- Entry module: Risu calls the global handlers you define here.
-- Add more files under src/ and pull them in with require('name').

function onStart(id)
    -- runs when a chat begins
end

listenEdit('editOutput', function(id, value, meta)
    -- transform each model output; must return the new value
    return value
end)
"""

_TEST_TMPL = '''import os

from luapack.testing import load_pack

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_output_is_unchanged_by_default():
    emu = load_pack(PACK)
    out = emu.run_mode("editOutput", data="hello")
    assert out["res"] == "hello"
'''


def _compile(bundle: str) -> int:
    try:
        RisuEmulator.compile_check(bundle)
    except LuaSyntaxError as exc:
        print(f"compile: FAILED\n{exc}")
        return 1
    print("compile: OK")
    return 0


def cmd_build(args) -> int:
    res = bundler.write_pack(args.path)
    rel = os.path.relpath(res["out"], args.path)
    print(f"bundled {len(res['modules'])} module(s) -> {os.path.join(args.path, rel)}")
    if res["config"]["low_level_access"]:
        print("note: pack declares low_level_access; enable it in Risu too.")
    return _compile(res["bundle"])


def cmd_check(args) -> int:
    res = bundler.build_pack(args.path)
    return _compile(res["bundle"])


def cmd_test(args) -> int:
    tests_dir = os.path.join(args.path, "tests")
    if not os.path.isdir(tests_dir):
        print(f"no tests/ directory in {args.path}")
        return 1
    env = dict(os.environ)
    env["PYTHONPATH"] = _REPO_ROOT + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.call(
        [sys.executable, "-m", "pytest", tests_dir, "-q"], env=env
    )


def cmd_new(args) -> int:
    pack_dir = args.path
    name = os.path.basename(os.path.abspath(pack_dir))
    if os.path.exists(os.path.join(pack_dir, "luapack.toml")):
        print(f"{pack_dir} already contains a luapack.toml")
        return 1
    os.makedirs(os.path.join(pack_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(pack_dir, "tests"), exist_ok=True)
    _write(os.path.join(pack_dir, "luapack.toml"), _TOML_TMPL.format(name=name))
    _write(os.path.join(pack_dir, "src", "main.lua"), _MAIN_TMPL)
    _write(os.path.join(pack_dir, "tests", "test_main.py"), _TEST_TMPL)
    print(f"created pack '{name}' at {pack_dir}")
    print(f"  edit src/main.lua, then: python -m luapack build {pack_dir}")
    return 0


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="luapack")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for cmd, fn, helptext in (
        ("build", cmd_build, "bundle src/ -> dist/bundle.lua and syntax-check"),
        ("check", cmd_check, "bundle in memory and syntax-check"),
        ("test", cmd_test, "run the pack's pytest tests"),
        ("new", cmd_new, "scaffold a new pack"),
    ):
        p = sub.add_parser(cmd, help=helptext)
        p.add_argument("path", nargs="?" if cmd != "new" else None, default=".")
        p.set_defaults(func=fn)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
