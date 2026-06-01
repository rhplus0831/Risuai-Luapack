# API: `cbs(value)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('cbs', ...)`)

Expands a CBS `{{...}}` template string in the current character context.

## Signature

```lua
cbs(value)
```

Note: `cbs` does **not** take an access key. It runs `risuChatParser(value, {
chara = getCurrentCharacter() })` and returns the result.

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `value` | string | A template containing CBS syntax (e.g. `{{char}}`, `{{getvar::hp}}`). |

## Returns

`string` — the template with all CBS expanded against the current character.

**Variable-writing CBS does not run here.** The parser is invoked without
`runVar`, so `{{setvar}}`, `{{addvar}}`, `{{setdefaultvar}}` and similar have no
effect; only reads/expansions take place.

## Permission

Always available — the implementation never checks `id` (and takes no `id`). It
works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- None directly. Delegates to Risu's CBS engine in the current character context.

## Example

```lua
function onStart(id)
    local line = cbs('Hi {{user}}, you are talking to {{char}}.')
    log(line)
    local hp = cbs('{{getvar::hp}}')   -- read-only expansion
    log(hp)
end
```

## See also

- CBS reference: [`{{getvar}}`](../cbs/variables/getvar.md) and the rest of [`../cbs/`](../cbs/)
- [`getPersonaDescription`](getPersonaDescription.md) (also CBS-parses its result)
