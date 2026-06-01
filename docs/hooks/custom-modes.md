# Hook: Custom / manual-trigger modes

- Layer: Hook (custom mode — default global dispatch)
- Define: global `function <ModeName>(id)`
- Fires: when a manual trigger / named button runs the pack's Lua with a mode that is not a built-in
- Permission tier: Safe (plus low-level if the trigger has `lowLevelAccess`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (the `default` case in the mode dispatch of `runScripted`; `runLuaButtonTrigger`)

Any trigger name that is not a built-in mode is dispatched to a global function
of that exact name.

## When it fires

When a manual trigger contains a Lua trigger effect, Risu runs the pack's Lua
with `mode` set to the trigger's name. The Lua runtime handles the built-in
modes first (`input`, `output`, `start`, `onButtonClick`, and the
`editRequest`/`editInput`/`editOutput`/`editDisplay` listeners). If the mode is
none of those, the `default` case does a global lookup for a function whose
name exactly matches the mode string and calls it with the access key `(id)`.

This is why a button emitted as `{{button::Open::OpenMenu}}` — or an element with
`risu-trigger="OpenMenu"` — is handled by a global `function OpenMenu(id)`.
(Note: an element with `risu-trigger` routes here even if it also carries
`risu-btn`; `risu-trigger` wins and [`onButtonClick`](onButtonClick.md) is not
called. See [Display HTML](../element/display-html.md).)

## How to handle

Define a global function named exactly like the trigger/mode. Risu dispatches
by global name, so it must not live inside a module table. Names must match the
emitted trigger string exactly.

```lua
function OpenMenu(id)
    -- runs when a trigger named "OpenMenu" fires
    reloadDisplay(id)
end
```

Generated or dynamic mode names can be served through an `_G` metatable (Lua's
normal global-lookup mechanism), but explicit global functions are easier to
lint, test, and review — prefer them unless you genuinely need dynamic names.

## Receives

| Arg | Description |
|-----|-------------|
| `id` | The [access key](../element/access-key.md) for this run (safe tier; low-level too if the trigger has `lowLevelAccess`). |

Custom modes are dispatched with `(id)` only — they do not receive the
button payload that [`onButtonClick`](onButtonClick.md) gets. If the handler must
do nothing when the matching global is absent, Risu simply skips dispatch (the
global lookup returns nil).

## Return value

Return `false` to set `stopSending`. Any other return value (including `nil`)
proceeds normally.

## Capabilities

- Can: everything a safe hook can — read/write chat variables, mutate chat
  ([`addChat`](../api/addChat.md), [`setChat`](../api/setChat.md)), read/write
  character fields, call [`reloadDisplay`](../api/reloadDisplay.md), and call
  low-level APIs if the trigger has `lowLevelAccess`.
- Cannot: receive a payload argument (use [`onButtonClick`](onButtonClick.md)
  with `risu-btn` if you need a payload), or be reached via a module table — the
  function must be a top-level global.

## See also

- Hooks: [`onButtonClick`](onButtonClick.md), [`onStart`](onStart.md)
- Elements: [Display HTML & buttons](../element/display-html.md), [Access key & tiers](../element/access-key.md)
- API: [`reloadDisplay`](../api/reloadDisplay.md)
