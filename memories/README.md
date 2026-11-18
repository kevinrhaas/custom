# Memories: a family photo album

A private-feeling, static photo album for a family's old photos, letters and keepsakes. Lauren scans the boxes into a Google Drive folder. Relatives, grandparents included, open their own invite link and can look through the photos, read the stories and save copies. Nobody has an account, a password or a login.

Live at **https://custom.polecat.live/memories/** (GitHub Pages, served from this repo's `site/` folder).

House rules: static-first, no build step, no frameworks. Plain HTML, ES modules and CSS, and vendored code only (nothing loaded from a CDN at runtime).

## File layout

```
site/memories/
  index.html            the album (app shell)
  js/config.js          immutable invite/bootstrap settings and runtime configuration
  js/settings.js        validated device settings and offline-aware defaults
  data/settings.json    shared defaults for browsers without their own settings
  js/local-metadata.js  approved photo labels saved on this device
  js/app.js             the UI
  js/library.js         loads the photos and normalizes them (the Library contract lives here)
  js/sources/manifest.js  source: data/library.json (the sample set)
  js/sources/drive.js     source: a shared Google Drive folder
  js/gate.js            the invite gate ("This album is just for family.")
  css/skins.css         looks (skins): tokens for light and dark
  css/app.css           app layout
  css/gate.css          gate styles (.gate-*), reads only skin tokens
  admin/                settings, invitations, and photo review (noindex)
  vendor/polecat-shell/ access.js (invite tokens), icons.js, fonts
  vendor/qrcode/        qrcode-generator 2.0.4 (MIT, Kazuhiko Arase), ESM build

memories/               (outside site/, not published)
  README.md             this file
  LAUREN-GUIDE.md       one-page guide for Lauren
  tools/test-drive-parse.mjs   unit tests for the Drive source (names, captions, paging, errors)
  tools/test-gate-e2e.mjs      Playwright end-to-end: gate + admin page
  tools/shots/          screenshots from the e2e run (390x780, light and dark)
```

## Edit and save in the admin page

Open `/memories/admin/`, unlock with the existing admin key, then use **Album
settings**. Change the names, welcome message, photos, or look and press **Save**.
Connection details and less-used choices are folded away. No GitHub token,
configuration file editing, or publishing step is needed.

Choices, including the Drive connection key, are saved in this browser's
localStorage. They take effect on this device and persist across visits; other
browsers keep the shared defaults. Clearing website data removes local choices.
The form reports a failed save if browser storage is blocked or full.

A valid local override takes precedence over `data/settings.json`. Without one,
the album loads that shared default, then its validated offline cache, then the
bootstrap defaults. Invalid local data does not stop the album from opening and
can be replaced by saving again in admin. Invite verification stays in bootstrap
code and cannot be changed by the settings form. The browser Drive key must be restricted as
described below; AI provider keys are kept separately by the local caption tool.

## Public settings and technical defaults

| Field | What it does |
|---|---|
| `title` | Album name: welcome page, browser tab, gate. |
| `honorees` | `[{ name, years }]`, names on the album with optional dates or notes. |
| `dedication` | One or two sentences under the names. |
| `keeper` | Who hands out links ("Ask Lauren for your own link"). |
| `people` | Names to spot in titles and captions automatically. |
| `sample` | `true` shows a small "Sample photos" note. Set to `false` for real photos. |
| `source` | `'manifest'` (data/library.json) or `'drive'`. |
| `manifestUrl` | Path to the manifest when `source: 'manifest'`. |
| `metadataUrl` | Default tags/people/caption sidecar, default `data/tags.json`; `false` or `null` disables the sidecar. |
| `localMetadata` | Set to `false` when a tool needs source data without saved device labels. |
| `drive.apiKey` | Browser API key, restricted (see below). |
| `drive.folderId` | The ID from the folder's share link. A full share URL works too. |
| `access.enabled` | Turns the invite gate on or off. |
| `access.prefix` | localStorage namespace (`memories`). |
| `access.publicKey` | ECDSA P-256 public key (SPKI, base64). It can only check links, not make them. |
| `access.revoked` | Invite IDs (`jti`) turned off for everyone. |
| `defaultSkin` | The look a first-time visitor sees. |
| `helper` | Name of the person who helps maintain the site. |

