@echo off
setlocal

if not exist .venv (
  py -m venv .venv
)

call .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt pyinstaller

pyinstaller --noconfirm --windowed --name MediaHubDownloader main.py

echo Build complete. EXE output is in dist\\MediaHubDownloader
echo.
echo IMPORTANT: For production distribution, you should:
echo 1. Sign the executable with a code signing certificate
echo 2. Consider using tools like SignTool (Windows) for signing
echo 3. For more advanced distribution, consider using WiX or similar tools
echo 4. Notarization is not applicable for Windows (it's a macOS requirement)
endlocal