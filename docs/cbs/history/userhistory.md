# CBS: `{{userhistory}}`

- Layer: CBS function
- Category: history
- Aliases: `usermessages`, `user_history`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`userhistory`)

Returns all user messages as a JSON array.

## Syntax

```text
{{userhistory}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Filters the current chat's messages to those with role `user` and returns them
as a JSON array. Each element is a cloned message object (containing `role`,
`data`, and other metadata); its `data` field is run through Risu's chat parser
before serialization, so CBS templates inside the message text are expanded.

## Example

```text
{{userhistory}}
```

## See also

- CBS: [`{{charhistory}}`](charhistory.md), [`{{history}}`](history.md)
