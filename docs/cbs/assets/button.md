# CBS: `{{button::text::trigger}}`

- Layer: CBS function
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`button`)

Emits an HTML button that runs a manual trigger when clicked.

## Syntax

```text
{{button::text::trigger}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `text` | yes | The visible button label. |
| 2 | `trigger` | yes | The manual-trigger name to fire on click. |

## Behavior

Returns the markup

```html
<button class="button-default" risu-trigger="trigger">text</button>
```

The `risu-trigger` attribute names a manual trigger. When the user clicks the
button, Risu dispatches that trigger. If the trigger is a Lua trigger effect,
Risu invokes the Lua runtime with the mode set to the trigger name, which falls
through to a global function of that name (see
[custom modes](../../hooks/custom-modes.md)). So `{{button::Open::OpenMenu}}` is
handled by `function OpenMenu(id) ... end`.

## Example

```text
{{button::Open menu::OpenMenu}}
```

```lua
function OpenMenu(id)
    -- runs when the button is clicked
end
```

## See also

- CBS: [`{{trigger-id}}`](../identity/trigger-id.md)
- Element: [Display HTML](../../element/display-html.md)
- Hook: [Custom modes](../../hooks/custom-modes.md)
