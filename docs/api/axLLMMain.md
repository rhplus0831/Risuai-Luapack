# API: `axLLMMain(id, promptStr, useMultimodal, optionsStr)`

- Layer: Host API (`declareAPI`)
- Permission tier: Low-level (requires `lowLevelAccess`)
- Async: yes (`:await()`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('axLLMMain', ...)`)

The raw auxiliary-model sub-request: JSON string in, JSON string out. Routes
to the `'otherAx'` (auxiliary) model. Behaves exactly like
[`LLMMain`](LLMMain.md) except for the target model. Prefer the [`axLLM`](axLLM.md)
preamble helper, which handles JSON for you.

## Signature

```lua
axLLMMain(id, promptStr, useMultimodal, optionsStr)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `promptStr` | string (JSON) | `JSON.parse`d into an array of `{ role, content }`. Role mapping: `system`/`sys` -> `system`; `user` -> `user`; `assistant`/`bot`/`char` -> `assistant`; anything else -> `assistant`. Missing `content` becomes `''`. |
| `useMultimodal` | boolean | Optional (default `false`). When `true`, [inlay tokens](../element/inlay-tokens.md) in each message's content are extracted and attached as multimodal input. |
| `optionsStr` | string (JSON) | Optional (default `''`). Parsed permissively; recognized: `{"streaming": true}` forces streaming. Invalid JSON yields `{}`. |

## Returns

A Promise resolving to a JSON string `{"success": <bool>, "result": <string>}`.
Decode it with `json.decode`. On a `fail`/`multiline` result, `success` is
`false`.

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
- [Inlay tokens](../element/inlay-tokens.md) — multimodal extraction when
  `useMultimodal = true`.

## Example

```lua
function onOutput(id)
    local raw = axLLMMain(id, json.encode({
        { role = 'user', content = 'Classify the mood.' },
    }), false, ''):await()
    local reply = json.decode(raw)
    if reply.success then
        log(reply.result)
    end
end
```

## See also

- Preamble helper: [`axLLM`](axLLM.md)
- Main model: [`LLMMain`](LLMMain.md), [`LLM`](LLM.md)
- One-shot: [`simpleLLM`](simpleLLM.md)
- Elements: [Promise / await](../element/promise-async.md),
  [Inlay tokens](../element/inlay-tokens.md),
  [Access key & tiers](../element/access-key.md)
