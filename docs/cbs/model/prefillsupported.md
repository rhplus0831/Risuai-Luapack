# CBS: `{{prefillsupported}}`

- **Layer:** CBS function
- **Category:** model
- **Aliases:** `prefill_supported`, `prefill`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`prefillsupported`)

Returns whether the current model supports response prefill.

## Syntax

```text
{{prefillsupported}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns `1` if the current model id (`db.aiModel`) starts with `claude`, else
`0`. Prefill lets the request seed the beginning of the assistant's reply, which
Risu treats as a Claude-model capability. The detection is purely a
case-sensitive `startsWith('claude')` check on the model id; any non-Claude id
returns `0`. The aliases `{{prefill}}` and `{{prefill_supported}}` behave
identically.

## Example

```text
{{#if {{prefillsupported}}}}prefill enabled{{/if}}
```

## See also

- CBS: [`{{model}}`](model.md), [`{{metadata}}`](metadata.md)
