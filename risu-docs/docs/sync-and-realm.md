# Sync, Realm, and Drive

Three cross-cutting integrations that move user data between machines or share
it with the community.

| Area | Source | Purpose |
|------|--------|---------|
| Multiuser sync | `src/ts/sync/multiuser.ts` | Peer-to-peer chat sync via PeerJS. |
| Realm (hub) | `src/ts/realm.ts`, `src/lib/UI/Realm/` | Community character sharing at `realm.risuai.net`. |
| Drive / backup | `src/ts/drive/` | Google Drive backup + Risuai-hub account backups + local file backup. |

---

## 1. Multiuser (PeerJS)

`src/ts/sync/multiuser.ts`.

- **Topology.** One host, multiple clients. Host owns the authoritative chat
  state. PeerJS (`peerjs`) for WebRTC signalling and data channel.
- **Lazy import.** PeerJS is imported on first use (`multiuser.ts:11`).
- **Shared state stores** (`:56-58`): `ConnectionOpenStore`,
  `ConnectionIsHost`, `RoomIdStore`.
- **Room creation.** `createMultiuserRoom()` (`:60`) — host creates a UUID
  room id and listens for peers.

### Wire protocol

Messages between peers use string tags + arbitrary payloads, serialised with
`safeStructuredClone`:

| Tag | Direction | Payload |
|-----|-----------|---------|
| `receive-char` | Host → Peer | Character card + single chat page. |
| `receive-asset` | Host → Peer | Asset (`Uint8Array`). |
| `request-chat-sync` | Peer → Host | Ask for authoritative chat state. |
| `receive-chat` | Host → Peer | Sync confirmation. |
| `request-chat-safe` | Peer → Host | Are these pending changes safe? |

A map-based queue (`:55`) on the host handles concurrent "is this safe?"
requests.

### Limits

- No conflict resolution — the host wins.
- No persistent server. If the host disconnects, the room dies.

---

## 2. Realm (community hub)

`src/ts/realm.ts`. UI under `src/lib/UI/Realm/`.

- **What it is.** A web service at `realm.risuai.net` where users upload
  character cards (PNG-embedded) and others download them. Account-tied via
  `db.account.token` / `db.account.id`.
- **Upload flow** (`realm.ts:17-38`):
  1. `shareRealmCardData()` (`:17`) exports the current character as a PNG
     buffer (V3 card format).
  2. `openRealm(name, data)` (`:33`) constructs a URL of the form
     `https://realm.risuai.net/upload?token={tk}&token_id={id}#filedata={base64data}`
     and opens it.
  3. A `postMessage` handshake (`:10-14`) confirms the realm frame is ready.
- **Browse / download.** `lib/UI/Realm/RealmMain.svelte` (browser),
  `RealmPopUp.svelte` (details), `RealmFrame.svelte` (full-page hub),
  `RealmUpload.svelte` (upload), `RealmLicense.svelte` (license viewer).
  Downloaded cards land in `db.characters` as normal characters.

---

## 3. Drive & backup

### Google Drive — `src/ts/drive/drive.ts`

OAuth 2.0 flow → upload encrypted DB to Drive.

- `checkDriver(type)` (`:12`) — start OAuth; `type ∈ save | load | loadtauri
  | savetauri | reftoken`.
- `checkDriverInit()` (`:55`) — handle OAuth callback, exchange code for
  token.
- `backupDrive(ACCESS_TOKEN)` (`:117`) — upload database + asset map.
- `loadDrive(token, type)` — download/restore (paired with `backupDrive`).

### Local backup — `src/ts/drive/backuplocal.ts`

`SaveLocalBackup()` (`:21`) streams the DB + assets to disk via a
`LocalWriter`. Voice (VITS) files and emotion images are included
(`:50-56`).

### Risuai hub account backups — `src/ts/drive/accounter.ts`

Account-tied backups stored on the Risuai backend.

- `saveRisuAccountData()`, `loadRisuAccountData()`,
  `loadRisuAccountBackup()` (`:22-55`).
- Backup list retrieved from `/hub/backup/list`; restore by id.

---

## 4. Relationship to storage

These integrations *layer on top of* the local storage system
(see [storage.md](./storage.md)):

- Drive / hub backups upload the same `database.bin` produced by
  `RisuSaveEncoder`.
- Multiuser sync touches only the current character + chat, not the DB blob.
- Realm cards are character files, imported via the same path as drag-and-drop
  (`src/ts/characterCards.ts`).

---

## 5. Related docs

- [storage.md](./storage.md) — local persistence the backups serialise.
- [characters-and-lore.md](./characters-and-lore.md) — card formats used by
  Realm.
