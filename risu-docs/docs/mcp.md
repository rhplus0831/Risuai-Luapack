# Model Context Protocol (MCP)

Risuai implements a JSON-RPC 2.0 MCP client for both built-in tool servers and
external (plugin- or user-configured) ones. Source: `src/ts/process/mcp/`.

---

## 1. Core types & registry

- `MCPClient` — `mcplib.ts:80` — the JSON-RPC 2.0 client. Speaks
  HTTP+SSE; pluggable transport so stdio child-processes and plugin
  callbacks also work.
- `MCPToolHandler` — `mcplib.ts:75` — abstract base for tool providers.
- `MCPClientLike` — `internalmcp.ts:8` — interface for in-process clients
  that don't speak the real protocol (built-ins, plugins).
- `MCPs`, `callOnlyMCPs` — `mcp.ts:17-18` — global registries keyed by
  identifier.
- `initializeMCPs(additionalMCPs)` — `mcp.ts:23` — lazy load of built-ins +
  external entries.

Protocol version: `2025-03-26` (`mcplib.ts:89`).

---

## 2. Built-in tool servers

All registered with identifiers under the `internal:` prefix.

| Identifier | File | Tools |
|------------|------|-------|
| `internal:fs` | `filesystemclient.ts` | `fs_read_file`, `fs_write_file`, `fs_list_directory` (File System Access API). |
| `internal:dice` | `dice.ts:27-37` | `rollDice(notation)` — `2d6+3` syntax. |
| `internal:googlesearch` | `googlesearchclient.ts` | Google Custom Search; needs API key + engine id in DB. |
| `internal:graphmem` | `graphmem.ts:70-80` | `writeMemory`, `readMemory` over a connected memory graph. |
| `internal:aiaccess` | `aiaccess.ts:53-68` | `runLLM(model, messages)` — proxies a sub-LLM call to the normal or "lite" model. |
| `internal:risuai` | `risuaccess/client.ts:7-99` | Risuai-specific tools — character / chat / module handlers with detailed metadata. |

---

## 3. Plugin-registered MCP servers

`process/mcp/pluginmcp.ts:1-58`.

- `CustomPluginMCPClient` extends `MCPClientLike` and delegates
  `getToolList` and `callTool` to plugin-supplied callbacks.
- `registerMCPModule(identifier, …)` — `:36-54` — validates that
  `identifier.startsWith('plugin:')`, creates the client, adds it to
  `MCPs` / `callOnlyMCPs`.
- `unregisterMCPModule(identifier)` — `:56-58`.

Plugins call these via the V3 API (`risuai.registerMCP` / `unregisterMCP`,
wired in `apiV3/v3.svelte.ts:1093-1094`).

---

## 4. Wire protocol

The full HTTP+SSE path lives in `MCPClient` (`mcplib.ts:80-…`). Behaviour:

- **Initialization.** Standard `initialize` → `notifications/initialized`
  handshake, advertising protocol version `2025-03-26`.
- **Tool discovery.** `tools/list` → cached.
- **Invocation.** `tools/call` with `{name, arguments}` → streamed JSON-RPC
  response via SSE.
- **Custom transport.** The client accepts a transport callback so non-HTTP
  servers (stdio, plugin-internal) can plug in without changing the call
  sites.

---

## 5. Surfacing tools to the LLM

The chat pipeline collects tools from all active MCP entries and folds them
into the request as function/tool declarations (provider-dependent shape —
OpenAI `tools`, Anthropic `tools`, Gemini `function_declarations`). See
[requests.md](./requests.md).

When the model emits a tool call, the result is dispatched to
`MCPClient.callTool()` and the response is fed back as a follow-up turn.

---

## 6. Configuration

- **Built-ins** — toggled in Settings → Advanced.
- **Custom external** — user adds an entry pointing at a URL; `initializeMCPs`
  picks it up on next load.
- **Plugin-supplied** — registered programmatically at plugin load time and
  torn down on plugin unload.

---

## 7. Playground

`src/lib/Playground/PlaygroundMCP.svelte` exposes a tester for invoking MCP
tools directly without going through a chat turn — useful for verifying a
configuration or debugging a plugin-registered server.

---

## 8. Related docs

- [plugins.md](./plugins.md) — how plugins can register MCP modules.
- [requests.md](./requests.md) — how tools surface in provider payloads.
