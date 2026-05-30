"""Tests for CBS validation and the Lua name lint."""
import os

import pytest

from luapack import cbs, lint

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE = os.path.join(_REPO, "packs", "example")


# --------------------------------------------------------------------------- #
# CBS function names (drift guard) + validation
# --------------------------------------------------------------------------- #
def test_cbs_names_extracted():
    names = cbs.load_cbs_names()
    assert len(names) > 100
    for n in ["char", "user", "getvar", "setvar", "calc", "random", "roll"]:
        assert n in names, n


@pytest.mark.parametrize("tpl", [
    "{{char}}",
    "hp = {{getvar::hp}}",
    "{{calc::1+1}} and {{char}}",
    "{{#if::x}}yes{{/if}}",   # block construct, not a function
    "{{ {{user}} }}",          # nested/dynamic name
    "no cbs at all",
])
def test_cbs_valid(tpl):
    assert cbs.validate(tpl) == []


def test_cbs_unclosed():
    issues = cbs.validate("{{getvar::hp")
    assert any(i["severity"] == "error" and "unclosed" in i["message"] for i in issues)


def test_cbs_unmatched():
    issues = cbs.validate("x }} y")
    assert any(i["severity"] == "error" and "unmatched" in i["message"] for i in issues)


def test_cbs_typo_suggests():
    issues = cbs.validate("{{getvarr::hp}}")
    assert issues and "getvar" in issues[0]["message"]


# --------------------------------------------------------------------------- #
# Lua name lint
# --------------------------------------------------------------------------- #
def test_example_pack_is_clean():
    assert lint.check_pack(EXAMPLE) == []


def _codes(src):
    return {f["code"] for f in lint.check_source("m.lua", src)}


def test_handler_typo_flagged():
    assert "handler" in _codes("function onOuput(id) end")


def test_invalid_listen_type_is_error():
    f = lint.check_source("m.lua", "listenEdit('editOput', function(i, v, m) return v end)")
    assert any(x["code"] == "listen-type" and x["severity"] == "error" for x in f)


def test_valid_listen_type_ok():
    assert "listen-type" not in _codes("listenEdit('editOutput', function(i, v, m) return v end)")


def test_reserved_shadow_flagged():
    assert "shadow" in _codes("function json(x) return x end")


def test_api_typo_flagged():
    f = lint.check_source("m.lua", "function onStart(id) setChatVarr(id, 'a', 'b') end")
    assert any(x["code"] == "call-typo" and "setChatVar" in x["message"] for x in f)


def test_user_helper_not_flagged():
    src = (
        "local function formatThing(x) return x end\n"
        "function onStart(id) formatThing(getName(id)) end"
    )
    assert "call-typo" not in _codes(src)


def test_cbs_inside_string_literal_flagged():
    src = "function onStart(id) addChat(id, 'char', '{{getvarr::x}}') end"
    assert "cbs" in _codes(src)


def test_cbs_not_matched_in_comment_or_code():
    # {{ }} only validated inside string literals, not bare code/comments
    assert "cbs" not in _codes("-- {{getvarr}} in a comment\nfunction onStart(id) end")


def test_cbs_pattern_fragment_not_flagged():
    # gsub builds CBS-ish patterns by concatenation ('{{raw::'..x..'}}'); the
    # unbalanced braces within a single string literal must NOT be reported.
    src = "function onStart(id) local x='a' addChat(id,'char',('{{raw::'..x..'.}}')) end"
    assert [f for f in lint.check_source("m.lua", src) if f["code"] == "cbs"] == []


def test_syntax_error_reported_with_line():
    f = lint.check_source("m.lua", "function onStart(id)\n  this is not lua")
    assert any(x["code"] == "syntax" for x in f)
