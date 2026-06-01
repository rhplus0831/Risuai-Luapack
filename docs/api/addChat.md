# API: `addChat(id, role, value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('addChat', ...)`)

Appends a new message to the end of the current chat.

## Signature

```lua
addChat(id, role, value)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `role` | string | `"user"` stores a user message; **any other value becomes `"char"`**. |
| `value` | string | The message text. `nil` is coerced to an empty string. |

## Returns

Nothing.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
**not** available to [`editDisplay`](../hooks/editDisplay.md) listeners (which
hold only an edit-display key). Available from `onStart`/`onInput`/`onOutput`,
button/custom modes, and the request/input/output edit hooks.

## Elements used

- [Chat message](../element/chat-message.md) — the appended message uses the
  stored shape `{ role = 'user'|'char', data = '<string>' }`. Pass a **string**
  for `value`, not an OpenAI-style `{ role, content }` object.

## Example

```lua
function onStart(id)
    addChat(id, 'char', 'Hello!')
    addChat(id, 'system', 'logged in')   -- 'system' is coerced to 'char'
end
```

## See also

- [`insertChat`](insertChat.md) (insert at an index), [`setChat`](setChat.md)
  (replace text), [`removeChat`](removeChat.md), [`setFullChat`](setFullChat.md)
- Hook timing: [`onOutput`](../hooks/onOutput.md), [`onStart`](../hooks/onStart.md)
