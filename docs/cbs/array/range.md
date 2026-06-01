# CBS: `{{range::spec}}`

- **Layer:** CBS function
- **Category:** array
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`range`)

Generates a JSON array of a numeric sequence.

## Syntax

```text
{{range::spec}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `spec` | yes | A JSON array describing the sequence (see below). |

## Behavior

`spec` is parsed as a JSON array and interpreted by how many entries it has:

- `[N]` (one entry) -> `start = 0`, `end = N`, `step = 1`: yields `0 .. N-1`.
- `[start, end]` (two entries) -> `step = 1`: yields `start .. end-1`.
- `[start, end, step]` (three entries) -> yields `start, start+step, ...` while
  `i < end`.

The loop is `for (i = start; i < end; i += step)`, so `end` is **exclusive** and
each produced value is converted to a string. Because the condition is strictly
`i < end`, a non-positive `step` (or a `start` already past `end`) produces an
empty array `[]` rather than looping. If `spec` is not valid JSON it parses to an
empty array, which is treated as the single-entry form with `N = NaN` and yields
`[]`.

The result is a JSON array string suitable for [`{{join}}`](join.md),
[`{{spread}}`](spread.md), or the array accessors.

## Example

```text
{{range::[5]}}        -> ["0","1","2","3","4"]
{{range::[2,5]}}      -> ["2","3","4"]
{{range::[2,8,2]}}    -> ["2","4","6"]
```

## See also

- CBS: [`{{makearray}}`](makearray.md), [`{{arraylength}}`](arraylength.md)
- CBS: [`{{join}}`](join.md), [`{{spread}}`](spread.md)
