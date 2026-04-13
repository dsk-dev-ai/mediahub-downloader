@echo off
setlocal

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt pyinstaller

pyinstaller --noconfirm --windowed --name MediaHubDownloader main.py

echo Build complete. EXE output is in dist\MediaHubDownloader
