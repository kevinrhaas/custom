# Draft object tags and captions with Claude

This is an optional, local preparation step for the album. It sends selected scans
to Anthropic, saves suggested object/scene tags and short captions, then lets Lauren
review them in the album admin page. It does **not** identify people or publish
anything automatically. Face grouping is a separate browser-only tool.

The CLI needs **Node 20 or newer**, no packages, and an Anthropic API key with access
to a vision-capable Claude model. No live Anthropic request was made while building
this feature; its API, failure and resume paths were tested with mock responses.

## Prepare the scans

1. Open the album admin page and use **Download AI photo list**. This preserves the
   album photo IDs, including Google Drive IDs, so suggestions attach to the correct
   photo when imported.
2. Download the original photos you want to tag to a folder on your computer. Put
   the downloaded JSON list in that folder. Remove entries from the list for scans
   you do not want to send to Anthropic.
3. Check that each `path` matches the local filename. The admin export reports and
   omits ambiguous duplicate filenames; give those originals unique names and
   export again, or add their correct IDs and paths to the list manually. When
   different chapters reuse a filename, keep chapter subfolders and use paths such as
   `01 Early years/1948 - Wedding day.jpg`. Two different photo IDs cannot point to
   the same local file. Never change an `id` merely to match a filename.
4. Use JPG or PNG copies no larger than **5 MiB** and **8,000 pixels per side**.
   Smaller copies, around 1,600 pixels on the longest side, usually suffice for
   tagging and cost less to process. Keep original scans separately. Convert HEIC,
   GIF, WebP and PDF files to JPG/PNG before tagging.

The minimum input format is:

```json
{
  "photos": [
    { "id": "the-album-photo-id", "path": "1948 - Wedding day.jpg" }
  ]
}
```

An album manifest with a `photos` array, `id` and local `src` fields also works.
Paths are relative to the list's folder, unless `--root` supplies another folder.
Remote URLs are rejected; the CLI never downloads Drive files for you. Title and
caption fields in the exported list are not sent to the AI provider.

## Run locally

Keep `ANTHROPIC_API_KEY` in your local environment or use your password manager's
environment integration. Do not put it in `config.js`, the photo list, a command
line argument, a browser form, or any committed file.

From the repository root:

```sh
node memories/tools/tag-photos.mjs \
  --input /path/to/scans/photo-list.json \
  --out /path/to/private/album.drafts.json
```

Photos are sent to Anthropic when this command runs, and normal API charges apply.
Start with a list containing one test photo, check its result, then run a larger
batch. The CLI checks every local file's presence, image header, dimensions and
size before its first paid request. It keeps only one image in memory at a time.

The default model is `claude-haiku-4-5`. Override it with `--model MODEL` or
`ANTHROPIC_MODEL` if your account uses a different vision-capable Claude model.
The CLI always calls Anthropic's official Messages API over HTTPS; it does not
accept a custom endpoint. Run with `--help` to see the options.

Store `*.drafts.json` outside `site/` and outside Git. Drafts can contain mistaken
captions and are not ready for visitors. Output files are created with owner-only
permissions where the operating system supports them.

## Review, approve and save

1. In the admin photo review tool, import the draft JSON file.
2. Check the photo, edit its tags/caption and approve only what you want the album to
   see. A faint scan may produce no useful tags; omission is safer than a guess.
3. Choose **Save approved tags**. The album can now search those additions on
   this device and browser. No publishing token or file editing is needed.
   Download a backup if you want to keep another copy. To share labels with
   everyone, add them to the photos' Drive descriptions.

The draft format is:

```json
{
  "version": 1,
  "photos": {
    "the-album-photo-id": {
      "tags": ["wedding", "bouquet"],
      "caption": "Two people stand outdoors with a bouquet."
    }
  },
  "provenance": {
    "the-album-photo-id": {
      "sha256": "hash-of-local-image-bytes",
      "model": "claude-haiku-4-5",
      "promptVersion": 1
    }
  }
}
```

Provenance is for local resume only; the admin importer does not need it. The
output contains no API key, original image bytes, filenames, or face descriptors.
Human names can be added separately through the admin review tool or a `People:`
line in Drive. The AI pass is intentionally instructed not to name people or infer
relationships, sensitive traits, dates or places.

## Resume and failures

Every completed draft is saved atomically before the next request. Re-run the same
command after a failure: photos with matching image hash, model and prompt version
are skipped. Changing a file or model refreshes its draft; it does not change the
previously saved tags. To deliberately re-draft an unchanged image, use a new
output file or remove that photo's draft and provenance entries from a backup copy.

The output retains completed entries from earlier runs, including photos omitted
from a later input list. Use a new output file when starting a separate album or
when you want a clean subset. Never edit drafts in place while the CLI is running.

Rate limits and server errors get up to three retries with bounded waits. Network
failures are not automatically retried because a lost response may still have been
billed. Authentication, model access and malformed responses stop the run with a
short error, leaving earlier results intact. Check your key/account locally and
re-run; do not paste credentials into logs or chat.

Tests (no API key or network needed):

```sh
node --test memories/tools/test-ai-tagging.mjs
```

API reference: [Anthropic Messages](https://platform.claude.com/docs/en/api/messages).
