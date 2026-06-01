# CBS: `{{xor::s}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** `xorencrypt`, `xorencode`, `xore`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`xor`)

Obfuscates a string by XOR-ing each byte with `0xFF` and base64-encoding the
result.

## Syntax

```text
{{xor::s}}
{{xorencrypt::s}}
{{xorencode::s}}
{{xore::s}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `s` | yes | The plaintext string to obfuscate. |

## Behavior

UTF-8 encodes `s` (`new TextEncoder().encode`), XORs every byte with `0xFF`, and
returns the resulting bytes as a base64 string (`Buffer.from(buf).toString('base64')`).
This is simple obfuscation, not real encryption. Reverse it with
[`{{xordecrypt}}`](xordecrypt.md), which applies the same `0xFF` XOR after
base64-decoding.

## Example

```text
{{xor::hello}}
```

renders the base64 of `hello` with every byte inverted.

## See also

- CBS: [`{{xordecrypt}}`](xordecrypt.md) (reverse), [`{{crypt}}`](crypt.md)
