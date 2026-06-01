# Hook: `editDisplay` (mode `editDisplay`)

- **Layer:** Hook (edit listener)
- **Define:** `listenEdit('editDisplay', function(id, value, meta) ... return value end)`
- **Fires:** during display rendering, on the text about to be shown (stored chat is unchanged)
- **Permission tier:** Restricted **edit-display** — chat-var writes only; no chat/character mutation, no reload; **never** low-level
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`callListenMain` in `luaCodeWrapper`; `runLuaEditTrigger`; `ScriptingEditDisplayIds`)

`editDisplay` transforms what the user sees without changing the stored message.

## When it fires

`editDisplay` runs at display-render time, on the text about to be shown. It does
**not** modify stored chat — it only shapes the rendered output. In the display
pipeline, Lua `editDisplay` runs **first**, then CBS expands, then `editdisplay`
Regex Scripts run. (See the pipeline overview in
[`docs/README.md`](../README.md).) The string you return is what the later
display stages receive.

## How to handle

Register a handler with `listenEdit('editDisplay', fn)`. You may register
**multiple** handlers; they chain in registration order, each receiving the
previous handler's return value. Every handler **must `return` the value** —
forgetting `return` passes `nil` down the chain and blanks the displayed text. If
a handler errors, Risu keeps the original content.

```lua
listenEdit('editDisplay', function(id, value, meta)
    -- value is the display text (a string)
    return value
end)
```

## Receives

| Arg | Type | Description |
|-----|------|-------------|
| `id` | [access key](../element/access-key.md) | Restricted **edit-display** key (goes into `ScriptingEditDisplayIds` only). |
| `value` | string | The display text about to be rendered. |
| `meta` | table | Context Risu has for this run. The regex/display pipeline supplies `index`, the 0-based chat message index, when available. |

## Return value

**Return the transformed string.** Returning `nil` (or forgetting `return`)
blanks the displayed text. The returned string becomes the input to the next
`editDisplay` handler, then CBS, then `editdisplay` regex.

## What you can / cannot do here

This hook runs under the restricted edit-display tier — strictly narrower than
the safe tier the other hooks get.

- **Can:** rewrite the display string, read chat variables, and write chat
  variables via [`setChatVar`](../api/setChatVar.md)/`setState` (the only
  privileged write permitted here).
- **Cannot:** mutate chat or character data — [`addChat`](../api/addChat.md),
  [`setChat`](../api/setChat.md), [`setName`](../api/setName.md),
  [`setBackgroundEmbedding`](../api/setBackgroundEmbedding.md),
  [`upsertLocalLoreBook`](../api/upsertLocalLoreBook.md) all no-op. Cannot call
  [`reloadChat`](../api/reloadChat.md) or
  [`reloadDisplay`](../api/reloadDisplay.md). Never gets low-level access.

### Marker text + display-regex cooperation

`editDisplay` works best as a *renderer*, not a data store. The durable pattern
is to write stable marker text (or chat vars) from a safe hook like
[`onOutput`](onOutput.md), then convert markers to HTML in the display layer:

```lua
-- in a safe hook (onOutput), store a durable marker on the message:
function onOutput(id)
    local last = getChat(id, -1)
    setChat(id, -1, last.data .. '\n[[hp=' .. getChatVar(id, 'hp') .. ']]')
end

-- in editDisplay, turn the marker into a panel for display only:
listenEdit('editDisplay', function(id, value, meta)
    return (value:gsub('%[%[hp=(%d+)%]%]', '<div class="status">HP: %1</div>'))
end)
```

This keeps the stored message plain and robust while the visible message gets a
panel. An `editdisplay` Regex Script can do the same conversion and runs after
this hook, so split the work whichever way is easier to maintain.

## See also

- Hooks: [`onOutput`](onOutput.md), [`editOutput`](editOutput.md), [`editRequest`](editRequest.md)
- Elements: [Access key & tiers](../element/access-key.md), [Display HTML](../element/display-html.md)
- API: [`setChatVar`](../api/setChatVar.md)
