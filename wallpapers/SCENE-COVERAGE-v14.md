# Situation coverage · PocketFoldLive catalog v14 (2026-10-13)

The production catalog retains the original 157 IDs and adds 26 separate **publisher-origin mobile MP4** records, for 183 items. The added source links were extracted from actual MotionBGS mobile-page download buttons (MP4, 720×1280), not guessed download IDs.

## Minimum goal: 20 distinct artworks per situation per display

Situation | Native portrait artworks | Native landscape artworks | Distinct artworks usable if cross-aspect sharing is enabled
--- | ---: | ---: | ---:
Normal | 44 | 44 | 58
Night | 39 | 34 | 48
Low battery | 27 | 15 | 28
Critical battery | 20 | 7 | 20
Charging start | 23 | 10 | 23
Charging in progress | 24 | 12 | 25
Charging complete | 26 | 13 | 26

**Counting rule:** source URL must be a direct, user-initiated MP4, `recommendable=true`, and the requested situation must be explicitly in `recommendedScenes`. A portrait and landscape variant sharing one `artworkKey` count as one original; videos for unrelated situations do not count. Manual source-page downloads, existing local files and user-rejected videos do not artificially increase totals.

**Important scope:**
- Landscape *native* originals fall below 20 for several states. The 20-artwork goal there depends on a compatible APK with cross-aspect sharing and natural-aspect FIT/crop. Current stable build 76 does **not** provide that complete recommendation behavior; it is developed in private build 78.
- User dislikes, character/theme filters, broken remote sources or video codecs can lower the *actually available* count. Counts are catalog-level candidates, not a guarantee that all users will see 20 after their own filters.
- In charging situations, the 13 brighter newly added entries are accurately tagged as **atmosphere supplements only**, not actual charge-progress percentage, power transition, or battery glyph videos. The 13 darker entries similarly support quiet/low/critical mood; no assertion of real system measurements in the clip.
- The source remains a URL reference, not media bytes hosted in the repo. Playback, exact dimensions, redirect validation and preview are checked by the Android app at download time. Copyright holders retain their content.
- Retain the verified build-76 Android wallpaper Canvas/decoder-surface fix. Do not change live player internals to increase catalog counts.

## Priority of future discovery
1. Discover independent 9:16 and 16:9 MP4 publisher download buttons with in-app preview support.
2. Diversify by art, situation, theme and original motion rather than aliasing a source.
3. Only after direct sources are exhausted, list publisher attachment posts or manual-download/import sources separately.
