# MediaHub Downloader

![GitHub](https://img.shields.io/github/license/your-username/mediahub-downloader)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.11.1-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

A desktop media downloader built with `PySide6`, `yt-dlp`, and `FFmpeg`, now structured for production-style configuration and deployment.

## Features

- ✅ Login/signup flow (Supabase-backed or local dev mode)
- ✅ Media preview (title + thumbnail)
- ✅ MP4/MP3 downloads with quality selection
- ✅ Download progress, speed, ETA, and logs
- ✅ PRO upgrade page with payment integrations:
  - Stripe checkout session generation
  - Razorpay order generation
- ✅ Structured logging system
- ✅ Input validation and sanitization
- ✅ Comprehensive test suite
- ✅ Developer documentation and contributing guidelines
- ✅ Packaging helpers for:
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

Optional:
- `SESSION_FILE` (default: session.txt)
- `DEV_MODE` (default: false)

## Project Structure

```
mediahub-downloader/
├── app/                    # Main application code
│   ├── core/               # Core business logic
│   ├── services/           # External service integrations
│   ├── ui/                 # User interface components
│   └── utils/              # Utility functions and helpers
├── tests/                  # Test suite
├── deployment/             # Packaging and deployment scripts
├── scripts/                # Utility scripts
├── assets/                 # Static assets
├── config.py               # Configuration management
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── CONTRIBUTING.md         # Contribution guidelines
├── DEVELOPER_GUIDE.md      # Detailed developer documentation
└── README.md               # This file
```

## Testing

Run the test suite with:

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_config.py -v
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the powerful downloading engine
- [PySide6](https://doc.qt.io/qtforpython/) for the Python Qt bindings
- [Supabase](https://supabase.com) for the backend infrastructure
- [Stripe](https://stripe.com) and [Razorpay](https://razorpay.com) for payment processing