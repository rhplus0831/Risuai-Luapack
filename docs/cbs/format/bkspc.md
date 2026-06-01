# CBS: `{{bkspc}}`

- **Layer:** CBS function
- **Category:** format
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`bkspc`)

Removes the last word from the output produced so far.

## Syntax

```text
{{bkspc}}
```

## Arguments

None.

## Behavior

Acts like a backspace over a whole word. It reads the current accumulated output
(the nested root buffer), trims trailing whitespace, then walks back from the end
to the previous whitespace (space, newline, or tab) and drops everything from
there to the end. The buffer is rewritten in place via `setNestedRoot`, and
`{{bkspc}}` itself expands to an empty string.

If there is no output buffer yet, it does nothing and returns an empty string.
Because it mutates already-emitted text, the effect depends on what precedes it
in the same parse.

## Example

```text
hello world {{bkspc}} user
```

renders `hello user` — the word `world` is removed.

## See also

- CBS: [`{{erase}}`](erase.md) (remove the last sentence)
