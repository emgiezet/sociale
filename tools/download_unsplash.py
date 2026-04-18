#!/usr/bin/env python3
"""Download Unsplash images for LinkedIn posts using Playwright.

Usage:
    # Download all images:
    python tools/download_unsplash.py

    # Download specific range:
    python tools/download_unsplash.py --from 31 --to 46

    # Download single day:
    python tools/download_unsplash.py --day 5

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import os
import time
from playwright.sync_api import sync_playwright

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")

PHOTOS = {
    # === Day 01-30 ===
    "day-01": "https://unsplash.com/photos/turned-on-gray-laptop-computer-XJXWbfSo2f0",
    "day-02": "https://unsplash.com/photos/red-and-white-stop-road-sign-5EvOYDTolzE",
    "day-03": "https://unsplash.com/photos/silver-laptop-computer-near-notebook-ck0i9Dnjtj0",
    "day-04": "https://unsplash.com/photos/road-signs-point-toward-different-directions-and-destinations-pBYkX7uJd4s",
    "day-05": "https://unsplash.com/photos/printed-sticky-notes-glued-on-board-zoCDWPuiRuA",
    "day-06": "https://unsplash.com/photos/a-broken-glass-window-with-a-crack-in-it-XkYAM21-HXI",
    "day-07": "https://unsplash.com/photos/a-blueprint-of-a-building-with-a-bunch-of-windows-URnyBZCnlIs",
    "day-08": "https://unsplash.com/photos/the-polish-flag-waves-over-beautiful-turquoise-water-X9k_aHW1dbs",
    "day-09": "https://unsplash.com/photos/a-calculator-sitting-on-top-of-a-pile-of-money-zR7nFjjIAWE",
    "day-10": "https://unsplash.com/photos/open-notebook-with-pen-and-pencils-on-desk-n9AaeihA9HI",
    "day-11": "https://unsplash.com/photos/person-typing-on-smartphone-with-ai-chatbot-on-screen-CaRba5ZXJTQ",
    "day-12": "https://unsplash.com/photos/developer-working-on-multiple-screens-in-a-dark-office-v9iowyOH7QQ",
    "day-13": "https://unsplash.com/photos/white-and-black-usb-cable-2H06IWVVpiQ",
    "day-14": "https://unsplash.com/photos/two-women-talking-at-a-desk-in-an-office-aoweP90-XwM",
    "day-15": "https://unsplash.com/photos/blue-and-white-flags-on-pole-0NRkVddA2fw",
    "day-16": "https://unsplash.com/photos/speaker-presenting-on-stage-to-an-audience-AsxOJcsaR4g",
    "day-17": "https://unsplash.com/photos/a-person-looking-stressed-at-a-laptop-in-an-office-hjh8cCOUtoo",
    "day-18": "https://unsplash.com/photos/statue-of-lady-justice-holding-sword-and-scales-i3nVp_sBZbE",
    "day-19": "https://unsplash.com/photos/tools-neatly-organized-in-a-toolbox-WXoHE4GibYo",
    "day-20": "https://unsplash.com/photos/business-people-in-a-meeting-around-a-table-fQf9XTYNmQU",
    "day-21": "https://unsplash.com/photos/0IVop5v4MMU",
    "day-22": "https://unsplash.com/photos/team-brainstorming-with-sticky-notes-on-glass-wall-UtIr_UaiDmg",
    "day-23": "https://unsplash.com/photos/graphs-of-performance-analytics-on-a-laptop-screen-JKUTrJ4vK00",
    "day-24": "https://unsplash.com/photos/code-is-displayed-on-a-black-screen-HnfsOiBpzU0",
    "day-25": "https://unsplash.com/photos/cd7i9vYIyeY",
    "day-26": "https://unsplash.com/photos/a-person-writing-on-a-notebook-with-a-pen-ZDDF6LMvh2s",
    "day-27": "https://unsplash.com/photos/a-drawing-of-a-floor-plan-of-a-building--StEPF2CK2M",
    "day-28": "https://unsplash.com/photos/blue-and-yellow-star-flag-8Yw6tsB8tnc",
    "day-29": "https://unsplash.com/photos/a-computer-circuit-board-with-a-brain-on-it-_jg8xh2SsXQ",
    "day-30": "https://unsplash.com/photos/a-woman-explaining-something-to-a-group-of-people-XH8chLuj02g",

    # === Day 31-46 ===
    # Day 31 — Warsztaty AI dla zespołu — dlaczego
    "day-31": "https://unsplash.com/photos/a-group-of-people-sitting-at-desks-in-front-of-a-whiteboard-F60486ko0r0",
    # Day 32 — Zakres warsztatów AI
    "day-32": "https://unsplash.com/photos/two-people-drawing-on-whiteboard-26MJGnCM0Wc",
    # Day 33 — Opór przy legacy kodzie
    "day-33": "https://unsplash.com/photos/vintage-computer-monitor-and-disk-drives-CkvEbt2U-70",
    # Day 34 — Nowe projekty z AI od dnia zero
    "day-34": "https://unsplash.com/photos/rocket-ship-launching-during-daytime-Ptd-iTdrCJM",
    # Day 35 — Wyniki warsztatów — twarde dane
    "day-35": "https://unsplash.com/photos/a-computer-screen-with-a-bunch-of-data-on-it-bf9sZBcGQl4",
    # Day 36 — Warsztaty AI — oferta
    "day-36": "https://unsplash.com/photos/three-men-sitting-while-using-laptops-and-watching-man-beside-whiteboard-wD1LRb9OeEo",
    # Day 37 — Wybór modelu LLM do RAG — koszty vs benchmarki
    "day-37": "https://unsplash.com/photos/online-checkout-screen-with-payment-details-and-shopping-cart-sr927_EVdqk",
    # Day 38 — Chunking danych w RAG
    "day-38": "https://unsplash.com/photos/stack-of-jigsaw-puzzle-pieces-3y1zF4hIPCg",
    # Day 39 — Realne koszty RAG — 3 architektury
    "day-39": "https://unsplash.com/photos/a-calculator-sitting-on-top-of-a-pile-of-money-zR7nFjjIAWE",
    # Day 40 — HyDE — vector search nie łączy kontekstu
    "day-40": "https://unsplash.com/photos/cable-network-M5tzZtFCOfs",
    # Day 41 — RAPTOR — chunking po 300 tokenów traci kontekst
    "day-41": "https://unsplash.com/photos/a-broken-glass-window-with-a-crack-in-it-XkYAM21-HXI",
    # Day 42 — RAG maskuje halucynacje
    "day-42": "https://unsplash.com/photos/man-with-white-face-mask-HvqKdTFLkfw",
    # Day 43 — RAG polecił produkt konkurencji
    "day-43": "https://unsplash.com/photos/curve-road-signage-5QvsD0AaXPk",
    # Day 44 — RAG product modeling
    "day-44": "https://unsplash.com/photos/a-drawing-of-a-plan-of-a-building-kl5hdStOjFk",
    # Day-45 — Ultimate RAG prompt halucynuje w 40%
    "day-45": "https://unsplash.com/photos/person-standing-in-front-of-optical-illusion-wall-ODbOdeQVF2Q",
    # Day 46 — RAG kosztuje 500 albo 15 000 miesięcznie
    "day-46": "https://unsplash.com/photos/a-grocery-store-window-displaying-price-tags-YdHEHUzI_no",
}


def extract_image_url(page):
    """Extract the main image URL from an Unsplash photo page."""
    og = page.query_selector('meta[property="og:image"]')
    if og:
        url = og.get_attribute("content")
        if url and "images.unsplash.com" in url:
            base = url.split("?")[0]
            return f"{base}?w=1200&q=80&fit=crop"

    for sel in [
        'img[data-test="photo-grid-masonry-img"]',
        'img[srcset*="images.unsplash.com"]',
        'img[src*="images.unsplash.com"]',
    ]:
        img = page.query_selector(sel)
        if img:
            src = img.get_attribute("src") or img.get_attribute("srcset")
            if src and "images.unsplash.com" in src:
                base = src.split("?")[0]
                return f"{base}?w=1200&q=80&fit=crop"

    return None


def download_photos(day_filter=None, day_from=None, day_to=None):
    photos = PHOTOS

    if day_filter is not None:
        key = f"day-{day_filter:02d}"
        if key in photos:
            photos = {key: photos[key]}
        else:
            print(f"Day {day_filter} not found in PHOTOS dict")
            return
    elif day_from is not None and day_to is not None:
        photos = {
            k: v for k, v in photos.items()
            if day_from <= int(k.split("-")[1]) <= day_to
        }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )

        total = len(photos)
        success = 0
        failed = []

        for i, (day, url) in enumerate(sorted(photos.items()), 1):
            target = os.path.join(IMAGES_DIR, f"{day}.jpg")
            print(f"[{i}/{total}] {day}...", end=" ", flush=True)

            try:
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(3)
                page.wait_for_load_state("networkidle", timeout=15000)

                img_url = extract_image_url(page)
                if not img_url:
                    print("SKIP (no image URL found)")
                    failed.append(day)
                    page.close()
                    continue

                response = page.request.get(img_url)
                if response.ok:
                    with open(target, "wb") as f:
                        f.write(response.body())
                    size_kb = os.path.getsize(target) / 1024
                    print(f"OK ({size_kb:.0f} KB)")
                    success += 1
                else:
                    print(f"FAIL (HTTP {response.status})")
                    failed.append(day)

                page.close()
                time.sleep(1)

            except Exception as e:
                print(f"ERROR: {e}")
                failed.append(day)
                try:
                    page.close()
                except:
                    pass

        browser.close()

        print(f"\n=== Done: {success}/{total} downloaded ===")
        if failed:
            print(f"Failed: {', '.join(failed)}")
            print("Open these manually:")
            for day in failed:
                print(f"  {day}: {PHOTOS[day]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Unsplash images for LinkedIn posts")
    parser.add_argument("--day", type=int, help="Download single day (e.g. --day 5)")
    parser.add_argument("--from", dest="day_from", type=int, help="Start day (e.g. --from 31)")
    parser.add_argument("--to", dest="day_to", type=int, help="End day (e.g. --to 46)")
    args = parser.parse_args()

    if args.day:
        download_photos(day_filter=args.day)
    elif args.day_from and args.day_to:
        download_photos(day_from=args.day_from, day_to=args.day_to)
    else:
        download_photos()
