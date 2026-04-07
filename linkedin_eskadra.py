"""
Skrypt do wysyłania zaproszeń LinkedIn dla grupy Eskadra.
Pierwsze uruchomienie: zaloguj się ręcznie i zapisz sesję.
Kolejne uruchomienia: używa zapisanej sesji.

LinkedIn Connect to <a> (link), nie <button>!
Kliknięcie przenosi na stronę /preload/custom-invite/
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

STATE_FILE = Path(__file__).parent / "linkedin_state.json"

ESKADRA = [
    ("Dawid Ostrowski", "https://www.linkedin.com/in/avedave/"),
    ("Sławomir Sawicki", "https://www.linkedin.com/in/slawomir-sawicki/"),
    ("Paweł Świerblewski", "https://www.linkedin.com/in/pswierblewski/"),
    ("Dariusz Koryto", "https://www.linkedin.com/in/dariuszkoryto/"),
    ("Jan Andrusikiewicz", "https://www.linkedin.com/in/janandrusikiewicz/"),
    ("Piotr Tynecki", "https://www.linkedin.com/in/piotrtynecki/"),
    ("Bartłomiej Paszkiewicz", "https://www.linkedin.com/in/bartlomiej-paszkiewicz-phd-8aa4a6a8/"),
    ("Mateusz Jabłoński", "https://www.linkedin.com/in/mateusz-jab%C5%82o%C5%84ski-73a96ba9/"),
    ("Karol Kowal", "https://www.linkedin.com/in/kowal-karol/"),
    ("Grzegorz Wasilewski", "https://www.linkedin.com/in/legard77/"),
    ("Agnieszka Ratajska", "https://pl.linkedin.com/in/agnieszka-ratajska"),
    ("Marzena Halama", "https://www.linkedin.com/in/marzena-halama"),
    ("Marcin Rozmus", "https://www.linkedin.com/in/marcin-rozmus"),
    ("Emilian Suchecki", "https://www.linkedin.com/in/emilian-suchecki"),
    ("Damian Ślimak", "https://www.linkedin.com/in/damian-slimak"),
    ("Przemysław Szyc", "https://www.linkedin.com/in/pszyc/"),
    ("Anna Bober", "https://www.linkedin.com/in/anna-maria-bober/"),
    ("Krzysztof Ropiak", "https://www.linkedin.com/in/krzysztof-ropiak-66a573b4/"),
]


def save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.linkedin.com/login")
        print("\n>>> Zaloguj się ręcznie w oknie przeglądarki.")
        print(">>> Po zalogowaniu naciśnij Enter tutaj...\n")
        input()
        context.storage_state(path=str(STATE_FILE))
        print(f"Sesja zapisana do {STATE_FILE}")
        browser.close()


def send_invites():
    if not STATE_FILE.exists():
        print("Brak zapisanej sesji. Uruchamiam logowanie...")
        save_session()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=str(STATE_FILE))
        page = context.new_page()

        results = {"sent": [], "connected": [], "pending": [], "failed": []}

        for name, url in ESKADRA:
            print(f"\n--- {name} ---")
            print(f"    {url}")
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(5)

            # Scroll do góry
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)

            first_name = name.split()[0]
            last_name = name.split()[-1]

            try:
                # 1. Szukaj Connect jako <a> z aria-label (główny sposób)
                connect_link = None
                for name_part in [name, first_name, last_name]:
                    link = page.locator(
                        f"a[aria-label*='{name_part}'][aria-label*='connect' i]"
                    ).first
                    try:
                        if link.is_visible(timeout=1500):
                            connect_link = link
                            break
                    except:
                        pass

                # 2. Fallback: szukaj <a> z tekstem Connect w górnej części (y < 200)
                if not connect_link:
                    all_connect_links = page.locator("a:has-text('Connect')").all()
                    for link in all_connect_links:
                        try:
                            box = link.bounding_box(timeout=500)
                            if box and box["y"] < 200:
                                connect_link = link
                                break
                        except:
                            pass

                # 3. Fallback: szukaj <button> Connect (stary LinkedIn UI)
                if not connect_link:
                    for name_part in [name, first_name, last_name]:
                        btn = page.locator(
                            f"button[aria-label*='{name_part}'][aria-label*='connect' i]"
                        ).first
                        try:
                            if btn.is_visible(timeout=1000):
                                connect_link = btn
                                break
                        except:
                            pass

                # 4. Sprawdź menu "More"
                if not connect_link:
                    more_btn = page.locator("button[aria-label='More']").first
                    try:
                        box = more_btn.bounding_box(timeout=1000)
                        if box and box["y"] < 200 and more_btn.is_visible(timeout=500):
                            more_btn.click()
                            time.sleep(1)
                            # Szukaj Connect w dropdown
                            dropdown_connect = page.locator(
                                "a:has-text('Connect'), "
                                "[role='menuitem']:has-text('Connect')"
                            ).first
                            if dropdown_connect.is_visible(timeout=1500):
                                connect_link = dropdown_connect
                            else:
                                page.keyboard.press("Escape")
                    except:
                        pass

                if connect_link:
                    print(f"    Klikam Connect...")
                    # Overlay blokuje .click() — użyj href bezpośrednio lub force click
                    href = connect_link.get_attribute("href")
                    if href:
                        # Nawiguj bezpośrednio na stronę invite
                        if href.startswith("/"):
                            href = "https://www.linkedin.com" + href
                        page.goto(href, wait_until="domcontentloaded")
                    else:
                        # Fallback: force click (ignoruje overlay)
                        connect_link.click(force=True)
                    time.sleep(3)

                    # Po kliknięciu: może otworzyć stronę invite LUB modal
                    # Szukaj Send na stronie/modalu
                    sent = False
                    for selector in [
                        "button:has-text('Send without a note')",
                        "button:has-text('Send now')",
                        "button:has-text('Send invitation')",
                        "button:has-text('Send')",
                        "button:has-text('Wyślij bez notatki')",
                        "button:has-text('Wyślij')",
                        "[role='dialog'] button:has-text('Send')",
                        "a:has-text('Send without a note')",
                        "a:has-text('Send')",
                    ]:
                        try:
                            btn = page.locator(selector).first
                            if btn.is_visible(timeout=1000):
                                btn.click()
                                print(f"    Zaproszenie wysłane!")
                                results["sent"].append(name)
                                sent = True
                                break
                        except:
                            continue

                    if not sent:
                        # Debug: pokaż co jest na stronie
                        visible_btns = []
                        for el in page.locator("button, a").all():
                            try:
                                box = el.bounding_box(timeout=200)
                                if box and el.is_visible(timeout=200):
                                    text = el.inner_text(timeout=200).strip()[:40]
                                    aria = el.get_attribute("aria-label") or ""
                                    if text and box["y"] < 600:
                                        visible_btns.append(f"'{text}'")
                            except:
                                pass
                        print(f"    Elementy na stronie: {visible_btns[:15]}")
                        print(f"    URL: {page.url}")
                        print(f"    Nie znaleziono Send.")
                        results["failed"].append(name)
                else:
                    # Nie ma Connect - sprawdź czy już znajomy
                    msg_link = page.locator("a:has-text('Message')").first
                    try:
                        box = msg_link.bounding_box(timeout=1000)
                        if box and box["y"] < 200:
                            print(f"    Już w kontaktach (Message widoczny).")
                            results["connected"].append(name)
                            continue
                    except:
                        pass

                    print(f"    Brak Connect dla {name}.")
                    results["failed"].append(name)

            except Exception as e:
                print(f"    Błąd: {e}")
                results["failed"].append(name)

            # Pauza żeby LinkedIn nie zablokował
            time.sleep(3)

        # Podsumowanie
        print("\n" + "=" * 50)
        print("PODSUMOWANIE")
        print("=" * 50)
        if results["sent"]:
            print(f"\nWysłane ({len(results['sent'])}):")
            for n in results["sent"]:
                print(f"  + {n}")
        if results["connected"]:
            print(f"\nJuż w kontaktach ({len(results['connected'])}):")
            for n in results["connected"]:
                print(f"  = {n}")
        if results["pending"]:
            print(f"\nPending ({len(results['pending'])}):")
            for n in results["pending"]:
                print(f"  ~ {n}")
        if results["failed"]:
            print(f"\nNie udało się ({len(results['failed'])}):")
            for n in results["failed"]:
                print(f"  ! {n}")

        browser.close()


if __name__ == "__main__":
    send_invites()
