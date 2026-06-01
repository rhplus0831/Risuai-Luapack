# Hook: `onButtonClick` (mode `onButtonClick`)

- Layer: Hook (event mode)
- Define: global `function onButtonClick(id, data)`
- Fires: when a rendered chat button carrying `risu-btn="payload"` is clicked
- Permission tier: Safe (plus low-level if the trigger has `lowLevelAccess`)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (mode dispatch in `runScripted`; `runLuaButtonTrigger`)

`onButtonClick` is the handler for buttons embedded in displayed messages or
background HTML.

## When it fires

When the user clicks a rendered element carrying a `risu-btn` attribute, Risu
calls `runLuaButtonTrigger`, which dispatches mode `onButtonClick` and passes the
attribute's string value as `data`.

Two rules from the source bite if ignored:

- Buttons fire only in non-group chats. Group chats go through a different
  trigger path that does not emit `onButtonClick`.
- `risu-trigger` wins over `risu-btn`. If an element carries both
  `risu-trigger` and `risu-btn`, Risu treats it as a `risu-trigger` (a
  [custom-mode](custom-modes.md) dispatch by name) and `onButtonClick` is not
  called.

See [`display-html`](../element/display-html.md) for how to emit clickable
elements (CBS `{{button::...}}` and raw `risu-btn` / `risu-trigger` attributes).

## How to handle

Define a global function named `onButtonClick`. Risu dispatches by global
name, so it must not live inside a module table.

```lua
function onButtonClick(id, data)
    -- data is the risu-btn payload string of the clicked element
end
```

## Receives

| Arg | Description |
|-----|-------------|
| `id` | The [access key](../element/access-key.md) for this run (safe tier; low-level too if the trigger has `lowLevelAccess`). |
| `data` | The `risu-btn` payload string of the clicked element. |

## Return value

Return `false` to set `stopSending`. For a button that does not start a send,
the return value is otherwise unused.

## Capabilities

- Can: read `data` to branch on which button was clicked; read/write chat
  variables; mutate chat ([`addChat`](../api/addChat.md),
  [`setChat`](../api/setChat.md)); read/write character fields; call
  [`reloadDisplay`](../api/reloadDisplay.md) to refresh the UI; and call
  low-level APIs if the trigger has `lowLevelAccess`.
- Cannot: receive clicks from group chats, or from elements that also carry
  `risu-trigger` (those route to the named [custom-mode](custom-modes.md)
  handler instead).

```lua
function onButtonClick(id, data)
    if data == 'heal' then
        setChatVar(id, 'hp', '100')
        reloadDisplay(id)
    end
end
```

If you prefer one handler per button rather than branching on `data`, use a
named [custom-mode](custom-modes.md) function and emit `risu-trigger="Name"`
(or `{{button::Label::Name}}`) instead of `risu-btn`.

## See also

- Hooks: [Custom / manual-trigger modes](custom-modes.md), [`onStart`](onStart.md)
- Elements: [Display HTML & buttons](../element/display-html.md), [Access key & tiers](../element/access-key.md)
- API: [`reloadDisplay`](../api/reloadDisplay.md)
