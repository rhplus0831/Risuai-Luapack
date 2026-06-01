# API: `simpleLLM(id, prompt)`

- Layer: Host API (`declareAPI`)
- Permission tier: Low-level (requires `lowLevelAccess`)
- Async: yes (`:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('simpleLLM', ...)`)

A one-shot main-model call: pass a single user-message string, get back the
model's reply. Unlike [`LLM`](LLM.md)/[`LLMMain`](LLMMain.md), there is no role
array and no JSON encoding — `prompt` becomes one `{ role = 'user', content = prompt }`
message. There is no preamble helper; this host call returns a Lua table
directly (it does not return a JSON string).

## Signature

```lua
simpleLLM(id, prompt)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `prompt` | string | The text sent as a single `user` message to the main model. |

## Returns

A Promise. After `:await()`, a Lua table `{ success = <bool>, result = <string> }`:

- On success, `result` is the model's text reply.
- On a `fail`/`streaming`/`multiline` result, `success = false`.

Because the host returns a real object (not a JSON string), you do not
`json.decode` it.

## Permission

Low-level tier — the call no-ops unless `id` is in `ScriptingLowLevelIds`,
granted only to safe-mode runs when the character/module has `lowLevelAccess`
enabled. It is never available to edit listeners
([`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md),
[`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)),
which run with low-level access forced off. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.

## Example

```lua
function onOutput(id)
    local reply = simpleLLM(id, 'In one word, the mood: ' .. getCharacterLastMessage(id)):await()
    if reply.success then
        setChatVar(id, 'mood', reply.result)
    end
end
```

## See also

- Full prompt array: [`LLM`](LLM.md), [`LLMMain`](LLMMain.md)
- Auxiliary model: [`axLLM`](axLLM.md), [`axLLMMain`](axLLMMain.md)
- Elements: [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
