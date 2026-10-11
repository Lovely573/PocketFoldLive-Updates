# PocketFoldLive wallpaper gallery

The app reads the public catalog at `wallpapers/catalog-v1.json` each time the gallery opens.

## How to publish an eligible clip

1. Verify that the clip may be hosted and used in an app, including any underlying character/IP rights.
2. Publish the original animation or an Android-compatible MP4/WebM in a dedicated GitHub Release of this repository. Prefer 9:16 >=1080x1920 for the Fold cover, >=1080 on the shorter side for unfolded, or 16:9 1920x1080 for landscape. Prefer a subtle 3–10-second loop with the character moving while the background stays nearly fixed.
3. Add its metadata under `items` in `wallpapers/catalog-v1.json` with a unique `id`, a direct `https://github.com/Lovely573/PocketFoldLive-Updates/releases/download/.../file.mp4` URL, `mime`, `width`, `height`, `category`, `description`, and `credit`. The app only accepts release assets from this repository.
4. Existing installs pick up the new entry on the next gallery refresh; no APK update required.

The first file (`ranger-idle-cc0.gif`) is a **functional test clip**, not a preferred wallpaper recommendation. Original: [Ranger-Idle.gif by Kurt Kaiser](https://commons.wikimedia.org/wiki/File:Ranger-Idle.gif), CC0. Do not infer that publicly downloadable fan-made cartoon videos are automatically redistributable in this GitHub repository.

Apps retrieve and store a clip only after its preview is selected, and only overwrite the chosen scene/shape slot when the user confirms Apply.
