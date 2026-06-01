# Element: Modules

- **Kind:** Element (data structure)
- **Source:** `Refer/Risuai/src/ts/process/modules.ts` (`RisuModule`, `getModules`, `getModuleLorebooks`/`getModuleAssets`/`getModuleTriggers`/`getModuleRegexScripts`/`getModuleToggles`/`getModuleMcps`, `moduleUpdate`)

Reusable bundles of lore, regex, triggers, assets, toggles, MCP URLs, and
background HTML. Lua has no API to list them, but enabled modules affect Lua
indirectly.

## What it is

A `RisuModule` packages content that augments the current character/chat. The
set of **enabled** modules is computed by `getModules()` as the union of:

1. `db.enabledModules` — globally enabled module ids,
2. `chat.modules` — modules enabled for the current chat,
3. `character.modules` — modules enabled by the selected character,
4. `db.moduleIntergration` — a comma-separated id list (note the upstream
   spelling).

Modules are then resolved by id (or `namespace`) and de-duplicated.

## Shape / fields

The `RisuModule` interface (contribution-bearing fields):

| Field | Type | Contributes |
|-------|------|-------------|
| `lorebook?` | `loreBook[]` | lore entries (`getModuleLorebooks`) |
| `regex?` | `customscript[]` | regex scripts (`getModuleRegexScripts`) |
| `trigger?` | `triggerscript[]` | triggers incl. Lua (`getModuleTriggers`) |
| `assets?` | `[name, path, ext][]` | display assets (`getModuleAssets`) |
| `customModuleToggle?` | string | prompt-toggle lines (`getModuleToggles`) |
| `backgroundEmbedding?` | string | background HTML (`moduleUpdate`) |
| `mcp?` | `{ url }` | MCP server URLs (`getModuleMcps`) |
| `lowLevelAccess?` | boolean | grants low-level access to that module's triggers |

## How modules affect Lua

Lua has **no "list modules" host API.** But enabled modules reach Lua through
the shared pipelines:

- **Module Lua triggers run alongside character triggers.** `getModuleTriggers`
  appends them, and edit/button dispatch iterates character triggers *then*
  module triggers. A module trigger's `lowLevelAccess` comes from the module
  (and is forced off for edit listeners).
- **Module lore is visible to [`getLoreBooks`](../api/getLoreBooks.md)** and to
  normal lore activation (`loadLoreBooks`), since `getLoreBooksMain` includes
  `getModuleLorebooks()`.
- **Module assets are visible to [asset display tokens](asset-tokens.md)** —
  `{{img::name}}` etc. match the character assets plus module assets.
- **Module prompt toggles are readable via `getGlobalVar(id, 'toggle_key')`** —
  their `customModuleToggle` lines are appended to the sidebar definition. See
  [Prompt toggles](prompt-toggles.md).
- **Module background embedding is appended behind the chat** — see
  [Background embedding](background-embedding.md). (Lua's
  `getBackgroundEmbedding`/`setBackgroundEmbedding` touch only the character
  `backgroundHTML`, not this.)
- **Module regex scripts run in the same Regex Script pipeline** — see
  [Regex Script](regex-script.md).

## Used by

- APIs (indirectly): [`getLoreBooks`](../api/getLoreBooks.md),
  [`loadLoreBooks`](../api/loadLoreBooks.md),
  [`getGlobalVar`](../api/getGlobalVar.md)
- Elements: [Asset display tokens](asset-tokens.md),
  [Prompt toggles](prompt-toggles.md),
  [Background embedding](background-embedding.md),
  [Lorebook entry](lorebook-entry.md), [Regex Script](regex-script.md)

## See also

- Elements: [Lorebook entry](lorebook-entry.md), [Regex Script](regex-script.md),
  [Asset display tokens](asset-tokens.md), [Prompt toggles](prompt-toggles.md)
- Index: [`docs/README.md`](../README.md)
