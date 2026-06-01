# Risu feature notes for Lua scripts

These notes summarize Risu features and data surfaces from `Refer/Risuai` that
are useful when authoring Lua packs. They complement the generated API reference
by explaining what the values mean in Risu's database and where Lua fits beside
CBS, Regex Scripts, modules, background HTML, assets, lorebooks, and memory.

Primary source files used:

- `Refer/Risuai/src/ts/process/scriptings.ts` - Lua host APIs and dispatch.
- `Refer/Risuai/src/ts/process/scripts.ts` - Regex Script pipeline.
- `Refer/Risuai/src/ts/parser/parser.svelte.ts` - CBS, asset, inlay, and HTML
  display parsing.
- `Refer/Risuai/src/ts/storage/database.svelte.ts` - character, chat,
  lorebook, regex, and module data shapes.
- `Refer/Risuai/src/ts/process/modules.ts` - enabled module aggregation.
- `Refer/Risuai/src/ts/parser/chatVar.svelte.ts` - chat/global variable
  storage.

## Mental model

Lua does not receive a raw handle to the Risu database. It receives an access
key, `id`, and calls whitelisted host APIs. Those APIs mostly operate on the
currently selected character and current chat.

For direct function signatures, see [lua-api.md](./lua-api.md). This document
focuses on the surrounding data and mechanisms.

## Pipeline touch points

Lua and Regex Scripts run at several points in the chat flow:

1. User submits text.
2. Input triggers run before the submitted text is stored. Then the text is
   processed by `editinput` Regex Scripts and Lua
   `listenEdit('editInput', ...)` handlers, and that transformed text is stored
   as the user message.
3. Start triggers run after the current chat, including the latest user message,
   is available and before chat history is processed for the model request. Chat
   mutations here affect the upcoming request.
4. Risu assembles prompt sections: main prompt, description, persona, example
   messages, activated lorebooks, author note, chat history, memory, jailbreak,
   and global note.
5. Chat-history text used for the request is processed by `editprocess` Regex
   Scripts. Lua has no `editProcess` listener.
6. Lua `listenEdit('editRequest', ...)` handlers receive the outgoing message
   array and can rewrite it.
7. The model response is processed by `editoutput` Regex Scripts and Lua
   `listenEdit('editOutput', ...)` handlers before or while the reply is stored.
8. Output triggers run after the assistant reply is present in the chat. Chat
   mutations here affect the stored reply.
9. Display rendering runs asset parsing, Lua `listenEdit('editDisplay', ...)`,
   display triggers, CBS, `editdisplay` Regex Scripts, asset parsing again if
   the text changed, inlay parsing, Markdown/HTML rendering, and sanitization.

Inside the Regex Script pipeline, Lua edit handlers run first. This makes a
good division of labor:

- Lua writes stable marker text or chat variables.
- `editdisplay` Regex Scripts turn those markers into HTML panels.
- Background embedding supplies shared CSS and persistent UI shell HTML.

## Data Lua can read and write

### Chat variables

`getChatVar(id, key)` reads the current chat's `scriptstate["$" .. key]`.
Missing values fall back to the selected character's `defaultVariables`, then
the database `templateDefaultVariables`, and finally return `"null"`.

`setChatVar(id, key, value)` writes a string to the current chat state. It is
allowed in normal safe handlers and in the restricted `editDisplay` tier.

The helper `getState(id, name)` / `setState(id, name, value)` stores JSON under
the chat variable key `__<name>`. Use this for tables, arrays, counters, and
structured UI state.

### Global variables and prompt toggles

`getGlobalVar(id, key)` reads `db.globalChatVariables[key]`, returning `"null"`
when absent. Lua currently has no host API to write global variables.

Prompt toggles are global variables whose keys are prefixed with `toggle_`.
Risu builds the sidebar toggle UI from `db.customPromptTemplateToggle` plus
enabled modules' `customModuleToggle` text. The syntax is line based:

```text
key=Label
key=Label=select=One,Two,Three
key=Label=text
key=Label=textarea
=Section=group
==groupEnd
=Divider=divider
=Caption=caption
```

Checkbox toggles store `"1"` or `"0"`. Select toggles store the zero-based
option index string. Text and textarea toggles store the text. Lua can read
them with `getGlobalVar(id, 'toggle_key')`.

### Chat messages

Lua sees messages as `{ role, data, time }`. Risu stores message roles as
`"user"` or `"char"`; other roles passed to `addChat`, `insertChat`, or
`setChatRole` become `"char"`.

