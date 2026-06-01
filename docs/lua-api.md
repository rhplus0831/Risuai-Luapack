# Risu Lua API Reference

> API surface generated from `scriptings.ts` by `python -m luapack docs`; descriptions and entry-point summaries are curated — do not edit by hand.
> Concepts, gotchas, and how-to are in [lua-guide.md](./lua-guide.md).

Functions tagged _(await)_ return a promise; call `:await()` (the `LLM`/`axLLM`/`loadLoreBooks` helpers await and JSON-decode for you; image helpers await and return inlay strings).

## Entry points

Define the global / register the listener; Risu calls it per mode.

| Mode | You define | Fires when | Returns |
|------|-----------|-----------|---------|
| `start` | `function onStart(id)` | before the model request is sent | `false` stops sending |
| `input` | `function onInput(id)` | user input is submitted | `false` stops sending |
| `output` | `function onOutput(id)` | the model reply arrives | `false` stops sending |
| `onButtonClick` | `function onButtonClick(id, data)` | a chat button is clicked | value |
| `editRequest` | `listenEdit('editRequest', fn)` | the outgoing request is built | transformed message array |
| `editInput` | `listenEdit('editInput', fn)` | user input is processed | transformed text |
| `editOutput` | `listenEdit('editOutput', fn)` | the model reply is processed | transformed text |
| `editDisplay` | `listenEdit('editDisplay', fn)` | text is rendered (restricted edit-display tier) | transformed text |
| `<custom>` | `function <name>(id)` | run with mode='<name>' | value (`false` stops sending) |

Notes: `listenEdit` handlers are chained in registration order. `editDisplay` uses a restricted edit-display key: it can write chat vars, but cannot mutate chat or character data. Edit listeners never receive low-level access.

## Helpers

Provided by Risu's preamble. Prefer these over the raw `*Main` host calls when they handle JSON for you; `log`, `cbs`, and image helpers are exceptions that return or pass plain values.

| Helper | What it does |
|--------|--------------|
| `LLM(id, prompt, useMultimodal, options)` | Run a sub-request against the main model (low-level); roles accept `system`/`sys`, `user`, `assistant`/`bot`/`char`; optional multimodal extraction handles inlay tokens. |
| `axLLM(id, prompt, useMultimodal, options)` | Run a sub-request against the auxiliary model (low-level); same prompt/options shape as `LLM`. |
| `getCharacterImage(id)` | Return `{{inlayed::...}}` for the character image, or an empty string. Awaitable. |
| `getChat(id, index)` | Get one chat message as a table `{role, data, time}` (0-based; negative indexes work like JS `Array.at`). |
| `getFullChat(id)` | Get the whole chat as an array of `{role, data, time}`. |
| `getLoreBooks(id, search)` | Find local, character-global, and enabled-module lorebook entries whose `comment` exactly matches `search`; returned `content` is CBS-parsed. |
| `getPersonaImage(id)` | Return `{{inlayed::...}}` for the persona image, or an empty string. Awaitable. |
| `getState(id, name)` | Read a JSON-decoded state value (chat var, `__`-prefixed). |
| `listenEdit(type, func)` | Register a chained edit-trigger handler (editRequest/Input/Output/Display). |
| `loadLoreBooks(id)` | Load activated lorebooks and JSON-decode them (low-level, no reserve argument). |
| `log(value)` | Print a value to the dev console (JSON-encoded). |
| `setFullChat(id, value)` | Replace the whole chat from an array of `{role, data}`. |
| `setState(id, name, value)` | Write a JSON-encoded state value (chat var, `__`-prefixed). |

## Host functions

Injected globals. Most calls take the access-key `id` as their first argument (exceptions include `cbs` and `logMain`; see the guide). Grouped by permission tier.

### Always available

