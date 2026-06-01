# CBS: `{{isfirstmsg}}`

- **Layer:** CBS function
- **Category:** context
- **Aliases:** `isfirstmessage`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`isfirstmsg`)

Returns whether the template is being expanded in a first-message context.

## Syntax

```text
{{isfirstmsg}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns the string `1` when the matcher's `cbsConditions.firstmsg` flag is set
(i.e. the text being rendered is a character's first message / greeting), and
`0` otherwise. This is a boolean-style flag suitable for use in
`{{#if ...}}` blocks. In the same context, [`{{role}}`](role.md) reports `char`.

## Example

```text
{{#if {{isfirstmsg}}}}Welcome!{{/if}}
```

## See also

- CBS: [`{{role}}`](role.md), [`{{firstmsgindex}}`](firstmsgindex.md)
