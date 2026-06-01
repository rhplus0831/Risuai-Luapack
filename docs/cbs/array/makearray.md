# CBS: `{{makearray::a::b::...}}`

- Layer: CBS function
- Category: array
- Aliases: `array`, `a`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`makearray`)

Builds a JSON array from the supplied arguments.

## Syntax

```text
{{makearray::a::b::...}}
{{array::a::b::...}}
{{a::a::b::...}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | `a`, `b`, ... | no | Each argument becomes one array element. Variadic. |

## Behavior

Collects every argument after the function name and returns them as a JSON array
string, in order. Each argument is stored as a string, so numbers and JSON
fragments become quoted strings rather than numeric or nested-object values.
With no arguments the result is an empty array `[]`.

`makearray` is the producer side of the array family; the result can be consumed
by [`{{arrayelement}}`](arrayelement.md), [`{{arraylength}}`](arraylength.md),
[`{{join}}`](join.md), and the array mutators. To build the `::`-joined argument
string that [`{{spread}}`](spread.md) expects, build the array here and pass it
to `spread`. For key/value structures, use the dictionary builder `makedict`
(aliases `dict`, `makeobject`, `object`).

## Example

```text
{{makearray::a::b::c}}   -> ["a","b","c"]
{{array::1::2}}          -> ["1","2"]
```

## See also

- CBS: [`{{arrayelement}}`](arrayelement.md), [`{{arraylength}}`](arraylength.md)
- CBS: [`{{join}}`](join.md), [`{{spread}}`](spread.md), [`{{range}}`](range.md)
