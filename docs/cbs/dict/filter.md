# CBS: `{{filter::array::type}}`

- Layer: CBS function
- Category: dict
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`filter`)

Filters a JSON array, removing empty and/or duplicate entries.

## Syntax

```text
{{filter::array::type}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `array` | yes | A JSON array string. |
| 2 | `type` | yes | One of `all`, `nonempty`, or `unique`. |

## Behavior

Parses `array` as a JSON array and returns a new JSON array (via `makeArray`)
containing only the elements that pass the filter chosen by `type`:

- `all` — keep elements that are non-empty and the first occurrence of
  their value (drops empties and duplicates).
- `nonempty` — keep elements that are not the empty string.
- `unique` — keep only the first occurrence of each value (drops
  duplicates).

An unrecognized `type` falls back to `all`. Emptiness is tested as `f !== ''`
and uniqueness as `i === array.indexOf(f)`, so de-duplication keeps the earliest
position of each value.

## Example

```text
{{filter::["a","","a"]::unique}}
```

renders `["a",""]` (first occurrences kept; the empty string is a distinct
value under `unique`).

## See also

- CBS: [`{{makedict}}`](makedict.md), [`{{element}}`](element.md)
- CBS: [`{{sum}}`](../aggregate/sum.md), [`{{average}}`](../aggregate/average.md) (consume JSON arrays)
