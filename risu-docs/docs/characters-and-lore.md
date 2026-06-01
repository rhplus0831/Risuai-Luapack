# Character cards, lorebook, personas

The content layer: how characters are imported and exported, how world-info
("lorebook") is matched into a prompt, and how user personas work.

---

## 1. Character cards

`src/ts/characterCards.ts` handles five interchange formats. `src/ts/pngChunk.ts`
provides the PNG metadata primitives.

### Supported formats

| Extension | Format | Detail |
|-----------|--------|--------|
| `.png` (chara) | chara_card_v2 | Base64 JSON in a `chara` PNG tEXt chunk (`characterCards.ts:176-308`). |
| `.png` (ccv3) | chara_card_v3 | JSON in a `ccv3` PNG tEXt chunk with separate asset chunks (`:306-312`). |
| `.charx` (or `.jpg` wrapper) | CharX | ZIP + PNG + module data (`:80-162`). |
| `.json` | Direct export | Raw character JSON. |
| `.rcc` | Encrypted card | AES-encrypted with hash verification (`:315-365`). |

### Import path — `importCharacterCardSpec()` (`:716-1025`)

1. Parse the incoming file by extension.
2. Extract PNG metadata via `PngChunk.read(buf, ['chara', 'ccv3'])` or the
   streaming `PngChunk.readGenerator(buf)`.
3. Load any `chara-ext-asset_*` chunks as assets (emotion images, voice files,
   etc.).
4. Convert to the internal `character` shape — same shape used by `db.characters`
   (`storage/database.svelte.ts:1304-1458`).

### Export path — `exportCharacterCard()` and friends (`:1234-1500`)

1. `createBaseV2()` (`:1136-1231`) — assemble V2 card JSON.
2. `createBaseV3()` (implied around `:1326`) — V3 with asset metadata.
3. Embed emotions / assets / VITS voice files as base64 in PNG chunks (or
   ZIP entries for CharX).
4. Write via `PngChunk.write()` or `CharXWriter`.

### PNG metadata — `src/ts/pngChunk.ts`

- `PngChunk.read(data, names)` (`:94-129`) — parse tEXt chunks matching the
  requested names.
- `PngChunk.readGenerator(data)` (`:131-220`) — async iterator over chunks.
- `PngChunk.write(data, chunks)` (`:246-322`) — inject tEXt with CRC32.

### Encryption — `.rcc`

`characterCards.ts:315-365`. AES with a per-card key; integrity check via
hash.

### Multi-character (group chats)

A character entry can also be a `groupChat` (interface in
`database.svelte.ts`). Group ordering at chat-time lives in
`process/group.ts:52`.

---

## 2. Lorebook (world info)

`src/ts/process/lorebook.svelte.ts`.

### Entry shape

Approximate fields (from `lorebook.svelte.ts:18-40, 726-737`):

```ts
{
  key: string                // CSV of keywords
  secondkey: string          // selective AND keywords
  comment: string            // display name
  content: string            // text to inject
  mode: 'normal' | 'folder'
  insertorder: number        // priority
  alwaysActive: boolean
  selective: boolean         // require ALL keys when true
  useRegex: boolean
  extentions?: { ... }
}
```

Lorebooks live in three scopes:

- **Character** (`character.globalLore`).
- **Module** (`db.modules[].lorebook`).
- **Database** (`db.loreBook[]`).

### Selection logic — `loadLoreBookV3Prompt()` (`:74-660`)

Outer loop scans every candidate entry; the loop iterates until no new
entries activate (recursive scan). Within each iteration:

1. Tokenize the chat window (limited by `@@scan_depth`).
2. For each entry, test `key` against the window.
   - Case-insensitive, optionally `full_word_matching` (split on spaces) vs
     loose (strip spaces).
   - `secondkey` adds an AND constraint.
   - `selective` + `useRegex` adjust matching.
   - Negative keys (`exclude_keys`) veto.
3. Apply decorators (parsed in `:299-514`).
4. Add activated entries to a priority queue; re-scan if any new entry
   could change later matches (recursive).

After the loop:

5. Sort by `insertorder`, drop entries past the token budget
   (`db.loreBookToken`).
6. Return `{ actives, matchLog }`.

### Decorators

Inline directives recognised in the entry's `content` (`:299-514`):

| Decorator | Effect |
|-----------|--------|
| `@@depth N` | Insert at depth N in chat. |
| `@@scan_depth N` | Limit chat-window scan to last N messages. |
| `@@recursive` / `@@unrecursive` | Enable/disable recursive re-scan after activation. |
| `@@activate_only_after N` | Require chat length ≥ N. |
| `@@probability P` | P% activation chance per scan. |
| `@@role user | assistant | system` | Injection role. |
| `@@position` / `@@inject_at` / `@@inject_lore` | Advanced placement. |

### Editor & CRUD

- `addLorebook(type)`, `addLorebookFolder(type)` (`:15-72`).
- `importLoreBook()`, `exportLoreBook()` — JSON.
- `convertExternalLorebook()` — normalises Chub / AnyLore formats.
- UI: `src/lib/SideBars/LoreBook/`.

---

## 3. Personas

`src/ts/persona.ts`.

### Shape — `PersonaCard` (`:48-52`)

```ts
{
  name: string
  personaPrompt: string      // injected as system text
  note?: string
}
```

Personas live in `db.personas[]` with `db.selectedPersona` as the active
index. They also carry `icon` and `userIcon` fields used by the chat UI.

### Functions — `persona.ts:29-141`

- `saveUserPersona()` — persist to `db.personas[index]`.
- `changeUserPersona(id, mode)` — load persona into the session.
- `exportUserPersona()` — write a PNG with a `persona` chunk.
- `importUserPersona()` — read PNG, extract persona card.

UI: `src/lib/Setting/Pages/PersonaSettings.svelte` and `listedPersona.svelte`.

---

## 4. Where these data live in the DB

- `db.characters: (character | groupChat)[]` — character + chat history.
- `db.modules[].lorebook` — module-scoped lorebooks.
- `db.loreBook[]` — global lorebooks.
- `db.personas[]` + `db.selectedPersona` — user personas.

For the binary save format and storage backend, see [storage.md](./storage.md).

---

## 5. Related docs

- [scripting.md](./scripting.md) — triggers, CBS and Lua scripts that often
  live alongside a character.
- [processing-pipeline.md](./processing-pipeline.md) — when lorebooks are
  scanned during prompt assembly.
