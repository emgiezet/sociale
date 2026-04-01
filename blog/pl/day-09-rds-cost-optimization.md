---
day: 9
title: "Jak obniżyliśmy koszty AWS RDS o 35%: historia o widoczności, nie tylko optymalizacji"
pillar: Builder
language: pl
image: ../../images/day-09.jpg
image_unsplash_query: "cloud database optimization"
---

# Jak obniżyliśmy koszty AWS RDS o 35%: historia o widoczności, nie tylko optymalizacji

Gdy Twój rachunek w chmurze rośnie 40% rok do roku, podczas gdy baza użytkowników rośnie 30%, masz problem. Problem może polegać na tym, że Twoja infrastruktura jest droga. Albo może oznaczać, że koszty infrastruktury stały się niewidoczne.

Dla nas w Insly było tak i tak — ale głównie to drugie.

Ten artykuł dotyczy tego, jak zidentyfikowaliśmy i zajęliśmy się rzeczywistymi czynnikami kosztowymi w naszym setupie AWS RDS, oraz czego nauczyliśmy się o różnicy między optymalizacją a widocznością.

## Setup

Insly działa na PostgreSQL zarządzanym przez AWS RDS. Kiedy zaczęliśmy to dochodzenie, obsługiwaliśmy 150 000+ użytkowników na europejskich rynkach, z architekturą multi-tenant, gdzie dane każdej organizacji brokera są izolowane w tym samym klastrze bazodanowym.

Nasz setup RDS rozrósł się organicznie przez kilka lat. Mieliśmy wiele replik do odczytu, zautomatyzowane snapshoty, garść różnych klas instancji dla różnych środowisk i mieszankę konfiguracji. Rachunek był duży i rósł. Ale bardziej niż rozmiar, martwiło mnie to, że nikt w zespole nie potrafił precyzyjnie wyjaśnić, co napędza wzrost.

## Faza 1: Budowanie widoczności przed dotknięciem czegokolwiek

Pierwszą rzeczą, którą zrobiliśmy, nie była optymalizacja. Była to instrumentacja.

Spędziliśmy dwa tygodnie budując widoczność tego, co nasza infrastruktura RDS faktycznie robiła:

→ AWS Cost Explorer według zasobu, nie tylko według usługi — identyfikując, które konkretne instancje RDS odpowiadały za jaki ułamek kosztu
→ Metryki CloudWatch dla wykorzystania CPU, I/O i liczby połączeń na każdej instancji, zmapowane na porę dnia i dzień tygodnia
→ Dane wydajności zapytań z Performance Insights, pokazujące nam, które zapytania konsumowały najwięcej czasu bazodanowego
→ `pg_stat_statements` do uchwycenia wzorców zapytań przez pełny tydzień — obciążenia ubezpieczeniowe nie są jednorodne, a tydzień danych pokazał nam wzorce, które przegapilibyśmy w 2-godzinnym oknie profilowania
→ Podział magazynu: magazyn danych vs. magazyn kopii zapasowych vs. magazyn snapshotów

Ta praca z widocznością była upokarzająca. Znaleźliśmy rzeczy, o których nie wiedzieliśmy.

## Co znaleźliśmy

**Znalezisko 1: Zawsze włączone repliki do odczytu dla burstowych obciążeń**

Mieliśmy repliki do odczytu wielkości naszego szczytowego obciążenia, działające 24/7. Nasz rzeczywisty wzorzec obciążenia był wysoce burstowy — poranki w poniedziałki i okresy raportowania końca miesiąca były 5–10x większe od bazowego obciążenia. Poza tymi okresami repliki były wykorzystywane w 20–30%.

Rozwiązanie: auto-skalowanie replik Aurora, które pozwala instancjom repliki skalować się w górę podczas szczytów i w dół podczas poza-szczytowych. Implementacja zajęła jeden dzień. Wpływ na koszty był natychmiastowy.

**Znalezisko 2: Zapytania analityczne działające na primary**

