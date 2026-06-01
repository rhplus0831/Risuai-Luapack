# CBS: `{{dictelement::obj::key}}`

- Layer: CBS function
- Category: dict
- Aliases: `objectelement`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`dictelement`)

Reads a single value out of a JSON object by key.

## Syntax

```text
{{dictelement::obj::key}}
{{objectelement::obj::key}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `obj` | yes | A JSON object string, e.g. `{"name":"John"}`. |
| 2 | `key` | yes | The property name to look up. |

## Behavior

Parses `obj` as a JSON object and returns the value stored under `key`. If the
key is missing (or `obj` does not parse as an object), the result is the literal
string `"null"`. When the looked-up value is itself an object or array it is
re-serialized with `JSON.stringify`; any other value is coerced to a string.

Parsing uses Risu's `parseDict`, which falls back to an empty object `{}` when
`obj` is not valid JSON, so a malformed object also yields `"null"`.

## Example

```text
{{dictelement::{"name":"John"}::name}}
```

renders `John`.

## See also

- CBS: [`{{element}}`](element.md) (nested path), [`{{objectassert}}`](objectassert.md), [`{{makedict}}`](makedict.md)
