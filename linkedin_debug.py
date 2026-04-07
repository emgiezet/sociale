"""Debug: dump HTML nagłówka profilu + wszystkie klikalne elementy."""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

STATE_FILE = Path(__file__).parent / "linkedin_state.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state=str(STATE_FILE))
    page = context.new_page()

    page.goto("https://www.linkedin.com/in/emilian-suchecki/", wait_until="domcontentloaded")
    time.sleep(5)

    # Scroll do góry żeby upewnić się że header jest widoczny
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1)

    page.screenshot(path="debug_profile_top.png", full_page=False)

    # 1. Dump HTML sekcji profilu (top card)
    print("\n=== HTML NAGŁÓWKA PROFILU ===\n")
    for selector in [
        ".pv-top-card",
        ".ph5.pb5",
        ".scaffold-layout__main .artdeco-card:first-child",
        "section.artdeco-card:first-of-type",
        "#profile-content",
    ]:
        try:
            el = page.locator(selector).first
            if el.is_visible(timeout=1000):
                html = el.inner_html(timeout=2000)
                # Wypisz tylko fragmenty z button/a/connect/message/follow
                lines = html.split(">")
                for line in lines:
                    lower = line.lower()
                    if any(k in lower for k in ["connect", "message", "follow", "pending", "button", "role=\"button", "aria-label"]):
                        print(f"  [{selector}] ...{line[:150]}>")
                print()
        except Exception as e:
            print(f"  [{selector}] nie znaleziono: {e}\n")

    # 2. Wszystkie elementy z role="button"
    print("\n=== ELEMENTY Z role='button' (widoczne) ===\n")
    role_btns = page.locator("[role='button']").all()
    for i, btn in enumerate(role_btns):
        try:
            if not btn.is_visible(timeout=300):
                continue
            tag = btn.evaluate("el => el.tagName")
            text = btn.inner_text(timeout=300).strip().replace("\n", " ")[:60]
            aria = btn.get_attribute("aria-label") or ""
            href = btn.get_attribute("href") or ""
            print(f"  [{i:3d}] <{tag}> text='{text}' aria='{aria[:60]}' href='{href[:60]}'")
        except:
            pass

    # 3. Linki w górnej części strony (pierwsze 500px)
    print("\n=== LINKI W GÓRNEJ CZĘŚCI (do 500px) ===\n")
    all_links = page.locator("a").all()
    for a in all_links:
        try:
            box = a.bounding_box(timeout=300)
            if box and box["y"] < 500:
                text = a.inner_text(timeout=300).strip().replace("\n", " ")[:60]
                href = a.get_attribute("href") or ""
                aria = a.get_attribute("aria-label") or ""
                cls = a.get_attribute("class") or ""
                if text or aria:
                    print(f"  y={box['y']:.0f} text='{text}' aria='{aria[:40]}' href='{href[:50]}' cls='{cls[:50]}'")
        except:
            pass

    # 4. Wszystkie klikalne elementy w top 500px
    print("\n=== KLIKALNE W TOP 500px (button, a, [role=button], div[onclick]) ===\n")
    clickables = page.locator("button, a, [role='button']").all()
    for el in clickables:
        try:
            box = el.bounding_box(timeout=200)
            if box and box["y"] < 500 and el.is_visible(timeout=200):
                tag = el.evaluate("el => el.tagName")
                text = el.inner_text(timeout=200).strip().replace("\n", " ")[:50]
                aria = el.get_attribute("aria-label") or ""
                if text or aria:
                    print(f"  y={box['y']:.0f} <{tag}> text='{text}' aria='{aria[:50]}'")
        except:
            pass

    print("\n>>> Screenshots: debug_profile_top.png")
    print(">>> Zamykam za 5s...")
    time.sleep(5)
    browser.close()
