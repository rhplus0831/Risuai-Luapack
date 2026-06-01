# Element: Chat message (`{role, data, time}`)

- Kind: Element (data structure)
- Source: `Refer/Risuai/src/ts/storage/database.svelte.ts` (`Message` interface), `Refer/Risuai/src/ts/process/scriptings.ts` (`getChatMain`, `getFullChatMain`, `setFullChatMain`, `addChat`, `insertChat`, `setChat`, `setChatRole`)

The shape Lua sees for a stored chat message, and how it differs from the
OpenAI-style request message used by LLM prompts and `editRequest`.

## What it is

Risu stores each chat turn as a `Message` object. The full database `Message`
has many fields (`saying`, `chatId`, `generationInfo`, `disabled`, …), but the
slice Lua receives through `getChatMain`/`getFullChatMain` is just three fields:

```lua
{ role = 'user'|'char', data = '<string>', time = <number> }
```

`getChat(id, index)` (the JSON wrapper over `getChatMain`) returns one such
table; `getFullChat(id)` returns an array of them. When the index is out of
range `getChatMain` returns `null` (so `getChat` yields `nil`).

## Shape / fields

| Field | Type | Notes |
|-------|------|-------|
| `role` | string | Only ever `"user"` or `"char"`. Any role string other than `"user"` is normalized to `"char"`. |
| `data` | string | The message text. This is a plain string, not a structured object. |
| `time` | number | Message timestamp; `0` when the stored message has no `time`. |

## Roles are only `user` or `char`

Risu's `Message.role` type is `'user'|'char'`. Every mutation API normalizes the
role: `addChat`, `insertChat`, and `setChatRole` compute
`role === 'user' ? 'user' : 'char'`, so any role string other than `"user"`
becomes `"char"` (including `"assistant"`, `"system"`, `"bot"`, `""`, …).

```lua
addChat(id, 'system', 'logged in')   -- stored with role = 'char'
setChatRole(id, -1, 'assistant')     -- becomes 'char'
```

## `data` is a string, not `{role, content}`

The stored shape and the OpenAI-style request shape are different objects. Do
not pass an OpenAI-style `{role, content}` table to the chat mutators:

- `setChat(id, index, value)` writes `value ?? ''` straight into `message.data`.
- `addChat`/`insertChat` push `{ role, data = value ?? '' }`.
- `setFullChat(id, value)` (wrapper over `setFullChatMain`) JSON-encodes the
  array and rebuilds each message as `{ role = v.role, data = v.data }` — it
  reads `data`, not `content`, and drops `time`.

Pass a finished string. If you hand a Lua table to `setChat`, it is not a
portable way to set message text.

## Contrast: OpenAI-style request messages

LLM prompts and the `editRequest` hook use the OpenAI message shape instead:

```lua
{ role = 'system'|'user'|'assistant', content = '<string>' }
```

When you call [`LLM`](../api/LLM.md)/[`axLLM`](../api/axLLM.md), Risu maps the
`role` you supply onto `system`/`user`/`assistant`:

| You pass | Mapped to |
|----------|-----------|
| `system`, `sys` | `system` |
| `user` | `user` |
| `assistant`, `bot`, `char` | `assistant` |
| anything else | `assistant` (default) |

Missing `content` defaults to an empty string. So a stored `char` message
(`{role='char', data='...'}`) and a request `assistant` message
(`{role='assistant', content='...'}`) describe the same speaker in two different
shapes — keep them straight.

## Indices are 0-based, negative wraps

Chat indices are JavaScript-style and 0-based. The host uses
`message.at(index)`, so negative indices behave like JS `Array.at`:
`getChat(id, -1)` reads the last message, `setChat(id, -1, value)` rewrites it.
`cutChat(id, start, end)` keeps the half-open range `[start, end)`.

## Used by

- APIs that return this shape: [`getChat`](../api/getChat.md),
  [`getFullChat`](../api/getFullChat.md)
- APIs that write it: [`addChat`](../api/addChat.md),
  [`insertChat`](../api/insertChat.md), [`setChat`](../api/setChat.md),
  [`setChatRole`](../api/setChatRole.md), [`setFullChat`](../api/setFullChat.md)
- Hooks that read/mutate chat: [`onStart`](../hooks/onStart.md),
  [`onOutput`](../hooks/onOutput.md); the request-shape contrast is used by
  [`editRequest`](../hooks/editRequest.md)

## See also

- Elements: [Access key & tiers](access-key.md), [Promise / await](promise-async.md)
- CBS: [`{{getvar}}`](../cbs/variables/getvar.md)
- Index: [`docs/README.md`](../README.md)
