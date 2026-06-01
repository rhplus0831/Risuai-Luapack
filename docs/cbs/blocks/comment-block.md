# CBS: `{{// comment}}`

- Layer: CBS function (doc-only construct)
- Category: blocks
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`//`)

A hidden comment whose content is removed entirely.

## Syntax

```text
{{// comment}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `comment` | yes | The comment text (everything after `//`). |

## Behavior

`{{// ...}}` is registered as a `doc_only` construct: the whole `{{...}}` is
consumed by the parser and replaced with nothing. The comment text appears
nowhere — not in the displayed chat and not in the model request. Use it to
annotate a template for your own reference.

This is the *hidden* counterpart to [`{{comment::text}}`](../format/comment.md),
which renders a visible styled `<div>` in display mode.

## Example

```text
{{// reminder: bump this counter each turn}}
{{setvar::turn::{{calc::{{getvar::turn}}+1}}}}
```

The first line produces no output at all.

## See also

- CBS: [`{{comment::text}}`](../format/comment.md) (visible comment)
- Block: [`{{#pure}}`](pure.md), [`{{#escape}}`](escape.md)
