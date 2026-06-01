# CBS: `{{tempvar::name}}`

- **Layer:** CBS function
- **Category:** variables
- **Aliases:** `gettempvar`
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`tempvar`)

Reads a temporary variable that lives only during the current parse.

## Syntax

```text
{{tempvar::name}}
{{gettempvar::name}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `name` | yes | The temporary-variable name to read. |

## Behavior

Looks up `name` in the parse-local variable table and returns its value. The
table is created fresh each time the parser runs and is discarded when the parse
finishes, so a temporary variable never persists between sends or across
separate template strings. If `name` was never set this parse, the function
returns an empty string.

Temporary variables are the read/write pair to [`{{settempvar}}`](settempvar.md).
Unlike [`{{setvar}}`](setvar.md) / [`{{getvar}}`](getvar.md), they are not saved
to the chat and do not require `runVar` to take effect.

## Example

```text
{{settempvar::greeting::Hello}}{{tempvar::greeting}} there
```

renders `Hello there`.

## See also

- Element: [Chat variables](../../element/chat-variables.md)
- CBS: [`{{settempvar}}`](settempvar.md), [`{{getvar}}`](getvar.md), [`{{return}}`](return.md)
