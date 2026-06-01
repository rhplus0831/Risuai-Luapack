# Element: Access key (`id`) and permission tiers

- Kind: Element (runtime concept)
- Source: `Refer/Risuai/src/ts/process/scriptings.ts` (`ScriptingSafeIds`, `ScriptingEditDisplayIds`, `ScriptingLowLevelIds`, and the per-mode key setup near the bottom of `runScripted`)

## What it is

Lua never receives a raw handle to Risu's database. Instead Risu generates a
fresh opaque key (a UUID) for each script run, passes it to your handler as the
first argument (conventionally named `id`), and registers that key in one or
more permission sets for the duration of the run. Every host call takes the key
as its first argument and checks it against those sets before doing anything
privileged.

```lua
function onStart(id)
    local hp = getChatVar(id, 'hp')   -- id first, always
    setChatVar(id, 'hp', '100')
end
```

The key is deleted as soon as the run finishes, so it cannot be cached and
reused across runs. Passing the wrong key (or no key) to a privileged host call
makes that call silently no-op.

## The three tiers

| Set | Granted to | Lets the key call |
|-----|------------|-------------------|
| `ScriptingSafeIds` | normal modes (`start`, `input`, `output`, `onButtonClick`, custom) and the request/input/output edit hooks | chat/character mutation: `addChat`, `setChat`, `setName`, `setBackgroundEmbedding`, `upsertLocalLoreBook`, `reloadDisplay`, … |
| `ScriptingEditDisplayIds` | the `editDisplay` hook only | chat-var writes via `setChatVar` only — no chat/character mutation |
| `ScriptingLowLevelIds` | safe-mode runs when the character/module has `lowLevelAccess` | network/model/disk: `LLMMain`, `axLLMMain`, `simpleLLM`, `request`, `similarity`, `generateImage`, `loadLoreBooksMain`, image getters |

A few reads (`getChatVar`, `getGlobalVar`, `getChatMain`, `getChatLength`,
`getName`, `cbs`, `logMain`, …) carry no guard at all — they work for any
key (the "always available" tier).

## How the tier is chosen per run

- If the mode is `editDisplay`, the key goes into `ScriptingEditDisplayIds`
  only. It can write chat vars but cannot mutate chat or character data, and it
  never gets low-level access.
- For every other mode the key goes into `ScriptingSafeIds`. If the
  character/trigger has `lowLevelAccess` enabled, the same key is *also* added to
  `ScriptingLowLevelIds`.
- Edit listeners never get low-level access. `editRequest`, `editInput`, and
  `editOutput` run with the low-level flag forced off, even when the character
  has `lowLevelAccess`.

## Notes / constraints

- Low-level APIs only work if `lowLevelAccess` is enabled on the
  character/trigger in Risu. In luapack, declare it in `luapack.toml`
  (`low_level_access = true`) and grant it per test call
  (`emu.run_mode('output', low_level=True)`).
- The exceptions that ignore the key entirely are `log(value)`, `logMain(value)`,
  and `cbs(value)`.

## Used by

- Every host API (`docs/api/`) takes `id` first — see for example
  [`addChat`](../api/addChat.md), [`setChatVar`](../api/setChatVar.md),
  [`LLMMain`](../api/LLMMain.md).
- Hooks (`docs/hooks/`) decide which tier the key lands in: see
  [`editDisplay`](../hooks/editDisplay.md) (restricted) vs
  [`onStart`](../hooks/onStart.md) (safe + optional low-level).

## See also

- [Chat variables](chat-variables.md), [Promise / await](promise-async.md)
