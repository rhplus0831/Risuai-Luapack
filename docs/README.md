# Risu Lua & CBS reference

Source-grounded reference for authoring [RisuAI](https://github.com/kwaroran/RisuAI)
content with luapack. Every page is derived from the RisuAI source under
`Refer/Risuai` and is organized one item per file:

| Folder | What it documents |
|--------|-------------------|
| [`element/`](element/) | Shared data shapes and runtime concepts (the building blocks the APIs, hooks, and CBS functions reference). |
| [`hooks/`](hooks/) | The event/edit entry points Risu calls: when each fires, what it receives, what it returns, and which permissions it gets. |
| [`api/`](api/) | The Lua host functions (`declareAPI`) and the preamble helpers, grouped by permission tier. |
| [`cbs/`](cbs/) | The `{{...}}` Callback System functions, grouped by category. |

## How Risu runs your script

You paste one Lua string into Risu. Risu wraps it in a fixed preamble
(`luaCodeWrapper`) that defines the [preamble helpers](#preamble-helpers-wrap-a-raw-host-call)
and injects the [host functions](#host-apis), then runs your code so it can
define the global handlers Risu calls per mode (`onStart`, `onOutput`, edit
listeners, custom modes). Each host call takes an opaque
[access key `id`](element/access-key.md) as its first argument; that key carries
the [permission tier](element/access-key.md) of the current run.

## The chat pipeline (when hooks fire)

```
            (user submits text)
                   |
   onInput  --->  editInput regex + listenEdit('editInput')  --->  stored as the user message
                   |
   onStart        (user message is now stored; request not yet built)
                   |
   prompt assembly: description, persona, examples, lorebooks, author note, history, memory, jb
                   |
   editprocess regex (history text only; NO Lua equivalent)
                   |
   listenEdit('editRequest')   (rewrite the assembled OpenAI-style message array)
                   |
            request --> model
                   |
   editOutput regex + listenEdit('editOutput')   (transform the reply text)
                   |
   onOutput       (reply is now stored)
                   |
   display: asset parse -> listenEdit('editDisplay') -> CBS -> editdisplay regex -> inlay parse -> Markdown/HTML -> sanitize
```

- `onInput` runs before the user text is stored; use [`editInput`](hooks/editInput.md) to rewrite the stored text.
- `onStart` runs after the user message is stored, before the request is built; chat mutations here change the upcoming request.
- [`editRequest`](hooks/editRequest.md) sees the fully assembled outgoing array (after memory/lorebook assembly) and rewrites only the request, not stored chat.
- `onOutput` runs after the reply is stored; chat mutations here change the stored reply.
- Edit listeners run before the matching Regex Scripts. They never receive low-level access. [`editDisplay`](hooks/editDisplay.md) runs under the restricted edit-display tier (chat-var writes only).

### Hook timing matrix

| Entry point | When it runs | Receives | Return/effect | Stored chat | Model request | Permission tier |
|-------------|--------------|----------|---------------|-------------|---------------|-----------------|
| [`onInput`](hooks/onInput.md) | Immediately after user submit, before the new user message is stored. | `id` only. | Return `false` to stop the send; other returns are ignored. | Can mutate existing chat, but cannot read the submitted text as a stored message. | Indirect only, through chat mutations before request assembly. | Safe, plus low-level if the character has `lowLevelAccess`. |
| [`editInput`](hooks/editInput.md) | Before the submitted text is stored, after the `editInput` Regex Script stage in the send pipeline. | `id`, `value` string, `meta`. | Return the replacement user text. | Yes: returned text becomes the stored user message. | Yes: stored text is part of the upcoming request. | Safe; low-level is always forced off. |
| [`onStart`](hooks/onStart.md) | After the user message is stored, before prompt/history assembly. | `id` only. | Return `false` to stop the send; other returns are ignored. | Yes: can mutate chat and character state. | Yes: mutations affect the upcoming request. | Safe, plus low-level if the character has `lowLevelAccess`. |
| [`editRequest`](hooks/editRequest.md) | After prompt assembly and before the request is sent to the model. | `id`, OpenAI-style message array, `meta`. | Return the replacement request array. | No: stored chat is unchanged. | Yes: only the outgoing request changes. | Safe; low-level is always forced off. |
| [`editOutput`](hooks/editOutput.md) | On the model reply text before or while it is stored. | `id`, reply string, `meta`. | Return the replacement reply text. | Yes: returned text becomes the stored assistant message. | No: generation already happened. | Safe; low-level is always forced off. |
| [`onOutput`](hooks/onOutput.md) | After the assistant reply has been added to chat. | `id` only. | Return `false` to set `stopSending`; other returns are ignored. | Yes: can mutate the stored reply and other chat state. | No: request already completed. | Safe, plus low-level if the character has `lowLevelAccess`. |
| [`editDisplay`](hooks/editDisplay.md) | During display rendering. | `id`, display string, `meta` with index when available. | Return the replacement display string. | No: display only. | No: display only. | Restricted edit-display; chat-var writes only; never low-level. |
| [`onButtonClick`](hooks/onButtonClick.md) | When a rendered chat button with `risu-btn` is clicked. | `id`, `data` payload. | Handler side effects only. | Yes, if the handler mutates chat. | Only if the handler starts or influences later sends. | Safe, plus low-level if the trigger has `lowLevelAccess`. |
| [Custom modes](hooks/custom-modes.md) | When a manual trigger name is dispatched to a global function with that name. | `id` only. | Handler side effects only. | Yes, if the handler mutates chat. | Only if the handler starts or influences later sends. | Safe, plus low-level if the trigger has `lowLevelAccess`. |

## CBS syntax basics

- Form: `{{name::arg1::arg2}}`. Names are matched case-insensitively, and spaces, underscores, and hyphens are ignored (`{{trigger_id}}` == `{{triggerid}}`).
- Arguments split on `::`; a single `:` also works when there is no `::` in the call.
- Recursion: a function's output is itself parsed; expansion stops at 20 nested calls. Unknown functions are left in the text literally.
- Calculator shorthand: [`{{? 2 + 2 * 3}}`](cbs/blocks/calc-shorthand.md).
- Rewrites: `<user>`, `<char>`, and `<bot>` are rewritten to `{{user}}`/`{{char}}`/`{{bot}}`.
- Variable writes (`{{setvar}}`, `{{addvar}}`, `{{setdefaultvar}}`) only take effect when the parser runs with `runVar` enabled (so Lua's [`cbs`](api/cbs.md) helper does not run them).

---

## Elements

- [Chat message (`{role, data, time}`)](element/chat-message.md) — The shape Lua sees for a stored chat message, and how it differs from the OpenAI-style request message used by LLM prompts and `editRequest`.
- [Promise / `async()` (awaiting host calls)](element/promise-async.md) — Some host calls are asynchronous. Risu's Lua VM injects a `Promise` type and an `async()` wrapper so you can await them.
- [Background embedding (`backgroundHTML`)](element/background-embedding.md) — Persistent HTML rendered behind the chat. Risu's UI calls it "background embedding", but the character field Lua touches is `backgroundHTML`.
- [Chat variables (per-chat string state)](element/chat-variables.md) — Persistent per-chat string variables, stored on the current chat and read with a defined fallback chain.
- [Display HTML (sanitization & chat buttons)](element/display-html.md) — How Risu sanitizes the HTML it renders for chat / display output, and the custom attributes that turn markup into clickable triggers.
- [Global variables (read-only from Lua)](element/global-variables.md) — Cross-chat string variables stored in the database, readable from Lua but not writable.
- [Access key (`id`) and permission tiers](element/access-key.md) — Lua never receives a raw handle to Risu's database. Instead Risu generates a fresh opaque key (a UUID) for each script run, passes it to your handler as the first argument (conventionally named `id`), and registers that key in one or more permission sets for the duration of the run. Every host call takes the key as its first argument and checks it against those sets before doing anything privileged.
- [Asset display tokens (`{{img::}}`, `{{video::}}`, …)](element/asset-tokens.md) — Tokens the display parser expands into image/video/audio/background HTML when it renders chat text and background embedding. These are display helpers, not multimodal attachments — contrast inlay tokens.
- [Inlay tokens (`{{inlay::}}`, `{{inlayed::}}`, `{{inlayeddata::}}`)](element/inlay-tokens.md) — Tokens that reference files in Risu's inlay storage. They render as media for display and can be attached as multimodal input to LLM calls — unlike asset display tokens.
- [Lorebook entry](element/lorebook-entry.md) — The structured world-info entry Risu activates into prompts, and how Lua reads and writes it.
- [Modules](element/modules.md) — Reusable bundles of lore, regex, triggers, assets, toggles, MCP URLs, and background HTML. Lua has no API to list them, but enabled modules affect Lua indirectly.
- [Regex Script](element/regex-script.md) — User-defined find/replace rules that run in Risu's text pipeline. Lua cooperates with them by writing marker text; Lua itself has no `editprocess` listener.
- [Prompt toggles (`toggle_` globals)](element/prompt-toggles.md) — User-facing sidebar controls whose state is stored as `toggle_`-prefixed global variables, readable from Lua.

## Hooks

- [`onInput` (mode `input`)](hooks/onInput.md) — `onInput` runs at the very start of a send, the moment the user submits text.
- [`editInput` (mode `editInput`)](hooks/editInput.md) — `editInput` transforms the text the user just submitted before Risu stores it.
- [`onStart` (mode `start`)](hooks/onStart.md) — `onStart` runs once per send, at the start of request assembly. By this point the latest user message has already been stored in the chat, but Risu has not yet assembled the prompt (description, persona, lorebooks, history, …) or sent anything to the model. Mutating chat here therefore changes the upcoming request.
- [`editRequest` (mode `editRequest`)](hooks/editRequest.md) — `editRequest` lets you inspect or rewrite the final outgoing message array without touching stored chat.
- [`editOutput` (mode `editOutput`)](hooks/editOutput.md) — `editOutput` transforms the model reply text before it becomes the stored assistant message.
- [`onOutput` (mode `output`)](hooks/onOutput.md) — `onOutput` runs once the assistant reply is present in the chat.
- [`editDisplay` (mode `editDisplay`)](hooks/editDisplay.md) — `editDisplay` transforms what the user sees without changing the stored message.
- [`onButtonClick` (mode `onButtonClick`)](hooks/onButtonClick.md) — `onButtonClick` is the handler for buttons embedded in displayed messages or background HTML.
- [Custom / manual-trigger modes](hooks/custom-modes.md) — Any trigger name that is not a built-in mode is dispatched to a global function of that exact name.

## Host APIs

Lua-callable functions grouped by permission tier (see [Access key & permission tiers](element/access-key.md)). Each call takes the access-key `id` as its first argument unless the API page explicitly says otherwise.

### Always available

- [`cbs(value)`](api/cbs.md) — Expands a CBS `{{...}}` template string in the current character context.
- [`getAuthorsNote(id)`](api/getAuthorsNote.md) — Returns the current chat's author's note (`chat.note`).
- [`getCharacterFirstMessage(id)`](api/getCharacterFirstMessage.md) — Returns the selected character's first/greeting message (`char.firstMessage`).
- [`getCharacterImageMain(id)`](api/getCharacterImageMain.md) — The raw host call behind `getCharacterImage`. Loads the selected character's image into Risu's inlay store and returns an `{{inlayed::id}}` token, or `''`. The preamble helper `getCharacterImage` simply awaits this; prefer it unless you have a reason to call the raw form.
- [`getCharacterLastMessage(id)`](api/getCharacterLastMessage.md) — Returns the data of the most recent char-role message in the chat.
- [`getChatLength(id)`](api/getChatLength.md) — Returns the number of messages currently in the chat.
- [`getChatMain(id, index)`](api/getChatMain.md) — Returns one chat message as a JSON string. This is the raw host call; in Lua prefer the `getChat` preamble helper, which decodes the JSON for you.
- [`getChatVar(id, key)`](api/getChatVar.md) — Reads the current value of a persistent chat variable as a string.
- [`getFullChatMain(id)`](api/getFullChatMain.md) — Returns the whole chat as a JSON string: an array of message objects. This is the raw host call; in Lua prefer the `getFullChat` preamble helper, which decodes the JSON for you.
- [`getGlobalVar(id, key)`](api/getGlobalVar.md) — Reads a global chat variable shared across all chats.
- [`getLoreBooksMain(id, search)`](api/getLoreBooksMain.md) — The raw host call behind `getLoreBooks`: same exact `comment` lookup across the three lore scopes, but returns a JSON string rather than a decoded table. Prefer the `getLoreBooks` preamble helper, which decodes for you.
- [`getName(id)`](api/getName.md) — Returns the name of the currently selected character.
- [`getPersonaDescription(id)`](api/getPersonaDescription.md) — Returns the active persona prompt, CBS-parsed in the selected-character context.
- [`getPersonaImageMain(id)`](api/getPersonaImageMain.md) — The raw host call behind `getPersonaImage`. Loads the current persona (user) icon into Risu's inlay store and returns an `{{inlayed::id}}` token, or `''`. The preamble helper `getPersonaImage` simply awaits this; prefer it unless you have a reason to call the raw form.
- [`getPersonaName(id)`](api/getPersonaName.md) — Returns the active user/persona name (`getUserName()`).
- [`getUserLastMessage(id)`](api/getUserLastMessage.md) — Returns the data of the most recent user-role message in the chat.
- [`hash(id, value)`](api/hash.md) — Hashes a string using Risu's `hasher`.
- [`logMain(value)`](api/logMain.md) — Raw console logger: prints a parsed JSON string to the developer console.

### Safe (modifies chat/character; blocked in edit-display)

- [`addChat(id, role, value)`](api/addChat.md) — Appends a new message to the end of the current chat.
- [`alertConfirm(id, value)`](api/alertConfirm.md) — Asks the user a yes/no question and resolves to a boolean.
- [`alertError(id, value)`](api/alertError.md) — Shows an error alert to the user.
- [`alertInput(id, value)`](api/alertInput.md) — Prompts the user for a line of text and resolves to what they typed.
- [`alertNormal(id, value)`](api/alertNormal.md) — Shows an informational alert/toast to the user.
- [`alertSelect(id, value)`](api/alertSelect.md) — Presents the user with a list of choices and resolves to the one they pick.
- [`cutChat(id, start, end)`](api/cutChat.md) — Trims the chat to a contiguous range of messages.
- [`getBackgroundEmbedding(id)`](api/getBackgroundEmbedding.md) — Returns the selected character's background embedding HTML (`char.backgroundHTML`).
- [`getDescription(id)`](api/getDescription.md) — Returns the description (`desc`) of the currently selected character.
- [`getTokens(id, value)`](api/getTokens.md) — Returns the token count of a string using Risu's active tokenizer.
- [`insertChat(id, index, role, value)`](api/insertChat.md) — Inserts a new message at a given index, shifting later messages down.
- [`reloadChat(id, index)`](api/reloadChat.md) — Requests a re-render of a single chat message.
- [`reloadDisplay(id)`](api/reloadDisplay.md) — Requests a refresh of the whole chat display / GUI.
- [`removeChat(id, index)`](api/removeChat.md) — Removes a single message from the chat.
- [`setBackgroundEmbedding(id, data)`](api/setBackgroundEmbedding.md) — Sets the selected character's background embedding HTML (`char.backgroundHTML`).
- [`setCharacterFirstMessage(id, data)`](api/setCharacterFirstMessage.md) — Sets the selected character's first/greeting message (`char.firstMessage`).
- [`setChat(id, index, value)`](api/setChat.md) — Replaces the text of the message at a given index.
- [`setChatRole(id, index, value)`](api/setChatRole.md) — Changes the role of the message at a given index.
- [`setDescription(id, desc)`](api/setDescription.md) — Sets the description (`desc`) of the currently selected character.
- [`setFullChatMain(id, value)`](api/setFullChatMain.md) — Replaces the entire chat message array from a JSON string. This is the raw host call; in Lua prefer the `setFullChat` preamble helper, which JSON-encodes for you.
- [`setName(id, name)`](api/setName.md) — Sets the name of the currently selected character.
- [`sleep(id, time)`](api/sleep.md) — Pauses the handler for a given number of milliseconds.
- [`stopChat(id)`](api/stopChat.md) — Halts the current send by setting the run's `stopSending` flag.
- [`upsertLocalLoreBook(id, name, content, options)`](api/upsertLocalLoreBook.md) — Creates or replaces a current-chat local lorebook entry, keyed by its `comment` (`name`). Any existing chat-local entry with the same `comment` is removed first, then a fresh entry is pushed. Only chat-local lore is writable from Lua — there is no API to edit character-global or module lore.

### Safe or edit-display

- [`setChatVar(id, key, value)`](api/setChatVar.md) — Writes a persistent chat variable.

### Low-level (requires `lowLevelAccess`)

- [`axLLMMain(id, promptStr, useMultimodal, optionsStr)`](api/axLLMMain.md) — The raw auxiliary-model sub-request: JSON string in, JSON string out. Routes to the `'otherAx'` (auxiliary) model. Behaves exactly like `LLMMain` except for the target model. Prefer the `axLLM` preamble helper, which handles JSON for you.
- [`generateImage(id, value, negValue)`](api/generateImage.md) — Generates an AI image from a prompt (and optional negative prompt), stores it in Risu's inlay store, and returns an `{{inlay::id}}` token you can drop into chat text or feed back into a multimodal LLM call.
- [`LLMMain(id, promptStr, useMultimodal, optionsStr)`](api/LLMMain.md) — The raw main-model sub-request: JSON string in, JSON string out. Routes to the `'model'` (main) model. Prefer the `LLM` preamble helper, which JSON-encodes the prompt/options and JSON-decodes the reply for you. Call this directly only if you need to control the JSON yourself.
- [`loadLoreBooksMain(id, reserve)`](api/loadLoreBooksMain.md) — The raw activated-lore loader behind `loadLoreBooks`. Runs Risu's real lore activation and returns a JSON array of prompt-ready entries, honoring a caller-supplied `reserve` token budget. Prefer the `loadLoreBooks` preamble helper, which awaits and decodes for you (but passes no reserve).
- [`request(id, url)`](api/request.md) — Performs an HTTPS GET request and returns the response as a JSON string. Heavily restricted: HTTPS only, short URLs only, rate-limited, and a few hosts are blocked outright.
- [`similarity(id, source, value)`](api/similarity.md) — Embedding-based similarity search. The candidate strings in `value` are embedded with the configured embedding model (via `HypaProcesser`), then ranked against the embedded `source` query. Returns the candidates sorted by similarity to `source`.
- [`simpleLLM(id, prompt)`](api/simpleLLM.md) — A one-shot main-model call: pass a single user-message string, get back the model's reply. Unlike `LLM`/`LLMMain`, there is no role array and no JSON encoding — `prompt` becomes one `{ role = 'user', content = prompt }` message. There is no preamble helper; this host call returns a Lua table directly (it does not return a JSON string).

### Preamble helpers (wrap a raw host call)

- [`axLLM(id, prompt, useMultimodal, options)`](api/axLLM.md) — Runs a sub-request against the auxiliary model and returns the decoded result. Identical in shape to `LLM` but routes to the auxiliary model (`'otherAx'`) instead of the main one. This is the high-level wrapper over the raw `axLLMMain`: it JSON-encodes the prompt/options, awaits, and JSON-decodes the reply.
- [`getCharacterImage(id)`](api/getCharacterImage.md) — Returns the selected character's image as an `{{inlayed::id}}` token, or an empty string if there is no usable image. This is a thin preamble wrapper that just awaits the raw `getCharacterImageMain`.
- [`getChat(id, index)`](api/getChat.md) — Returns one chat message as a decoded Lua table `{role, data, time}`.
- [`getFullChat(id)`](api/getFullChat.md) — Returns the whole chat as a decoded Lua array of `{role, data, time}` tables.
- [`getLoreBooks(id, search)`](api/getLoreBooks.md) — Finds lorebook entries whose `comment` exactly matches `search`, across all three lore scopes, and returns them as a Lua array. This is the preamble wrapper over `getLoreBooksMain`: it calls the raw function and `json.decode`s the result for you.
- [`getPersonaImage(id)`](api/getPersonaImage.md) — Returns the current persona (user) icon as an `{{inlayed::id}}` token, or an empty string if there is no usable icon. A thin preamble wrapper that awaits the raw `getPersonaImageMain`.
- [`getState(id, name)`](api/getState.md) — Reads a JSON-decoded "state" value stored in a `__`-prefixed chat variable.
- [`listenEdit(type, func)`](api/listenEdit.md) — Registers a chained edit-trigger handler for one of the four edit hooks.
- [`LLM(id, prompt, useMultimodal, options)`](api/LLM.md) — Runs a sub-request against the chat's main model and returns the decoded result. This is the high-level convenience wrapper over the raw `LLMMain`: it JSON-encodes the prompt and options for you, awaits the host call, and JSON-decodes the `{ success, result }` reply back into a Lua table.
- [`loadLoreBooks(id)`](api/loadLoreBooks.md) — Runs Risu's real activated-lore selection and returns the prompt-ready entries, decoded into a Lua array. Unlike `getLoreBooks` (an exact `comment` lookup), this performs the actual activation Risu would use when building a request. It is the preamble wrapper over the raw `loadLoreBooksMain`: it awaits the host call and `json.decode`s the result. The helper passes no reserve token budget.
- [`log(value)`](api/log.md) — Logs any Lua value to the developer console by JSON-encoding it.
- [`setFullChat(id, value)`](api/setFullChat.md) — Replaces the entire chat from a Lua array of `{role, data}` tables.
- [`setState(id, name, value)`](api/setState.md) — Writes a JSON-encoded "state" value into a `__`-prefixed chat variable.

## CBS functions

The `{{...}}` Callback System, grouped by category.

### Identity & character

- [`{{char}}`](cbs/identity/char.md) — Returns the display name (or nickname) of the current character/bot.
- [`{{description}}`](cbs/identity/description.md) — Returns the current character's description field.
- [`{{exampledialogue}}`](cbs/identity/exampledialogue.md) — Returns the current character's example dialogue/messages.
- [`{{personality}}`](cbs/identity/personality.md) — Returns the current character's personality field.
- [`{{scenario}}`](cbs/identity/scenario.md) — Returns the current character's scenario field.
- [`{{trigger_id}}`](cbs/identity/trigger-id.md) — Returns the `risu-id` of the element that fired the current manual trigger.
- [`{{user}}`](cbs/identity/user.md) — Returns the active user/persona name.

### Prompts & notes

- [`{{authornote}}`](cbs/prompts/authornote.md) — Returns the chat's author's note.
- [`{{globalnote}}`](cbs/prompts/globalnote.md) — Returns the global note (also called the system note).
- [`{{jb}}`](cbs/prompts/jb.md) — Returns the jailbreak prompt text.
- [`{{mainprompt}}`](cbs/prompts/mainprompt.md) — Returns the main system prompt.
- [`{{persona}}`](cbs/prompts/persona.md) — Returns the user persona prompt text.

### Chat history

- [`{{charhistory}}`](cbs/history/charhistory.md) — Returns all character messages as a JSON array.
- [`{{history}}` / `{{history::role}}`](cbs/history/history.md) — Returns the chat history as a JSON array.
- [`{{lastmessage}}`](cbs/history/lastmessage.md) — Returns the content of the last message in the chat, regardless of role.
- [`{{lastmessageid}}`](cbs/history/lastmessageid.md) — Returns the 0-based index of the last message in the chat.
- [`{{lorebook}}`](cbs/history/lorebook.md) — Returns all active lorebook entries as a JSON array.
- [`{{previouscharchat}}`](cbs/history/previouscharchat.md) — Returns the most recent character message, falling back to the greeting.
- [`{{previouschatlog::index}}`](cbs/history/previouschatlog.md) — Returns the content of the message at a given chat index.
- [`{{previoususerchat}}`](cbs/history/previoususerchat.md) — Returns the most recent user message.
- [`{{userhistory}}`](cbs/history/userhistory.md) — Returns all user messages as a JSON array.

### Variables

- [`{{addvar::name::amount}}`](cbs/variables/addvar.md) — Adds a number to a persistent chat variable.
- [`{{getglobalvar::name}}`](cbs/variables/getglobalvar.md) — Reads a global chat variable, shared across all chats and characters.
- [`{{getvar::name}}`](cbs/variables/getvar.md) — Returns the value of a persistent chat variable.
- [`{{return::value}}`](cbs/variables/return.md) — Sets the parser's return value and forces it to stop.
- [`{{setdefaultvar::name::value}}`](cbs/variables/setdefaultvar.md) — Sets a chat variable only if it is not already set.
- [`{{settempvar::name::value}}`](cbs/variables/settempvar.md) — Sets a temporary variable that lives only during the current parse.
- [`{{setvar::name::value}}`](cbs/variables/setvar.md) — Sets a persistent chat variable.
- [`{{tempvar::name}}`](cbs/variables/tempvar.md) — Reads a temporary variable that lives only during the current parse.

### Chat context & flags

- [`{{blank}}`](cbs/context/blank.md) — Returns an empty string.
- [`{{chatindex}}`](cbs/context/chatindex.md) — Returns the index of the message currently being processed.
- [`{{firstmsgindex}}`](cbs/context/firstmsgindex.md) — Returns the index of the selected first message / alternate greeting.
- [`{{isfirstmsg}}`](cbs/context/isfirstmsg.md) — Returns whether the template is being expanded in a first-message context.
- [`{{jbtoggled}}`](cbs/context/jbtoggled.md) — Returns whether the jailbreak prompt is enabled.
- [`{{maxcontext}}`](cbs/context/maxcontext.md) — Returns the configured maximum context length.
- [`{{role}}`](cbs/context/role.md) — Returns the role of the current message.

### Model & metadata

- [`{{axmodel}}`](cbs/model/axmodel.md) — Returns the id of the auxiliary / sub model.
- [`{{metadata::key}}`](cbs/model/metadata.md) — Returns a piece of system / application metadata selected by `key`.
- [`{{model}}`](cbs/model/model.md) — Returns the id of the currently selected AI model.
- [`{{prefillsupported}}`](cbs/model/prefillsupported.md) — Returns whether the current model supports response prefill.

### Date & time

- [`{{date::format::timestamp}}`](cbs/datetime/date.md) — Formats a date/time with a custom format string.
- [`{{idleduration}}`](cbs/datetime/idleduration.md) — Returns the time elapsed since the last message in the chat (HH:MM:SS).
- [`{{isodate}}`](cbs/datetime/isodate.md) — Returns the current UTC date (YYYY-MM-DD).
- [`{{isotime}}`](cbs/datetime/isotime.md) — Returns the current UTC time (HH:MM:SS).
- [`{{messagedate}}`](cbs/datetime/messagedate.md) — Returns the local date on which the current message was sent.
- [`{{messageidleduration}}`](cbs/datetime/messageidleduration.md) — Returns the elapsed time between the current user message and the previous user message (HH:MM:SS).
- [`{{messagetime}}`](cbs/datetime/messagetime.md) — Returns the local time at which the current message was sent (HH:MM:SS).
- [`{{messageunixtimearray}}`](cbs/datetime/messageunixtimearray.md) — Returns every message timestamp in the current chat as a JSON array.
- [`{{time}}`](cbs/datetime/time.md) — Returns the current local time.
- [`{{unixtime}}`](cbs/datetime/unixtime.md) — Returns the current unix time in seconds.

### Math

- [`{{abs::n}}`](cbs/math/abs.md) — Returns the absolute value of a number.
- [`{{calc::expr}}`](cbs/math/calc.md) — Evaluates a math expression and returns the result.
- [`{{ceil::n}}`](cbs/math/ceil.md) — Rounds a number up to the nearest integer.
- [`{{fixnum::n::decimals}}`](cbs/math/fixnum.md) — Formats a number to a fixed number of decimal places.
- [`{{floor::n}}`](cbs/math/floor.md) — Rounds a number down to the nearest integer.
- [`{{pow::base::exp}}`](cbs/math/pow.md) — Raises a number to a power.
- [`{{remaind::a::b}}`](cbs/math/remaind.md) — Returns the remainder of dividing one number by another (modulo).
- [`{{round::n}}`](cbs/math/round.md) — Rounds a number to the nearest integer.

### Comparison & logic

- [`{{all::...}}`](cbs/logic/all.md) — Logical AND across many values.
- [`{{and::a::b}}`](cbs/logic/and.md) — Logical AND of two boolean values.
- [`{{any::...}}`](cbs/logic/any.md) — Logical OR across many values.
- [`{{equal::a::b}}`](cbs/logic/equal.md) — Tests two values for exact string equality.
- [`{{greater::a::b}}`](cbs/logic/greater.md) — Numeric "greater than" comparison.
- [`{{greaterequal::a::b}}`](cbs/logic/greaterequal.md) — Numeric "greater than or equal to" comparison.
- [`{{less::a::b}}`](cbs/logic/less.md) — Numeric "less than" comparison.
- [`{{lessequal::a::b}}`](cbs/logic/lessequal.md) — Numeric "less than or equal to" comparison.
- [`{{not::a}}`](cbs/logic/not.md) — Logical NOT of a boolean value.
- [`{{notequal::a::b}}`](cbs/logic/notequal.md) — Tests two values for string inequality.
- [`{{or::a::b}}`](cbs/logic/or.md) — Logical OR of two boolean values.

### String

- [`{{capitalize::s}}`](cbs/string/capitalize.md) — Capitalizes the first character of a string.
- [`{{contains::s::sub}}`](cbs/string/contains.md) — Tests whether a substring appears anywhere within a string.
- [`{{endswith::s::sub}}`](cbs/string/endswith.md) — Tests whether a string ends with a given substring.
- [`{{length::s}}`](cbs/string/length.md) — Returns the character count of a string.
- [`{{lower::s}}`](cbs/string/lower.md) — Converts a string to lowercase.
- [`{{replace::s::find::to}}`](cbs/string/replace.md) — Replaces every occurrence of a substring with another string.
- [`{{reverse::s}}`](cbs/string/reverse.md) — Reverses the input string.
- [`{{split::s::delim}}`](cbs/string/split.md) — Splits a string on a delimiter and returns the parts as a JSON array.
- [`{{startswith::s::sub}}`](cbs/string/startswith.md) — Tests whether a string begins with a given substring.
- [`{{tonumber::s}}`](cbs/string/tonumber.md) — Strips everything except digits and decimal points from a string.
- [`{{trim::s}}`](cbs/string/trim.md) — Strips leading and trailing whitespace from a string.
- [`{{upper::s}}`](cbs/string/upper.md) — Converts a string to uppercase.

### Array

- [`{{arrayassert::array::index::value}}`](cbs/array/arrayassert.md) — Ensures a given index exists in a JSON array, extending it if necessary.
- [`{{arrayelement::array::index}}`](cbs/array/arrayelement.md) — Returns the element at a given index of a JSON array.
- [`{{arraylength::array}}`](cbs/array/arraylength.md) — Returns the number of elements in a JSON array.
- [`{{arraypop::array}}`](cbs/array/arraypop.md) — Returns a JSON array with its last element removed.
- [`{{arraypush::array::element}}`](cbs/array/arraypush.md) — Returns a JSON array with one element appended to the end.
- [`{{arrayshift::array}}`](cbs/array/arrayshift.md) — Returns a JSON array with its first element removed.
- [`{{arraysplice::array::index::deleteCount::element}}`](cbs/array/arraysplice.md) — Removes and/or inserts elements at an index and returns the modified array.
- [`{{join::array::sep}}`](cbs/array/join.md) — Joins the elements of a JSON array into one string with a separator.
- [`{{makearray::a::b::...}}`](cbs/array/makearray.md) — Builds a JSON array from the supplied arguments.
- [`{{range::spec}}`](cbs/array/range.md) — Generates a JSON array of a numeric sequence.
- [`{{spread::array}}`](cbs/array/spread.md) — Joins a JSON array with `::` so it can be spread into another CBS call's arguments.

### Object / dictionary

- [`{{dictelement::obj::key}}`](cbs/dict/dictelement.md) — Reads a single value out of a JSON object by key.
- [`{{element::json::key1::key2::...}}`](cbs/dict/element.md) — Walks a path of keys/indices into a nested JSON value and returns what it finds.
- [`{{filter::array::type}}`](cbs/dict/filter.md) — Filters a JSON array, removing empty and/or duplicate entries.
- [`{{makedict::k=v::k2=v2::...}}`](cbs/dict/makedict.md) — Builds a JSON object from `key=value` arguments.
- [`{{objectassert::obj::key::value}}`](cbs/dict/objectassert.md) — Sets a default on a JSON object: writes the key only if it is not already present, then returns the object.

### Aggregation

- [`{{average::...}}`](cbs/aggregate/average.md) — Returns the arithmetic mean of a set of numbers.
- [`{{max::...}}`](cbs/aggregate/max.md) — Returns the largest of a set of numbers.
- [`{{min::...}}`](cbs/aggregate/min.md) — Returns the smallest of a set of numbers.
- [`{{sum::...}}`](cbs/aggregate/sum.md) — Adds up a set of numbers.

### Random & dice

- [`{{dice::XdY}}`](cbs/random/dice.md) — Rolls dice in `XdY` notation and returns the sum.
- [`{{hash::s}}`](cbs/random/hash.md) — Turns a string into a deterministic ~7-digit number.
- [`{{pick::...}}`](cbs/random/pick.md) — Like `{{random}}`, but the choice is hash-stable: it stays the same across re-renders of the same message.
- [`{{randint::min::max}}`](cbs/random/randint.md) — Returns a random integer in an inclusive range.
- [`{{random::...}}`](cbs/random/random.md) — Returns a random number, or a random element chosen from its arguments.
- [`{{roll::XdY}}`](cbs/random/roll.md) — Rolls dice (true random) with sensible defaults and returns the sum.
- [`{{rollp::XdY}}`](cbs/random/rollp.md) — Like `{{roll}}`, but hash-stable: the same message rolls the same result across re-renders.

### Encoding & cipher

- [`{{crypt::s::shift}}`](cbs/encoding/crypt.md) — A Caesar-style shift cipher over UTF-16 code units; with the default shift it is its own inverse.
- [`{{fromhex::hex}}`](cbs/encoding/fromhex.md) — Converts a hexadecimal string to its decimal value.
- [`{{tohex::num}}`](cbs/encoding/tohex.md) — Converts a decimal number to its hexadecimal string.
- [`{{u::hex}}`](cbs/encoding/u.md) — Returns the character for a hexadecimal code unit.
- [`{{ue::hex}}`](cbs/encoding/ue.md) — Returns the character for a hexadecimal code unit. Despite the "encode" name, its behavior is identical to `{{u}}` (a *decode*).
- [`{{unicodedecode::codepoint}}`](cbs/encoding/unicodedecode.md) — Returns the character for a decimal code unit.
- [`{{unicodeencode::s::index}}`](cbs/encoding/unicodeencode.md) — Returns the UTF-16 code unit of a character in a string.
- [`{{xor::s}}`](cbs/encoding/xor.md) — Obfuscates a string by XOR-ing each byte with `0xFF` and base64-encoding the result.
- [`{{xordecrypt::b64}}`](cbs/encoding/xordecrypt.md) — Reverses `{{xor}}`: base64-decodes, then XORs each byte with `0xFF`.

### Assets & media tokens

- [`{{asset::name}}`](cbs/assets/asset.md) — Renders a character/module asset as an image or a video, chosen by file extension.
- [`{{assetlist}}`](cbs/assets/assetlist.md) — Returns a JSON array of the current character's additional asset names.
- [`{{audio::name}}`](cbs/assets/audio.md) — Renders an audio player for a named asset.
- [`{{bg::name}}`](cbs/assets/bg.md) — Renders a full-size background div from a named asset — only in background mode.
- [`{{bgm::name}}`](cbs/assets/bgm.md) — Emits a hidden background-music control element.
- [`{{button::text::trigger}}`](cbs/assets/button.md) — Emits an HTML button that runs a manual trigger when clicked.
- [`{{chardisplayasset}}`](cbs/assets/chardisplayasset.md) — Returns a JSON array of the character's display asset names, filtered by the prebuilt-asset exclusion settings.
- [`{{emotion::name}}`](cbs/assets/emotion.md) — Renders an emotion image for the current character.
- [`{{emotionlist}}`](cbs/assets/emotionlist.md) — Returns a JSON array of the current character's emotion image names.
- [`{{file::name::base64}}`](cbs/assets/file.md) — Renders a filename chip in display mode, or decodes embedded base64 content otherwise.
- [`{{image::name}}`](cbs/assets/image.md) — Renders a framed image block.
- [`{{img::name}}`](cbs/assets/img.md) — Renders a bare inline image.
- [`{{inlay::id}}`](cbs/assets/inlay.md) — Renders an inlay-store asset by id, unstyled. Display only.
- [`{{inlayed::id}}`](cbs/assets/inlayed.md) — Renders an inlay-store asset by id, styled. Display only.
- [`{{inlayeddata::id}}`](cbs/assets/inlayeddata.md) — Renders an inlay-store asset by id, styled — and is included in the model request.
- [`{{moduleassetlist::namespace}}`](cbs/assets/moduleassetlist.md) — Returns a JSON array of a module's asset names.
- [`{{path::name}}`](cbs/assets/path.md) — Expands to the bare URL/path of a named asset (no HTML tag).
- [`{{raw::name}}`](cbs/assets/raw.md) — Expands to the bare URL/path of a named asset (no HTML tag).
- [`{{risu::size}}`](cbs/assets/risu.md) — Emits the Risu logo as an `<img>`.
- [`{{source::char}}` / `{{source::user}}`](cbs/assets/source.md) — Expands to the character or user profile image URL/path (bare, no HTML tag).
- [`{{video::name}}`](cbs/assets/video.md) — Renders a video player with controls.
- [`{{video-img::name}}`](cbs/assets/video-img.md) — Renders a muted, looping video — background-style, no controls.

### Formatting & display

- [`{{bkspc}}`](cbs/format/bkspc.md) — Removes the last word from the output produced so far.
- [`{{br}}`](cbs/format/br.md) — Emits a single literal newline character.
- [`{{cbr::n}}`](cbs/format/cbr.md) — Emits the escaped two-character sequence `\n`, optionally repeated.
- [`{{codeblock::code}}`](cbs/format/codeblock.md) — Renders text as a fenced code block, optionally with a language for syntax highlighting.
- [`{{comment::text}}`](cbs/format/comment.md) — Renders a visible, styled comment block.
- [`{{declare::name}}`](cbs/format/declare.md) — Sets a parser flag that other CBS behavior can read.
- [`{{erase}}`](cbs/format/erase.md) — Removes the last sentence from the output produced so far.
- [escaped literal characters](cbs/format/escaped-characters.md) — A family of zero-argument CBS functions that emit characters which *display* as `{`, `}`, `{{`, `}}`, `(`, `)`, `<`, `>`, `:`, or `;` but are not re-parsed as CBS / HTML syntax.
- [`{{hiddenkey::keys}}`](cbs/format/hiddenkey.md) — Marks lorebook activation keys that never reach the model.
- [`{{iserror::s}}`](cbs/format/iserror.md) — Tests whether a string looks like an error message.
- [`{{ruby::text::ruby}}`](cbs/format/ruby.md) — Renders ruby text (furigana) as HTML.
- [`{{tex::latex}}`](cbs/format/tex.md) — Wraps an expression as display-mode LaTeX/KaTeX math.

### Blocks & control flow

- [`{{? expression}}`](cbs/blocks/calc-shorthand.md) — Inline calculator: evaluates a math expression and returns the result.
- [`{{:else}}`](cbs/blocks/else.md) — The else clause inside a `{{#when}}` block.
- [`{{// comment}}`](cbs/blocks/comment-block.md) — A hidden comment whose content is removed entirely.
- [`{{#each ARRAY as V}} ... {{/each}}`](cbs/blocks/each.md) — Iterates over a JSON array, rendering the body once per element. The current element is read with `{{slot::V}}`.
- [`{{#escape}} ... {{/escape}}`](cbs/blocks/escape.md) — Escapes braces and parentheses in its body, treating the content as literal text.
- [`{{#if cond}} ... {{/if}}`](cbs/blocks/if.md) — Legacy conditional block. Deprecated — use `{{#when}}` instead.
- [`{{#if_pure cond}} ... {{/if_pure}}`](cbs/blocks/if-pure.md) — Legacy conditional that preserves whitespace. Deprecated — use `{{#when::keep::cond}}` instead.
- [`{{#pure}} ... {{/pure}}`](cbs/blocks/pure.md) — Legacy raw block: renders its contents without CBS processing. Deprecated — use `{{#puredisplay}}` instead.
- [`{{#puredisplay}} ... {{/puredisplay}}`](cbs/blocks/puredisplay.md) — Renders content without CBS processing, escaping the braces so a later pass cannot re-parse them.
- [`{{#when ...}} ... {{/when}}`](cbs/blocks/when.md) — The current conditional block: renders its body only when the condition is truthy. Replaces the deprecated `{{#if}}`.
- [`{{position::name}}`](cbs/blocks/position.md) — Declares a named position that lorebook `@@position` injection can target.
- [`{{slot::name}}`](cbs/blocks/slot.md) — The current loop/block slot value, used inside `{{#each}}`.

### Modules

- [`{{moduleenabled::namespace}}`](cbs/modules/moduleenabled.md) — Tests whether a module is currently enabled.

---

These pages are hand-authored and grounded in `Refer/Risuai` (the source of truth). When Risu's Lua API, CBS, or hooks change, update the matching page and this index. See [`../AGENTS.md`](../AGENTS.md) for repo conventions.
