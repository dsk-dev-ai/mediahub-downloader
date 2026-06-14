#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt pyinstaller

pyinstaller --noconfirm --windowed --name mediahub-downloader main.py

echo "Binary output is in dist/mediahub-downloader"
echo ""
echo "IMPORTANT: For production distribution, you should consider:"
echo "1. Code signing is less common on Linux but can be done with GPG signatures"
echo "2. For AppImage distribution, consider using appimagetool"
echo "3. For Snap/Flatpak distribution, those frameworks have their own signing mechanisms"
echo "4. Notarization is not applicable for Linux (it's a macOS requirement)"