# MediaHub Downloader Developer Guide

This guide provides detailed information for developers working on MediaHub Downloader.

## Architecture Overview

MediaHub Downloader follows a modular architecture:

```
mediahub-downloader/
├── app/
│   ├── core/           # Core business logic
│   ├── services/       # External service integrations
│   ├── ui/             # User interface components
│   └── utils/          # Utility functions and helpers
├── tests/              # Test suite
├── config.py           # Configuration management
└── main.py             # Application entry point
```

### Core Modules

- **app.core.worker**: Handles download operations in separate threads
- **app.services.auth**: Manages user authentication with Supabase
- **app.services.payment**: Handles payment processing with Stripe and Razorpay
- **app.services.user**: Manages user session and preferences
- **app.utils.logger**: Structured logging system

### UI Components

- **app.ui.login_window**: Authentication interface
- **app.ui.main_window**: Main application interface with tabs for Home, Downloader, and Upgrade

## Key Features

### 1. Authentication System
- Supabase-based user authentication
- Development mode for testing without external services
- Session persistence

### 2. Download Engine
- Built on yt-dlp for robust video/audio downloading
- Multi-threaded downloads using QThread
- Progress tracking and status updates
- Format and quality selection

### 3. Payment Integration
- Stripe integration for credit card payments
- Razorpay integration for alternative payment methods
- Development mode for testing payments

### 4. Logging System
- Structured logging with file and console outputs
- Debug, info, warning, and error levels
- Contextual logging for debugging

## Configuration

Configuration is managed through environment variables and the `config.py` module:

- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon key
- `STRIPE_SECRET_KEY`: Stripe secret key
- `STRIPE_PRICE_ID`: Stripe price ID for PRO subscription
- `STRIPE_SUCCESS_URL`: URL for successful Stripe payments
- `STRIPE_CANCEL_URL`: URL for cancelled Stripe payments
- `RAZORPAY_KEY_ID`: Razorpay key ID
- `RAZORPAY_KEY_SECRET`: Razorpay key secret
- `SESSION_FILE`: File to store session data
- `DEV_MODE`: Enable development mode

## Testing

### Unit Tests
Located in the `tests/` directory, using pytest.

### Test Fixtures
Common test fixtures are in `tests/conftest.py`:

- `temp_dir`: Provides a temporary directory for tests
- `mock_env`: Sets up mock environment variables

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_config.py -v
```

## Continuous Integration

The project uses GitHub Actions for CI. Workflows are defined in `.github/workflows/`.

## Release Process

1. Update version number in appropriate files
2. Create a git tag for the release
3. Build distribution packages
4. Upload to PyPI (for Python packages) or release assets (for executables)
5. Create GitHub release with notes

## Internationalization

Currently, the application is English-only. Future versions may support multiple languages using Qt's translation system.

## Accessibility

The application follows basic accessibility guidelines:
- Sufficient color contrast
- Keyboard navigable interface
- Screen reader friendly labels

## Security Considerations

- Never hardcode secrets or API keys
- Use environment variables for sensitive data
- Validate and sanitize all user inputs
- Use prepared statements for database queries
- Keep dependencies updated