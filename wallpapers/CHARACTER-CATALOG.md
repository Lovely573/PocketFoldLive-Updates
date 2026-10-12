# PocketFoldLive character catalog (build 62 / v0.25.0)

The app reads `wallpapers/catalog-v12.json` (129 publisher-linked variants).

## Personal use vs public distribution

- For the owner's private wallpaper use, publisher-hosted and publicly downloadable MP4 files may be linked and downloaded directly on demand. Do not mirror another creator's MP4 into this GitHub repository.
- A shared `recommendable` clip must have an identifiable original publisher page and a matching public download attachment/button. The Android client verifies the bytes (MP4), video dimensions, and orientation again before applying. Site-link inspection is **not** a promise of successful playback on every phone.
- A user may import a personally chosen original from the supported publisher pages without adding it to the curated catalog. This private import is not uploaded and does not turn into a public recommendation.
- Avoid download-protection bypasses, misleading ownership/license labels, circuit-board visuals, disorienting background motion, and obvious duplicates.
- If a requested theme has no compatible video for a scene/orientation, leave the configured wallpaper unchanged instead of filling it with another character. Keep a stable `artworkKey` across orientations so likes/dislikes remain unified.

## Character coverage in catalog v12

- Pokémon and Sanrio retain existing verified originals.
- Shin-chan: 8 public MP4 attachments are available from MINUHOME posts 6193 and 6797. Portrait classification is provisional, checked against the actual MP4 before applying on device.
- Detective Conan: one FHD landscape original at `https://motionbgs.com/detective-conan` and one separate Conan/Haibara FHD/HEVC MP4 original at `https://www.desktophut.com/Detective-Conan-Ai-Haibara-Anime-Live-Wallpaper`.
- DesktopHut originals are downloaded from the creator page's public original-MP4 button to the device. This is not a claim that every Android video decoder supports HEVC; the app previews before allowing Apply.
- Doraemon: publisher links for Nature Adventure, Sky Adventure (portrait/landscape), and Galaxy Float.
- Hello Jadoo: no confirmed publicly downloadable MP4 source has been added, and no other character is substituted.
- Keep `catalog-v11.json` unchanged so users with build 62 do not fetch new source URLs that its original-link allowlist cannot handle.

## Technical requirements

- Prefer 9:16 HD or better for the cover, 16:9 FHD for unfolded/landscape, H.264 MP4 loops, calm character motion.
- At most 500 catalog entries; preserve `id`, `artworkKey`, `recommendedScenes`, `orientation`, `mime`, `sourcePage`, `credit`.
- The catalog updater announces new verified entries without downloading every file. Broken publisher links should be fixed or removed.
- The revoked automated crawler remains disabled; do not bypass source website restrictions.

## Catalog v13: source-only Shin-chan videos

- Added two independently published original source pages: [Shin-chan Flashlight Search](https://www.chicswipe.com/live-wallpaper/shin-chan-flashlight-search-live-wallpaper) and [Shin-chan Cherry Blossom Blowing Bubbles](https://www.chicswipe.com/live-wallpaper/shin-chan-cherry-blossom-blowing-bubbles-live-wallpaper). Their pages display a Download Video action.
- These two are `recommendable: false` until their exact media URLs, downloaded MP4 bytes and portrait video dimensions have been checked. The in-app gallery exposes an original-page download button and the personal media picker. Do not represent these as ready-to-play auto-theme videos.
- Built-in same-character fallback in build 64: when a scene has fewer than two matching artworks of the selected theme and screen orientation, users can enable other compatible artworks from that same theme. Each card identifies actual scene matches vs same-theme stand-ins. This does not increase the number of unique videos.
- Earlier `catalog-v11.json` and `catalog-v12.json` are intentionally retained for older app builds.
