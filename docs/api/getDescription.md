# API: `getDescription(id)`

- Layer: Host API (`declareAPI`)
- Permission tier: Safe (blocked in `editDisplay`)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getDescription', ...)`)

Returns the description (`desc`) of the currently selected character.

## Signature

```lua
getDescription(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingSafeIds`. |

## Returns

`string` — `char.desc` of the selected character.

Throws `Character is a group` if the selected character is a group chat
(`char.type === 'group'`), which has no single description.

## Permission

Safe tier — unusually for a getter, this one is guarded: the call no-ops unless
`id` is in `ScriptingSafeIds`. It is therefore not available to
[`editDisplay`](../hooks/editDisplay.md) listeners. Available from
`onStart`/`onInput`/`onOutput`, button/custom modes, and the
request/input/output edit hooks. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Reads the selected character's `desc` field.

## Example

```lua
function onStart(id)
    local desc = getDescription(id)
    log(desc)
end
```

## See also

- [`setDescription`](setDescription.md) (change the description)
- [`getName`](getName.md), [`getCharacterFirstMessage`](getCharacterFirstMessage.md)
