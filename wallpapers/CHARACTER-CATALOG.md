# PocketFoldLive character catalog (build 62 / v0.25.0)

The app reads `wallpapers/catalog-v11.json` (128 publisher-linked variants).

## Personal use vs public distribution

- For the owner's private wallpaper use, publisher-hosted and publicly downloadable MP4 files may be linked and downloaded directly on demand. Do not mirror another creator's MP4 into this GitHub repository.
- A shared `recommendable` clip must have an identifiable original publisher page and a matching public download attachment/button. The Android client verifies the bytes (MP4), video dimensions, and orientation again before applying. Site-link inspection is **not** a promise of successful playback on every phone.
- A user may import a personally chosen original from the supported publisher pages without adding it to the curated catalog. This private import is not uploaded and does not turn into a public recommendation.
- Avoid download-protection bypasses, misleading ownership/license labels, circuit-board visuals, disorienting background motion, and obvious duplicates.
- If a requested theme has no compatible video for a scene/orientation, leave the configured wallpaper unchanged instead of filling it with another character. Keep a stable `artworkKey` across orientations so likes/dislikes remain unified.

## Character coverage in catalog v11

- Pokémon and Sanrio retain existing verified originals.
- Shin-chan: 8 public MP4 attachments are available from MINUHOME posts 6193 and 6797. Portrait classification is provisional, checked against the actual MP4 before applying on device.
- Detective Conan: one FHD landscape fan-made original, publisher download link at `https://motionbgs.com/detective-conan`.
- Doraemon: publisher links for Nature Adventure, Sky Adventure (portrait/landscape), and Galaxy Float.
- Hello Jadoo: no confirmed publicly downloadable MP4 source has been added, and no other character is substituted.

## Technical requirements

- Prefer 9:16 HD or better for the cover, 16:9 FHD for unfolded/landscape, H.264 MP4 loops, calm character motion.
- At most 500 catalog entries; preserve `id`, `artworkKey`, `recommendedScenes`, `orientation`, `mime`, `sourcePage`, `credit`.
- The catalog updater announces new verified entries without downloading every file. Broken publisher links should be fixed or removed.
- The revoked automated crawler remains disabled; do not bypass source website restrictions.
