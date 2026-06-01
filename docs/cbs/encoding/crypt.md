# CBS: `{{crypt::s::shift}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** `crypto`, `caesar`, `encrypt`, `decrypt`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`crypt`)

A Caesar-style shift cipher over UTF-16 code units; with the default shift it is
its own inverse.

## Syntax

```text
{{crypt::s}}
{{crypt::s::shift}}
{{caesar::s::shift}}
{{encrypt::s}}
{{decrypt::s}}
```

(also `crypto`)

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The string to transform. |
| 2 | `shift` | no | The shift amount. Defaults to `32768`; a `NaN` value also falls back to `32768`. |

## Behavior

For each character of `s`, the code unit is read with `charCodeAt`. Code units
above `65535` are passed through unchanged. Otherwise `shift` is added and the
result wrapped into the 16-bit range (`if(shiftedCode > 65535) shiftedCode -= 65536`),
and the shifted character is emitted with `String.fromCharCode`.

The default shift of `32768` is exactly half of `65536`, so applying `{{crypt}}`
twice with the default returns the original text — the same call **encrypts and
decrypts**, which is why `encrypt` and `decrypt` are aliases of one function.
With a custom `shift`, decrypt by running again with the complementary shift
(`65536 - shift`).

## Example

```text
{{crypt::hello}}
```

renders the shifted form; `{{crypt::{{crypt::hello}}}}` renders `hello` again.

## See also

- CBS: [`{{xor}}`](xor.md), [`{{xordecrypt}}`](xordecrypt.md)