## The Library contract

Every source returns the same raw shape, `{ chapters, photos }`, and `library.js` normalizes it. The full contract is in the header comment of [`site/memories/js/library.js`](../site/memories/js/library.js). The UI reads nothing else.

The Drive source also sets `fallback` and `thumbFallback` on each photo. The UI swaps to those if the main image fails to load.

## How the Drive source reads the folder

`loadDrive({ apiKey, folderId })` in `js/sources/drive.js`:

- **Root subfolders become chapters**, in name order. A leading sort number is dropped ("01 Early years" becomes "Early years"; a folder called "1950s" keeps its name). The folder's Drive description becomes the chapter blurb.
- **Images directly in the root** go into a last chapter called "The album".
- **One level of nested folders** is folded into its parent chapter. Anything deeper is ignored.
- **Only `image/*` files** are used. PDFs, docs and videos are skipped, so scan letters as JPG or PNG, not PDF.
- **Title and year come from the file name** (`parseName`):
  `1948 - Wedding day.jpg` → 1948, "Wedding day". `c1948` / `~1948` / `about 1948` / `circa 1948` → about 1948. `1940s …` → 1940, approximate. A year at the end also works: `Wedding day (about 1948).jpg`. Underscores and slug dashes become spaces, and ALL-CAPS names are calmed down. Camera names like `IMG_2231` give no title, so the caption's first sentence is used instead (or "A family photo").
- **No year in the name?** It falls back to the photo's camera date, but only if that date is older than the year the file was added to Drive. Scanners stamp the scan date, and we don't want every 1950s scan labeled 2026.
- **Caption = the file's Drive description.** `#keepsake` / `#letter` in it sets the kind (and is removed). A line `Place: Joliet` (or `Where: …`) sets the place. A folder with "keepsake" in its name makes its photos keepsakes, and "letters" makes them letters.
- **Image URLs:** `src`/`thumb` = `https://lh3.googleusercontent.com/d/<id>=w1600` / `=w480`. The fallbacks use `https://drive.google.com/thumbnail?id=<id>&sz=w1600|w480`. Downloads use `https://drive.google.com/uc?export=download&id=<id>` with the original file name.
- **Errors** are thrown with friendly messages and an `err.code`: `no-key`, `no-folder`, `not-folder`, `not-shared` (404), `key` (invalid key), `referrer` (key not allowed on this address), `api-disabled`, `quota`, `forbidden`, `network`, `empty`. If Drive is unreachable, `library.js` falls back to the last good copy saved on the device.

Run the tests: `node memories/tools/test-drive-parse.mjs`

## Drive setup, step by step

1. **Make the folder.** In Lauren's Google Drive, create one folder for the album (for example "Family album"). Subfolders inside it are the chapters.
2. **Share it.** Right-click the folder, choose **Share**, and under *General access* pick **Anyone with the link** with the **Viewer** role. Copy the link. The folder ID is the long part after `/folders/`.
3. **Open the Google Cloud console** (console.cloud.google.com) with any Google account and create a project (for example "family-album").
4. **Enable the Drive API:** APIs & Services → Library → "Google Drive API" → **Enable**.
5. **Create an API key:** APIs & Services → Credentials → **Create credentials → API key**.
6. **Restrict the key** (Edit API key):
   - *Application restrictions:* **Websites** (HTTP referrers), and add
     `https://custom.polecat.live/*`. Use a separate development key with localhost referrers if local testing is needed.
   - *API restrictions:* **Restrict key** → only **Google Drive API**.
   - Save. Restrictions can take a few minutes to take effect.
7. **Enter it:** unlock `/memories/admin/` and choose Google Drive photos in **Album settings**. Paste the folder link, then enter the key under **Connection details**. **Check the folder** can show its chapters and photo counts.
8. **Save.** Reopen the album to use these settings on this device. No file editing or publishing is needed.

A referrer-restricted, Drive-only key is designed to be public in browser code. It can only read files that are already shared publicly.

## Invites

