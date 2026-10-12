# PocketFoldLive character wallpaper catalog policy

The app's catalog is `wallpapers/catalog-v10.json` (124 known entries as of v56).

- Prioritize character-focused animated wallpapers: Pokemon (Pikachu, Eevee, Gengar, Charmander), Shin-chan, Sanrio, and similarly cute cartoons.
- Do not add NASA documentaries, unrelated technical/circuit videos, or arbitrary media just to increase the total count.
- Only add a new candidate after manually checking the original publisher page, intended download link, MP4 playback, clip quality, aspect ratio and suitability for a wallpaper loop.
- The original media file remains on its publisher's website. GitHub contains only references/metadata, not repackaged media.
- Ensure the publisher permits personal download and the link does not circumvent technical restrictions. Remove broken or restricted links rather than retrying prohibited access.
- Use a stable `artworkKey` for portrait and landscape variants of the same artwork; user dislike/favorite preferences rely on it.
- Give each variant a unique `id`, and verify `recommendedScenes`, `orientation`, `mime`, tags, title, and source credit.
- Keep at most 500 catalog items, as the current client parser limits its input.
- After a verified catalog change, the in-app **catalog checker** detects genuinely new artwork and informs the user. It never downloads all video files in the background.

Automated source crawling was removed after MotionBGS returned HTTP 403 to GitHub Actions. Weekly source-discovery scheduling must not be re-enabled until a documented/authorized feed or API has been verified against real new character video entries.
