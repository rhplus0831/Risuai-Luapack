# Risu Lua API Reference

> Generated from `scriptings.ts` by `python -m luapack docs` — do not edit by hand.
> Concepts, gotchas, and how-to are in [lua-guide.md](./lua-guide.md).

Functions tagged _(await)_ return a promise; call `:await()` (the `LLM`/`axLLM`/`loadLoreBooks` helpers do this for you).

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
| `editDisplay` | `listenEdit('editDisplay', fn)` | text is rendered (read-only tier) | transformed text |
| `<custom>` | `function <name>(id)` | run with mode='<name>' | value (`false` stops sending) |

## Helpers

Provided by Risu's preamble. Prefer these over the raw `*Main` host calls — they handle JSON for you.

| Helper | What it does |
|--------|--------------|
| `LLM(id, prompt, useMultimodal, options)` | Run a sub-request against the main model (low-level). Awaitable. |
| `axLLM(id, prompt, useMultimodal, options)` | Run a sub-request against the auxiliary model (low-level). Awaitable. |
| `getCharacterImage(id)` | Inlay string for the character image. Awaitable. |
| `getChat(id, index)` | Get one chat message as a table `{role, data, time}` (0-based). |
| `getFullChat(id)` | Get the whole chat as an array of `{role, data, time}`. |
| `getLoreBooks(id, search)` | Find lorebook entries whose comment matches `search`. |
| `getPersonaImage(id)` | Inlay string for the persona image. Awaitable. |
| `getState(id, name)` | Read a JSON-decoded state value (chat var, `__`-prefixed). |
| `listenEdit(type, func)` | Register an edit-trigger handler (editRequest/Input/Output/Display). |
| `loadLoreBooks(id)` | Load activated lorebooks within a token budget (low-level). |
| `log(value)` | Print a value to the dev console (JSON-encoded). |
| `setFullChat(id, value)` | Replace the whole chat from an array of `{role, data}`. |
| `setState(id, name, value)` | Write a JSON-encoded state value (chat var, `__`-prefixed). |

## Host functions

Injected globals. Every call takes the access-key `id` as its first argument (see the guide). Grouped by permission tier.

### Always available

| Function | What it does |
|----------|--------------|
| `cbs(value)` | Expand a CBS `{{...}}` template string. |
| `getAuthorsNote(id)` | Author's note for the chat. |
| `getCharacterFirstMessage(id)` | Character's first message. |
| `getCharacterImageMain(id)` _(await)_ | Raw `getCharacterImage`. |
| `getCharacterLastMessage(id)` | Most recent character message. |
| `getChatLength(id)` | Number of messages. |
| `getChatMain(id, index)` | Raw `getChat` (returns a JSON string). |
| `getChatVar(id, key)` | Read a chat variable (string). |
| `getFullChatMain(id)` | Raw `getFullChat` (returns a JSON string). |
| `getGlobalVar(id, key)` | Read a global chat variable. |
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
| `addChat(id, role, value)` | Append a message (role 'user' or 'char'). |
| `alertConfirm(id, value)` _(await)_ | Ask a yes/no question. Awaitable. |
| `alertError(id, value)` | Show an error alert. |
| `alertInput(id, value)` _(await)_ | Prompt for text input. Awaitable. |
| `alertNormal(id, value)` | Show an info alert. |
| `alertSelect(id, value)` _(await)_ | Prompt to pick from options. Awaitable. |
| `cutChat(id, start, end)` | Keep only messages in [start, end). |
| `getBackgroundEmbedding(id)` | Character background HTML. |
| `getDescription(id)` | Character description. |
| `getTokens(id, value)` _(await)_ | Token count of a string. Awaitable. |
| `insertChat(id, index, role, value)` | Insert a message at an index. |
| `reloadChat(id, index)` | Trigger a re-render of one message. |
| `reloadDisplay(id)` | Trigger a display refresh. |
| `removeChat(id, index)` | Remove the message at an index. |
| `setBackgroundEmbedding(id, data)` | Set the character background HTML. |
| `setCharacterFirstMessage(id, data)` | Set the character's first message. |
| `setChat(id, index, value)` | Replace the text of the message at an index. |
| `setChatRole(id, index, value)` | Set the role of the message at an index. |
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
| `generateImage(id, value, negValue)` _(await)_ | Generate an image, returns an inlay (low-level). Awaitable. |
| `loadLoreBooksMain(id, reserve)` _(await)_ | Raw `loadLoreBooks` (returns a JSON string). |
| `request(id, url)` _(await)_ | HTTPS GET (≤120 chars, 5/min, low-level). Awaitable. |
| `similarity(id, source, value)` _(await)_ | Embedding similarity search (low-level). Awaitable. |
| `simpleLLM(id, prompt)` _(await)_ | One-shot model call (low-level). Awaitable. |
