# CBS: `{{charhistory}}`

- **Layer:** CBS function
- **Category:** history
- **Aliases:** `charmessages`, `char_history`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`charhistory`)

Returns all character messages as a JSON array.

## Syntax

```text
{{charhistory}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Filters the current chat's messages to those with role `char` and returns them
as a JSON array. Each element is a cloned message object (containing `role`,
`data`, and other metadata); its `data` field is run through Risu's chat parser
before serialization, so CBS templates inside the message text are expanded.

## Example

```text
{{charhistory}}
```

## See also

- CBS: [`{{userhistory}}`](userhistory.md), [`{{history}}`](history.md)
