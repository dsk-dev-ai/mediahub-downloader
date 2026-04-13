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
