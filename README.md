# MediaHub Downloader

A desktop media downloader built with `PySide6`, `yt-dlp`, and `FFmpeg`, now structured for production-style configuration and deployment.

## Features
- Login/signup flow (Supabase-backed or local dev mode)
- Media preview (title + thumbnail)
- MP4/MP3 downloads with quality selection
- Download progress, speed, ETA, and logs
- PRO upgrade page with payment integrations:
  - Stripe checkout session generation
  - Razorpay order generation
- Packaging helpers for:
  - Windows `.exe` builds
  - Ubuntu/Debian `.deb` builds

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Environment Variables
All configuration is read from `.env` via `config.py`.

Never commit your real `.env` file. `.gitignore` is configured to keep it private.

Required for production usage:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_PRICE_ID`
- `STRIPE_SUCCESS_URL`
- `STRIPE_CANCEL_URL`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

## Packaging
- Windows: `scripts/build_windows.bat`
- Linux binary: `./scripts/build_linux.sh`
- Debian package skeleton: `deployment/linux-deb/`

## Status
✅ Production-ready baseline architecture (config, payments, packaging scripts, and safer defaults).
