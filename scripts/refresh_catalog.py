#!/usr/bin/env python3
"""Weekly, bounded discovery of publicly downloadable MotionBGS MP4 references.

No third-party MP4 is hosted in this repository. Do not bypass paywalls/DRM.
A candidate is added only if source pages and both MP4 headers are readable.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = "https://motionbgs.com"
CATALOG = Path("wallpapers/catalog-v10.json")
SOURCES = (
    ("pokemon", "포켓몬", {"pokemon", "character", "2d"}),
    ("hello-kitty", "산리오", {"sanrio", "character", "cute", "2d"}),
    ("cat", "동물", {"animal", "cat", "cute", "2d"}),
    ("nature", "자연", {"background", "calm", "2d"}),
)
BAD = re.compile(r"pixel|8.bit|glitch|circuit|matrix|scary|terror|horror|violent|gore|gun|blood|nsfw", re.I)
MP4_ROUTE = re.compile(r"^/dl/(hd|mhd)/(\d{1,8})/?$")
PAGE_ROUTE = re.compile(r"^/[a-z0-9][a-z0-9-]{5,}/?$")
IGNORED = {"about", "privacy", "contact", "dmca", "terms", "categories", "guide"}
HEADERS = {"User-Agent": "Mozilla/5.0 (PocketFoldLive personal catalog discovery/1.0)"}
MAX_NEW_ARTWORKS = 8
MAX_CATALOG_ITEMS = 480


def get_page(session, url):
    response = session.get(url, timeout=18, headers=HEADERS)
    response.raise_for_status()
    if not response.url.startswith(ROOT + "/"):
        raise ValueError("unapproved host")
    return BeautifulSoup(response.text, "html.parser")


def list_candidates(soup):
    found = {}
    for link in soup.select("a[href]"):
        address = urljoin(ROOT, link.get("href", ""))
        parsed = urlparse(address)
        if parsed.netloc != "motionbgs.com" or not PAGE_ROUTE.fullmatch(parsed.path):
            continue
        slug = parsed.path.strip("/")
        if slug in IGNORED:
            continue
        label = link.get_text(" ", strip=True)
        image = link.find("img")
        title = (label if len(label) > 8 else
                 (image.get("alt", "") if image is not None else ""))
        title = re.sub(r"\s+(4K|HD)$", "", title, flags=re.I).strip()
        if len(title) < 7 or BAD.search(title):
            continue
        found[address] = title[:90]
    return found


def direct_link(soup, kind):
    for link in soup.select("a[href]"):
        path = urlparse(urljoin(ROOT, link.get("href", ""))).path
        match = MP4_ROUTE.fullmatch(path)
        if match and match.group(1) == kind:
            return urljoin(ROOT, path), match.group(2)
    return None


def mobile_source(desktop_soup):
    for link in desktop_soup.select("a[href]"):
        address = urljoin(ROOT, link.get("href", ""))
        p = urlparse(address)
        if p.netloc == "motionbgs.com" and p.path.startswith("/mobile/") and len(p.path) > 9:
            return address
    return None


def valid_mp4(session, url):
    # Inspect a few header bytes only: never download or mirror the media here.
    try:
        with session.get(url, headers={**HEADERS, "Range": "bytes=0-31"},
                         timeout=25, stream=True, allow_redirects=True) as response:
            if response.status_code not in (200, 206):
                return False
            if urlparse(response.url).scheme != "https":
                return False
            mime = response.headers.get("Content-Type", "").lower()
            if "text/html" in mime or "text/plain" in mime:
                return False
            total = response.headers.get("Content-Range", "").split("/")[-1]
            if not total.isdigit():
                total = response.headers.get("Content-Length", "")
            if total.isdigit() and not 80_000 <= int(total) <= 70_000_000:
                return False
            iterator = response.iter_content(chunk_size=32)
            data = next(iterator, b"")
            return len(data) >= 12 and data[4:8] == b"ftyp"
    except (requests.RequestException, OSError, ValueError):
        return False


def scene_tags(title, category):
    name = title.lower()
    if BAD.search(name):
        return []
    if any(x in name for x in ("rain", "night", "moon", "sleep", "dream", "stars", "cloud")):
        return ["NIGHT", "NORMAL"]
    if any(x in name for x in ("lightning", "glow", "power", "spark", "fire", "shine", "energy")):
        return ["CHARGING_START", "CHARGING", "FULL_BATTERY"]
    if any(x in name for x in ("forest", "lake", "water", "meadow", "ocean", "nature")):
        return ["NORMAL", "FULL_BATTERY"]
    return ["NORMAL", "FULL_BATTERY"]


def make_item(title, category, tags, kind, media_url, page, artwork_id):
    portrait = kind == "mhd"
    return {
        "id": f"motion-auto-{artwork_id}-{'portrait' if portrait else 'wide'}",
        "title": title + (" · 세로" if portrait else " · 펼침"),
        "category": category,
        "description": "정기 탐색 · 원본 사이트 제공 MP4 · 선택 후 개인 기기에 저장",
        "url": media_url,
        "sourcePage": page,
        "approxMB": 0,
        "mime": "video/mp4",
        "width": 720 if portrait else 1920,
        "height": 1280 if portrait else 1080,
        "credit": "MotionBGS · 원본 링크 (영상 재배포 없음)",
        "recommendedScenes": scene_tags(title, category),
        "orientation": "세로" if portrait else "가로",
        "style": "2D/3D",
        "quality": "원본 MP4 헤더 확인 · 재생 확인은 앱에서",
        "recommendable": True,
        "tasteTags": sorted(tags | ({"calm"} if category == "자연" else {"cute"})),
        "artworkKey": f"motionbgs:{artwork_id}",
        "recommendationGroup": category,
    }


def discover(session, catalog):
    items = catalog["items"]
    known_ids = {item["id"] for item in items}
    known_artwork = {item.get("artworkKey", "") for item in items}
    # Old records may use the unprefixed /mobile URL as the artwork identity.
    known_pages = set()
    for item in items:
        page = item.get("sourcePage", "")
        if page.startswith(ROOT + "/"):
            known_pages.add(page.replace(ROOT + "/mobile/", ROOT + "/"))
    new = []
    errors = 0
    for tag, category, tags in SOURCES:
        if len(new) >= MAX_NEW_ARTWORKS or len(items) + 2 * len(new) >= MAX_CATALOG_ITEMS:
            break
        for page_num in (1, 2):
            address = f"{ROOT}/tag:{tag}/" + (f"{page_num}/" if page_num > 1 else "")
            try:
                listings = list_candidates(get_page(session, address))
            except (requests.RequestException, ValueError) as exc:
                errors += 1
                print(f"Discovery source unavailable {address}: {type(exc).__name__} {str(exc)[:160]}")
                continue
            for source, title in listings.items():
                if (source in known_pages or BAD.search(title)
                    or len(new) >= MAX_NEW_ARTWORKS
                    or len(items) + 2 * len(new) >= MAX_CATALOG_ITEMS):
                    continue
                try:
                    page = get_page(session, source)
                    wide = direct_link(page, "hd")
                    mobile_page = mobile_source(page)
                    mobile = get_page(session, mobile_page) if mobile_page else None
                    portrait = direct_link(mobile, "mhd") if mobile is not None else None
                    if not wide or not portrait or wide[1] != portrait[1]:
                        continue
                    artwork_id = wide[1]
                    if f"motionbgs:{artwork_id}" in known_artwork:
                        known_pages.add(source)
                        continue
                    if not valid_mp4(session, wide[0]) or not valid_mp4(session, portrait[0]):
                        continue
                    pair = (
                        make_item(title, category, tags, "mhd", portrait[0], mobile_page, artwork_id),
                        make_item(title, category, tags, "hd", wide[0], source, artwork_id),
                    )
                    if any(item["id"] in known_ids for item in pair):
                        continue
                    new.append(pair)
                    known_artwork.add(f"motionbgs:{artwork_id}")
                    known_pages.add(source)
                    print(f"Accepted {artwork_id}: {title}")
                except (requests.RequestException, ValueError) as exc:
                    errors += 1
                    print(f"Skip {source}: {type(exc).__name__}")
                time.sleep(0.15)
    return new, errors


def self_test():
    soup = BeautifulSoup(
        '<a href="/rayquaza-flying-in-the-dark-sky">Rayquaza Flying in the Dark Sky 4K</a>'
        '<a href="/tag:pokemon/">Pokemon</a>'
        '<a href="/pixel-cat">Pixel Cat 4K</a>',
        "html.parser")
    assert list(list_candidates(soup)) == [ROOT + "/rayquaza-flying-in-the-dark-sky"]
    details = BeautifulSoup(
        '<a href="/dl/hd/1039">HD mp4</a><a href="/mobile/rayquaza-flying-in-the-dark-sky">For Mobile</a>',
        "html.parser")
    assert direct_link(details, "hd") == (ROOT + "/dl/hd/1039", "1039")
    assert mobile_source(details) == ROOT + "/mobile/rayquaza-flying-in-the-dark-sky"
    assert scene_tags("Pikachu Lightning", "포켓몬")[0] == "CHARGING_START"
    assert scene_tags("Pixel Cat", "동물") == []
    print("Local discovery parser self-tests passed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    session = requests.Session()
    found, errors = discover(session, data)
    print(f"Validated new artworks: {len(found)}, skipped page errors: {errors}")
    if not found:
        print("No validated additions; catalog unchanged.")
        return
    for pair in found:
        data["items"].extend(pair)
    if len(data["items"]) > 500:
        raise ValueError("catalog exceeds app 500-item limit")
    ids = [item["id"] for item in data["items"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate catalog IDs")
    data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if not args.dry_run:
        CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
        print(f"Published {len(found) * 2} new oriented variants; total {len(ids)}.")
    else:
        print("Dry run; no catalog change.")


if __name__ == "__main__":
    main()
