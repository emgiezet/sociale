---
day: 27
title: "Architektura Insly: Budowanie wielodostępnej platformy ubezpieczeniowej na dużą skalę"
pillar: Builder
language: pl
image: ../../images/day-27.jpg
image_unsplash_query: "system architecture diagram enterprise"
---

# Architektura Insly: Budowanie wielodostępnej platformy ubezpieczeniowej na dużą skalę

Większość postów o architekturze opisuje idealny system. Ten opisuje system, który faktycznie mamy — jak ewoluował, decyzje, które go ukształtowały i co zrobilibyśmy inaczej zaczynając od zera dziś.

Insly to oprogramowanie do zarządzania ubezpieczeniami obsługujące 150 000+ użytkowników na rynkach europejskich. To nie jedna aplikacja — to platforma łącząca brokerów ubezpieczeniowych z ubezpieczycielami, systemami zarządzania polisami, procesorami płatności i ubezpieczającymi. Architektura odzwierciedla tę złożoność.

## Cztery systemy

Platforma Insly ma cztery główne komponenty. Rozumienie, jak się łączą, wyjaśnia gdzie żyją najtrudniejsze problemy.

**QMT: Narzędzie Zarządzania Ofertami**

Główny przepływ pracy brokera: żądaj ofert, porównuj produkty, wystawiaj polisy. Tu brokerzy spędzają czas. Integruje się z systemami ubezpieczycieli — część z nich to nowoczesne API REST, część to SOAP z 2008 roku, który pozostanie SOAP dopóki ubezpieczyciel nie zdecyduje się przebudować swojego systemu rdzeniowego, co nie nastąpi prędko.

Złożoność tutaj to heterogeniczność integracji. Każdy ubezpieczyciel mówi nieco innym dialektem. Ta sama konceptualna operacja — "daj mi ofertę dla tego ryzyka" — mapuje się na różne schematy danych, różne podejścia do uwierzytelniania, różne konwencje obsługi błędów, różne oczekiwania SLA. Warstwa integracji w QMT jest jedną z najbardziej pracochłonnych w utrzymaniu części platformy, bo dostosowuje jednolity interfejs do heterogenicznego zewnętrznego świata.

**Calcly: Silnik Kalkulacyjny**

Składki ubezpieczeniowe są kalkulowane, nie pobierane. Calcly zawiera logikę kalkulacyjną: tabele taryfowe, czynniki ratingowe, reguły zniżek, dostosowania specyficzne dla kraju.

To jest deterministyczne, wersjonowane i audytowalne. Obliczenie uruchomione dla konkretnego wejścia w konkretnym czasie musi zawsze produkować ten sam wynik — bo ubezpieczający jest rozliczany na jego podstawie, regulatorzy mogą go audytować i spory są rozwiązywane z odwołaniem do niego.

Calcly to też część systemu, której AI nie dotyka. Obliczenia składek, ustalenia zakresu ubezpieczenia i interpretacje regulacyjne nie są operacjami probabilistycznymi. Wymagają dokładnej, audytowalnej logiki. LLM nie powinno być proszonym o te obliczenia. Ta granica jest jawna i egzekwowana na poziomie architektury.

**Insly3: Platforma Rdzeniowa**

Zarządzanie cyklem życia polisy, generowanie dokumentów, śledzenie roszczeń, rekordy klientów. System ewidencji.

Insly3 jest najstarszą warstwą, nosi najwięcej logiki domenowej i jest gdzie wyzwania jakości danych są najbardziej widoczne. To też miejsce gdzie ciężar RODO jest największy: retencja danych, prawo do usunięcia, logi dostępu, wymogi minimalizacji danych. Każdy element danych osobowych w systemie — imiona ubezpieczających, adresy, informacje finansowe, deklaracje zdrowotne — ma konkretne obowiązki obsługi, które są zarządzane tutaj.

Dla obciążeń AI, Insly3 jest głównym źródłem danych. Nasze systemy RAG pytają dokumenty polis przechowywane w Insly3. Nasze funkcje ekstrakcji AI pracują z danymi polis. To tworzy skrzyżowanie compliance: systemy AI muszą obsługiwać dane Insly3 zgodnie z tymi samymi ograniczeniami RODO, które stosują się do samego Insly3.

**InslyPay: Warstwa Płatności**

Mobilne przetwarzanie płatności składek ubezpieczeniowych. Zgodne z PSD2. Łączy się z bramkami płatności, obsługuje uzgadnianie, wiąże płatności z rekordami polis.

InslyPay jest zbudowane jako modularne, bo regulacje płatności zmieniają się szybciej niż regulacje polis. Logika biznesowa dla nieudanych płatności — okresy prolongaty, zapobieganie wygaśnięciu, ścieżki przywrócenia — to logika domenowa ubezpieczeń, która musiała być zbudowana jawnie, nie odziedziczona od ogólnej infrastruktury płatności.

## Fundament wielodostępności

Wielodostępność to pierwsza decyzja architektoniczna, która kształtuje wszystko inne. W Insly każda organizacja brokera ubezpieczeniowego działa jako całkowicie izolowany tenant.

To nie jest tylko wymóg bezpieczeństwa. To wymóg zaufania biznesowego. Brokerzy ubezpieczeniowi są często bezpośrednimi konkurentami. Portfel biznesowy brokera — jego relacje z klientami, jego portfolio, jego strategie cenowe — to jego główny zasób konkurencyjny. Wiarygodność systemu zależy od gwarancji, że te dane są prawdziwie izolowane.

