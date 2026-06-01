# CBS: `{{hiddenkey::keys}}`

- **Layer:** CBS function
- **Category:** format
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`hiddenkey`)

Marks lorebook activation keys that never reach the model.

## Syntax

```text
{{hiddenkey::keys}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `keys` | yes | The activation key text. |

## Behavior

The callback always returns an empty string, so the construct contributes nothing
to the rendered output or the model request. Its purpose is positional: when used
inside lorebook content, the `keys` text acts as an activation key for lorebook
scanning (it can trigger lore entries) **without** being included in what is sent
to the model. In other words, it lets a lore entry be matched by a phrase that
the model never sees.

The name is matched case-insensitively with spaces/underscores/hyphens ignored,
so `{{hidden_key::...}}` is equivalent to `{{hiddenkey::...}}`.

## Example

```text
{{hiddenkey::secret-trigger}}
```

registers `secret-trigger` as an activation key but emits nothing.

## See also

- Element: [Lorebook entry](../../element/lorebook-entry.md)
- CBS: [`{{position}}`](../blocks/position.md)
