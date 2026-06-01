# API: `getPersonaDescription(id)`

- **Layer:** Host API (`declareAPI`)
- **Permission tier:** Always available (no key guard)
- **Async:** no
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`declareAPI('getPersonaDescription', ...)`)

Returns the active persona prompt, CBS-parsed in the selected-character context.

## Signature

```lua
getPersonaDescription(id)
```

## Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | [access key](../element/access-key.md) | The key passed to your handler. Accepted for convention; this call carries **no key guard**. |

## Returns

`string` — `getPersonaPrompt()` after being run through `risuChatParser` with
`{ chara = <selected character> }`. CBS templates in the persona prompt (for
example `{{user}}`, `{{char}}`) are therefore expanded against the selected
character before the value is returned. Variable-writing CBS does not take effect
here (the parser runs without `runVar`).

## Permission

Always available — the implementation never checks `id` against any permission
set. It works from every mode, including [`editDisplay`](../hooks/editDisplay.md)
listeners. See [access key & tiers](../element/access-key.md).

## Elements used

- None. Reads the persona prompt and parses it against the selected character.

## Example

```lua
function onStart(id)
    local persona = getPersonaDescription(id)
    log(persona)
end
```

## See also

- [`getPersonaName`](getPersonaName.md) (the persona name)
- [`cbs`](cbs.md) (expand an arbitrary CBS template)
- [`getDescription`](getDescription.md) (the character description)
