# API: `reloadChat(id, index)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('reloadChat', ...)`)

Requests a re-render of a single chat message.

## Signature

```lua
reloadChat(id, index)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |
| `index` | number | 0-based index of the message to re-render. |

## Returns

Nothing.

## Behavior

The host bumps a per-index counter on an internal pointer
(`ReloadChatPointer[index]`), which Risu observes to re-render just that one
message. Use it after editing a single message (for example with
[`setChat`](setChat.md)) when a full [`reloadDisplay`](reloadDisplay.md) would be
heavier than needed. Indices are 0-based.

## Permission

Safe tier — the call no-ops unless `id` is in `ScriptingSafeIds`. It is therefore
not available to [`editDisplay`](../hooks/editDisplay.md) listeners. See
[access key & tiers](../element/access-key.md).

## Elements used

- [Chat message](../element/chat-message.md) — targets one message by index.
- [Display HTML](../element/display-html.md) — controls how that message renders.

## Example

```lua
function onButtonClick(id, data)
    setChat(id, 0, 'Updated opening line.')
    reloadChat(id, 0)
end
```

## See also

- [`reloadDisplay`](reloadDisplay.md) (whole view), [`setChat`](setChat.md),
  [`getChat`](getChat.md)
- Element: [Chat message](../element/chat-message.md)
