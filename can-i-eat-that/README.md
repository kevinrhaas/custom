# 🍽️ Can I Eat That?

Take a picture of something and an AI tells you whether it's edible. Single self-contained
HTML page — no build step, no server, no backend. You bring your own **Claude** or **Gemini**
API key, which is sent straight from your browser to the AI provider.

## How it works

1. Pick a provider (Claude or Gemini) and paste the matching API key.
   - Claude: https://console.anthropic.com/settings/keys
   - Gemini: https://aistudio.google.com/app/apikey
2. Take or choose a photo.
3. Tap **Can I eat it?** — the image is sent to the AI, which replies with a verdict
   (✅ Yes / ⚠️ Caution / 🚫 No), the identified item, a confidence score, and reasoning.

Your API key is stored only in your browser's `localStorage` and is never sent anywhere
except directly to the provider's API.

### Models used
- **Claude:** `claude-haiku-4-5` (fast, low cost, vision-capable)
- **Gemini:** `gemini-2.5-flash`

Both are called directly from the browser. Claude calls include the
`anthropic-dangerous-direct-browser-access: true` header, which is what enables
browser-side requests to the Anthropic API.

## Run locally

It's just one file — open it directly, or serve the folder:

```bash
cd can-i-eat-that
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploy (GitHub Pages)

A workflow at `.github/workflows/deploy-can-i-eat-that.yml` publishes this folder to
GitHub Pages on every push to `main`. To enable it:

1. In the repo, go to **Settings → Pages → Build and deployment → Source** and select
   **GitHub Actions**.
2. Push to `main` (or run the workflow manually from the **Actions** tab).
3. The app goes live at `https://<your-username>.github.io/<repo>/`.

## ⚠️ Disclaimer

This is a fun demo, **not** food-safety advice. The AI can be wrong. Never rely on it for
mushrooms, wild plants, berries, or anything potentially toxic. When in doubt, don't eat it.
