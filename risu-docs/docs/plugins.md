# Plugin system internals

> **Note.** [`../plugins.md`](../plugins.md) is the plugin-author guide.
> This document covers the *host-side* implementation under `src/ts/plugins/`.

There are two coexisting plugin APIs:

- **V2 (legacy).** Runs in the main thread under a sandboxed global. Files:
  `plugins.svelte.ts`, `pluginSafeClass.ts`, `pluginSafety.ts`.
- **V3 (current).** Runs in an iframe with `srcdoc` + CSP nonce; talks back
  via a postMessage RPC bridge. Files: `apiV3/factory.ts`,
  `apiV3/v3.svelte.ts`, `apiV3/transpiler.ts`, `apiV3/developMode.ts`,
  `apiV3/risuai.d.ts`.

---

## 1. V2 path

### Loading — `plugins/plugins.svelte.ts`

- `importPlugin()` (`:129-428`) — parse metadata, validate code safety
  (`pluginSafety.checkCodeSafety()`), transpile TS, store under
  `db.plugins`.
- `loadPlugins()` (`:432-443`) — filter enabled by version; delegate V2
  vs V3.
- `loadV2Plugin()` (`:811-904`) — execute via
  `new Function(args.join(','), modifiedCode)` with a sandboxed `this`.
- `pluginV2` registry (`:466-477`) — providers, script handlers, replacers,
  unload callbacks.
- `getV2PluginAPIs()` (`:506-809`) — builds the `Risuai.*` API surface.

### Sandbox model

- `getSafeGlobalThis()` returns only whitelisted globals (`console`,
  `alert`, timers).
- DOM access only via `safeDocument`, `safeLocalStorage`, `safeIdbFactory`.
- `allowedDbKeys` whitelist (`:479-504`) gates the database surface plugins
  see.

### Custom provider — `plugins.svelte.ts:528-533`

`addProvider(name, fn, opts)` registers an async function in
`pluginV2.providers` Map. The provider name is added to `customProviderStore`
and surfaces in the model picker.

### Safety primitives

- `pluginSafeClass.ts`:
  - `SafeLocalStorage` (`:9-48`) — wraps `localStorage` with the
    `safe_plugin_` prefix.
  - `SafeIdbFactory` (`:79-101`) — `indexedDB` filtered to `safe_plugin_*`
    databases.
  - `tagWhitelist` (`:103-270`) — ~200 allowed HTML/SVG tags.
    `<a>` is replaced with `<div>` to neutralise navigation.
  - `SafeDocument` (`:281-418`) — `createElement()` + the special
    `createAnchorElement(href)` with URL validation.
- `pluginSafety.ts:55-155`:
  - `checkCodeSafety(code)` parses via acorn, walks the AST, flags dangerous
    calls (`eval`, `Function`, `sessionStorage`, `cookieStore`), rewrites
    `window`/`localStorage` references to the safe proxies, and caches results
    by code hash.

---

## 2. V3 path

### Iframe + RPC bridge — `apiV3/factory.ts`

- `SandboxHost` class — owns the iframe, registers per-instance handlers,
  serialises arguments and results.
- `GUEST_BRIDGE_SCRIPT` (`:38-289`) — payload injected into the iframe.
  Sets up a `message` listener, exposes `window.risuai` as a `Proxy` that
  routes property reads/method calls into postMessage calls.
- `run(container, userCode)` (`:483-621`) — injects `<iframe srcdoc>` with a
  CSP nonce that blocks all inline scripts except the bridge script itself.

### Message protocol

- Objects marked `__classType = 'REMOTE_REQUIRED'` are serialised as refs;
  the host keeps them in `instanceRegistry`.
- Guest receives a ref → wraps in `Proxy` → all method calls become
  `CALL_INSTANCE` messages back to the host.
- Callbacks passed *to* the host are serialised as **callback refs**; the
  host invokes them later via `INVOKE_CALLBACK`; the guest returns via
  `CALLBACK_RETURN`.
- `AbortSignal` is serialised as `ABORT_SIGNAL_REF`; abort events forward via
  postMessage; cleanup at call end (`:417-440, 467-474`).
- Transferables (ArrayBuffer, MessagePort, ImageBitmap, Streams) are
  collected and passed as the second arg to `postMessage`
  (`:116-136`).

### Host-side API — `apiV3/v3.svelte.ts`

- `loadV3Plugins(plugins)` (`:1335-1341`) — unload existing, spawn iframes,
  wire up `SandboxHost`s.
- `executePluginV3(plugin)` (`:1343-1361`) — create hidden iframe, run user
  code in it.
