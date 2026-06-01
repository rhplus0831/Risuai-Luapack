# CBS: `{{trigger_id}}`

- **Layer:** CBS function
- **Category:** identity
- **Aliases:** `triggerid`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`trigger_id`)

Returns the `risu-id` of the element that fired the current manual trigger.

## Syntax

```text
{{trigger_id}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

When a manual trigger is fired by clicking an element in displayed HTML, Risu
records the `risu-id` attribute of that element in `CurrentTriggerIdStore`. This
function reads that store and returns the recorded ID. If no ID was provided
(the element had no `risu-id`, or the trigger was not started by a click), it
returns the literal string `"null"`.

This is the CBS counterpart of the value Lua handlers read from the trigger
context for custom/button modes.

## Example

```text
{{#if {{equal::{{trigger_id}}::buy-button}}}}You clicked Buy.{{/if}}
```

## See also

- Element: [Display HTML & triggers](../../element/display-html.md)
- Hook: [Custom / button modes](../../hooks/custom-modes.md)
