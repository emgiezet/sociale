---
day: 27
title_pl: "Rzadki wgląd w architekturę prawdziwej platformy InsurTech."
pillar: Builder
format: Technical
scheduled_date: 2026-04-30
posting_time: "07:30 CET"
hashtags: ["#InsurTech", "#ArchitekturaOprogramowania", "#AI", "#SystemDesign", "#EnterpriseEngineering"]
image: ../images/day-27.jpg
cta: "Zapisz dla inspiracji architekturą InsurTech"
blog_url: "https://mmx3.pl/blog/day-27-insly-architecture"
---

Rzadki wgląd w architekturę prawdziwej platformy InsurTech.

Większość dyskusji o architekturze InsurTech jest teoretyczna. Oto jak to faktycznie wygląda, gdy budujesz oprogramowanie dla brokerów ubezpieczeniowych w całej Europie, z ograniczeniami RODO, wymogami regulacyjnymi wielu krajów i systemami AI ułożonymi na szczycie legacy logiki domenowej.

Platforma Insly ma cztery główne systemy. Są odrębne, ale połączone — i rozumienie, jak się łączą, wyjaśnia, gdzie żyją najtrudniejsze problemy.

**QMT: Narzędzie Zarządzania Ofertami**

Główny przepływ pracy brokera: żądaj ofert, porównuj produkty, wystawiaj polisy. Tu brokerzy spędzają czas. Integrujemy się z API ubezpieczycieli — część z nich to nowoczesne REST, część to SOAP z 2008 roku i pozostanie SOAP dopóki ubezpieczyciel nie przebuduje swojego systemu rdzeniowego (co nie nastąpi prędko 😬). Złożoność tutaj to heterogeniczność integracji. Każdy ubezpieczyciel mówi nieco innym dialektem.

**Calcly: Silnik Kalkulacyjny**

Składki ubezpieczeniowe są kalkulowane, nie pobierane. Calcly zawiera logikę kalkulacyjną: tabele taryfowe, czynniki ratingowe, reguły zniżek, dostosowania specyficzne dla kraju. Deterministyczne, wersjonowane i audytowalne. Zmiana reguły kalkulacyjnej ma implikacje regulacyjne. To nie jest miejsce, gdzie AI ma improwizować 🚫

**Insly3: Platforma Rdzeniowa**

Zarządzanie cyklem życia polisy, generowanie dokumentów, śledzenie roszczeń, rekordy klientów. System ewidencji. Najstarsze warstwy, najwięcej logiki domenowej i największe wyzwania jakości danych. Tutaj też ciężar RODO jest największy: retencja danych, prawo do usunięcia, logi dostępu.

**InslyPay: Warstwa Płatności**

Mobilne przetwarzanie płatności składek. Zgodne z PSD2. Łączy się z bramkami płatności, obsługuje uzgadnianie, wiąże płatności z rekordami polis. Zbudowałem to jako modularne, bo regulacje płatności zmieniają się szybciej niż regulacje polis.

**Gdzie pasuje AI:**

AI nie przepisuje żadnego z tych systemów. AI siedzi obok nich. Moje systemy RAG pytają dokumenty polis przechowywane w Insly3. Funkcje AI wydobywają informacje z danych QMT, by asystować brokerom w przepływach pracy. Calcly pozostaje deterministyczny. Nie proszę LLM o obliczanie składek.

Zasada: AI augmentuje warstwę ludzką. Systemy ewidencji pozostają czyste, wersjonowane i audytowalne.

**Najtrudniejsze problemy architektoniczne w InsurTech nie są techniczne. Chodzi o wiedzenie, które części systemu nigdy nie powinny być dotykane przez AI.**

Zapisz dla inspiracji architekturą InsurTech, a jeśli budujesz coś podobnego, chętnie porównam notatki.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-27-insly-architecture

#InsurTech #ArchitekturaOprogramowania #AI #SystemDesign #EnterpriseEngineering
