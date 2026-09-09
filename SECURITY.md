# Security

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Report via a
[private security advisory](https://github.com/dsk-dev-ai/mediahub-downloader/security/advisories)
on GitHub. We aim to acknowledge reports within 3 business days.

## Current posture

- The app uses `yt-dlp` to download public media URLs. Only download content
  you have the right to access and store; respect site terms and creators'
  rights.
- Supabase/Stripe/Razorpay credentials are read from environment variables
  (`.env`). Never commit a `.env` file.
- When installed via `pip`, prefer installing inside a virtual environment.