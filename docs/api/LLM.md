# API: `LLM(id, prompt, useMultimodal, options)`

- **Layer:** Preamble helper (defined in `luaCodeWrapper`)
- **Permission tier:** Low-level (requires `lowLevelAccess`)
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`function LLM` in `luaCodeWrapper`, wrapping `declareAPI('LLMMain', ...)`)

Runs a sub-request against the chat's **main** model and returns the decoded
result. This is the high-level convenience wrapper over the raw
[`LLMMain`](LLMMain.md): it JSON-encodes the prompt and options for you, awaits
the host call, and JSON-decodes the `{ success, result }` reply back into a Lua
table.

## Signature

```lua
LLM(id, prompt, useMultimodal, options)   -- returns a Promise; call :await()
```

The preamble defines it as:

```lua
function LLM(id, prompt, useMultimodal, options)
    useMultimodal = useMultimodal or false
    options = options or {}
    return json.decode(LLMMain(id, json.encode(prompt), useMultimodal, json.encode(options)):await())
end
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `prompt` | array of `{ role, content }` | The chat messages. `role` is mapped: `system`/`sys` -> `system`; `user` -> `user`; `assistant`/`bot`/`char` -> `assistant`. Any unrecognized role falls through to `assistant`. Missing `content` becomes `''`. |
| `useMultimodal` | boolean | Optional (default `false`). When `true`, [inlay tokens](../element/inlay-tokens.md) inside each message's `content` are extracted and attached as multimodal input. |
| `options` | table | Optional (default `{}`). Recognized: `{ streaming = true }` forces a streaming request and the wrapper collects the streamed text for you. |

## Returns

A Promise. After `:await()`, a Lua table `{ success = <bool>, result = <string> }`:

- On success, `result` is the model's text reply.
- On failure (or a `multiline` result), `success = false` and `result` carries
  the error / partial text.

## Permission

Low-level tier — the raw `LLMMain` no-ops (returns `nil`, which then fails to
JSON-decode) unless `id` is in `ScriptingLowLevelIds`. That set is granted only
to safe-mode runs **when the character/module has `lowLevelAccess` enabled**. It
is **never** available to edit listeners ([`editRequest`](../hooks/editRequest.md),
[`editInput`](../hooks/editInput.md), [`editOutput`](../hooks/editOutput.md),
[`editDisplay`](../hooks/editDisplay.md)), which always run with low-level access
forced off. See [access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — the call is async; you must
  `:await()` it inside an `async` context.
- [Chat message](../element/chat-message.md) — the prompt uses the OpenAI-style
  `{ role, content }` shape, **not** Risu's stored `{ role, data }` shape.
- [Inlay tokens](../element/inlay-tokens.md) — when `useMultimodal = true`,
  `{{inlay::}}` / `{{inlayed::}}` / `{{inlayeddata::}}` tokens are pulled out of
  the content and attached as images.

## Example

```lua
function onOutput(id)
    local reply = LLM(id, {
        { role = 'system', content = 'You summarize in one sentence.' },
        { role = 'user',   content = getUserLastMessage(id) },
    }):await()
    if reply.success then
        log(reply.result)
    end
end
```

## See also

- Raw host call: [`LLMMain`](LLMMain.md)
- Auxiliary model: [`axLLM`](axLLM.md), [`axLLMMain`](axLLMMain.md)
- One-shot: [`simpleLLM`](simpleLLM.md)
- Elements: [Promise / await](../element/promise-async.md),
  [Inlay tokens](../element/inlay-tokens.md),
  [Access key & tiers](../element/access-key.md)
