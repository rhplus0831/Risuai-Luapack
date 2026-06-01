# CBS: `{{erase}}`

- Layer: CBS function
- Category: format
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`erase`)

Removes the last sentence from the output produced so far.

## Syntax

```text
{{erase}}
```

## Arguments

None.

## Behavior

Like [`{{bkspc}}`](bkspc.md) but at sentence granularity. It reads the current
accumulated output (the nested root buffer), trims trailing whitespace, then
walks back from the end until it hits a sentence terminator (`.`, `!`, `?`, or a
newline). Everything after that terminator is removed; the terminator itself is
kept. If no terminator is found, the whole buffer is cleared. The buffer is
rewritten in place via `setNestedRoot`, and `{{erase}}` itself expands to an
empty string.

If there is no output buffer yet, it does nothing and returns an empty string.

## Example

```text
hello world. what's in {{erase}} what's up
```

renders `hello world. what's up` — the trailing partial sentence is removed.

## See also

- CBS: [`{{bkspc}}`](bkspc.md) (remove the last word)
