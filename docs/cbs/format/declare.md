# CBS: `{{declare::name}}`

- Layer: CBS function
- Category: format
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`declare`)

Sets a parser flag that other CBS behavior can read.

## Syntax

```text
{{declare::name}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The declaration name. |

## Behavior

Sets `matcherArg.var["__declared_<name>__"]` to `"1"` and expands to an empty
string. The flag lives in the same variable map the parser threads through the
current parse, so it can be used to switch parser behavior or to signal to later
constructs that a given declaration is present. The value written is always
`"1"`; there is no `undeclare`.

Because the key is namespaced as `__declared_<name>__`, it does not collide with
ordinary chat variables read by [`{{getvar}}`](../variables/getvar.md).

## Example

```text
{{declare::spoilers}}
```

sets the internal flag `__declared_spoilers__` to `"1"`.

## See also

- CBS: [`{{settempvar}}`](../variables/settempvar.md), [`{{tempvar}}`](../variables/tempvar.md)
