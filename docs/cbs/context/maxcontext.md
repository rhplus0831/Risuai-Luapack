# CBS: `{{maxcontext}}`

- Layer: CBS function
- Category: context
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`maxcontext`)

Returns the configured maximum context length.

## Syntax

```text
{{maxcontext}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns `db.maxContext` as a string, i.e. the token limit configured for the
current model setup (for example `4096` or `8192`). This is the user's setting,
not a count of the tokens currently in use. The same value is also reachable via
[`{{metadata::maxcontext}}`](../model/metadata.md).

## Example

```text
Context budget: {{maxcontext}} tokens.
```

## See also

- CBS: [`{{model}}`](../model/model.md), [`{{metadata}}`](../model/metadata.md)
