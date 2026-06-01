# UI architecture

Risuai's UI is a single Svelte 5 application. There is no router — every
screen is conditionally rendered from `App.svelte` based on reactive stores in
`src/ts/stores.svelte.ts`.

---

## 1. Entry & root

- `src/main.ts` mounts `App.svelte`, kicks off `preLoadCheck()`,
  `loadData()`, `initHotkey()`.
- `src/App.svelte:103-260` is a long top-to-bottom `if/else` chain that
  decides what to mount. Order matters:
  1. Legal/config gate.
  2. April-fools easter egg.
  3. Loading spinner.
  4. Custom GUI settings menu.
  5. Welcome / first-setup.
  6. Settings panel.
  7. `MobileGUI` layout.
  8. Desktop layout (sidebar + chat).
  Modals overlay everything: `AlertComp`, `RealmPopUp`, `Presets`,
  `Bookmarks`, `PluginAlertModal`, `HypaV3Modal`, …
- `src/LiteMain.svelte` is a stripped-down entry for embeddable use.

---

## 2. Stores (`src/ts/stores.svelte.ts`)

Top-level reactive state. Important entries:

| Store | Role |
|-------|------|
| `DBState` | The reactive `Database` object (see [storage.md](./storage.md)). |
| `selectedCharID` | Current character index. |
| `settingsOpen`, `SettingsMenuIndex` | Settings panel visibility & tab. |
| `MobileGUI`, `MobileSideBar` | Mobile mode + active mobile tab. |
| `DynamicGUI`, `SizeStore` | Responsive switch (≤1024 px). |
| `sideBarStore` | Desktop sidebar visibility. |
| `alertStore`, `popupStore`, `easyPanelStore` | Modal/alert state. |
| `loadoutModalStore`, `irisStore`, `bookmarkStore` | Specialised modals. |
| `pluginAlertModalStore` | Plugin safety warnings. |
| `additionalSettingsMenu`, `additionalHamburgerMenu`, `additionalChatMenu` | Slots plugins push into. |
| `chatPanelStore` | Plugin-injected chat-panel HTML (sanitised). |
| `PlaygroundStore`, `OpenRealmStore` | Page selectors. |

`DBState.db.*` is what most UI two-way-binds against.

---

## 3. Responsive & GUI modes

- `DynamicGUI` (`stores.svelte.ts:10-26`) flips true when window width ≤ 1024 px.
  In that mode the sidebar becomes a fixed overlay (`z-30`) rather than a
  flex column.
- `MobileGUI` is explicit (set when the build/runtime is the mobile shape) —
  swaps in `lib/Mobile/MobileBody.svelte` with `MobileHeader` / footer tabs.
- Theme variant (`db.theme`, used in
  `lib/ChatScreens/ChatScreen.svelte:35-80`):
  - `classic` — centred chat with optional `ResizeBox` portrait.
  - `waifu` — side-by-side; `db.waifuWidth` / `waifuWidth2` controls split.
  - `waifuMobile` — portrait overlay on mobile.
- GUI mode 'lite' uses `lib/LiteUI/*` components.

---

## 4. Theming pipeline

- **Tokens.** `src/styles.css:5-59` declares Tailwind v4 theme tokens that
  map to CSS variables prefixed `--risu-theme-` (e.g. `bgcolor`, `textcolor`,
  `darkbg`, `darkbutton`, `borderc`, `selected`, `textcolor2`, `draculared`)
  plus palette ramps (primary/secondary/danger/neutral/success 50–900) and
  layout vars (`--sidebar-size`, `--risu-animation-speed`).
- **Schemes.** `src/ts/gui/colorscheme.ts` ships presets — `default`
  (Dracula), `dark`, `light`, `cherry`, `galaxy`, `nature`, `realblack` — each
  conforming to the `ColorScheme` interface and tagged `type: 'light' | 'dark'`.
- **Application.** On scheme/setting change, the scheme is written onto
  `document.documentElement` via `style.setProperty(...)`.
- **Editor.** `lib/Setting/Pages/Display/CustomColorSchemeEditor.svelte` lets
  users override individual tokens; the result is persisted in `DBState.db`.
- **Animation speed.** `src/ts/gui/animation.ts:updateAnimationSpeed()`
  syncs `db.animationSpeed` → `--risu-animation-speed`.
- **Sidebar size.** `src/ts/gui/guisize.ts:updateGuisize()` sets
  `--sidebar-size = (24 + 4 * db.sideBarSize)rem`.

When styling new components, use the Tailwind classes that reference the
theme vars (e.g. `bg-bgcolor`, `text-textcolor/90`, `border-borderc`) rather
than literal colours. Opacity modifiers work directly on these tokens.

---

## 5. Component map

### Chat surface — `lib/ChatScreens/`