In current Risu, stored message `data` is a string. The Lua wrappers
`getChat(id, index)` and `getFullChat(id)` JSON-decode that string into the
returned Lua table, and the mutation APIs write strings back to `message.data`.
Keep the two common shapes separate:

- Stored chat messages use `{ role = 'user'|'char', data = 'text' }`.
- Model/request messages use OpenAI-style `{ role = 'user'|'assistant'|'system',
  content = 'text' }`.

Passing a Lua table or `{content = ...}` object to `setChat` is not a portable
way to mutate chat; build the final string and pass that string.

Indices are JavaScript-style and 0-based. Negative indices work with
`Array.at`, so `getChat(id, -1)` reads the last message and `setChat(id, -1,
value)` changes it. `cutChat(id, start, end)` keeps the half-open range
`[start, end)`.

The current chat also has fields Lua can affect indirectly:

- `note` is the author's note, read by `getAuthorsNote(id)`.
- `localLore` is per-chat lorebook storage, written by `upsertLocalLoreBook`.
- `scriptstate` stores chat variables.
- `modules` can enable extra modules for this chat, but Lua cannot list or edit
  that module list directly.

### Manual trigger dispatch

When a manual trigger contains a Lua trigger effect, Risu invokes that Lua code
with mode set to the manual trigger name. The Lua runtime handles built-in modes
first (`start`, `input`, `output`, edit listeners, `onButtonClick`) and otherwise
does a global lookup for the mode string and calls that function with the access
key.

That is why a button emitted as `{{button::Open::OpenMenu}}` can be handled by
`function OpenMenu(id) ... end`. It also means generated trigger names can be
handled with Lua's normal global lookup mechanisms, including an `_G` metatable,
but explicit globals are easier to lint, test, and review.

### Character and persona data

Lua safe handlers can read or write selected character fields through host
APIs:

- `getName` / `setName`
- `getDescription` / `setDescription`
- `getCharacterFirstMessage` / `setCharacterFirstMessage`
- `getBackgroundEmbedding` / `setBackgroundEmbedding`
- `getCharacterLastMessage`, `getUserLastMessage`

Persona access is read-only from Lua:

- `getPersonaName(id)` reads the active user name.
- `getPersonaDescription(id)` returns the active persona prompt after CBS
  parsing in the selected character context.
- `getPersonaImage(id)` returns an inlay token for the active user icon, or an
  empty string.

`getCharacterImage(id)` similarly returns an inlay token for the selected
character image, or an empty string.

## Background embedding

Risu's UI calls this feature "background embedding", but the selected character
field behind Lua is `backgroundHTML`. Module data uses a separate
`backgroundEmbedding` field. At display time Risu renders:

```text
character.backgroundHTML + "\n" + enabled module backgroundEmbedding HTML
```

Lua `getBackgroundEmbedding(id)` and `setBackgroundEmbedding(id, html)` only
read or write the selected character's `backgroundHTML`. They do not return or
modify module background HTML. These calls require safe access, so they do not
work inside `editDisplay`.

The background string is parsed as Risu display content:

- CBS is expanded before rendering.
- Additional asset tokens are expanded in background mode.
- Markdown/HTML is sanitized.
- `<style>` tags are allowed, but CSS selectors are scoped under `.chattext`.
- Class selectors are internally prefixed with `x-risu-`.

That means this source:

```html
<style>
.status-panel { border: 1px solid currentColor; padding: 0.5rem; }
</style>
<div class="status-panel">HP: {{getvar::hp}}</div>
```

is rendered with a DOM class like `x-risu-status-panel`, and its CSS selector is
scoped under `.chattext`.

Background embedding is best for persistent display scaffolding and CSS. For
per-message panels, prefer marker text plus an `editdisplay` Regex Script.

The same display sanitizer and CSS rewriting apply to normal rendered chat and
to values returned from Lua `editDisplay`: class attributes are prefixed, class
selectors inside `<style>` are prefixed, and selectors are scoped under
`.chattext`.

## Regex Scripts

Regex Scripts are user-customizable find/replace rules. The active processing
path chains:

1. active preset regex (`db.presetRegex`),
2. selected character regex (`character.customscript`),
3. enabled module regex (`module.regex`).

In this Risu snapshot, `db.globalscript` still exists for the global regex UI
and import/export helper, but `processScriptFull` applies `db.presetRegex`
instead. When matching actual runtime behavior, check the active bot preset,
character, and enabled modules.

Each regex script has this shape:

```ts
{
  comment: string
  in: string
  out: string
  type: 'editinput' | 'editoutput' | 'editprocess' | 'editdisplay'
  flag?: string
  ableFlag?: boolean
}
```

