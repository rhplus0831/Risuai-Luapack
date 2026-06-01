# CBS: `{{risu::size}}`

- Layer: CBS function
- Category: assets
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`risu`)

Emits the Risu logo as an `<img>`.

## Syntax

```text
{{risu}}
{{risu::size}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `size` | no | Side length in pixels. Defaults to `45` when omitted. |

## Behavior

Returns

```html
<img src="/logo2.png" style="height:SIZEpx;width:SIZEpx" />
```

where `SIZE` is the first argument, or `45` if no argument is given. The logo is
always square (height equals width).

## Example

```text
{{risu}}
{{risu::60}}
```

## See also

- Element: [Display HTML](../../element/display-html.md)
