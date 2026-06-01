# Storage & save format

The storage layer abstracts five backends behind one interface, encodes the
database as a block-based binary file, and keeps up to 20 rotating backups.

Source roots: `src/ts/storage/`, `src/ts/bootstrap.ts`, `src/ts/globalApi.svelte.ts`.

---

## 1. Architecture overview

The runtime picks a single backend per session and routes all read/write
through it. There is no merging between backends.

```
       UI / DBState rune
              │
   globalApi.saveDb / loadDb
              │
        RisuSaveEncoder / Decoder         ← block format (msgpackr + gzip)
              │
        forageStorage (auto)              ← src/ts/storage/autoStorage.ts:12-174
              │
   ┌──────────┼──────────┬──────────┐
Account     OPFS       Node       LocalForage
sync        FS         proxy      (IndexedDB)
```

Backend selection (`autoStorage.ts:119-174`):

| Backend | Detection | When |
|---------|-----------|------|
| **AccountStorage** | `localStorage.accountst === 'able'` | Remote sync enabled |
| **NodeStorage** | `isNodeServer` flag | Hosted via `server/node/server.cjs` |
| **OPFS** | `FileSystemFileHandle` exists + `opfs_flag!` | Modern web with persistent quota |
| **TauriFS** | `isTauri` flag | Desktop app (handled in `bootstrap.ts:58-115`, not auto-storage) |
| **LocalForage** | Default fallback | Web IndexedDB/localStorage |

Account > OPFS > Node > LocalForage. The Tauri path is decided earlier, in
`bootstrap.ts`.

---

## 2. Save file format

The save file is a sequence of blocks. Each block records a type, name,
optional compression flag, and a length-prefixed payload.

- Magic header (`risuSave.ts:33-36, 52-82`):
  `[0x00, 'R','I','S','U','S','A','V','E', 0x00, 0x09]`.
- Payload: msgpackr-serialized objects, optionally gzipped via `CompressionStream`.
- Block types (`RisuSaveType`, `risuSave.ts:93-106`):
  | Code | Name | Purpose |
  |------|------|---------|
  | 0 | `CONFIG` | Version metadata |
  | 1 | `ROOT` | All non-character settings + `__directory` listing |
  | 2 | `CHARACTER_WITH_CHAT` | Single character + all its chats |
  | 4 | `BOTPRESET` | Saved preset |
  | 5 | `MODULES` | RisuModule |
  | 6 | `REMOTE` | Pointer to an external `remotes/*.local.bin` file |
  | 9 | `PLUGINS` | Plugin |
  | 10 | `LOADOUTS` | Named preferences |

Backward compatibility (`decodeRisuSave`, `risuSave.ts:623-667`) handles legacy
msgpackr, fflate-compressed, and raw JSON saves.

There is **no DB-level encryption.** Only individual preset exports can be
AES-encrypted with the hard-coded key `'risupreset'`
(`database.svelte.ts:2268`, `:2317`).

---

## 3. Database top-level shape

`src/ts/storage/database.svelte.ts` defines the `Database` interface
(~200 fields). The high-level shape:

```ts
interface Database {
  characters: (character | groupChat)[]   // characters + chat history
  botPresets: botPreset[]                  // inference configs
  modules:    RisuModule[]                 // plugin modules + lorebook data
  loadouts:   Loadout[]                    // preference snapshots
  plugins:    RisuPlugin[]                 // user plugins
  pluginCustomStorage: Record<string,any>  // save-scoped plugin state

  // Settings
  apiType: string
  mainPrompt: string
  jailbreak: string
  temperature: number
  maxContext: number

  // Identity
  username: string
  userIcon: string
  selectedPersona: number
  personas: { name, personaPrompt, icon, note }[]

  // Lorebook
  loreBook: { name, data: loreBook[] }[]
  loreBookDepth: number
  loreBookToken: number

  // Optional
  account?: { token, id, data: { refresh_token, access_token } }
  hypaMemory?: boolean
  // … ~150 more flags
}
```

Defaults are applied by `setDatabase()` in `database.svelte.ts:24-694`.
Characters are defined around `:1304-1458`.

---

## 4. Load / save / migrate

### Load (`bootstrap.ts:54-267`)

1. Read backend-specific file (`database.bin`).
2. `RisuSaveDecoder.decode()` walks blocks, rebuilds the `Database`.
3. On exception, iterate the up-to-20 timestamped backups in order.
4. `setDatabase(decoded)` populates the rune.

### Save (`globalApi.svelte.ts:291-485`)

1. `RisuSaveEncoder` is initialized with the current DB.
2. A `$effect.root` watches the reactive parts; on change → debounce 500 ms →
   `encoder.set(db, changeTracker)` produces block diffs.
3. Write `database/database.bin` plus `database/dbbackup-<ts>.bin`.
4. Account sync (`accountStorage.ts:18-182`) posts with 3 s spacing.
5. `BroadcastChannel('risu-db')` coordinates tabs.

### Migrate (`bootstrap.ts:333-505`)

Currently format v5 (`:480`). Steps include:

- Assign missing `chaId` UUIDs.
- Validate module lorebook is an array; alert on corruption (`:368-416`).
- Normalize asset paths (`:432-461`).
- Replace deprecated prompts (`:489-494`).
- Delete characters whose `trashTime` > 3 days (`:495-502`).

---

## 5. Backup & recovery

- `globalApi.svelte.ts:492-528` (`getDbBackups`) lists backups by timestamp and
  prunes everything past the 20 newest.
- On a failed primary decode, `bootstrap.ts:88-115` iterates backups newest →
  oldest until one decodes.
- Orphaned `remotes/*.local.bin` files older than 7 days are auto-cleaned
  (`bootstrap.ts:549-562`).

---

## 6. Remote account sync

`accountStorage.ts:18-182`:

- Auth: bearer token in `db.account.token`. Session id tracked client-side.
- Endpoints: `/api/account/read`, `/api/account/write`.
- 303 Not Modified short-circuits redundant pulls.
- No conflict resolution — last-write-wins.
- On any failure the code falls through to the local cache
  (`cachedForage`), so the app stays usable offline.

Toggles: `db.account.useSync`, `localStorage.accountst`,
`localStorage.dosync`, `localStorage.fallbackRisuToken`.

---

## 7. Per-backend notes

- **OPFS** (`opfsStorage.ts:3-63`) hex-encodes keys as filenames and uses
  `FileSystemFileHandle.createWritable()` for atomic writes.
- **NodeStorage** (`nodeStorage.ts:6-237`) signs requests with an ECDSA JWT
  (5 min expiry) and talks to `/api/{write,read,list,remove}`.
- **LocalForage** is the fallback. No per-key ceremony.
- **TauriFS** is handled inline in `bootstrap.ts:58-115` using
  `@tauri-apps/plugin-fs`.

---

## 8. Tab safety

- `BroadcastChannel('risu-db')` carries reload triggers, save claims, and
  session ids (`globalApi.svelte.ts:297-311`, `:437-439`).
- Concurrent tabs with account sync can still lose work — there's no
  cross-tab merge, just last-write-wins.

---

## 9. Danger / gotchas

- **No DB-level encryption.** Preset-level AES uses a hardcoded key.
- **OPFS migration** (`autoStorage.ts:146-165`) is one-way; deny/failure falls
  back to LocalForage and won't retry.
- **Backups are limited to 20.** Set `db.backupCount` higher if recoverability
  matters more than disk usage.
- **`REMOTE` block characters** load as empty if their `remotes/<chaId>.local.bin`
  file is missing (`risuSave.ts:578-581`) — no referential-integrity check.
