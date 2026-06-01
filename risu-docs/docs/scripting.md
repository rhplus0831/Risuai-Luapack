# Scripting: CBS, regex scripts, triggers, Lua/Python, commands

Five content-authoring layers run inside the chat pipeline. Each has its own
syntax, lifecycle, and access scope.

| Layer | What it does | File |
|-------|--------------|------|
| **CBS** | `{{name::args}}` template variables | `src/ts/cbs.ts` |
| **Regex scripts** | Pattern-driven find/replace + flow control | `src/ts/process/scripts.ts` |
| **Triggers** | Event-driven if/then with V2 visual syntax | `src/ts/process/triggers.ts` |
| **Lua / Python** | Sandboxed scripting with throttled APIs | `src/ts/process/scriptings.ts` |
| **Slash commands** | `/cmd arg1 key=val` directives | `src/ts/process/command.ts` |

---

## 1. CBS — Callback System

`src/ts/cbs.ts`.

### Syntax

`{{name::arg1::arg2}}`. Names can be aliased; arguments are split on `::`.

### Dispatch

A CBS function has signature
`(str, matcherArg, args, vars) => { text, var } | string | null`. The
`matcherArg` carries `chatID`, `db`, `chara`, `cbsConditions`, `displaying`,
`role`, `runVar` (`cbs.ts:74-77`).

Registration:

- `registerCBS(arg)` (`:147`) — bulk registration once at startup.
- `registerFunction(name, fn, aliases, description)` — add a single function.

Activation is *pattern-based* via `{{…}}` matching; there is no explicit hook
list. CBS expansion is recursive: a function's output is itself parsed.

### Built-in surface

Identity: `{{char}}`, `{{user}}`, `{{personality}}`, `{{description}}`,
`{{scenario}}`, `{{exampleMessage}}`, `{{persona}}`, `{{lorebook}}`,
`{{userhistory}}`, `{{charhistory}}`, `{{jb}}`, `{{mainprompt}}`.

Math / logic: `{{calc}}`, `{{greater}}`, `{{less}}`, `{{and}}`, `{{or}}`,
`{{not}}`.

String / array: `{{split}}`, `{{join}}`, `{{replace}}`, `{{length}}`,
`{{arrayelement}}`, `{{dictelement}}`.

Variables: `{{getvar}}`, `{{setvar}}`, `{{tempvar}}`, `{{getglobalvar}}`.

The full list (~100 functions) is enumerated in `cbs.ts:117-1433` and
documented in-app via the **CBS Docs** playground page.

---

## 2. Regex scripts

`src/ts/process/scripts.ts`.

### Entry points

- `processScript(char, data, mode, cbsConditions)` — sync wrapper.
- `processScriptFull(char, data, mode, chatID, cbsConditions)` — full
  pipeline with caching (`:99-387`).
- `exportRegex()` / `importRegex()` — JSON import/export.
- `resetScriptCache()` — invalidate cache.

### Lifecycle

1. **Mode filter** (`:152`). A script only runs if `script.type === mode`.
   Modes: `editinput`, `editoutput`, `editprocess`, `editdisplay` (`:18`).
2. **Pattern matching.** Regex flags come from `script.flag` (`:157`).
3. **Action handling** (`:160-250`):
   - `@@emo` — trigger emotion image (`:184`).
   - `@@inject` — modify chat at chatID (`:207`).
   - `@@move_top` / `@@move_bottom` — reorder matched text (`:213`).
   - `@@repeat_back` — copy matched text from history (`:252`).
   - default — replace with `script.out`, applying CBS substitution
     (`:291`).
4. **Cache.** Hash key includes script conditions, mode, and CBS flags
   (`:71`).

---

## 3. Triggers

`src/ts/process/triggers.ts`.

### Type — `:20-26`

```ts
interface triggerscript {
  comment: string
  type: 'start' | 'manual' | 'output' | 'input' | 'display' | 'request'
  conditions: TriggerCondition[]
  effect: TriggerEffect[]
  lowLevelAccess: boolean
}
```

### Execution — `runTrigger(char, mode, arg)` `:1058-1514+`

1. **Conditions** (`:1238-1309`):
   - `var` / `chatindex` / `value` — compare with `=`, `!=`, `>`, `<`,
     `>=`, `<=`, `null`, `true`.
   - `exists` — recursive search in chat history (depth, strict/loose/regex).
2. **Effects** (`:1333-1410`):
   - **Safe subset** (`:985-1021`) — math, string ops, loops, conditions.
   - **Low-level only** (`:1461+`) — alerts, LLM calls, image gen, similarity
     search. Requires `lowLevelAccess: true` on the character.
   - **Display mode** restricts allowed effects further; **request mode**
     even more so.
