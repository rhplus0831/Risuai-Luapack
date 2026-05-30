"""Behavioral tests for the Risu Lua emulator (M2 host surface + M1 spine).

These double as worked examples of how to test a Risu Lua bundle.
"""
import hashlib
import json

import pytest

from luapack.emulator import RisuEmulator, RisuState, Message, LuaSyntaxError


# --------------------------------------------------------------------------- #
# Compile / syntax
# --------------------------------------------------------------------------- #
def test_valid_bundle_compiles():
    RisuEmulator.compile_check("function onStart(id) end")


def test_invalid_bundle_raises():
    with pytest.raises(LuaSyntaxError):
        RisuEmulator.compile_check("function onStart(id) this is not lua")


# --------------------------------------------------------------------------- #
# Sync handlers + state
# --------------------------------------------------------------------------- #
def test_onstart_mutates_state(risu):
    emu = risu("""
        function onStart(id)
            setChatVar(id, 'hp', '100')
            addChat(id, 'char', 'Hello there')
            log({ msg = 'started', hp = getChatVar(id, 'hp') })
        end
    """)
    emu.run_mode("start")
    assert emu.state.chat_vars["hp"] == "100"
    assert [m.data for m in emu.state.messages] == ["Hello there"]
    assert emu.state.logs == [{"msg": "started", "hp": "100"}]


def test_get_and_set_state_json_roundtrip(risu):
    # getState/setState wrap chat vars as "__"-prefixed JSON.
    emu = risu("""
        function onStart(id)
            setState(id, 'counter', { n = 5, tags = { 'a', 'b' } })
            local v = getState(id, 'counter')
            setChatVar(id, 'n', tostring(v.n))
            setChatVar(id, 'first', v.tags[1])
        end
    """)
    emu.run_mode("start")
    # json.encode key order is not stable (Lua randomizes string-key hashing),
    # so compare structurally, not as a fixed string.
    assert json.loads(emu.state.chat_vars["__counter"]) == {"n": 5, "tags": ["a", "b"]}
    assert emu.state.chat_vars["n"] == "5"
    assert emu.state.chat_vars["first"] == "a"


def test_full_chat_get_and_set(risu):
    st = RisuState()
    st.seed_messages([("user", "hi"), ("char", "hello")])
    emu = risu("""
        function onStart(id)
            local chat = getFullChat(id)
            setChatVar(id, 'len', tostring(#chat))
            setChatVar(id, 'lastUser', getUserLastMessage(id))
            chat[#chat + 1] = { role = 'user', data = 'added' }
            setFullChat(id, chat)
        end
    """, state=st)
    emu.run_mode("start")
    assert emu.state.chat_vars["len"] == "2"
    assert emu.state.chat_vars["lastUser"] == "hi"
    assert [m.data for m in emu.state.messages] == ["hi", "hello", "added"]


def test_cut_remove_insert(risu):
    st = RisuState()
    st.seed_messages([("user", "0"), ("char", "1"), ("user", "2"), ("char", "3")])
    emu = risu("""
        function onStart(id)
            removeChat(id, 0)            -- drop "0"
            insertChat(id, 1, 'char', 'X')
            cutChat(id, 0, 2)           -- keep first two
        end
    """, state=st)
    emu.run_mode("start")
    assert [m.data for m in emu.state.messages] == ["1", "X"]


def test_stop_sending_on_false_return(risu):
    emu = risu("""
        function onOutput(id)
            stopChat(id)
            return false
        end
    """)
    out = emu.run_mode("output")
    assert out["res"] is False
    assert out["stop"] is True


# --------------------------------------------------------------------------- #
# Permission tiers
# --------------------------------------------------------------------------- #
def test_editdisplay_tier_can_write_vars_but_not_chat(risu):
    emu = risu("""
        listenEdit('editDisplay', function(id, value, meta)
            setChatVar(id, 'seen', 'yes')   -- allowed for editDisplay ids
            addChat(id, 'char', 'nope')     -- blocked (needs safe id)
            return value .. '!'
        end)
    """)
    out = emu.run_mode("editDisplay", data="hello")
    assert out["res"] == "hello!"
    assert emu.state.chat_vars["seen"] == "yes"
    assert emu.state.messages == []  # addChat was blocked


