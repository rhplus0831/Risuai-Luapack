# CBS: `{{blank}}`

- **Layer:** CBS function
- **Category:** context
- **Aliases:** `none`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`blank`)

Returns an empty string.

## Syntax

```text
{{blank}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Always returns `''` (the empty string). It is useful for clearing a value, for
producing an empty branch in a conditional, or as a no-op placeholder. The
alias `{{none}}` behaves identically.

## Example

```text
{{#if {{getvar::hidden}}}}{{blank}}{{:else}}visible{{/if}}
```

## See also

- CBS: [`{{getvar}}`](../variables/getvar.md)
- Element: [Chat variables](../../element/chat-variables.md)