3. **Effect types** — ~45 V1 + V2:
   - V1: `setvar`, `systemprompt`, `impersonate`, `command`, `cutchat`,
     `modifychat`, `showAlert`, `runLLM`, `checkSimilarity`.
   - V2 (indent-scoped visual): `v2SetVar`, `v2If`, `v2Loop`, `v2CutChat`,
     `v2GetArrayVar`, `v2Tokenize`, `v2CreateLorebook`, …
4. **Order.** V2 indent-based scoping; triggers run sequentially in
   character+module list order.

### When triggers fire

- `start` — when a chat begins.
- `manual` — explicit `/trigger name`.
- `input`, `output`, `display`, `request` — at the corresponding pipeline
  stage (see [processing-pipeline.md](./processing-pipeline.md)).

---

## 4. Lua / Python scripting

`src/ts/process/scriptings.ts`. The most powerful and most tightly-sandboxed
layer.

### Entry points

- `runScripted(code, arg)` (`:52-1145`) — execute Lua or Python.
- `runLuaEditTrigger()` (`:1371-1412`) — edit-mode hooks.
- `runLuaButtonTrigger()` (`:1414-1436`) — handle `risu-trigger` clicks.

### Lifecycle

1. **Engine creation** (`:75-104`). Lazy-init `LuaFactory`; create a
   per-mode persistent engine.
2. **API declaration** (`:105-442`). Functions are whitelisted via
   `declareAPI`:

   | Group | Examples |
   |-------|----------|
   | State | `getChatVar`, `setChatVar`, `getGlobalVar`, `getState` |
   | Chat | `getChatMain(id)`, `getFullChatMain(id)`, `setChat`, `removeChat` |
   | I/O | `alertNormal`, `alertInput`, `sleep(ms)`, `request(url)` (5 req/min, HTTPS only) |
   | LLM | `LLMMain(prompt, useMultimodal, opts)`, `axLLMMain`, `simpleLLM` |
   | Image | `generateImage`, `getCharacterImageMain`, `getPersonaImageMain` |
   | Lorebook | `getLoreBooksMain`, `upsertLocalLoreBook`, `loadLoreBooksMain` |

3. **Access control** (`:1036-1045`):
   - `ScriptingSafeIds` — can modify chat / vars.
   - `ScriptingEditDisplayIds` — read-only (edit modes).
   - `ScriptingLowLevelIds` — full I/O (requires character
     `lowLevelAccess: true`).
4. **Mode dispatch** (`:1050-1135`):
   `'input' | 'output' | 'start' | 'onButtonClick' | 'editRequest' |
   'editDisplay' | 'editInput' | 'editOutput'`.
   The script's `onInput(id)`, `onOutput(id)`, etc. function is called.

Python is provided via Pyodide (`process/pyworker.ts`).

---

## 5. Slash commands

`src/ts/process/command.ts:11-327`.

- `processMultiCommand(command)` — pipe split (`|`), chain results
  (`:11-39`).
- `processCommand(command, pipe)` — dispatch (`:42-302`).
- `commandParser()` — parse `/cmd arg1 key=val` (`:305-327`).

Built-ins:

- `/input text` → input dialog.
- `/send text` → add user message.
- `/sendas text` → add character message.
- `/setvar key=name value` → store variable.
- `/getvar key=name` → retrieve variable.
- `/trigger name` → invoke a trigger.
- `/echo text` → alert.
- `/buttons labels` → choice dialog.

---

## 6. Modules

`src/ts/process/modules.ts` is the loader for `RisuModule` (bundles of
lorebook + scripts + triggers + regex). Modules can ship lorebooks that activate
globally, and trigger packs that apply to every chat where the module is
enabled.

`src/ts/process/infunctions.ts` exposes the built-in functions that triggers
and Lua scripts can call.

---

## 7. Surface relationships

```
              (User message)
                    │
        ┌── input triggers / scripts (regex 'editinput')
        │
   prompt assembly  ──  CBS expansion runs throughout
        │
        ├── start triggers / scriptings 'start'
        ├── before_request triggers
        │
   request dispatch  →  AI provider
        │
        ├── output regex ('editoutput')
        ├── output triggers
        ├── output scriptings
        │
   display rendering
        │
        ├── display regex ('editdisplay')
        └── display triggers
```

---

## 8. Related docs

- [characters-and-lore.md](./characters-and-lore.md) — lorebook lives next to
  triggers/scripts in the character card.
- [processing-pipeline.md](./processing-pipeline.md) — when each hook fires.
- [plugins.md](./plugins.md) — V2/V3 plugins can register script handlers.
