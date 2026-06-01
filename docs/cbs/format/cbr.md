# CBS: `{{cbr::n}}`

- Layer: CBS function
- Category: format
- Aliases: `cnl`, `cnewline`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`cbr`)

Emits the escaped two-character sequence `\n`, optionally repeated.

## Syntax

```text
{{cbr}}
{{cbr::n}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `n` | no | How many times to repeat the escape sequence. Coerced to a number; values below 1 are clamped to 1. |

## Behavior

With no argument, returns the literal two-character string `\n` (a backslash
followed by `n`) — not an actual newline. With an argument, it repeats the
construct's matched text `Number(n)` times, with a minimum of 1 (any value `< 1`,
including non-numeric input that coerces to `NaN`/`0`, becomes 1).

Contrast with [`{{br}}`](br.md), which emits a real newline character. `{{cbr}}`
is for cases where you need the *literal* escape text to survive into a later
stage that interprets `\n` itself.

## Example

```text
{{cbr::3}}
```

emits `\n\n\n` as literal text.

## See also

- CBS: [`{{br}}`](br.md) (real newline)
