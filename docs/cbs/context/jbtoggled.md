# CBS: `{{jbtoggled}}`

- **Layer:** CBS function
- **Category:** context
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`jbtoggled`)

Returns whether the jailbreak prompt is enabled.

## Syntax

```text
{{jbtoggled}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Reads the global `db.jailbreakToggle` setting and returns `1` if the jailbreak
prompt is currently toggled on, `0` if it is off. This reflects only the toggle
state; the jailbreak prompt **text** itself is returned by
[`{{jb}}`](../prompts/jb.md) regardless of the toggle.

## Example

```text
{{#if {{jbtoggled}}}}{{jb}}{{/if}}
```

## See also

- CBS: [`{{jb}}`](../prompts/jb.md), [`{{maxcontext}}`](maxcontext.md)
- Element: [Prompt toggles](../../element/prompt-toggles.md)
