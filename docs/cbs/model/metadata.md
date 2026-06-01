# CBS: `{{metadata::key}}`

- Layer: CBS function
- Category: model
- Aliases: none
- Source: `Refer/Risuai/src/ts/cbs.ts` (`metadata`)

Returns a piece of system / application metadata selected by `key`.

## Syntax

```text
{{metadata::key}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `key` | yes | Case-insensitive metadata key. Must be one of the recognized keys listed in "Behavior". |

## Behavior

Lower-cases `key` and switches on it. An unrecognized key returns
`Error: <key> is not a valid metadata key.` The recognized keys (from `cbs.ts`)
are:

| Key(s) | Returns |
|--------|---------|
| `mobile` | `1` if running on mobile, else `0` |
| `local` | `1` if running under Tauri (desktop), else `0` |
| `node` | `1` if running on the Node server, else `0` |
| `version` | the app version string (`appVer`) |
| `majorversion` / `majorver` / `major` | the major part of the version |
| `language` / `locale` / `lang` | the Risu UI language (`db.language`) |
| `browserlanguage` / `browserlocale` / `browserlang` | `navigator.language` |
| `modelshortname` | model short name (falls back to name, then id) |
| `modelname` | model display name (falls back to id) |
| `modelinternalid` | model internal id (falls back to id) |
| `modelformat` | model format code |
| `modelprovider` | model provider code |
| `modeltokenizer` | model tokenizer code |
| `risutype` | `local` (Tauri), `node` (Node server), or `web` |
| `maxcontext` | the max context length (`db.maxContext`) |
| `imateapot` | a teapot emoji |

The `model*` keys resolve through `getModelInfo(db.aiModel)`.

## Example

```text
Risu {{metadata::version}} ({{metadata::risutype}}), model {{metadata::modelname}}.
```

## See also

- CBS: [`{{model}}`](model.md), [`{{axmodel}}`](axmodel.md), [`{{maxcontext}}`](../context/maxcontext.md)
