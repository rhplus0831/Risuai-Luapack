# CBS: `{{firstmsgindex}}`

- **Layer:** CBS function
- **Category:** context
- **Aliases:** `firstmessageindex`, `first_msg_index`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`firstmsgindex`)

Returns the index of the selected first message / alternate greeting.

## Syntax

```text
{{firstmsgindex}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the current chat's `fmIndex` as a string. `fmIndex` records which
greeting the chat started from when a character has multiple alternate
greetings. A value of `-1` means the **default** first message is in use; `0`,
`1`, ... select the corresponding alternate greeting. This is distinct from
[`{{chatindex}}`](chatindex.md), which is the position of the current message
within the chat.

## Example

```text
{{#if {{? {{firstmsgindex}} > -1}}}}Alternate greeting #{{firstmsgindex}}{{/if}}
```

## See also

- CBS: [`{{chatindex}}`](chatindex.md), [`{{isfirstmsg}}`](isfirstmsg.md)