- Invites are ECDSA P-256 signed tokens (`?invite=<payload>.<signature>`). `config.js` holds the **public** key, which can only check links. The **private (admin) key** makes links.
- **The admin key is never in this repo.** Kevin keeps it outside the repo and sends it to Lauren privately, once. She pastes it into `/memories/admin/`, which remembers it on her device (localStorage, `memories.adminkey`). **Lock this device** removes it.
- Links can last forever, 30 days or 1 year. A link opens the album on each device it's tapped on and is remembered there.
- **Turning a link off:** the admin page's "Turn off on this device" only affects Lauren's device. To turn a link off for everyone, add its ID to `CONFIG.access.revoked` (for example `revoked: ['AIIdsce4']`) and push. Lauren sees each link's ID on the admin page. Note that a device that already got in stays in. Revocation stops the link from opening the album anywhere new.
- **Rotating keys:** generate a new P-256 pair, put the new SPKI public key in `config.js`, and give Lauren the new private key. All old links stop working on new devices.

### Be honest about what this is

The invite gate is a **polite front door, not a lock**. The app's source is public. The photos are files in a Drive folder that anyone with the link can view, and their image URLs work without an invite. The gate keeps the album out of search engines and casual browsing, and it gives the family a calm, personal way in. If the family ever needs a real wall, put **Cloudflare Access** (email one-time codes) in front of `custom.polecat.live/memories/*`. Even then, the Drive files stay reachable by direct URL. A real fix means moving the photos off a public Drive folder.

## Adding a skin

1. Add a block to `css/skins.css` for both schemes:
   `html[data-skin="<id>"][data-scheme="light"] { … }` and `…[data-scheme="dark"] { … }`, defining the tokens listed in that file's header (`--bg --bg-2 --surface --surface-2 --text --muted --line --accent --accent-ink --focus --radius --radius-lg --shadow --font-display --font-body …`).
2. Add an entry to `js/skins.js` so it shows up in the album's style picker.
3. The gate and admin page need no changes. They read only these tokens, with warm fallbacks.

Check contrast in both light and dark, and at 390x780.

## Local preview

```sh
cd site && python3 -m http.server 8765
# album:  http://localhost:8765/memories/
# admin:  http://localhost:8765/memories/admin/
```

The Drive API key must allow `localhost/*` for Drive mode to work locally.

End-to-end test (needs Playwright, and the server above running from `site/`):

```sh
CHROMIUM_PATH=/path/to/chromium node memories/tools/test-gate-e2e.mjs
```

It creates an ephemeral key for the local browser fixture and mints tokens the same way `access.js` does. It checks the gate (no token, pasted link, raw code, bad and expired codes, admin key, and `?invite=` in the URL) and the admin page (unlock, make a link, list, turn off), then saves screenshots to `memories/tools/shots/`. No production admin key is needed. The settings suite covers device persistence, browser isolation, storage failures, and Drive checks against mocked APIs.

## Known caveats

