# Element: Background embedding (`backgroundHTML`)

- Kind: Element (data structure)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`getBackgroundEmbedding`, `setBackgroundEmbedding`), `Refer/Risuai/src/lib/ChatScreens/BackgroundDom.svelte` (render), `Refer/Risuai/src/ts/process/modules.ts` (`moduleBackgroundEmbedding`), `Refer/Risuai/src/ts/parser/parser.svelte.ts` (display parsing)

Persistent HTML rendered behind the chat. Risu's UI calls it "background
embedding", but the character field Lua touches is `backgroundHTML`.

## What it is

Two separate sources feed the background layer:

- Character: `character.backgroundHTML`.
- Modules: each enabled module's `backgroundEmbedding`, concatenated by
  `moduleUpdate` into the `moduleBackgroundEmbedding` store.

`BackgroundDom.svelte` renders the concatenation:

```text
(character.backgroundHTML || '') + "\n" + (module backgroundEmbedding || '')
```

through `ParseMarkdown(..., 'back')` (background display mode).

## What Lua can touch

[`getBackgroundEmbedding(id)`](../api/getBackgroundEmbedding.md) and
[`setBackgroundEmbedding(id, html)`](../api/setBackgroundEmbedding.md) read and
write only the selected character's `backgroundHTML`. They do not see or
modify the module `backgroundEmbedding` half of the rendered output.

Both calls are Safe tier — guarded on `ScriptingSafeIds`. They are *not*
`editDisplay`-capable: an `editDisplay` listener holds only an edit-display key,
so these calls no-op there. (This is the same Safe tier as `setName`,
`addChat`, etc.)

```lua
function onStart(id)
    setBackgroundEmbedding(id, [[
<style>
.status-panel { padding: 0.5rem; border: 1px solid currentColor; }
</style>
<div class="status-panel">HP: {{getvar::hp}}</div>
]])
    reloadDisplay(id)
end
```

## How the string is rendered

The background HTML goes through the display pipeline in background mode:

- CBS is parsed first (`risuChatParser`), so `{{getvar::hp}}` etc. expand.
- Asset tokens are expanded in background mode — notably `{{bg::name}}`
  only renders here (see [Asset display tokens](asset-tokens.md)).
- The result is sanitized like all [display HTML](display-html.md): `<style>` is
  allowed but each class selector is rewritten with an `x-risu-` prefix and
  scoped under `.chattext`; class attributes are likewise prefixed.

So source written as `class="status-panel"` renders with DOM class
`x-risu-status-panel`, and a `<style>` rule `.status-panel { … }` becomes
`.chattext .x-risu-status-panel { … }`.

## Shape / fields

| Source | Field | Lua access |
|--------|-------|------------|
| character | `backgroundHTML` | read/write (Safe tier) |
| module | `backgroundEmbedding` | none (appended at render only) |

## Used by

- APIs: [`getBackgroundEmbedding`](../api/getBackgroundEmbedding.md),
  [`setBackgroundEmbedding`](../api/setBackgroundEmbedding.md)
- Modules contribute the second half — see [Modules](modules.md)

## See also

- Elements: [Display HTML](display-html.md), [Asset display tokens](asset-tokens.md),
  [Regex Script](regex-script.md), [Access key & tiers](access-key.md)
- Index: [`docs/README.md`](../README.md)
