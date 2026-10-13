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


## 2026-10-13 direct-media expansion (catalog-v14 compatible)

- Added **22 new directly linked MP4 media variants from 17 distinct scenes** (16 landscape, 6 portrait) without renaming/removing the original 135 catalog IDs. Public live catalog now contains **157** entries.
- Expanded the selection with Stitch (including Night Stars), Kirby (sleeping and regular), Pokemon (Sobble, Umbreon, Pikachu rain), Snoopy, Totoro, We Bare Bears, Animal Crossing, Adventure Time, Gravity Falls, Cinnamoroll, Tom and Jerry, and relaxing cat/frog scenes.
- **First choice**: publisher-provided `motionbgs.com/dl/hd/{id}` or `/dl/mhd/{id}` MP4 links that the app can download and preview after the user taps the choice.
- **Secondary fallback only**: original-post file attachments (Shin-chan), or source-page-only references needing manual download and subsequent private import. Do not replace automatically playable candidates with page-only placeholders simply to inflate counts.
- No third-party MP4 bytes or character artwork are copied into this repository. These entries are source links, not licenses or claims of ownership. Respect publisher permissions and use for the user's personal wallpaper.
- Catalogue page/download-button URLs and the site's published dimension labels were reviewed. Actual Android decode, content and source availability still require the app's post-download checks.
- To support old app builds, this update intentionally keeps `schemaVersion: 14` and the same live URL. A new app build is **not** required to see newly published choices after refreshing the catalogue; offline devices may temporarily use their prior cached list.
- For future app builds, thumbs-up/down per *exact media ID* avoids treating a portrait and landscape variant as the same choice. Distinct variants still share an artworkKey for grouping in automatic theme rotation.

## Final character video expansion · catalog freeze (2026-10-13)

**User decision:** stop additional video discovery after Shin-chan, Detective Conan, and Tom & Jerry search; prioritize improvements to UX, recommendations, performance, media preview, error handling and stability.

- Shin-chan: 8 original MP4 attachments across MINUHOME publisher posts are already listed for app-resolved download, plus 2 Chicswipe original-page references requiring user-driven import. Search found other pages but not a **new, nonduplicate, freely accessible and approved direct MP4**; thus no unverifiable new automatic catalog IDs were created.
- Detective Conan: 2 direct original sources remain in catalog (MotionBGS Detective Conan and DesktopHut Conan/Haibara). New search results primarily led back to the same files or separately distributed/paid wallpaper sets; no new confirmed direct free MP4 was added.
- Tom & Jerry: original MotionBGS live wallpaper `tom-and-jerry` is a genuinely distinct artwork from the existing `tom-and-jerry-old-tv` item. Add both directly downloadable versions from original publisher links: **HD 1920×1080 MP4** at `/dl/hd/8321` and **Mobile HD 720×1280 MP4** at `/dl/mhd/8321`. Both use artworkKey `motionbgs:8321` so they count as **one unique artwork** across screen orientations.
- Catalog total: **204 → 206 file variants** (one new artwork). Existing media IDs/URLs and votes/settings are never reset or modified.
- No third-party media is copied to GitHub; direct media URLs are used only for user-requested preview/download. On-device byte, codec, resolution, rights and availability checks still matter.

### Next, do not add more videos

1. Verify private build 78 on Fold8 and retain the known-good build 76 live wallpaper decoder Surface/Canvas producer fix. Do **not** automatically publish a private APK until it works on the target device.
2. Improve recommendations: likes/dislikes consistently filtered across all picker modes; distinct artwork first, native aspect first; clear direct vs manual source status; progress through candidate rotation with no surprising repeat.
3. Improve navigation and UX: a simpler situation list (normal day/night, battery low/critical, charging start/in-progress/complete); folded/unfolded with stable status labels and one-current-video preview.
4. Optimize catalog caching, load-once preview and error recovery: no thumbnail flicker or repeated download on scroll, preserve current selection if an origin goes offline, display download failure reasons without replacing wallpaper.
5. Test fold/unfold and charge/discharge end-to-end before the next public update.

This document records the scope stop. Future work should prioritize application functionality, not increasing the number of candidate videos.