- **lh3 / thumbnail URLs are not a documented Google API.** `lh3.googleusercontent.com/d/<id>` and `drive.google.com/thumbnail` work for publicly shared files today, but Google can rate-limit them (HTTP 429) or change them. That's why every photo carries a fallback. If both fail for a big album, the robust option is a one-time export of resized copies into `photos/` plus a manifest.
- **Downloads** go to `drive.google.com/uc?export=download`, which sends the original file as an attachment. The `download` attribute is ignored across origins, so the file name comes from Drive (it's the original name anyway). Very large files (>100 MB) get Google's virus-scan page, which isn't an issue for photos.
- **HEIC** files from iPhones are listed (they're `image/*`). The thumbnail URLs return a JPEG rendering, but the download is still HEIC, which older Windows PCs can't open. Scanning to JPG avoids this.
- The Drive source has been tested against mocked API responses and error bodies. A live test folder still needs the family's restricted Drive API key and folder link; that setup has not yet been verified.

## Search tags, AI drafts, and local face groups

The album now searches explicit `tags` and `people` as well as titles, captions,
places, years, and chapter names. Google's Photos face groups and object labels
are not imported.

### Manual labels in Drive

Add these lines to a photo's Description box:

```text
June with the pony at the county fair.
Place: Joliet
Tags: horse, county fair, Ferris wheel
People: June Hale; Walter Hale
```

`Tags:` and `People:` accept comma- or semicolon-separated lists, including
repeated lines. These lines become searchable metadata rather than appearing
in the caption. Names found in the title/caption still work too.

### Review before saving

Unlock `/memories/admin/` and open **Tag photos**. Edit a photo's labels and
caption, import AI drafts, or use local face grouping. Suggestions remain drafts
until approved. Press **Save approved tags** to make approved additions searchable
on this device and browser. Drafts stay in the review tool. Downloading an approved
backup is optional. The save checks for changes from another open tab and asks you
to resolve conflicting edits. Drive descriptions remain the way to share labels
with all visitors.

Saved device labels are separate from draft work and are scoped to the photo
source and Drive folder. They replace the default sidecar's additions for that
source. Only approved text is stored in this search layer; no images or face
vectors are included. The loader can skip it with `localMetadata: false`.

The public metadata format is:

```json
{
  "version": 1,
  "photos": {
    "stable-photo-id": {
      "tags": ["horse", "county fair"],
      "people": ["June Hale"],
      "caption": "June with the pony at the county fair."
    }
  }
}
```

Use the exact album photo ID (the Drive file ID in Drive mode), not its title.
Tags and people are added to source metadata. An explicit `caption` replaces the
source caption; omit it to keep future edits in Drive visible. An empty caption
is an intentional replacement. Drafts, API keys, and face vectors must never be
added to this public file. The loader accepts only the text fields above.
`CONFIG.metadataUrl` selects the sidecar; `false` or `null` disables it.

### AI captions and object tags

AI tagging runs as a local command with Claude. Only the selected images are
sent to Anthropic when the command is run with a configured API key. The public
website never receives that key. The command drafts object/scene tags and a
caption, not people's identities. Review uncertain details, especially on faded
scans; no model can guarantee correct recognition.

See [the AI tagging guide](AI-TAGGING.md) for inputs, key setup, resumable runs,
and importing drafts. Keep the key and draft output outside `site/`; neither is
needed by relatives. Live API testing is deferred until a key is connected.

### Local face grouping

The admin tool uses locally selected image files and vendored models. Match
files to their album photos, scan, review the suggested groups, and supply the
names yourself. Correct individual mismatches before accepting suggestions.
Selected image bytes and face embeddings are processed locally in the browser;
the AI caption command is a separate, explicitly run operation. The saved
metadata contains only confirmed names associated with photo IDs.

Face grouping is approximate, particularly for old, blurred, or profile photos.
Use a desktop for large batches and keep the originals. There is no automatic
identification and no demographic or emotion analysis.

## Validation and remaining setup

Run the offline regression checks from the repository root:

```sh
node memories/tools/test-drive-parse.mjs
node memories/tools/test-metadata.mjs
node memories/tools/test-faces.mjs
node memories/tools/test-tagging-state.mjs
node --test memories/tools/test-ai-tagging.mjs
node --test memories/tools/test-settings.mjs
node --test memories/tools/test-local-metadata.mjs
```

These also run in the scoped Family album tests GitHub Actions workflow. For
browser checks, start the local server above and use Playwright with Chromium:

```sh
CHROMIUM_PATH=/path/to/chromium node memories/tools/test-tagging-e2e.mjs
CHROMIUM_PATH=/path/to/chromium node memories/tools/test-faces-e2e.mjs
CHROMIUM_PATH=/path/to/chromium node memories/tools/test-settings-e2e.mjs
```

The tagging browser suite creates an ephemeral test key and intercepts only the
local browser's configuration response. It never rotates the deployed invite key.
The face suite defaults to a sample illustration with no detectable face; set
`FACE_TEST_IMAGE=/path/to/portrait.jpg` to exercise detection and name approval
with a real photographic fixture. Neither face test uploads the selected image.

The existing Drive connection is preserved. Family details and future Drive
changes can now be saved on each device from the admin form. Keep the original
admin key in a password manager and outside Git. Do not rotate the invite key
just to run tests. Claude live calls remain optional and unconnected until
the maintainer supplies a local key.
