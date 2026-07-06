#!/usr/bin/env python3
"""
Instagram Unfollowers Detector
===============================
Detect who doesn't follow you back on Instagram.

Features:
  - Mutual followers
  - Users who don't follow you back
  - Users you don't follow back
  - Export to JSON / TXT / CSV

Two modes:
  1) Live — login via instaloader (auto-fetch)
  2) Export — from Instagram data export (no login)
"""

import json
import os
import csv
import sys
import time
from pathlib import Path
from collections import namedtuple

try:
    import instaloader
except ImportError:
    instaloader = None

# ─── Config ──────────────────────────────────────────────────────────
EXPORT_DIR = Path.home() / "Downloads" / "instagram-export"
OUTPUT_DIR = Path.home() / "instagram-unfollowers" / "results"

Category = namedtuple("Category", ["username", "full_name"])


# ═══════════════════════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════════════════════
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"


def banner():
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════╗
║        🔍 Instagram Unfollowers Detector 🔍          ║
║     Mutual | No Follow-Back | Not Following Back     ║
╚══════════════════════════════════════════════════════╝{C.RESET}
""")


# ═══════════════════════════════════════════════════════════════════════
# METHOD 1: INSTALOADER (Live API)
# ═══════════════════════════════════════════════════════════════════════
def fetch_via_instaloader(username):
    """Fetch followers & following via instaloader."""
    if instaloader is None:
        print(f"{C.RED}❌ instaloader not installed.{C.RESET}")
        print(f"   Run: pip install instaloader")
        return None, None

    print(f"{C.YELLOW}⏳ Fetching data for @{username}...{C.RESET}")
    print(f"{C.DIM}   (This may take a while for large accounts){C.RESET}")
    print(f"{C.DIM}   IG may ask for 2FA or email verification{C.RESET}\n")

    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
    )

    # ── Login ──
    try:
        session_file = Path.home() / ".instaloader" / f"session-{username}"
        if session_file.exists():
            L.load_session_from_file(username)
            print(f"{C.GREEN}✅ Loaded saved session{C.RESET}")
        else:
            print(f"{C.YELLOW}🔑 Login required (session saved for next time){C.RESET}")
            L.interactive_login(username)
    except Exception:
        print(f"{C.YELLOW}🔑 Login required...{C.RESET}")
        try:
            L.interactive_login(username)
        except Exception as e:
            print(f"{C.RED}❌ Login failed: {e}{C.RESET}")
            return None, None

    # ── Fetch profile ──
    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except Exception as e:
        print(f"{C.RED}❌ Could not fetch profile: {e}{C.RESET}")
        return None, None

    followers_set = {}
    following_set = {}

    # Followers
    print(f"{C.CYAN}📥 Fetching followers ({profile.followers} users)...{C.RESET}")
    try:
        count = 0
        for follower in profile.get_followers():
            followers_set[follower.username] = follower.full_name
            count += 1
            if count % 100 == 0:
                print(f"   ... {count} followers fetched")
            time.sleep(0.5)
    except Exception as e:
        print(f"{C.YELLOW}⚠️  Stopped at {count} followers: {e}{C.RESET}")
    print(f"{C.GREEN}   ✅ {len(followers_set)} followers loaded{C.RESET}\n")

    # Following
    print(f"{C.CYAN}📤 Fetching following ({profile.followees} users)...{C.RESET}")
    try:
        count = 0
        for followee in profile.get_followees():
            following_set[followee.username] = followee.full_name
            count += 1
            if count % 100 == 0:
                print(f"   ... {count} following fetched")
            time.sleep(0.5)
    except Exception as e:
        print(f"{C.YELLOW}⚠️  Stopped at {count} following: {e}{C.RESET}")
    print(f"{C.GREEN}   ✅ {len(following_set)} following loaded{C.RESET}\n")

    return followers_set, following_set


# ═══════════════════════════════════════════════════════════════════════
# METHOD 2: INSTAGRAM DATA EXPORT
# ═══════════════════════════════════════════════════════════════════════
def parse_json(filepath):
    """Parse Instagram data export JSON."""
    users = {}
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        if "string_list_data" in entry:
            for item in entry["string_list_data"]:
                uname = item.get("value", "")
                if uname:
                    users[uname] = entry.get("title", "")
        elif "href" in entry:
            href = entry.get("href", "")
            if "instagram.com/" in href or "/users/" in href:
                uname = href.rstrip("/").split("/")[-1]
                if uname:
                    users[uname] = entry.get("title", "")
    return users


def parse_csv(filepath):
    """Parse Instagram data export CSV."""
    users = {}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uname = (row.get("Username") or row.get("username")
                     or row.get("follower_username") or "")
            full = (row.get("Full Name") or row.get("full_name")
                    or row.get("follower_full_name") or "")
            if uname.strip():
                users[uname.strip()] = full.strip()
    return users


def find_export_files(export_dir):
    """Auto-detect follower/following files."""
    export_dir = Path(export_dir)
    followers_file = None
    following_file = None

    patterns_f = ["followers*.json", "followers*.csv", "follower_list*"]
    patterns_g = ["following*.json", "following*.csv", "following_list*"]

    for pat in patterns_f:
        files = sorted(export_dir.glob(pat))
        if files:
            followers_file = files[0]
            break

    for pat in patterns_g:
        files = sorted(export_dir.glob(pat))
        if files:
            following_file = files[0]
            break

    # Search in activity / connections subfolders
    for pattern in [
        "*/your_instagram_activity", "*/Connections",
        "*/connections",
    ]:
        for d in export_dir.glob(pattern):
            fl = list(d.glob("**/followers*"))
            fg = list(d.glob("**/following*"))
            if fl and not followers_file:
                followers_file = fl[0]
            if fg and not following_file:
                following_file = fg[0]

    return followers_file, following_file


def fetch_via_export():
    """Load from Instagram data export files."""
    print(f"{C.CYAN}📂 Looking in: {EXPORT_DIR}{C.RESET}\n")

    f_fl, f_fg = find_export_files(EXPORT_DIR)

    if not f_fl:
        path = input(f"{C.YELLOW}   Followers file not found. Path (Enter=skip): {C.RESET}").strip()
        if path:
            f_fl = Path(path)

    if not f_fg:
        path = input(f"{C.YELLOW}   Following file not found. Path (Enter=skip): {C.RESET}").strip()
        if path:
            f_fg = Path(path)

    if not f_fl or not f_fg:
        print(f"{C.RED}❌ Both followers AND following files are required.{C.RESET}")
        return None, None

    print(f"{C.GREEN}   ✅ Followers: {f_fl.name}{C.RESET}")
    print(f"{C.GREEN}   ✅ Following: {f_fg.name}{C.RESET}\n")

    loader = parse_json if str(f_fl).endswith(".json") else parse_csv
    followers_set = loader(f_fl)

    loader = parse_json if str(f_fg).endswith(".json") else parse_csv
    following_set = loader(f_fg)

    print(f"{C.GREEN}   📥 {len(followers_set)} followers loaded{C.RESET}")
    print(f"{C.GREEN}   📤 {len(following_set)} following loaded{C.RESET}\n")

    return followers_set, following_set


# ═══════════════════════════════════════════════════════════════════════
# ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
def analyze(followers_set, following_set):
    f_fl = set(followers_set.keys())
    f_fg = set(following_set.keys())

    mutual_un  = sorted(f_fl & f_fg)
    no_fb_un   = sorted(f_fg - f_fl)      # you follow, they don't
    not_fb_un  = sorted(f_fl - f_fg)      # they follow, you don't

    mutual = [Category(u, following_set.get(u, followers_set.get(u, ""))) for u in mutual_un]
    no_fb  = [Category(u, following_set.get(u, "")) for u in no_fb_un]
    not_fb = [Category(u, followers_set.get(u, "")) for u in not_fb_un]

    return mutual, no_fb, not_fb


# ═══════════════════════════════════════════════════════════════════════
# DISPLAY
# ═══════════════════════════════════════════════════════════════════════
def display_results(mutual, no_fb, not_fb):
    print(f"\n{C.BOLD}{'═' * 55}{C.RESET}")
    print(f"{C.BOLD}  📊 RESULTS SUMMARY{C.RESET}")
    print(f"{C.BOLD}{'═' * 55}{C.RESET}\n")

    total_fl = len(mutual) + len(not_fb)
    total_fg = len(mutual) + len(no_fb)

    print(f"  Total Followers : {C.CYAN}{total_fl}{C.RESET}")
    print(f"  Total Following : {C.CYAN}{total_fg}{C.RESET}")
    print(f"  Mutual          : {C.GREEN}{len(mutual)}{C.RESET}")
    print(f"  No Follow Back  : {C.RED}{len(no_fb)}{C.RESET}")
    print(f"  You Don't Follow: {C.YELLOW}{len(not_fb)}{C.RESET}")
    print()

    # ── No follow back ──
    print(f"{C.BOLD}{'─' * 55}{C.RESET}")
    print(f"{C.RED}  ❌ DON'T FOLLOW BACK ({len(no_fb)} users){C.RESET}")
    print(f"{C.DIM}     (You follow them, but they don't follow you){C.RESET}")
    print(f"{C.BOLD}{'─' * 55}{C.RESET}")
    if no_fb:
        for i, u in enumerate(no_fb, 1):
            nm = f" ({u.full_name})" if u.full_name else ""
            print(f"  {C.DIM}{i:3d}.{C.RESET} @{u.username}{C.DIM}{nm}{C.RESET}")
    else:
        print(f"  {C.GREEN}Everyone follows you back! 🎉{C.RESET}")
    print()

    # ── Not following back ──
    print(f"{C.BOLD}{'─' * 55}{C.RESET}")
    print(f"{C.YELLOW}  ⚠️  YOU DON'T FOLLOW BACK ({len(not_fb)} users){C.RESET}")
    print(f"{C.DIM}     (They follow you, but you don't follow them){C.RESET}")
    print(f"{C.BOLD}{'─' * 55}{C.RESET}")
    if not_fb:
        for i, u in enumerate(not_fb, 1):
            nm = f" ({u.full_name})" if u.full_name else ""
            print(f"  {C.DIM}{i:3d}.{C.RESET} @{u.username}{C.DIM}{nm}{C.RESET}")
    else:
        print(f"  {C.GREEN}You follow everyone back! 🎉{C.RESET}")
    print()

    # ── Mutual ──
    print(f"{C.BOLD}{'─' * 55}{C.RESET}")
    print(f"{C.GREEN}  ✅ MUTUAL FOLLOW ({len(mutual)} users){C.RESET}")
    print(f"{C.DIM}     (You follow each other){C.RESET}")
    print(f"{C.BOLD}{'─' * 55}{C.RESET}")
    if mutual:
        for i, u in enumerate(mutual[:20], 1):
            print(f"  {C.DIM}{i:3d}.{C.RESET} @{u.username}")
        if len(mutual) > 20:
            print(f"  {C.DIM}... and {len(mutual) - 20} more (see export files){C.RESET}")
    print()


# ═══════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════
def export_results(mutual, no_fb, not_fb):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")

    # JSON
    data = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "mutual": len(mutual),
            "no_follow_back": len(no_fb),
            "not_following_back": len(not_fb),
        },
        "no_follow_back": [
            {"username": u.username, "full_name": u.full_name} for u in no_fb
        ],
        "not_following_back": [
            {"username": u.username, "full_name": u.full_name} for u in not_fb
        ],
        "mutual": [
            {"username": u.username, "full_name": u.full_name} for u in mutual
        ],
    }
    jp = OUTPUT_DIR / f"unfollowers_{ts}.json"
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # TXT
    tp = OUTPUT_DIR / f"unfollowers_{ts}.txt"
    with open(tp, "w", encoding="utf-8") as f:
        f.write(f"Instagram Unfollowers Report — {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(f"Mutual: {len(mutual)} | No Follow Back: {len(no_fb)} | "
                f"You Don't Follow: {len(not_fb)}\n\n")
        f.write(f"❌ DON'T FOLLOW BACK ({len(no_fb)}):\n{'-' * 40}\n")
        for u in no_fb:
            f.write(f"  @{u.username}")
            if u.full_name:
                f.write(f"  ({u.full_name})")
            f.write("\n")
        f.write(f"\n⚠️  YOU DON'T FOLLOW BACK ({len(not_fb)}):\n{'-' * 40}\n")
        for u in not_fb:
            f.write(f"  @{u.username}")
            if u.full_name:
                f.write(f"  ({u.full_name})")
            f.write("\n")
        f.write(f"\n✅ MUTUAL ({len(mutual)}):\n{'-' * 40}\n")
        for u in mutual:
            f.write(f"  @{u.username}\n")

    # CSV
    cp = OUTPUT_DIR / f"no_follow_back_{ts}.csv"
    with open(cp, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["username", "full_name", "profile_url"])
        for u in no_fb:
            w.writerow([u.username, u.full_name,
                        f"https://instagram.com/{u.username}"])

    print(f"{C.GREEN}  💾 Exported:{C.RESET}")
    print(f"     📄 {jp}")
    print(f"     📄 {tp}")
    print(f"     📄 {cp}\n")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    banner()

    print(f"  {C.BOLD}Choose method:{C.RESET}")
    print(f"  {C.CYAN}[1]{C.RESET} 🔑 Login via Instagram (instaloader) — live data")
    print(f"  {C.CYAN}[2]{C.RESET} 📂 Load from Instagram data export — no login")
    print()

    choice = input(f"  Choice (1/2): ").strip()

    followers_set = None
    following_set = None

    if choice == "1":
        username = input(f"  Instagram username: ").strip()
        if not username:
            print(f"{C.RED}❌ Username required!{C.RESET}")
            return
        followers_set, following_set = fetch_via_instaloader(username)
    elif choice == "2":
        followers_set, following_set = fetch_via_export()
    else:
        print(f"{C.RED}❌ Invalid choice{C.RESET}")
        return

    if not followers_set or not following_set:
        print(f"{C.RED}❌ Could not load data.{C.RESET}")
        return

    print(f"{C.CYAN}🔍 Analyzing...{C.RESET}")
    mutual, no_fb, not_fb = analyze(followers_set, following_set)
    display_results(mutual, no_fb, not_fb)
    export_results(mutual, no_fb, not_fb)

    print(f"{C.BOLD}{'═' * 55}{C.RESET}")
    print(f"  {C.GREEN}Done! 🔍{C.RESET}")
    print(f"  {C.DIM}Results: {OUTPUT_DIR}{C.RESET}")
    print(f"{C.BOLD}{'═' * 55}{C.RESET}")


if __name__ == "__main__":
    main()
