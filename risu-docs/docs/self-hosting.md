# Self-hosting (Node, Hono, Docker)

Two server implementations live in `server/`:

- **`server/node/`** — production Express + WebSocket server. Stable.
- **`server/hono/`** — WIP modern Hono router targeting Node, Bun, and
  Cloudflare Workers.

For container deployment, see §5.

---

## 1. Node server — `server/node/server.cjs`

The current production self-host. ~Express + WS + rate limiting +
`openid-client`.

### Boot

- Default port **6001** (see `server.sh` / `server.bat:37`).
- Static frontend served from `dist/` (produced by `pnpm build`).
- Persistent volume: `save/` (passwords, JWT keys, character data).

### Auth

`server.cjs:101-156` — `isAuthorizedJwtHeader()`:

- **Password.** Plaintext hex stored in `save/__password` (or the magic
  string `__password`).
- **JWT.** ECDSA ES256, public-key cached in memory. Token expiry checked
  inline (`:123`).
- **PKCE OAuth2** flow for the Risuai-hub login. JWT key registration is
  part of the flow.
- Rate limits: 2000 req/min authenticated, 10 attempts / 30 s for login.

There are no server-side sessions — everything is stateless JWT validation.

### Endpoints

The script bundles many endpoints; the main groups, inferred from rate
limiters + handlers + AGENTS notes:

- `/streamed_fetch` — proxy streaming of outbound AI requests. Mirrors the
  Tauri `streamed_fetch` command. Buffered up to 2 MB; 600 s default
  timeout; max 64 active jobs; 512 pending events. Heartbeats keep clients
  alive (`server.cjs:46-56`).
- `/login`, `/auth` — token generation/validation.
- `/save/{char_id}` — character data persistence (account-storage mode).
- `/plugin/*` — plugin install/list (implied by AGENTS notes).
- `/user/...` — OAuth/account endpoints.

The frontend's `nodeStorage.ts` (`src/ts/storage/`) signs requests with an
ECDSA JWT (5 min expiry) to talk to `/api/{write,read,list,remove}`.

### Run scripts

- `server.sh` (Unix) and `server.bat` (Windows) build the frontend and start
  the server.
- Honours `NODE_ENV`, `PORT`, `TRUST_PROXY`,
  `VITE_RISU_LEGAL_CONFIGURED`, `VITE_RISU_LITE`, ad config.

---

## 2. Hono server — `server/hono/`

Lightweight router. Multi-target. **Currently WIP** — the Node server is
recommended (`server/hono/README.md:2-3`).

### Entry points

- `src/cf.ts:1-4` — `export default app` for Cloudflare Workers.
- `src/node.ts:1-9` — `@hono/node-server` on port 3000.
- `src/bun.ts` — Bun runtime (minimal).

### App

`src/app/index.ts:1-10` registers CSRF middleware and stub routes (`"Hello
Hono!"`). The intent is feature parity with the Node server on a
Workers-compatible codebase.

### Cloudflare config

`wrangler.jsonc` — `compatibility_date: 2025-12-26`. The Hono server *is*
designed for Workers; the `cf.ts` entry exports the app directly. Full
deployment is gated on feature parity.

### Build

```bash
pnpm hono:build
```

Runs `vite build --sourcemap` then `server/hono/src/utils/postbuild.js`.

---

## 3. Docker

`Dockerfile:1-44`:

- Multi-stage: `base` → `deps` → `builder` → `runtime`.
- Base: `node:24-slim`. pnpm via Corepack.
- Production: `pnpm build` + `pnpm runserver`.
- Expose port **6001**.
- Persistent volume: `/app/save`.

`docker-compose.yml` provides a one-command run. The image is published to
GHCR as `ghcr.io/kwaroran/risuai:latest` and tag-versioned.

### Compose quickstart

```bash
curl -L https://raw.githubusercontent.com/kwaroran/Risuai/refs/heads/main/docker-compose.yml \
  | docker compose -f - up -d
# → http://localhost:6001
```

---

## 4. Environment variables (Node server)

| Var | Purpose |
|-----|---------|
| `NODE_ENV` | `production` for built mode. |
| `PORT` | Port to listen on (default 6001). |
| `TRUST_PROXY` | Trust X-Forwarded-* (1/0). |
| `VITE_RISU_LEGAL_CONFIGURED` | Build-time legal gate flag. |
| `VITE_RISU_LITE` | Build the Lite variant. |
| `KEI_*`, `RISU_AD_*` | Optional Kei cloud / ad config. |

---

## 5. Related docs

- [storage.md](./storage.md) — the client side that talks to `/api/write` etc.
- [tauri.md](./tauri.md) — equivalent transport for the desktop build.
- [build-and-test.md](./build-and-test.md) — frontend build commands the
  server relies on.
