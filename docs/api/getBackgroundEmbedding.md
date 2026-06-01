# API: `getBackgroundEmbedding(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Safe (blocked in `editDisplay`)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getBackgroundEmbedding', ...)`)

Returns the selected character's background embedding HTML (`char.backgroundHTML`).

## Signature

```lua
getBackgroundEmbedding(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |

## Returns

`string` — `char.backgroundHTML` of the selected character.

## Permission

Safe tier — unusually for a getter, this one is guarded: the call no-ops unless
`id` is in `ScriptingSafeIds`. It is therefore **not** available to
[`editDisplay`](../hooks/editDisplay.md) listeners. Available from
`onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- [Background embedding](../element/background-embedding.md) — the
  `backgroundHTML` block rendered behind the chat.

## Example

```lua
function onStart(id)
    local html = getBackgroundEmbedding(id)
    log(html)
end
```

## See also

- [`setBackgroundEmbedding`](setBackgroundEmbedding.md) (change it)
- Element: [Background embedding](../element/background-embedding.md)
