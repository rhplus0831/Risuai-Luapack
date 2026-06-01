# API: `log(value)`

- Layer: Preamble helper (defined in `luaCodeWrapper`, not `declareAPI`)
- Permission tier: Always available (no key guard)
- Async: no
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper` -> `function log`)

Logs any Lua value to the developer console by JSON-encoding it.

## Signature

```lua
log(value)
```

Note: `log` does not take an access key — it is a convenience wrapper.

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `value` | any | Any JSON-encodable Lua value (string, number, table, …). It is passed through `json.encode` and then to [`logMain`](logMain.md). |

The body is literally `logMain(json.encode(value))`, so a table is serialized to
JSON, and `logMain` then `JSON.parse`s it back before `console.log` — meaning the
console receives the structured value, not a JSON string.

## Returns

Nothing.

## Permission

Always available — neither `log` nor the underlying `logMain` checks any key. It
works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Writes to the browser/dev console.

## Example

```lua
function onStart(id)
    log({ name = getName(id), len = getChatLength(id) })
end
```

## See also

- [`logMain`](logMain.md) (the raw underlying call)
- [`cbs`](cbs.md), [`getTokens`](getTokens.md)
