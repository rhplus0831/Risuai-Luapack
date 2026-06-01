# API: `axLLM(id, prompt, useMultimodal, options)`

- Layer: Preamble helper (defined in `luaCodeWrapper`)
- Permission tier: Low-level (requires `lowLevelAccess`)
- Async: yes (`:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`function axLLM` in `luaCodeWrapper`, wrapping `declareAPI('axLLMMain', ...)`)

Runs a sub-request against the auxiliary model and returns the decoded
result. Identical in shape to [`LLM`](LLM.md) but routes to the auxiliary model
(`'otherAx'`) instead of the main one. This is the high-level wrapper over the
raw [`axLLMMain`](axLLMMain.md): it JSON-encodes the prompt/options, awaits, and
JSON-decodes the reply.

## Signature

```lua
axLLM(id, prompt, useMultimodal, options)   -- returns a Promise; call :await()
```

The preamble defines it as:

```lua
function axLLM(id, prompt, useMultimodal, options)
    useMultimodal = useMultimodal or false
    options = options or {}
    return json.decode(axLLMMain(id, json.encode(prompt), useMultimodal, json.encode(options)):await())
end
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `prompt` | array of `{ role, content }` | Chat messages. Role mapping: `system`/`sys` -> `system`; `user` -> `user`; `assistant`/`bot`/`char` -> `assistant`; anything else -> `assistant`. Missing `content` becomes `''`. |
| `useMultimodal` | boolean | Optional (default `false`). When `true`, [inlay tokens](../element/inlay-tokens.md) in each message's content are extracted and attached as multimodal input. |
| `options` | table | Optional (default `{}`). Recognized: `{ streaming = true }` forces a streaming request and the wrapper collects the streamed text. |

## Returns

A Promise. After `:await()`, a Lua table `{ success = <bool>, result = <string> }`
(same shape as [`LLM`](LLM.md)).

## Permission

Low-level tier — the raw `axLLMMain` no-ops unless `id` is in
`ScriptingLowLevelIds`, granted only to safe-mode runs when the
character/module has `lowLevelAccess` enabled. It is never available to
edit listeners ([`editRequest`](../hooks/editRequest.md),
[`editInput`](../hooks/editInput.md), [`editOutput`](../hooks/editOutput.md),
[`editDisplay`](../hooks/editDisplay.md)), which run with low-level access forced
off. See [access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.
- [Inlay tokens](../element/inlay-tokens.md) — multimodal extraction when
  `useMultimodal = true`.

## Example

```lua
function onOutput(id)
    local reply = axLLM(id, {
        { role = 'user', content = 'Rate the tone 1-10: ' .. getCharacterLastMessage(id) },
    }):await()
    if reply.success then
        setChatVar(id, 'tone', reply.result)
    end
end
```

## See also

- Raw host call: [`axLLMMain`](axLLMMain.md)
- Main model: [`LLM`](LLM.md), [`LLMMain`](LLMMain.md)
- One-shot: [`simpleLLM`](simpleLLM.md)
- Elements: [Promise / await](../element/promise-async.md),
  [Inlay tokens](../element/inlay-tokens.md),
  [Access key & tiers](../element/access-key.md)
