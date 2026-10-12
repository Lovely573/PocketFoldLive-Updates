#!/usr/bin/env python3
"""Find NASA-hosted, directly playable MP4 video links for a personal wallpaper catalog.

Only URL metadata goes to GitHub. Nothing is downloaded into the repository.
NASA attribution and source links are retained, and questionable third-party
copyright markers are excluded. Missing/unsuitable media is safely skipped.
"""
from __future__ import annotations
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import os
from pathlib import Path
from urllib.parse import quote, urlparse
import requests

CATALOG = Path("wallpapers/catalog-v10.json")
SEARCH = "https://images-api.nasa.gov/search"
MAX_NEW = 4
MAX_SIZE = 70_000_000
QUERIES = ["aurora", "earth timelapse", "nebula animation", "northern lights", "galaxy visualization"]
GOOD = re.compile(r"aurora|timelapse|time.lapse|animation|visualization|nebula|earth from|northern lights|night lights|space view", re.I)
BAD = re.compile(r"podcast|webcast|lecture|explainer|interview|episode|news|live:|live stream|q&a|press conference|rocket launch|rollout|report|talk|briefing|behind the scenes|science live|tutorial|copyright", re.I)
HEADERS = {"User-Agent": "PocketFoldLive wallpaper discovery/1.0 (github.com/Lovely573/PocketFoldLive-Updates)"}


def secure_url(address):
    if not isinstance(address, str):
        return None
    address = requests.utils.requote_uri(address.replace("http://images-assets.nasa.gov/", "https://images-assets.nasa.gov/"))
    info = urlparse(address)
    if info.scheme != "https" or info.netloc != "images-assets.nasa.gov" or info.query or info.fragment:
        return None
    return address


def size_and_header(session, url):
    try:
        with session.get(url, headers={**HEADERS, "Range": "bytes=0-31"}, stream=True, timeout=20) as r:
            if r.status_code != 206 or r.headers.get("Content-Type", "").split(";")[0] != "video/mp4":
                return None
            if not secure_url(r.url):
                return None
            content_range = r.headers.get("Content-Range", "")
            matched = re.fullmatch(r"bytes 0-31/(\d+)", content_range)
            if matched is None:
                return None
            length = int(matched.group(1))
            if not 80_000 < length <= MAX_SIZE:
                return None
            data = next(r.iter_content(chunk_size=32), b"")
            if len(data) < 12 or data[4:8] != b"ftyp":
                return None
            return length
    except requests.RequestException:
        return None


def characteristics(session, url, expected_size):
    # Validate from the real local bytes; ffprobe HTTP directly is not reliable on
    # every CDN and can falsely reject otherwise playable MP4s.
    if not shutil.which("ffprobe"):
        print("NASA validator unavailable: ffprobe is not installed")
        return None
    fd, name = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)
    try:
        total = 0
        with session.get(url, headers=HEADERS, stream=True, timeout=40) as response:
            response.raise_for_status()
            if not secure_url(response.url):
                print("NASA full download redirected away:", response.url[:150])
                return None
            with open(name, "wb") as target:
                for chunk in response.iter_content(chunk_size=128 * 1024):
                    total += len(chunk)
                    if total > MAX_SIZE:
                        return None
                    target.write(chunk)
        if abs(total - expected_size) > 128:
            print("NASA full download length mismatch:", total, expected_size, url[-60:])
            return None
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
             "-of", "json", name],
            capture_output=True, text=True, timeout=25, check=True,
        )
        info = json.loads(p.stdout)
        stream = next(s for s in info.get("streams", []) if s.get("codec_type") == "video")
        width, height = int(stream.get("width", 0)), int(stream.get("height", 0))
        duration = float(info.get("format", {}).get("duration") or 0)
        print("NASA inspected:", width, height, round(duration, 1), url[-65:])
        if width < 960 or height < 540 or width <= height or duration <= 0 or duration > 240:
            return None
        return width, height, duration
    except (requests.RequestException, OSError, subprocess.SubprocessError, StopIteration, ValueError, KeyError) as exc:
        print("NASA probe failed:", type(exc).__name__, str(exc)[:90])
        return None
    finally:
        os.remove(name)



