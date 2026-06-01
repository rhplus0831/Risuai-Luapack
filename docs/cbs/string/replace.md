# CBS: `{{replace::s::find::to}}`

- Layer: CBS function
- Category: string
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`replace`)

Replaces every occurrence of a substring with another string.

## Syntax

```text
{{replace::s::find::to}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to operate on. |
| 2 | `find` | yes | The substring to search for. |
| 3 | `to` | yes | The replacement string. |

## Behavior

Returns `s` with all occurrences of `find` replaced by `to`, using the
literal JavaScript `String.prototype.replaceAll`. The match is
case-sensitive and treats `find` as a plain string, not a regular
expression. If `find` is not present, `s` is returned unchanged.

## Example

```text
{{replace::Hello World::o::0}}   -> Hell0 W0rld
```

## See also

- CBS: [`{{contains}}`](contains.md), [`{{split}}`](split.md)
- CBS: [`{{trim}}`](trim.md)