def test_low_level_gating(risu):
    emu = risu("""
        function onOutput(id)
            local r = LLM(id, { { role = 'user', content = 'hi' } })
            setChatVar(id, 'reply', r.result)
            return r.success
        end
    """)
    # With low-level access the call succeeds.
    out = emu.run_mode("output", low_level=True)
    assert emu.state.chat_vars["reply"] == "MOCKED"
    assert out["res"] is True
    assert len(emu.state.llm_calls) == 1

    # Without it, LLM() returns nil -> script errors -> swallowed; no write.
    emu.state.chat_vars.pop("reply", None)
    out = emu.run_mode("output", low_level=False)
    assert "reply" not in emu.state.chat_vars
    assert out["error"] is not None


# --------------------------------------------------------------------------- #
# Async / Promise bridge
# --------------------------------------------------------------------------- #
def test_edit_output_listener(risu):
    emu = risu("""
        listenEdit('editOutput', function(id, value, meta)
            return value .. ' [edited]'
        end)
    """)
    out = emu.run_mode("editOutput", data="model text")
    assert out["res"] == "model text [edited]"


def test_edit_request_array_roundtrip(risu):
    # editRequest carries an OpenAI-style message array; tests array fidelity.
    emu = risu("""
        listenEdit('editRequest', function(id, value, meta)
            value[#value + 1] = { role = 'system', content = 'INJECTED' }
            return value
        end)
    """)
    out = emu.run_mode("editRequest", data=[{"role": "user", "content": "hi"}])
    assert out["res"] == [
        {"role": "user", "content": "hi"},
        {"role": "system", "content": "INJECTED"},
    ]


def test_llm_mock_callable(risu):
    st = RisuState()
    st.mock_llm = lambda prompt_json, kind: {"success": True, "result": f"{kind}:ok"}
    emu = risu("""
        function onOutput(id)
            local r = LLM(id, { { role = 'user', content = 'x' } })
            setChatVar(id, 'r', r.result)
        end
    """, state=st)
    emu.run_mode("output", low_level=True)
    assert emu.state.chat_vars["r"] == "model:ok"


# --------------------------------------------------------------------------- #
# Lorebooks
# --------------------------------------------------------------------------- #
def test_lorebook_upsert_and_search(risu):
    emu = risu("""
        function onStart(id)
            upsertLocalLoreBook(id, 'Geography', 'The realm is vast.', { key = 'map' })
            local found = getLoreBooks(id, 'Geography')
            setChatVar(id, 'content', found[1].content)
            setChatVar(id, 'key', found[1].key)
        end
    """)
    emu.run_mode("start")
    assert emu.state.chat_vars["content"] == "The realm is vast."
    assert emu.state.chat_vars["key"] == "map"
    assert emu.state.local_lore[0]["comment"] == "Geography"


# --------------------------------------------------------------------------- #
# Low-level externals (mocked)
# --------------------------------------------------------------------------- #
def test_request_guards_and_mock(risu):
    st = RisuState()
    st.mock_http = {"status": 200, "data": "hello"}
    emu = risu("""
        function onStart(id)
            local ok = json.decode(request(id, 'https://example.com/x'):await())
            setChatVar(id, 'ok_status', tostring(ok.status))
            local bad = json.decode(request(id, 'http://insecure.com'):await())
            setChatVar(id, 'bad_status', tostring(bad.status))
            local banned = json.decode(request(id, 'https://risuai.net/a'):await())
            setChatVar(id, 'banned_status', tostring(banned.status))
        end
    """, state=st)
    emu.run_mode("start", low_level=True)
    assert emu.state.chat_vars["ok_status"] == "200"
    assert emu.state.chat_vars["bad_status"] == "400"   # not https
    assert emu.state.chat_vars["banned_status"] == "400"  # banned host


def test_similarity_echo(risu):
    emu = risu("""
        function onStart(id)
            local res = similarity(id, 'q', { 'a', 'b', 'c' }):await()
            setChatVar(id, 'first', res[1])
            setChatVar(id, 'count', tostring(#res))
        end
    """)
    emu.run_mode("start", low_level=True)
    assert emu.state.chat_vars["first"] == "a"
    assert emu.state.chat_vars["count"] == "3"


def test_hash_is_deterministic(risu):
    emu = risu("""
        function onStart(id)
            setChatVar(id, 'h', hash(id, 'abc'):await())
        end
    """)
    emu.run_mode("start")
    assert emu.state.chat_vars["h"] == hashlib.sha256(b"abc").hexdigest()


def test_alert_input_queue(risu):
    st = RisuState()
    st.input_responses = ["Risu"]
    emu = risu("""
        function onStart(id)
            local name = alertInput(id, 'Your name?'):await()
            setChatVar(id, 'name', name)
        end
    """, state=st)
    emu.run_mode("start")
    assert emu.state.chat_vars["name"] == "Risu"
    assert emu.state.alerts == [{"type": "input", "value": "Your name?"}]
