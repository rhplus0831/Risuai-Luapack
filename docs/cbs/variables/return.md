# CBS: `{{return::value}}`

- **Layer:** CBS function
- **Category:** variables
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`return`)

Sets the parser's return value and forces it to stop.

## Syntax

```text
{{return::value}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `value` | yes | The value to set as the parse result. |

## Behavior

Stores `value` into the internal `__return__` variable and sets the
`__force_return__` flag to `"1"`. The flag tells the parser to stop and use
`__return__` as the result of the parse, so any remaining template text after
this call is not processed. The function itself returns an empty string and
emits nothing at the point it appears.

This is the CBS way to short-circuit a template and hand back a computed value,
typically from within a triggered script that evaluates a CBS expression.

## Example

```text
{{#if {{getvar::done}}}}{{return::finished}}{{/if}}keep going
```

When `done` is truthy the parse stops and yields `finished`; otherwise it
renders `keep going`.

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{tempvar}}`](tempvar.md), [`{{settempvar}}`](settempvar.md)
