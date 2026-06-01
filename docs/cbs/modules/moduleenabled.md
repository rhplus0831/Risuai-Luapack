# CBS: `{{moduleenabled::namespace}}`

- Layer: CBS function
- Category: modules
- Aliases: `module_enabled`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`moduleenabled`)

Tests whether a module is currently enabled.

## Syntax

```text
{{moduleenabled::namespace}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `namespace` | yes | The module's namespace to look up. |

## Behavior

Iterates the currently enabled/loaded modules and returns `"1"` if one has a
`namespace` exactly equal to the argument, otherwise `"0"`. The comparison is on
the module namespace, not its display name.

The name is matched case-insensitively with spaces/underscores/hyphens ignored,
so `{{module_enabled::...}}` is the same construct.

## Example

```text
{{#when {{moduleenabled::dice-roller}}}}Dice module is on.{{/when}}
```

renders the body only when a module with namespace `dice-roller` is enabled.

## See also

- Element: [Modules](../../element/modules.md)
- Block: [`{{#when ...}}`](../blocks/when.md)