- `makeRisuaiAPIV3(iframe, plugin)` (`:627-1326`) — assemble the `risuai.*`
  surface (~1300 methods) including permission gates.

### SafeElement / SafeDocument / SafeMutationObserver

DOM is exposed only via wrappers (`v3.svelte.ts:57-477`):

- **SafeElement** wraps a node; only `x-` prefixed attributes are accessible
  (`:114-125`). Mouse / pointer / scroll events fire immediately; **keyboard**
  events are delayed a random 0–99 ms to resist fingerprinting
  (`:241-335`).
- **SafeDocument** extends SafeElement, adds `createElement(tag)` (whitelist
  + URL validation for `<a>`), DOMPurify on `setInnerHTML` / `setOuterHTML`.
- **SafeMutationObserver** wraps `MutationObserver`; mutations are reified as
  SafeElement refs; elements are tracked via an injected `x-identifier`
  attribute.

### Permissions — `v3.svelte.ts:556-613`

Per-plugin per-action consent stored in localforage `plugin_permissions`,
keyed by code hash. Actions include: `fetchLogs`, `db`, `mainDom`, `replacer`,
`provider`, `sendChat`. Cache TTL ~3 days, then re-confirm.

### UI registration

Plugins extend the host UI by pushing into reactive arrays
(`v3.svelte.ts:918-1108`): `additionalSettingsMenu`,
`additionalFloatingActionButtons`, `additionalHamburgerMenu`,
`additionalChatMenu`. `setChatPanel()` sanitises HTML via DOMPurify and pushes
into `chatPanelStore`. Plugins register tear-down via
`addPluginUnloadCallback()` (`:481-486`).

### Custom provider — `v3.svelte.ts:668-695`

`addProvider()` wraps the function in a permission gate (action `provider`),
creates an `LLMModel` metadata entry stored in `customV3ProviderMetaStore`,
and forces `mode = 'v3'` for safety.

### MCP bridge — `v3.svelte.ts:1093-1094`

Delegates to `pluginmcp.ts` (`registerMCPModule`, `unregisterMCPModule`).
Plugin MCP module identifiers must start with `plugin:`. See [mcp.md](./mcp.md).

### Storage

- **Save-scoped.** `pluginStorage.*` (`:1179-1185`) reads/writes
  `db.pluginCustomStorage` → syncs with save files.
- **Device-local.** `getLocalPluginStorage()` returns a
  `SafeLocalPluginStorage` backed by localforage (`:1158-1160`).

### Hot reload — `apiV3/developMode.ts:5-57`

`hotReloadPluginFiles()` uses File System Access API to pick a local file,
polls `lastModified` every 500 ms, re-imports + transpiles on change.

### Transpilation — `apiV3/transpiler.ts:1-10`

`pluginCodeTranspiler(code)` runs sucrase with the TypeScript transform,
preserving async.

### Type surface — `apiV3/risuai.d.ts`

Single ~2000-line file describing every API a V3 plugin can consume:
`SafeElement`, `SafeDocument`, `SafeClassArray`, `SafeMutationObserver`,
storage interfaces, UI registration, providers, TTS hooks, script handlers,
replacers, body interceptors, MCP, color schemes, text themes.

---

## 3. Security boundaries

What plugins can't reach:

- The real `window`, `document`, `localStorage`, `indexedDB` — only the safe
  proxies.
- `<a>` elements — replaced by `<div>` unless created via the audited
  `createAnchorElement()`.
- Inline scripts other than the bridge — CSP nonce blocks them.
- Database keys outside `allowedDbKeys` (V2) or the action-gated reads (V3).
- High-resolution timing of keyboard input — randomised delay.

What plugins *can* do (with consent):

- Register custom AI providers, scripts, replacers.
- Add UI to settings/menus/chat panels.
- Persist data (save-scoped or device-local).
- Register MCP modules.
- Call out via `risuai.fetch` (host-mediated; permission `fetchLogs`).

---

## 4. Plugin/MCP bridge — `process/mcp/pluginmcp.ts:1-58`

- `CustomPluginMCPClient` extends `MCPClientLike`; delegates `getToolList`
  and `callTool` to plugin callbacks.
- `registerMCPModule()` (`:36-54`) — identifier must start with `plugin:`,
  client added to global registry.
- `unregisterMCPModule()` (`:56-58`) — removal.

---

## 5. Related docs

- [`../plugins.md`](../plugins.md) — author-facing guide.
- [requests.md](./requests.md) — where custom providers plug in.
- [mcp.md](./mcp.md) — plugin-registered MCP servers.
