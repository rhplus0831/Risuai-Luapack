# Element: Promise / `async()` (awaiting host calls)

- **Kind:** Element (runtime concept)
- **Source:** `Refer/Risuai/src/ts/process/scriptings.ts` (`luaCodeWrapper` — the injected `async`/`Promise` plumbing and the high-level wrappers; the `async`/`await` host declarations)

Some host calls are asynchronous. Risu's Lua VM injects a `Promise` type and an
`async()` wrapper so you can await them.

## What it is

Risu's wrapper (prepended to every script as `luaCodeWrapper`) exposes:

- a `Promise` object, and
- `async(callback)` — wraps a function so that, when called, it runs the body in
  a coroutine and returns a `Promise`, resuming the coroutine each time an
  awaited inner promise settles.

An **awaitable host call returns a promise**; you get the result by calling
`:await()` on it:

```lua
local resultJson = LLMMain(id, json.encode(prompt), false, '{}'):await()
```

You almost never call the raw `*Main` form. The high-level helpers do the await
(and JSON) for you (see below).

## High-level helpers await for you

These wrappers, defined in `luaCodeWrapper`, await internally and (where noted)
JSON-decode the result, so you call them like ordinary synchronous functions:

| Helper | Wraps | Does for you |
|--------|-------|--------------|
| [`LLM`](../api/LLM.md) | `LLMMain(...):await()` | `json.encode` prompt/options in, `json.decode` result out |
| [`axLLM`](../api/axLLM.md) | `axLLMMain(...):await()` | same as `LLM` |
| [`loadLoreBooks`](../api/loadLoreBooks.md) | `loadLoreBooksMain(id):await()` | `json.decode` result |
| [`getCharacterImage`](../api/getCharacterImage.md) | `getCharacterImageMain(id):await()` | returns the inlay string |
| [`getPersonaImage`](../api/getPersonaImage.md) | `getPersonaImageMain(id):await()` | returns the inlay string |

Inside the standard handlers (`onStart`, `onInput`, `onOutput`,
`onButtonClick`) and the `listenEdit(...)` callbacks, Risu already runs your code
in an async context, so calling these helpers directly just works.

## Awaitable host calls

Host functions that return a promise (so the raw `*Main`/low-level form needs
`:await()`, and which therefore require an async context):

- LLM: `LLMMain`, `axLLMMain`, `simpleLLM`
- Lore: `loadLoreBooksMain`
- Images: `generateImage`, `getCharacterImageMain`, `getPersonaImageMain`
- Low-level: `request`, `similarity`
- Utility: `sleep`, `getTokens`, `hash`
- Alerts that wait for the user: `alertInput`, `alertSelect`, `alertConfirm`

The synchronous calls (`getChat*`, `setChat*`, `getChatVar`/`setChatVar`,
`getGlobalVar`, `addChat`, `getName`, `cbs`, `log`, …) return immediately and
need no await.

## Manual / custom triggers must wrap themselves

The built-in handlers run async automatically, but a **manual / custom trigger**
(dispatched by global name) or a button handler that calls an awaitable API must
wrap its body in `async(...)` itself, or the await has no coroutine to suspend:

```lua
OpenMenu = async(function(id)
    local choice = alertSelect(id, {'Fight', 'Flee'}):await()
    -- ...
end)
```

Here `OpenMenu` is the global the manual trigger dispatches to, and `async`
turns it into a promise-returning coroutine so `:await()` works.

## Used by

- APIs: [`LLM`](../api/LLM.md), [`axLLM`](../api/axLLM.md),
  [`loadLoreBooks`](../api/loadLoreBooks.md),
  [`generateImage`](../api/generateImage.md),
  [`getCharacterImage`](../api/getCharacterImage.md),
  [`getPersonaImage`](../api/getPersonaImage.md), and the low-level
  [`request`](../api/request.md) / [`similarity`](../api/similarity.md)
- Hooks: the built-in [`onStart`](../hooks/onStart.md) /
  [`onOutput`](../hooks/onOutput.md) / [`onButtonClick`](../hooks/onButtonClick.md)
  run async for you; manual triggers must wrap with `async`

## See also

- Elements: [Access key & tiers](access-key.md), [Lorebook entry](lorebook-entry.md)
- Index: [`docs/README.md`](../README.md)
