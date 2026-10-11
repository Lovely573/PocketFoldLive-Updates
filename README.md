# PocketFoldLive Updates

This is the **public APK-only distribution repository** for PocketFoldLive. The Android application source remains in a separate **private** repository and is not published here.

## Publishing a new version

1. Download the signed `PocketFoldLive.apk` from the **private project** CI build.
2. Open [Create a new release](https://github.com/Lovely573/PocketFoldLive-Updates/releases/new).
3. Enter a tag matching the Android `versionCode`, for example **`v26`** for build 26; a future build 27 should use **`v27`**.
4. Upload the signed file with exactly the name **`PocketFoldLive.apk`**.
5. Click **Publish release**, leaving it marked as the latest stable release (not a prerelease).

The app reads the public [latest Release API](https://api.github.com/repos/Lovely573/PocketFoldLive-Updates/releases/latest). It requires neither a GitHub account nor a token. Android will ask for confirmation before installation.

**Important:** Anyone with the public Release link can download its APK. Never commit private source code, credentials, or signing secrets here.
