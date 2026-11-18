# Memories: a family photo album

A private-feeling, static photo album for a family's old photos, letters and keepsakes. Lauren scans the boxes into a Google Drive folder. Relatives, grandparents included, open their own invite link and can look through the photos, read the stories and save copies. Nobody has an account, a password or a login.

Live at **https://custom.polecat.live/memories/** (GitHub Pages, served from this repo's `site/` folder).

House rules: static-first, no build step, no frameworks. Plain HTML, ES modules and CSS, and vendored code only (nothing loaded from a CDN at runtime).

## File layout

```
site/memories/
  index.html            the album (app shell)
  js/config.js          THE file to edit: names, dedication, keeper, photo source, invite settings
  js/app.js             the UI
  js/library.js         loads the photos and normalizes them (the Library contract lives here)
  js/sources/manifest.js  source: data/library.json (the sample set)
  js/sources/drive.js     source: a shared Google Drive folder
  js/gate.js            the invite gate ("This album is just for family.")
  css/skins.css         looks (skins): tokens for light and dark
  css/app.css           app layout
  css/gate.css          gate styles (.gate-*), reads only skin tokens
  admin/                Lauren's "Make invite links" page (noindex)
  vendor/polecat-shell/ access.js (invite tokens), icons.js, fonts
  vendor/qrcode/        qrcode-generator 2.0.4 (MIT, Kazuhiko Arase), ESM build

memories/               (outside site/, not published)
  README.md             this file
  LAUREN-GUIDE.md       one-page guide for Lauren
  tools/test-drive-parse.mjs   unit tests for the Drive source (names, captions, paging, errors)
  tools/test-gate-e2e.mjs      Playwright end-to-end: gate + admin page
  tools/shots/          screenshots from the e2e run (390x780, light and dark)
```

## config.js fields

| Field | What it does |
|---|---|
| `title` | Album name: welcome page, browser tab, gate. |
| `honorees` | `[{ name, years }]`, the people the album remembers. |
| `dedication` | One or two sentences under the names. |
| `keeper` | Who hands out links ("Ask Lauren for your own link"). |
| `people` | Names to spot in titles and captions automatically. |
| `sample` | `true` shows a small "Sample photos" note. Set to `false` for real photos. |
| `source` | `'manifest'` (data/library.json) or `'drive'`. |
| `manifestUrl` | Path to the manifest when `source: 'manifest'`. |
| `drive.apiKey` | Browser API key, restricted (see below). |
| `drive.folderId` | The ID from the folder's share link. A full share URL works too. |
| `access.enabled` | Turns the invite gate on or off. |
| `access.prefix` | localStorage namespace (`memories`). |
| `access.publicKey` | ECDSA P-256 public key (SPKI, base64). It can only check links, not make them. |
| `access.revoked` | Invite IDs (`jti`) turned off for everyone. |
| `defaultSkin` | The look a first-time visitor sees. |
| `helper` *(optional)* | Name shown on the admin page as the person who edits config.js. Defaults to "Kevin". |

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
     `custom.polecat.live/*` and `localhost/*` (add `127.0.0.1/*` too if you preview that way).
   - *API restrictions:* **Restrict key** → only **Google Drive API**.
   - Save. Restrictions can take a few minutes to take effect.
7. **Check it:** open `/memories/admin/`, expand **Check the Google Drive folder**, and paste the key and the folder link. It lists the chapters and photo counts, shows a few thumbnails, and gives you a snippet to copy.
8. **Edit `js/config.js`:** paste the snippet, which sets `sample: false`, `source: 'drive'` and `drive: { apiKey, folderId }`. Commit and push.

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
ADMIN_KEY_FILE=/path/outside/repo/memories-ADMIN-KEY.txt node memories/tools/test-gate-e2e.mjs
```

It mints tokens with the private key the same way `access.js` does. It checks the gate (no token, pasted link, raw code, bad and expired codes, `?invite=` in the URL) and the admin page (unlock, make a link, list, turn off, and a Drive check against a fake Drive API), then saves screenshots to `memories/tools/shots/`.

## Known caveats

- **lh3 / thumbnail URLs are not a documented Google API.** `lh3.googleusercontent.com/d/<id>` and `drive.google.com/thumbnail` work for publicly shared files today, but Google can rate-limit them (HTTP 429) or change them. That's why every photo carries a fallback. If both fail for a big album, the robust option is a one-time export of resized copies into `photos/` plus a manifest.
- **Downloads** go to `drive.google.com/uc?export=download`, which sends the original file as an attachment. The `download` attribute is ignored across origins, so the file name comes from Drive (it's the original name anyway). Very large files (>100 MB) get Google's virus-scan page, which isn't an issue for photos.
- **HEIC** files from iPhones are listed (they're `image/*`). The thumbnail URLs return a JPEG rendering, but the download is still HEIC, which older Windows PCs can't open. Scanning to JPG avoids this.
- The Drive API can't be reached from the build sandbox, so the Drive source was tested against a faithful fake of the API's responses and error bodies, not live Google.
