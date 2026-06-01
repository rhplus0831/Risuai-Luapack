# CBS: `{{model}}`

- **Layer:** CBS function
- **Category:** model
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`model`)

Returns the id of the currently selected AI model.

## Syntax

```text
{{model}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns `db.aiModel`, the identifier of the main model selected in Risu (for
example `gpt-4` or a `claude-*` id). This is the raw stored id; for a
human-friendly display name use [`{{metadata::modelname}}`](metadata.md). The
secondary model is reported by [`{{axmodel}}`](axmodel.md).

## Example

```text
Running on {{model}}.
```

## See also

- CBS: [`{{axmodel}}`](axmodel.md), [`{{metadata}}`](metadata.md), [`{{prefillsupported}}`](prefillsupported.md)