`in` is an ECMAScript regex pattern without slash delimiters. If `ableFlag` is
false, Risu uses the default `g` flag. If `ableFlag` is true, `flag` is used
after unsupported letters are removed; supported regex flags are `d`, `g`, `i`,
`m`, `s`, `u`, `v`, and `y`.

Replacement text supports normal JavaScript replacement captures:

- `$&` for the full match.
- `$1`, `$2`, and so on for numeric captures.
- `$<name>` for named captures.
- `$n` as a Risu shorthand for a newline.
- `{{data}}` as a Risu shorthand for the full match.

When `flag` contains angle-bracket metadata, Risu removes the metadata from the
real regex flags and treats it as actions:

```text
g<cbs>
g<order 10>
g<move_top,no_end_nl>
```

Useful actions and output prefixes:

- `<cbs>` parses the input pattern through CBS before building the regex.
- `<order N>` sorts regex scripts by descending order number.
- `<move_top>` / `<move_bottom>` remove matches and move replacement output to
  the start or end of the text.
- `<inject>` or output beginning with `@@inject` commits the current processed
  text back to the stored message at the current chat index, then removes the
  match from display text.
- `<repeat_back>` or output beginning with `@@repeat_back` copies a previous
  same-role match when the current text does not match. Optional positions are
  `start`, `end`, `start_nl`, and `end_nl`.
- Output beginning with `@@emo <name>` activates a matching character emotion
  image.
- `<no_end_nl>` suppresses Risu's automatic newline after replacements ending
  in `>`.

Use `editdisplay` regex for decoration when you do not want to mutate stored
chat text. Use `editoutput` when the transformed text should become the stored
assistant reply. Use `editinput` when the transformed text should become the
stored user message. Use `editprocess` when the transformed text should affect
the model request but not the stored/displayed chat.

## Assets, emotions, and inlays

Lua can emit tokens that Risu's display parser later expands. These work in
normal chat display and in background embedding:

```text
{{raw::assetName}}       asset URL/path text
{{path::assetName}}      asset URL/path text
{{img::assetName}}       inline img tag
{{image::assetName}}     framed image block
{{video::assetName}}     video tag
{{video-img::assetName}} muted looping video tag
{{audio::assetName}}     audio tag
{{asset::assetName}}     image or video based on extension
{{bg::assetName}}        background div, only in background mode
{{bgm::assetName}}       hidden BGM control element
{{emotion::name}}        character emotion image
{{source::char}}         selected character image URL/path
{{source::user}}         active user icon URL/path
```

Assets come from selected character `additionalAssets` plus enabled module
`assets`. Emotion tokens use selected character `emotionImages`.

Inlay tokens are different. They point to files stored in Risu's inlay storage:

```text
{{inlay::id}}
{{inlayed::id}}
{{inlayeddata::id}}
```

Lua image APIs return these:

- `generateImage(id, prompt, negative)` returns `{{inlay::...}}`.
- `getCharacterImage(id)` and `getPersonaImage(id)` return `{{inlayed::...}}`.

For display, Risu replaces inlay tokens with image/video/audio HTML. For
low-level `LLM` / `axLLM` calls with multimodal extraction enabled, Risu scans
message text for inlay tokens, removes the token text, and attaches the file to
the subrequest.

Display asset tokens like `{{image::...}}` and `{{emotion::...}}` are not
multimodal attachments for Lua LLM calls. Use inlay tokens for that.

## Lorebooks

Risu has three lorebook scopes relevant to Lua:

- current chat local lore: `chat.localLore`
- selected character lore: `character.globalLore`
- enabled module lore: `module.lorebook`

`getLoreBooks(id, search)` does an exact lookup by entry `comment` across those
three scopes. It does not run normal key activation. Returned entry `content`
has already been CBS-parsed in the selected character context.

`upsertLocalLoreBook(id, name, content, options)` replaces any current-chat
local lorebook with the same `comment`, then pushes a new local entry. Options:

```lua
{
  alwaysActive = true,
  insertOrder = 100,
  key = "term1,term2",
  secondKey = "required term",
  regex = false,
}
```

If `secondKey` is non-empty, the new entry is marked selective.

`loadLoreBooks(id)` runs Risu's normal activated-lore selection and returns
prompt-ready `{ role, data }` entries. It requires low-level access because it
may tokenize and perform heavier prompt work. The raw host call accepts a
reserve token budget; the Lua helper uses Risu's default wrapper with no reserve
argument.

