# CBS: `{{jb}}`

- Layer: CBS function
- Category: prompts
- Aliases: `jailbreak`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`jb`)

Returns the jailbreak prompt text.

## Syntax

```text
{{jb}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the jailbreak prompt (`db.jailbreak`) used to modify AI behavior, after
running it through Risu's chat parser, so any CBS templates inside it are
expanded. This returns the text unconditionally; whether the jailbreak is
actually applied to the request is reflected by
[`{{jbtoggled}}`](../context/jbtoggled.md).

## Example

```text
{{#if {{jbtoggled}}}}{{jb}}{{/if}}
```

## See also

- CBS: [`{{jbtoggled}}`](../context/jbtoggled.md), [`{{mainprompt}}`](mainprompt.md), [`{{globalnote}}`](globalnote.md)
