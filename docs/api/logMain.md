# API: `logMain(value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('logMain', ...)`)

Raw console logger: prints a parsed JSON string to the developer console.

## Signature

```lua
logMain(value)
```

Note: `logMain` does **not** take an access key. It is the only low-level
logging primitive; most packs call [`log`](log.md) instead.

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `value` | string | A **JSON string**. The host runs `console.log(JSON.parse(value))`, so passing a non-JSON string will throw inside `JSON.parse`. |

Because of the `JSON.parse`, you almost always want the [`log`](log.md) helper,
which `json.encode`s its argument for you before calling `logMain`.

## Returns

Nothing.

## Permission

Always available — the implementation never checks `id` (and takes no `id`). It
works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Writes to the browser/dev console.

## Example

```lua
function onStart(id)
    logMain('"hello"')          -- console.log("hello")
    logMain('{"hp":100}')       -- console.log({ hp = 100 })
    log({ hp = 100 })            -- preferred: encodes for you
end
```

## See also

- [`log`](log.md) (preferred wrapper that encodes for you)
- [`cbs`](cbs.md)