| Component | Role |
|-----------|------|
| `ChatScreen.svelte` | Layout router: picks classic/waifu/waifuMobile, hosts wallpaper, emotion box, portrait transitions. |
| `DefaultChatScreen.svelte` | The actual chat UI inside the screen. |
| `Chat.svelte` / `Chats.svelte` | Chat tab management. |
| `ChatBody.svelte` | Iterates messages. |
| `Message.svelte` | Single message: avatar, name, body, action row (copy/bookmark/reroll/delete/translate/TTS), multi-page support, edit/partial-edit. |
| `EmotionBox.svelte` | Current expression image. |
| `BackgroundDom.svelte` | Animated background. |
| `Suggestion.svelte` | Suggested replies. |
| `AssetInput.svelte`, `PartialEditController.svelte`, `TransitionImage.svelte`, `ResizeBox.svelte` | Supporting widgets. |
| `CreatorQuote.svelte` | Character creator banner. |

### Top-level UI — `lib/UI/`

`MainMenu.svelte`, `ModelGrid.svelte`, `ModelList.svelte`,
`NanoGPTDashboard.svelte`, `NanoGPTProviderPicker.svelte`,
`OpenrouterProviderList.svelte`, `PopupButton.svelte`, `PopupList.svelte`,
`PromptDataItem.svelte`, `BaseRoundedButton.svelte`, `Accordion.svelte`,
`3DLoader.svelte`, `Googli.svelte`, `Title.svelte`.

- **GUI subfolder** — `lib/UI/GUI/*` is the older form-input set
  (`TextInput`, `NumberInput`, `SelectInput`, `CheckInput`, `ColorInput`,
  `SliderInput`, `SegmentedControl`). All two-way bind to `DBState.db.*`.
- **NewGUI subfolder** — newer style; used for newer pages.
- **Realm subfolder** — community hub: `RealmMain`, `RealmPopUp`,
  `RealmFrame`, `RealmUpload`, `RealmLicense`. See
  [sync-and-realm.md](./sync-and-realm.md).

### Sidebar — `lib/SideBars/`

`Sidebar.svelte` hosts character list, chat list (`SideChatList.svelte`),
character config (`CharConfig.svelte`), and dev tools (`DevTool.svelte`).
Sub-folders `Scripts/` and `LoreBook/` carry their respective editors.

### Settings — `lib/Setting/`

- `Settings.svelte` — side menu (desktop) / tabs (mobile). Selected via
  `SettingsMenuIndex`:
  - 1 Bot Settings
  - 2 Other Bot Settings
  - 3 Display Settings
  - 10 Language
  - 11 Accessibility
  - 12 Persona
  - 13 Prompt
  - 14 Advanced
  - Plus: Files, Plugins, Modules, Communities, Thanks
- `SettingRenderer.svelte` is a generic renderer used by some pages.
- `Pages/` holds individual setting pages (Display, Advanced, Persona,
  Plugin, Hotkey, Module, …).
- `Wrappers/` wraps groups of settings with shared chrome.
- `botpreset.svelte`, `listedPersona.svelte`, `lorepreset.svelte` are
  presentation helpers.

### Mobile — `lib/Mobile/`

`MobileHeader`, `MobileBody`, `MobileFooter`, `MobileCharacters`. Tabs are
switched via `MobileSideBar`.

### Modals & overlays — `lib/Others/`

`AlertComp.svelte` (the central alert/confirm/input dialog driven by
`alertStore`), `PluginAlertModal.svelte` (plugin-safety warnings),
`HypaV3Modal.svelte` and `HypaV3Modal/` subfolder, `BookmarkList`,
`ChatList`, `LoadoutModal`, `IrisModal`, `MonacoEditor`, `PopupEditor`,
`PromptDiffModal`, `QuickSettingsGUI`, `SavePopupIcon`, `WelcomeRisu`,
`Help`, `Legal`, `GithubStars`.

### Playground — `lib/Playground/`

A debug surface keyed by `PlaygroundStore` (number). Pages:

| Value | Page |
|-------|------|
| 2 | Chat (utility bot) |
| 3 | Embedding |
| 4 | Tokenizer |
| 5 | Syntax |
| 6 | Jinja |
| 7 | Regex |
| 8 | Image gen |
| 9 | Image translation |
| 10 | Translation |
| 11 | Subtitle |
| 12 | Parser |
| 13 | CBS docs |
| 14 | MCP |
| 15 | Inlay explorer |
| 16 | Tool conversion |

---

## 6. Alert & popup architecture

- `lib/Others/AlertComp.svelte` is driven by `alertStore` (type ∈ `none |
  error | warn | info | confirm | input | wait`). Promises resolve via the
  store-set value pattern. Stack-trace / branch / generation-info viewers are
  built in.
- `PluginAlertModal.svelte` is a dedicated risk-warning dialog gated by
  `pluginAlertModalStore`.
- All other modals are rendered as conditional overlays in `App.svelte:216-259`
  on top of the main layout.

---

## 7. Conventions for new components

- Use `DBState.db.*` for persistent state; transient state can stay local.
- Bind to theme tokens, not literal colours.
- Mobile-first responsive choices: gate desktop-only chrome on `!DynamicGUI`.
- For modal additions, follow the `popupStore` / `easyPanelStore` pattern
  rather than ad-hoc local booleans.
- For new playground pages, add a value to `PlaygroundStore` and a branch in
  `lib/Playground/PlaygroundMenu.svelte`.
