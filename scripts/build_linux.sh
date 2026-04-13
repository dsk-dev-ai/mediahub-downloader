#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt pyinstaller

pyinstaller --noconfirm --windowed --name mediahub-downloader main.py

echo "Binary output is in dist/mediahub-downloader"
