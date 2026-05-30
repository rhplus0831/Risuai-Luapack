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
import urllib.error
import urllib.request

from . import bundler, cbs, docgen, lint
from .emulator import LuaSyntaxError, RisuEmulator

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Source file fetch - no git, no full 186 MB clone.
RISU_RAW_BASE = "https://raw.githubusercontent.com/kwaroran/RisuAI/{ref}/{path}"

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
    -- runs before the model request is sent
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
    findings = lint.check_pack(args.path)
    for f in findings:
        print(f"{f['file']}:{f['line']}:{f['col']}: {f['severity']}: {f['message']}  [{f['code']}]")
    errors = sum(1 for f in findings if f["severity"] == "error")
    warnings = sum(1 for f in findings if f["severity"] == "warning")
    print(f"{errors} error(s), {warnings} warning(s)")
    if errors or (args.strict and warnings):
        return 1
    return 0


def cmd_check_cbs(args) -> int:
    issues = cbs.validate(args.template)
    for it in issues:
        print(f"col {it['offset'] + 1}: {it['severity']}: {it['message']}")
    if not issues:
        print("CBS OK")
    return 1 if any(it["severity"] == "error" for it in issues) else 0


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


def cmd_docs(args) -> int:
    if not os.path.exists(docgen.DEFAULT_SCRIPTINGS):
        print(f"Risu source not found: {docgen.DEFAULT_SCRIPTINGS}")
        return 1
    generated = docgen.generate_from_repo()
    out_path = os.path.join(_REPO_ROOT, "docs", "lua-api.md")
    if args.check:
        current = ""
        if os.path.exists(out_path):
            with open(out_path, "r", encoding="utf-8") as fh:
                current = fh.read()
        if current != generated:
            print("docs/lua-api.md is stale; run: python -m luapack docs")
            return 1
        print("docs: up to date")
        return 0
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(generated)
    print(f"wrote {os.path.relpath(out_path, _REPO_ROOT)}")
    return 0


def cmd_sync_source(args) -> int:
    ref = args.ref or docgen.RISU_REF
    failures = 0
    for spec in docgen.VENDORED_SOURCES:
        url = RISU_RAW_BASE.format(ref=ref, path=spec["raw"])
        dest = spec["dest"]
        name = os.path.relpath(dest, _REPO_ROOT)
        print(f"fetching {spec['raw']}")
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read()
        except urllib.error.HTTPError as exc:
            print(f"  failed: HTTP {exc.code} for ref '{ref}' - is the ref correct?")
            failures += 1
            continue
        except Exception as exc:  # network / SSL / timeout
            print(f"  failed: {exc}")
            failures += 1
            continue
        # Guard against writing a non-source 200 response (e.g. an HTML page).
        if spec["sentinel"].encode() not in data:
            print(f"  failed: response is not source (no '{spec['sentinel']}'); not writing {name}.")
            failures += 1
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(data)
        print(f"  wrote {name} ({len(data)} bytes)")
    if ref != docgen.RISU_REF:
        print("note: not the pinned ref - run pytest and `python -m luapack docs` to inspect drift.")
    return 1 if failures else 0


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="luapack")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for cmd, fn, helptext in (
        ("build", cmd_build, "bundle src/ -> dist/bundle.lua and syntax-check"),
        ("test", cmd_test, "run the pack's pytest tests"),
        ("new", cmd_new, "scaffold a new pack"),
    ):
        p = sub.add_parser(cmd, help=helptext)
        p.add_argument("path", nargs="?" if cmd != "new" else None, default=".")
        p.set_defaults(func=fn)

    pcheck = sub.add_parser("check", help="validate Lua (compile + names) and CBS syntax")
    pcheck.add_argument("path", nargs="?", default=".")
    pcheck.add_argument("--strict", action="store_true", help="treat warnings as failures")
    pcheck.set_defaults(func=cmd_check)

    pcbs = sub.add_parser("check-cbs", help="validate a CBS template string")
    pcbs.add_argument("template", help="the CBS string, e.g. \"{{getvar::hp}}\"")
    pcbs.set_defaults(func=cmd_check_cbs)

    pdocs = sub.add_parser("docs", help="regenerate docs/lua-api.md from Risu source")
    pdocs.add_argument("--check", action="store_true", help="fail if the file is stale")
    pdocs.set_defaults(func=cmd_docs)

    psync = sub.add_parser("sync-source", help="fetch Risu's scriptings.ts (pinned by default)")
    psync.add_argument("--ref", default=None, help="git ref/SHA (default: pinned RISU_REF)")
    psync.set_defaults(func=cmd_sync_source)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
