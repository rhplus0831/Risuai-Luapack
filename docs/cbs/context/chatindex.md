# CBS: `{{chatindex}}`

- **Layer:** CBS function
- **Category:** context
- **Aliases:** `chat_index`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`chatindex`)

Returns the index of the message currently being processed.

## Syntax

```text
{{chatindex}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| - | - | - | Takes no arguments. |

## Behavior

Returns `matcherArg.chatID` as a string: the 0-based index of the message whose
context this template is being expanded in. When the template is **not** scoped
to a specific message (for example in prompt-level expansions rather than a
per-message render), the index is `-1`. Per-message helpers such as
[`{{messagetime}}`](../datetime/messagetime.md) and
[`{{role}}`](role.md) read this same index.

## Example

```text
This is message #{{chatindex}}.
```

## See also

- CBS: [`{{role}}`](role.md), [`{{firstmsgindex}}`](firstmsgindex.md), [`{{messagetime}}`](../datetime/messagetime.md)
- Element: [Chat message](../../element/chat-message.md)
