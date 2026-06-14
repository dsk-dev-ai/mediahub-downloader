# Ubuntu/Debian Package Build

1. Build binary with `./scripts/build_linux.sh`.
2. Copy binary to `deployment/linux-deb/mediahub-downloader/usr/local/bin/`.
3. Build package:

```bash
dpkg-deb --build deployment/linux-deb/mediahub-downloader
```

4. Install package:

```bash
sudo dpkg -i deployment/linux-deb/mediahub-downloader.deb
```

## IMPORTANT: Production Distribution Notes

For production distribution of Linux packages, you should consider:

1. **Code Signing**: While less common on Linux than Windows/macOS, you can sign your packages with GPG:
   - Create a GPG key for signing
   - Sign your .deb packages with `dpkg-sig` or similar tools
   - Distribute your public key so users can verify signatures

2. **Repository Signing**: If you host an APT repository, sign the repository metadata:
   - Sign Release files with GPG
   - Users add your public key to trust your repository

3. **Notarization**: Not applicable for Linux (this is a macOS-specific requirement)

4. **Alternative Distribution Formats**:
   - Consider Snapcraft or Flatpak for broader Linux distribution
   - These formats have their own signing and verification mechanisms
   - AppImage is another option with available signing tools