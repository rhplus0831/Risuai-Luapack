# CBS: `{{element::json::key1::key2::...}}`

- **Layer:** CBS function
- **Category:** dict
- **Aliases:** `ele`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`element`)

Walks a path of keys/indices into a nested JSON value and returns what it finds.

## Syntax

```text
{{element::json::key1::key2::...}}
{{ele::json::key1::key2::...}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `json` | yes | A JSON string to start from (object or array). |
| 2.. | keys | yes | One or more keys/indices applied in order to descend the structure. |

## Behavior

Starting from `json`, the function applies each remaining argument in sequence.
At every step the current string is `JSON.parse`d; if the parsed value is `null`
or is neither an object nor an array, traversal stops and `"null"` is returned.
Otherwise the next argument is used to index into it, and that result becomes the
current value for the next step.

If at any step the indexed value is falsy (missing key, `undefined`, empty
string, `0`, …), the result is `"null"`. If `JSON.parse` ever throws, the result
is also `"null"`. After the last key, the current value is returned as-is.

Each key indexes the freshly parsed value, so object keys and numeric array
indices both work as path segments.

## Example

```text
{{element::{"user":{"name":"John"}}::user::name}}
```

renders `John`.

## See also

- CBS: [`{{dictelement}}`](dictelement.md) (single key), [`{{makedict}}`](makedict.md), [`{{objectassert}}`](objectassert.md)