Wdrażamy wielodostępność głównie przez bezpieczeństwo na poziomie wierszy na PostgreSQL, z identyfikacją tenanta propagowaną przez warstwę serwisową aplikacji. Każde zapytanie do bazy danych jest automatycznie ograniczone do uwierzytelnionego tenanta. Nie ma ścieżek kodu, które mogą uzyskać dostęp do danych między tenantami bez jawnego omijania kontekstu tenanta.

Dla obciążeń AI, wielodostępność dodaje złożoność. Indeksy wektorowe są albo per-tenant (pełna izolacja, wyższy koszt przechowywania) albo współdzielone z filtrowaniem metadanych (niższy koszt, bardziej złożona weryfikacja izolacji). Używamy indeksów per-tenant dla wrażliwych dokumentów ubezpieczeniowych i współdzielonych z filtrowaniem dla niewrażliwych danych referencyjnych.

## Integracja zdarzeniowa

We wczesnej historii platformy, integracje były wdrażane jako synchroniczne wywołania z rdzeniowej aplikacji. Zdarzenie wiązania polisy uruchamiało sekwencyjny łańcuch: powiadom ubezpieczyciela, wygeneruj dokument, zaksięguj, wyślij e-mail potwierdzający. Gdy jakikolwiek krok zawodził, cały łańcuch zawodził.

Migrowaliśmy do integracji zdarzeniowej przez kilka lat. Obecna architektura: gdy znaczące zdarzenie biznesowe ma miejsce — polisa związana, płatność otrzymana, roszczenie złożone — zdarzenie jest publikowane na naszym szynie zdarzeń. Systemy downstream konsumują zdarzenia niezależnie, z własną logiką ponownych prób i obsługą błędów.

Korzyści są znaczące. Awarie integracji są izolowane: jeśli generowanie dokumentu zawodzi, polisa jest nadal związana i wpis księgowy jest nadal zaksięgowany. Nowe integracje mogą być dodawane bez modyfikowania rdzeniowego przepływu zarządzania polisami. Przetwarzanie może być skalowane niezależnie na podstawie wolumenu.

Koszty są realne. Spójna finalność wymaga akceptacji, że systemy downstream mogą być chwilowo niezsynchronizowane z rdzeniowym stanem bazy danych. Ewolucja schematu zdarzeń wymaga starannego wersjonowania. Debugowanie problemów między systemami wymaga śledzenia zdarzeń przez logi wielu serwisów.

Dla większości naszych przypadków integracji, korzyści zdecydowanie przewyższają koszty.

## Warstwa AI: Addytywna, Nie Transformatywna

Kiedy zacząliśmy dodawać możliwości AI, podjęliśmy przemyślaną decyzję architektoniczną: AI będzie addytywna, a nie transformatywna. Nie zastąpimy istniejącej architektury AI. Dodamy możliwości AI jako opcjonalne warstwy z ścieżkami fallback.

Ta decyzja wynikała ze świadomości ryzyka operacyjnego. System produkcyjny z 150 000 dokumentów miesięcznie nie może sobie pozwolić, by nieudana integracja AI wpływała na rdzeniową funkcjonalność. Utrzymując możliwości AI w oddzielnych, niezależnie wdrażalnych serwisach, możemy stopniowo wprowadzać funkcje AI, szybko wycofywać je jeśli działają słabo i oceniać je pod kątem konkretnych przypadków użycia.

Architektura: oddzielne serwisy Python dla obciążeń ML, połączone z rdzeniową aplikacją Symfony przez wewnętrzne API. Flagi funkcji w warstwie aplikacji określają, kiedy możliwości AI są używane versus fallback do ścieżek nie-AI. Każda funkcja AI ma odpowiadający jej fallback nie-AI.

Nigdy nie mieliśmy incydentu produkcyjnego, w którym awaria serwisu AI wpłynęłaby na rdzeniową funkcjonalność transakcji ubezpieczeniowych.

## Co Zrobilibyśmy Inaczej

Zaczynając od zera z obecną wiedzą:

**Wcześniejsza inwestycja w event sourcing.** Nasza obecna architektura przechwytuje zdarzenia dla celów integracji, ale nie dla pełnej rekonstrukcji ścieżki audytu. W kontekście ubezpieczeniowym, możliwość rekonstrukcji dokładnego stanu polisy w dowolnym historycznym momencie byłaby wartościowa dla compliance i rozwiązywania sporów. Retrofitowanie event sourcingu jest drogie.

**Bardziej agresywne API-first od pierwszego dnia.** Spędziliśmy lata z aplikacją webową jako specjalnym przypadkiem omijającym warstwę API. Budowanie wszystkiego jako konsumenta API od początku zaoszczędziłoby kilka projektów refaktoringu.

**Wcześniejsza infrastruktura testowa wielodostępności.** Testowanie izolacji wielodostępności jest trudne i nie zainwestowaliśmy w dedykowaną infrastrukturę testową dla niej wystarczająco wcześnie.

Rzeczy, które zrobiliśmy dobrze: architektura integracji zdarzeniowej, fundament Symfony — jego stabilność i kompozycyjność służyły nam dobrze przez ponad dekadę — i addytywne podejście do możliwości AI.

Architektura to sekwencja decyzji, nie projekt, który był dobry od początku. Najbardziej użyteczną rzeczą, którą mogę podzielić, jest rozumowanie stojące za decyzjami, nie tylko same decyzje. Rozumowanie to co się przenosi do nowych kontekstów.