Kilka wewnętrznych zadań raportowych działało na podstawowej instancji bazodanowej. Zostało to pierwotnie ustawione, bo „replika do odczytu czasami ma lag replikacji i potrzebujemy aktualnych danych." Zadania raportowe zostały ostatecznie zaplanowane na noce i weekendy, żeby zmniejszyć wpływ. Ale „noce i weekendy" oznaczały, że konkurowały z ruchem transakcyjnym końca-dnia-strefy-czasowej.

Przenieśliśmy je na dedykowaną replikę raportowania i zaakceptowaliśmy drobny lag replikacji. Dla raportów analitycznych lag kilku sekund nie ma znaczenia. Redukcja obciążenia na podstawowej instancji poprawiła wydajność transakcyjną i zmniejszyła wymagania klasy instancji.

**Znalezisko 3: Inflacja magazynu**

Automatyczne snapshoty były przechowywane przez 35 dni domyślnie. Mieliśmy stare środowiska deweloperskie i testowe, które zostały częściowo wycofane — instancje zostały usunięte, ale snapshoty pozostały. Mieliśmy ręczne snapshoty robione dla konkretnych sesji debugowania lata temu.

Łączny magazyn snapshotów: znacznie więcej niż nasz aktywny magazyn danych.

Wdrożenie polityki retencji snapshotów i czyszczenie starych snapshotów zajęło kilka godzin i nie miało żadnych operacyjnych wad.

**Znalezisko 4: Jedno katastrofalne zapytanie**

Najbardziej impaktującym pojedynczym znaleziskiem było zapytanie w naszej wielodostępnej warstwie dostępu do danych, które było, słowami inżyniera, który je ostatecznie naprawił, „zapytaniem, które miało doskonały sens przy 10 000 wierszy i było absolutnym nonsensem przy 10 milionach."

Zapytanie łączyło kilka tabel bez indeksu na kluczu złączenia. Kolumna była dodana przez migrację, która zaniedbała utworzenie indeksu. Przy naszej bieżącej skali to zapytanie wykonywało się przy każdym żądaniu do często używanej części aplikacji.

Dodanie brakującego indeksu zmniejszyło czas wykonania zapytania z ~800ms do ~12ms. Redukcja I/O była widoczna natychmiast w metrykach CloudWatch.

Trzy z naszych 10 najdroższych zapytań odpowiadały za ponad 60% obciążenia CPU. Dwa z tych trzech nie miały indeksów na filtrowanych kolumnach. Kod legacy, dodany lata temu, nigdy nieodwiedzony.

## Wyniki

W ramach tych interwencji nasze koszty RDS spadły o około 35% w ciągu 90 dni, bez redukcji wydajności ani niezawodności.

Ale prawdziwa lekcja to nie „optymalizuj zapytania bazodanowe" ani „przeglądaj retencję snapshotów."

## Prawdziwa lekcja

**Koszty rosną cicho, dopóki nie zbudujesz widoczności.**

Żaden z problemów, które znaleźliśmy, nie był nowy. Zawsze włączone repliki do odczytu były takie od ponad roku. Zapytania analityczne na primary były tam od dwóch lat. Osierocone snapshoty gromadziły się od kiedy zaczęliśmy używać RDS. Złe zapytanie zostało wprowadzone w migracji osiemnaście miesięcy wcześniej.

Nie znaleźliśmy ich, bo nie szukaliśmy. A nie szukaliśmy, bo nie mieliśmy dashboardów, alertów ani regularnego procesu przeglądu, który by je ujawnił.

Zmiana, która będzie miała najbardziej trwały wpływ, to nie żadna z konkretnych optymalizacji. To dodanie widoczności kosztów AWS do naszego cotygodniowego przeglądu inżynierskiego. Nie jako ćwiczenie compliance, ale jako sygnał: gdy koszty odbiegają od oczekiwań, coś w naszym systemie się zmieniło i chcemy to zrozumieć.

Ten sposób myślenia o widoczności — instrumentuj najpierw, rozumiej zanim optymalizujesz — to lekcja, którą przeniosę do każdego wyzwania infrastrukturalnego.

Jakie są czynniki kosztowe w Twoim setupie AWS, na które ostatnio nie patrzyłeś? Odpowiedź może Cię zaskoczyć.
