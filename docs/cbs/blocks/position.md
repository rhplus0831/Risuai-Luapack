# CBS: `{{position::name}}`

- Layer: CBS function (doc-only construct)
- Category: blocks
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`position`, doc-only)

Declares a named position that lorebook `@@position` injection can target.

## Syntax

```text
{{position::name}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The position name. |

## Behavior

`{{position}}` is registered as a `doc_only` construct: it marks a named point in
the text. Other Risu features can then inject content at that point — in
particular the `@@position <name>` lorebook decorator, which places a lore entry
relative to the declared position rather than at a fixed depth.

Per the registered description: *"Defines the position which can be used in
various features such as @@position &lt;positionName&gt; decorator."*

## Example

```text
{{position::scene}}
```

declares a position named `scene` that an `@@position scene` lore entry can be
injected at.

## See also

- Element: [Lorebook entry](../../element/lorebook-entry.md)
- CBS: [`{{hiddenkey}}`](../format/hiddenkey.md)