| Function | What it does |
|----------|--------------|
| `cbs(value)` | Expand a CBS `{{...}}` template string; variable-writing CBS does not run through this helper. |
| `getAuthorsNote(id)` | Author's note for the chat. |
| `getCharacterFirstMessage(id)` | Character's first message. |
| `getCharacterImageMain(id)` _(await)_ | Raw `getCharacterImage`. |
| `getCharacterLastMessage(id)` | Most recent character message. |
| `getChatLength(id)` | Number of messages. |
| `getChatMain(id, index)` | Raw `getChat` (returns a JSON string). |
| `getChatVar(id, key)` | Read a chat variable (string). |
| `getFullChatMain(id)` | Raw `getFullChat` (returns a JSON string). |
| `getGlobalVar(id, key)` | Read a global chat variable, including custom toggle values stored as `toggle_<key>`. |
| `getLoreBooksMain(id, search)` | Raw `getLoreBooks` (returns a JSON string). |
| `getName(id)` | Character name. |
| `getPersonaDescription(id)` | Persona (user) description, CBS-parsed. |
| `getPersonaImageMain(id)` _(await)_ | Raw `getPersonaImage`. |
| `getPersonaName(id)` | Persona (user) name. |
| `getUserLastMessage(id)` | Most recent user message. |
| `hash(id, value)` _(await)_ | Hash a string. Awaitable. |
| `logMain(value)` | Raw `log` (takes a JSON string). |

### Safe — modifies chat/character (blocked in edit-display tier)

| Function | What it does |
|----------|--------------|
| `addChat(id, role, value)` | Append a message (role `user`; any other role becomes `char`). |
| `alertConfirm(id, value)` _(await)_ | Ask a yes/no question. Awaitable. |
| `alertError(id, value)` | Show an error alert. |
| `alertInput(id, value)` _(await)_ | Prompt for text input. Awaitable. |
| `alertNormal(id, value)` | Show an info alert. |
| `alertSelect(id, value)` _(await)_ | Prompt to pick from options. Awaitable. |
| `cutChat(id, start, end)` | Keep only messages in `[start, end)`. |
| `getBackgroundEmbedding(id)` | Character background HTML. |
| `getDescription(id)` | Character description. |
| `getTokens(id, value)` _(await)_ | Token count of a string. Awaitable. |
| `insertChat(id, index, role, value)` | Insert a message with JS `splice` semantics. |
| `reloadChat(id, index)` | Trigger a re-render of one message. |
| `reloadDisplay(id)` | Trigger a display refresh. |
| `removeChat(id, index)` | Remove the message at an index with JS `splice` semantics. |
| `setBackgroundEmbedding(id, data)` | Set the character background HTML. |
| `setCharacterFirstMessage(id, data)` | Set the character's first message. |
| `setChat(id, index, value)` | Replace the text of the message at an index; negative indexes work like JS `Array.at`. |
| `setChatRole(id, index, value)` | Set role to `user`; any other value becomes `char`; negative indexes work like JS `Array.at`. |
| `setDescription(id, desc)` | Set the character description. |
| `setFullChatMain(id, value)` | Raw `setFullChat` (takes a JSON string). |
| `setName(id, name)` | Set the character name. |
| `sleep(id, time)` _(await)_ | Wait N milliseconds. Awaitable. |
| `stopChat(id)` | Stop the current send. |
| `upsertLocalLoreBook(id, name, content, options)` | Create/replace a local lorebook entry. |

### Safe or edit-display

| Function | What it does |
|----------|--------------|
| `setChatVar(id, key, value)` | Write a chat variable. |

### Low-level — requires `lowLevelAccess`

| Function | What it does |
|----------|--------------|
| `LLMMain(id, promptStr, useMultimodal, optionsStr)` _(await)_ | Raw `LLM` (JSON in, JSON out). |
| `axLLMMain(id, promptStr, useMultimodal, optionsStr)` _(await)_ | Raw `axLLM` (JSON in, JSON out). |
| `generateImage(id, value, negValue)` _(await)_ | Generate an image and return `{{inlay::...}}` (low-level). Awaitable. |
| `loadLoreBooksMain(id, reserve)` _(await)_ | Raw `loadLoreBooks` with a reserve budget (returns a JSON string). |
| `request(id, url)` _(await)_ | HTTPS GET (<=120 chars; current Risu code allows 6/min before 429; low-level); returns a JSON string. Awaitable. |
| `similarity(id, source, value)` _(await)_ | Embedding similarity search (low-level). Awaitable. |
| `simpleLLM(id, prompt)` _(await)_ | One-shot user-prompt model call (low-level); returns `{success, result}`. Awaitable. |
