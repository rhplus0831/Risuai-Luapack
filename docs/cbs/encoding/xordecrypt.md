# CBS: `{{xordecrypt::b64}}`

- **Layer:** CBS function
- **Category:** encoding
- **Aliases:** `xordecode`, `xord`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`xordecrypt`)

Reverses [`{{xor}}`](xor.md): base64-decodes, then XORs each byte with `0xFF`.

## Syntax

```text
{{xordecrypt::b64}}
{{xordecode::b64}}
{{xord::b64}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `b64` | yes | A base64 string produced by [`{{xor}}`](xor.md). |

## Behavior

Decodes `b64` from base64 (`Buffer.from(b64, 'base64')`), XORs every byte with
`0xFF`, and returns the bytes decoded as UTF-8 text
(`new TextDecoder().decode(buf)`). Applied to the output of [`{{xor}}`](xor.md)
on the same input it reproduces the original string, since XOR with `0xFF` is its
own inverse.

## Example

```text
{{xordecrypt::{{xor::hello}}}}
```

renders `hello`.

## See also

- CBS: [`{{xor}}`](xor.md) (forward), [`{{crypt}}`](crypt.md)
