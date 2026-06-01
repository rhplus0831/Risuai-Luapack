# CBS: `{{objectassert::obj::key::value}}`

- Layer: CBS function
- Category: dict
- Aliases: `dictassert`, `object_assert`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`objectassert`)

Sets a default on a JSON object: writes the key only if it is not already
present, then returns the object.

## Syntax

```text
{{objectassert::obj::key::value}}
{{dictassert::obj::key::value}}
{{object_assert::obj::key::value}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `obj` | yes | A JSON object string. |
| 2 | `key` | yes | The property name to default. |
| 3 | `value` | yes | The value to set when `key` is absent. |

## Behavior

Parses `obj` as a JSON object. If the value at `key` is falsy (missing,
`undefined`, `0`, empty string, etc. — the check is `if(!dict[key])`), the
object's `key` is set to `value`. The (possibly modified) object is then
returned via `JSON.stringify`. An existing truthy value is left untouched.

Because the guard is a JavaScript truthiness test, a key whose current value is
an empty string, `0`, or `false` is treated as absent and will be
overwritten. Parsing uses `parseDict`, so a non-object input starts from an
empty object `{}`.

## Example

```text
{{objectassert::{"a":1}::b::2}}
```

renders `{"a":1,"b":"2"}`.

## See also

- CBS: [`{{makedict}}`](makedict.md), [`{{dictelement}}`](dictelement.md), [`{{element}}`](element.md)
