# Element: Regex Script

- **Kind:** Element (data structure)
- **Source:** `Refer/Risuai/src/ts/storage/database.svelte.ts` (`customscript` interface), `Refer/Risuai/src/ts/process/scripts.ts` (`processScriptFull`, `executeScript`)

User-defined find/replace rules that run in Risu's text pipeline. Lua cooperates
with them by writing marker text; Lua itself has no `editprocess` listener.

## Shape / fields

The database `customscript` interface:

| Field | Type | Description |
|-------|------|-------------|
| `comment` | string | Human label for the rule. |
| `in` | string | An **ECMAScript regex pattern without slash delimiters** (e.g. `\[\[hp=(\d+)\]\]`). |
| `out` | string | Replacement text (supports the captures below). |
| `type` | string | One of `editinput`, `editoutput`, `editprocess`, `editdisplay`. |
| `flag?` | string | Regex flags (and bracketed action metadata) when `ableFlag` is set. |
| `ableFlag?` | boolean | When false, Risu forces the flag `g`; when true, `flag` is used. |

The active scripts run as `db.presetRegex` ++ `character.customscript` ++
enabled-module regex, in that order.

## `type` — when it runs

| `type` | Stage |
|--------|-------|
| `editinput` | transforms submitted user text before it is stored |
| `editoutput` | transforms the model reply before/while it is stored |
| `editprocess` | transforms chat-history text for the model request (not stored/displayed) |
| `editdisplay` | transforms text for rendering only (does not mutate stored chat) |

Lua edit listeners run **first** within each stage. Note Lua has listeners for
`editInput`/`editOutput`/`editRequest`/`editDisplay` but **no `editprocess`
listener** — only Regex Scripts can act at the `editprocess` stage.

## Flags

`in` is compiled with `new RegExp(in, flag)`. If `ableFlag` is false the flag is
`g`. If `ableFlag` is true, Risu starts from `flag`, then:

- removes unsupported letters, keeping only `d g i m s u v y`;
- de-duplicates repeated flags;
- if nothing remains, falls back to `u`.

## Replacement captures (in `out`)

Standard JavaScript replacement plus Risu shorthands:

| Token | Meaning |
|-------|---------|
| `$&` | the full match |
| `$1`, `$2`, … | numbered capture groups |
| `$<name>` | named capture group |
| `$n` | Risu shorthand for a newline (`\n`) |
| `{{data}}` | Risu shorthand for the full match (rewritten to `$&`) |

After replacement, output ending in `>` gets an automatic trailing newline
unless the `no_end_nl` action is present.

## Action / flag directives

When `ableFlag` is true and `flag` contains `<...>` metadata, the bracketed
items are stripped from the real regex flags and treated as actions
(comma-separated, e.g. `g<order 10,move_top>`). Some actions are equivalently
expressed as an `out` prefix beginning with `@@`:

| Directive | Effect |
|-----------|--------|
| `<cbs>` | parse the `in` pattern through CBS before building the regex |
| `<order N>` | set sort order; scripts are sorted by **descending** order number |
| `<move_top>` / `<move_bottom>` | remove matches and prepend / append the replacement to the text |
| `<inject>` or `out` starting `@@inject` | commit the processed text back to the stored message at the current chat index, then remove the match from display |
| `<repeat_back>` or `out` starting `@@repeat_back` | when the text does not match, copy a previous same-role match (optional position `start` / `end` / `start_nl` / `end_nl`) |
| `out` starting `@@emo <name>` | activate a matching character emotion image |
| `<no_end_nl>` | suppress the automatic trailing newline after replacements ending in `>` |

(`@@inject` and `@@repeat_back` only take effect when a real chat index is
available, i.e. `chatID !== -1`.)

## Lua cooperation pattern

Have Lua write a durable marker, then let an `editdisplay` Regex Script turn it
into HTML:

```lua
function onOutput(id)
    local last = getChat(id, -1)
    setChat(id, -1, last.data .. '\n[[hp=' .. getChatVar(id, 'hp') .. ']]')
end
```

```text
in:       \[\[hp=(\d+)\]\]
out:      <div class="status-panel">HP: $1</div>
type:     editdisplay
flag:     g
ableFlag: true
```

The stored message stays plain text; the rendered message gets a panel.

## Used by

- Hooks: pairs with [`editDisplay`](../hooks/editDisplay.md),
  [`editInput`](../hooks/editInput.md), [`editOutput`](../hooks/editOutput.md)
  (Lua listeners run before the matching regex stage)
- Modules contribute regex scripts — see [Modules](modules.md)

## See also

- Elements: [Display HTML](display-html.md), [Modules](modules.md),
  [Chat message](chat-message.md)
- Index: [`docs/README.md`](../README.md)
