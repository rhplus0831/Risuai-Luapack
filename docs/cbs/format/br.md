# CBS: `{{br}}`

- Layer: CBS function
- Category: format
- Aliases: `newline`
- Source: `Refer/Risuai/src/ts/cbs.ts` (`br`)

Emits a single literal newline character.

## Syntax

```text
{{br}}
```

## Arguments

None.

## Behavior

Returns one `"\n"` character (an actual newline, not the two-character escape
`\n`). Useful for inserting line breaks in a template where typing a raw newline
would be inconvenient or would get collapsed by surrounding block trimming.

For an *escaped* newline (the literal backslash-n text, optionally repeated), use
[`{{cbr}}`](cbr.md) instead.

## Example

```text
Line one{{br}}Line two
```

renders as two lines.

## See also

- CBS: [`{{cbr}}`](cbr.md) (escaped newline), [`{{blank}}`](../context/blank.md)
