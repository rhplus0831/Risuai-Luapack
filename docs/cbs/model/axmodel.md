# CBS: `{{axmodel}}`

- Layer: CBS function
- Category: model
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`axmodel`)

Returns the id of the auxiliary / sub model.

## Syntax

```text
{{axmodel}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns `db.subModel`, the identifier of the secondary ("auxiliary" or "sub")
model Risu uses for specialized tasks such as embedding, summarization or other
secondary processing, as distinct from the main chat model reported by
[`{{model}}`](model.md).

## Example

```text
Aux model: {{axmodel}}
```

## See also

- CBS: [`{{model}}`](model.md), [`{{metadata}}`](metadata.md)