def candidates(session, query):
    try:
        r = session.get(SEARCH, params={"q": query, "media_type": "video", "page_size": 15},
                        timeout=25, headers=HEADERS)
        r.raise_for_status()
        return r.json().get("collection", {}).get("items", [])
    except (requests.RequestException, ValueError) as exc:
        print("NASA source unavailable:", query, type(exc).__name__)
        return []


def discover():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    old_ids = {x["id"] for x in data["items"]}
    old_artwork = {x.get("artworkKey", "") for x in data["items"]}
    session = requests.Session()
    accepted = []
    seen = set()
    for query in QUERIES:
        if len(accepted) >= MAX_NEW or len(data["items"]) + len(accepted) >= 480:
            break
        for item in candidates(session, query):
            if len(accepted) >= MAX_NEW or len(data["items"]) + len(accepted) >= 480:
                break
            meta = (item.get("data") or [{}])[0]
            source_id = meta.get("nasa_id", "")
            title = meta.get("title", "").strip()
            description = str(meta.get("description", ""))[:1200]
            # The source library can include third-party media; reject explicit copyright signs.
            if not source_id or source_id in seen or not GOOD.search(title) or BAD.search(title) or "copyright" in description.lower():
                continue
            print("NASA possible:", title[:80])
            seen.add(source_id)
            artwork = "nasa:" + source_id
            if artwork in old_artwork:
                continue
            asset_url = secure_url(item.get("href", ""))
            if not asset_url or not asset_url.endswith("/collection.json"):
                continue
            try:
                response = session.get(asset_url, timeout=20, headers=HEADERS)
                response.raise_for_status()
                files = response.json()
            except (requests.RequestException, ValueError):
                continue
            mp4s = []
            for original in files:
                link = secure_url(original)
                if link and link.lower().endswith(".mp4") and "/video/" in link:
                    mp4s.append(link)
            # Choose a smaller HD derivative; original media may be hundreds of megabytes.
            def priority(link):
                return next((i for i, suffix in enumerate(("~medium.mp4", "~large.mp4", "~mobile.mp4", "~small.mp4", "~preview.mp4"))
                             if link.endswith(suffix)), 10)
            for link in sorted(set(mp4s), key=priority):
                length = size_and_header(session, link)
                if length is None:
                    print("NASA candidate invalid size/header:", link[-75:])
                    continue
                info = characteristics(session, link, length)
                if info is None:
                    print("NASA candidate invalid characteristics:", link[-75:], length)
                    continue
                width, height, duration = info
                hashed = hashlib.sha256(source_id.encode()).hexdigest()[:16]
                video_id = "nasa-auto-" + hashed
                if video_id in old_ids:
                    break
                is_night = bool(re.search(r"aurora|night|nebula|galaxy", title, re.I))
                rec = {
                    "id": video_id,
                    "title": "NASA · " + title[:90],
                    "category": "우주·자연",
                    "description": "NASA 원본 영상 · 개인용 우주/자연 배경 · " +
                                   str(round(duration)) + "초 · 출처 확인 가능",
                    "url": link,
                    "sourcePage": "https://images.nasa.gov/details/" + quote(source_id, safe=""),
                    "approxMB": round(length / 1_000_000, 2),
                    "mime": "video/mp4",
                    "width": width,
                    "height": height,
                    "credit": "NASA Image and Video Library · 영상 원본 사이트",
                    "recommendedScenes": ["NIGHT", "NORMAL"] if is_night else ["NORMAL"],
                    "orientation": "가로",
                    "style": "원본 영상",
                    "quality": f"MP4 · {width}×{height} · 원본 크기/재생 길이 검사",
                    "recommendable": True,
                    "tasteTags": ["background", "calm", "space"],
                    "artworkKey": artwork,
                    "recommendationGroup": "우주·자연",
                }
                accepted.append(rec)
                old_ids.add(video_id)
                old_artwork.add(artwork)
                print("Validated NASA HD wallpaper:", title, width, height,
                      round(duration, 1), "seconds", round(length / 1_000_000, 2), "MB")
                break
    if accepted:
        data["items"].extend(accepted)
        data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("NASA validated new artwork:", len(accepted), "total catalog items:", len(data["items"]))


if __name__ == "__main__":
    discover()
