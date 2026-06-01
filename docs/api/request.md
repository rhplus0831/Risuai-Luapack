# API: `request(id, url)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Low-level (requires `lowLevelAccess`)
- **Async:** yes (`:await()`)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('request', ...)`)

Performs an HTTPS **GET** request and returns the response as a JSON string.
Heavily restricted: HTTPS only, short URLs only, rate-limited, and a few hosts
are blocked outright.

## Signature

```lua
request(id, url)   -- returns a Promise; call :await()
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Must be in `ScriptingLowLevelIds`. |
| `url` | string | The target URL. Must start with `https://` and be **at most 120 characters**. |

## Returns

A Promise resolving to a **JSON string** `{"status": <number>, "data": <string>}`.
Decode it with `json.decode`. `data` is the response body on success, or an
error message on failure. Notable statuses the host returns itself:

| Status | Meaning |
|--------|---------|
| `429` | Rate limit exceeded (more than ~5-6 requests per minute). |
| `413` | URL longer than 120 characters. |
| `400` | Non-HTTPS URL, a blocked host, or an internal fetch error. |

## Constraints

- **HTTPS only** — non-`https://` URLs return `400`.
- **URL <= 120 characters** — longer URLs return `413`.
- **Rate-limited** — the counter resets every 60 seconds; once more than 5
  requests have been made in the window the next returns `429` (roughly 5-6 per
  minute).
- **Blocked hosts** — URLs starting with `https://realm.risuai.net`,
  `https://risuai.net`, or `https://risuai.xyz` return `400`.
- **GET only** — there is no way to send a body, custom headers, or another
  method.

## Permission

Low-level tier — the call no-ops unless `id` is in `ScriptingLowLevelIds`,
granted only to safe-mode runs **when the character/module has `lowLevelAccess`
enabled**. It is **never** available to edit listeners
([`editRequest`](../hooks/editRequest.md), [`editInput`](../hooks/editInput.md),
[`editOutput`](../hooks/editOutput.md), [`editDisplay`](../hooks/editDisplay.md)),
which run with low-level access forced off. See
[access key & permission tiers](../element/access-key.md).

## Elements used

- [Promise / await](../element/promise-async.md) — async; `:await()` it.

## Example

```lua
function onStart(id)
    local raw = request(id, 'https://example.com/api/status'):await()
    local res = json.decode(raw)
    if res.status == 200 then
        log(res.data)
    end
end
```

## See also

- Elements: [Promise / await](../element/promise-async.md),
  [Access key & tiers](../element/access-key.md)
- Other low-level calls: [`similarity`](similarity.md),
  [`generateImage`](generateImage.md)