Lorebook content can include decorators recognized by Risu's lorebook loader,
such as `@@depth`, `@@scan_depth`, `@@recursive`, `@@unrecursive`,
`@@activate_only_after`, `@@probability`, `@@role`, `@@position`,
`@@inject_at`, and `@@inject_lore`.

## Embeddings, memory, and similarity

"Background embedding" is HTML. It is unrelated to vector embeddings.

Lua's `similarity(id, source, values)` is the vector-embedding helper. It:

1. Creates a temporary `HypaProcesser`.
2. Embeds the candidate `values` with the user's configured embedding model.
3. Embeds `source` as the query.
4. Returns the candidate strings sorted by similarity.

This requires low-level access. It uses the same embedding configuration as
Risu's Hypa memory features, including local Transformers.js models, OpenAI
embedding models, Voyage Context 3, or a custom OpenAI-compatible embedding
endpoint.

Risu's memory systems (`supaMemory`, `hypaV2`, `hypaV3`, `hanuraiMemory`) inject
their results during prompt assembly. Lua does not get a direct memory database
API, but `editRequest` can inspect or rewrite the final message array after
memory has been assembled.

## Modules

Enabled modules are merged from:

- global enabled module IDs: `db.enabledModules`
- current chat modules: `chat.modules`
- selected character modules: `character.modules`
- comma-separated integration IDs: `db.moduleIntergration`

Enabled modules can contribute lorebooks, regex scripts, triggers, assets,
prompt toggles, MCP URLs, and background embedding HTML.

Lua has no direct "list modules" host API. Still, modules affect Lua scripts in
these ways:

- Module Lua triggers run alongside character Lua triggers.
- Module regex scripts run in the same Regex Script pipeline.
- Module lorebooks are visible to `getLoreBooks` and normal lore activation.
- Module assets are visible to asset tokens.
- Module background embedding is appended behind the chat.
- Module prompt toggles are readable through `getGlobalVar(id, 'toggle_key')`.

## Good Lua cooperation patterns

### Marker plus display regex

Write simple, durable text from Lua:

```lua
function onOutput(id)
    setChat(id, -1, getChat(id, -1).data .. "\n[[status hp=" .. getChatVar(id, "hp") .. "]]")
end
```

Then let an `editdisplay` Regex Script turn it into HTML:

```text
in:  \[\[status hp=(\d+)\]\]
out: <div class="status-panel">HP: $1</div>
type: editdisplay
flag: g
ableFlag: true
```

The stored message stays plain and robust. The visible message gets a panel.

### Background CSS plus Lua state

Use Lua to set persistent background HTML once, then update chat variables:

```lua
function onStart(id)
    setBackgroundEmbedding(id, [[
<style>
.status-panel { padding: 0.5rem; border: 1px solid currentColor; }
</style>
]])
    setChatVar(id, "hp", getChatVar(id, "hp") == "null" and "100" or getChatVar(id, "hp"))
    reloadDisplay(id)
end
```

Use Regex Scripts or display HTML to read `{{getvar::hp}}`.

### Lorebook as per-chat configuration

Use local lorebooks when a script needs model-visible state that should survive
as part of the chat:

```lua
function SaveScene(id)
    upsertLocalLoreBook(id, "scene-state", "The room is locked.", {
        alwaysActive = true,
        insertOrder = 50,
    })
end
```

Use `getLoreBooks(id, "scene-state")` to read named entries back, and
`loadLoreBooks(id)` when you need the currently activated lore context.

### One-shot prompt directives from `onStart`

Because `onStart` runs after the submitted user message is stored but before
chat history is sent, it can prepend a one-shot directive to the latest message:

```lua
function onStart(id)
    local last = getChat(id, -1)
    if last and last.role == "user" then
        setChat(id, -1, "<AD>Describe the scene more slowly.</AD>\n\n" .. last.data)
    end
end
```

This is useful for queued director-style instructions, but it mutates stored
chat. If the directive should affect only the outgoing request and not the saved
history, use `listenEdit('editRequest', ...)` instead.

## Boundaries worth remembering

- `editDisplay` Lua can write chat variables but cannot mutate chat,
  character, background, or lorebook data.
- Lua cannot write global variables or prompt toggle values.
- Lua cannot directly list or edit Regex Scripts, enabled modules, presets, or
  additional assets.
- Lua can cooperate with those systems by writing chat variables, marker text,
  background HTML, local lorebooks, and inlay tokens.
- Asset tokens are display helpers; inlay tokens are the right bridge for
  multimodal Lua LLM calls.
- `similarity` uses vector embeddings; background embedding uses HTML.
