# CBS: `{{makedict::k=v::k2=v2::...}}`

- **Layer:** CBS function
- **Category:** dict
- **Aliases:** `dict`, `d`, `makeobject`, `object`, `o`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`makedict`)

Builds a JSON object from `key=value` arguments.

## Syntax

```text
{{makedict::k=v::k2=v2::...}}
{{dict::k=v::k2=v2::...}}
{{object::k=v::k2=v2::...}}
```

(also `d`, `makeobject`, `o`)

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1.. | pairs | yes | One or more `key=value` strings. Each becomes a property. |

## Behavior

Each argument is split on the **first** `=`: everything before it is the key,
everything after is the value. Arguments with no `=` are skipped (invalid pairs
are ignored). The collected pairs are returned as a JSON object via
`JSON.stringify`.

Because only the first `=` is used as the separator, values may themselves
contain `=`. All values are stored as strings, so numbers come out quoted (for
example `age=25` becomes `"age":"25"`). If a later argument repeats a key, it
overwrites the earlier one.

## Example

```text
{{makedict::name=John::age=25}}
```

renders `{"name":"John","age":"25"}`.

## See also

- CBS: [`{{dictelement}}`](dictelement.md), [`{{element}}`](element.md), [`{{objectassert}}`](objectassert.md)
