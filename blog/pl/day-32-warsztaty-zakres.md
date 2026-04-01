---
day: 32
title: "Dokładny zakres warsztatów AI dla 15 programistów (i dlaczego podzieliłem je na dwie ścieżki)"
pillar: Educator
language: pl
image: ../../images/day-32.jpg
image_unsplash_query: "workshop agenda whiteboard developers team"
---

# Dokładny zakres warsztatów AI dla 15 programistów (i dlaczego podzieliłem je na dwie ścieżki)

Kiedy decydowałem się poprowadzić warsztaty AI dla piętnastu programistów w Insly, pierwsza decyzja projektowa była tą, którą według mnie większość ludzi podejmuje źle: nie próbowałem prowadzić jednych ujednoliconych warsztatów dla wszystkich.

Podzieliłem je na dwie ścieżki.

To jest pełne rozwinięcie: co było w programie, dlaczego podział, jak były zbudowane sesje i kluczowe decyzje, które ukształtowały curriculum.

## Dlaczego dwie ścieżki

Programiści, którzy przyszli na te warsztaty, nie byli jednorodną grupą. Część pracowała nad nowymi projektami od zera — nowe mikroserwisy, nowe API, kod gdzie mają pełną kontrolę nad architekturą. Inni siedzeli głęboko w utrzymaniu legacy — aplikacje Symfony z 2012 i 2015 roku, codebasy bez testów, funkcje, których nikt już w pełni nie rozumie, i profil ryzyka organizacyjnego, który sprawiał, że "przepiszmy to od nowa" było niemożliwą odpowiedzią.

Te dwie grupy mają naprawdę różne problemy, i jeden program warsztatów nie służyłby żadnej z nich dobrze.

Programista budujący nowy serwis w Pythonie nie potrzebuje sesji o tym, jak prosić AI o wyjaśnienie nieznanego kodu — napisał ten kod, rozumie go. Z kolei programista utrzymujący dwunastoletnią aplikację PHP nie potrzebuje sesji o architekturze greenfield z AI — to nie jest jego ograniczenie.

Mieszanie ich razem dałoby albo warsztaty za proste dla inżynierów od legacy (którzy potrzebują konkretnych technik na specyficzne trudne problemy), albo za zaawansowane dla inżynierów od nowych projektów (którzy najpierw muszą zbudować podstawowe nawyki).

Dwie ścieżki, działające równolegle w pewnych sesjach, ze wspólnymi sesjami na tematy przekrojowe.

## Ścieżka 1: Nowe projekty

Ta ścieżka była dla programistów budujących nowe systemy — nowe serwisy, nowe funkcjonalności, nowe codebasy. Problemy tutaj są inne: nie "jak rozumiem istniejący bałagan", ale "jak buduję szybciej, lepiej, z AI jako częścią workflow."

**Konfiguracja środowiska i wybór narzędzi**

Zaczęliśmy tutaj, bo pominięcie tego prowadzi do chaosu. Cursor, GitHub Copilot, lokalne modele przez Ollama, Claude w przeglądarce — to nie są zamienne narzędzia, i decyzja co używać kiedy ma znaczenie.

Kryteria, które omówiłem: latencja i integracja z workflow (Cursor do pracy w edytorze), wrażliwość na prywatność (lokalny Ollama dla rzeczy, które nie powinny opuszczać maszyny), pułap możliwości (kiedy potrzebujesz pełnego modelu, nie wersji lite) i koszt. Żadne narzędzie nie wygrywa we wszystkich wymiarach; właściwa odpowiedź zależy od zadania.

**Integracja z workflow — pisanie kodu, z którym AI może pomóc**

To była jedna z mniej oczywistych sesji. Okazuje się, że to jak strukturyzujesz kod znacząco wpływa na to, jak dobrze AI może przy nim pomagać. Małe, dobrze nazwane funkcje z jasnymi inputami i outputami są łatwiejsze dla AI niż duże, rozbudowane metody z efektami ubocznymi. To i tak dobra inżynieria — ale sformułowanie tego jako "kod przyjazny dla AI" dało programistom praktyczny powód, żeby się tym zająć w nowy sposób.

Omówiliśmy też inżynierię promptów specyficznie dla developmentu: nie generyczne promptowanie, ale jak dać modelowi AI właściwy kontekst — istniejące interfejsy, sygnatury typów, istniejące testy — żeby to, co generuje, pasowało do rzeczywistego codebase'u.

**Code review wspomagany przez AI**

Użycie modelu AI jako pierwszego recenzenta przed ludzkim code review. To jeden z najwyżej wartościowych workflow'ów, jakie znam: przesuń swój diff przez Claude lub GPT-4 z promptem, który prosi o błędy logiczne, przypadki brzegowe i niespójności stylowe, zanim otworzysz PR. To nie zastępuje ludzkiego review — usuwa łatwo wykrywalny szum, żeby ludzkie review mogło skupić się na tym, co ważne.

**Generowanie testów dla nowego kodu**

Pisanie unit testów dla nowych funkcji przy użyciu AI. Obietnica: weź funkcję, którą właśnie napisałeś, wklej ją, poproś o zestaw testów, uzyskaj 80% pokrycia w pięć minut zamiast czterdziestu pięciu. Rzeczywistość: działa, z zastrzeżeniami. Testy generowane przez AI wymagają review — często testują happy path i przegapiają przypadki brzegowe, a czasem testują implementację zamiast zachowania. Omówiliśmy jak promptować po lepsze testy i jak krytycznie recenzować testy wygenerowane przez AI.

**Generowanie dokumentacji**

Specyfikacje OpenAPI z handlerów route'ów. Sekcje README z kodu. Komentarze inline dla nieoczywistej logiki. To kategoria pracy, którą programiści konsekwentnie odkładają na później, bo jest ważna, ale nie pilna — AI sprawia, że jest wystarczająco szybka, żeby nie było już dobrego usprawiedliwienia.

**Szybkość prototypowania**

Od pomysłu do działającego proof-of-concept w czasie jednego spotkania planistycznego. Pokazałem budowanie małego funkcjonalnego prototypu podczas sesji — to naprawdę różni się od tradycyjnego pisania kodu, i zobaczenie tego zmienia sposób myślenia programistów o wczesnych etapach pracy nad featurem.

## Ścieżka 2: Systemy legacy i istniejący kod

Ta ścieżka była dla programistów pracujących z kodem, którego nie napisali, w systemach, które nagromadziły lata złożoności, z ograniczeniami sprawiającymi, że szeroko zakrojone zmiany są ryzykowne.

**Rozumienie nieznanego kodu**

Najbardziej natychmiast praktyczna umiejętność: "wyjaśnij mi tę klasę." Nie jako jednorazowy trik, ale jako systematyczne podejście do eksploracji nieznanego codebase'u. Pokazałem techniki dawania AI wystarczającego kontekstu do produkcji trafnych wyjaśnień — nie tylko wklejanie funkcji, ale włączenie interfejsu, który implementuje, serwisu, który wywołuje, wyjątku, który łapie.

I co kluczowe: jak oceniać wyjaśnienie. AI może się mylić z pewnym siebie tonem. Omówiliśmy konkretne sygnały sugerujące, że model zgaduje zamiast rozumieć — niespójności, niejasny język o zachowaniu, wyjaśnienia nie uwzględniające przypadków brzegowych w rzeczywistym kodzie.

**Bezpieczny refaktoring z AI**

Jak refaktoryzować legacy kod bez psucia go. Kluczowy insight: testy są siatką bezpieczeństwa, która sprawia, że refaktoring wspomagany przez AI jest możliwy. Jeśli masz testy, możesz pozwolić AI robić zmiany i weryfikować testami. Jeśli nie masz testów — co jest częste w legacy codebasach — najpierw musisz je wygenerować.

To prowadziło naturalnie do następnej sesji.

**Generowanie testów dla nieprzetestowanego kodu**

To jedna z najwyżej wartościowych aplikacji AI w kontekście legacy. Dla kodu bez istniejących testów: testy charakteryzacyjne — napisz testy dokumentujące co kod aktualnie robi, nie co powinien robić. Te "złote testy" nie walidują poprawności; tworzą baseline, który pozwala wykryć kiedy refaktoring zmienia zachowanie.

AI jest naprawdę dobry w generowaniu testów charakteryzacyjnych. Sesja pokazała jak to robić systematycznie: daj modelowi funkcję, daj mu przykładowe inputy jeśli dostępne, poproś o testy uchwytujące aktualne zachowanie, przejrzyj pod kątem kompletności.

**Polowanie na bugi jako para**

Użycie AI jako drugiego mózgu przy trudnym debugowaniu. Nie "powiedz mi co jest nie tak z tym kodem", ale bardziej ustrukturyzowany dialog: oto symptom, oto ścieżka kodu, którą prześledzałem, oto co wykluczyłem, czego mi brakuje? Wartość nie leży w tym, że AI znajduje buga — leży w tym, że artykułowanie problemu AI często samo w sobie naprowadza na odpowiedź, a czasem AI widzi coś, co przeoczyłeś.

**Planowanie migracji i modernizacji**

Użycie AI do pomocy w planowaniu większych zmian: migracja do nowszej wersji PHP, ekstrakcja serwisu z monolitu, refaktoring modelu danych. AI jest tu użyteczny nie jako implementator, ale jako partner myślowy — pomagając mapować zależności, identyfikować ryzykowne zmiany, szkicować sekwencję migracji.

## Sesje wspólne

Niektóre tematy dotyczyły obu ścieżek i były prowadzone razem.

**Bezpieczeństwo i prywatność**

Co możesz bezpiecznie udostępniać AI API? Czego nie możesz? Plany enterprise, polityki retencji danych, opcje self-hosted. Dla firmy przetwarzającej dane ubezpieczeniowe, te tematy nie są opcjonalne — są obowiązkowe. Omówiliśmy też prompt injection i specyficzne problemy bezpieczeństwa kodu generowanego przez AI. W kontekście RODO i wymagań branży ubezpieczeniowej, właściwe podejście do prywatności danych przy korzystaniu z AI API to nie formalność — to fundament.

**Ocena outputu AI**

Najważniejsza przekrojowa umiejętność: skąd wiesz, czy to co AI wyprodukował jest poprawne? To nie tylko code review — to inny rodzaj krytycznego czytania. Output AI ma specyficzne wzorce błędów: często jest syntaktycznie poprawny i semantycznie błędny; ma tendencję do produkowania brzmiących przekonująco, ale niepoprawnych wyjaśnień; wypełni wzorzec, który rozpoznaje, nawet jeśli ten wzorzec jest błędny dla konkretnego kontekstu.

Spędziliśmy na tym pełną sesję, bo odpowiedź na "jak ufam kodowi wygenerowanemu przez AI" nie brzmi "nie ufaj" i nie "ufaj w pełni" — brzmi "rozwiń konkretny osąd o tym, gdzie AI jest wiarygodny, a gdzie nie."

**Integracja w codzienny workflow**

Jak budować nawyki zamiast używać AI tylko gdy o nim pamiętasz. Które zadania najbardziej korzystają z pomocy AI (rozumienie, generowanie, transformacja), które korzystają najmniej (złożone rozumowanie systemowe, rozwiązywanie nowych problemów), i jak strukturyzować dzień, żeby używać AI tam, gdzie jest mocny.

## Struktura: 30/70, zawsze na prawdziwym kodzie

Każdy dzień był z grubsza trzydzieści procent zorganizowanej prezentacji i siedemdziesiąt procent pracy praktycznej.

Praca praktyczna oznaczała: Twoje rzeczywiste zadania, Twój rzeczywisty codebase, Twoje rzeczywiste itemy ze sprintu. Nie ćwiczenia, które zaprojektowałem. Nie aplikacje Hello World. Prawdziwa praca, która i tak musiała być zrobiona, teraz robiona z pomocą AI.

To miało znaczenie. Najszybszym sposobem na budowanie pewności siebie z narzędziami AI jest skuteczne użycie ich na prawdziwym problemie. Najszybszym sposobem na budowanie dobrego osądu jest używanie ich na problemach, które już rozumiesz, żebyś mógł dokładnie oceniać output.

Dałem też jawny czas na "produktywną porażkę" — próbowanie użycia AI w sposób, który nie działał, rozumienie dlaczego, i uczenie się wzorców porażek. Jest to celowo wbudowane w harmonogram, bo wzorce porażek AI nie są intuicyjne, i trzeba je napotkać w kontekście niskiego ryzyka.

## Kluczowe decyzje curriculum

**Nie nauczam narzędzi — nauczam osądu.** Każda sesja była sformułowana wokół decyzji: kiedy używać AI, jak oceniać output AI, co weryfikować. Konkretne narzędzia się zmienią. Osąd się nie zmieni.

**Adresowanie pytania "czy to bezpieczne" bezpośrednio, na początku.** Nie na końcu jako afterthought. To pytanie blokowało część programistów przed zaangażowaniem się, i potrzebowało prawdziwej odpowiedzi zanim cokolwiek innego mogło trafić.

**Uwzględnienie przypadków porażek.** Pokazałem przykłady AI będącego w błędzie z pewnością siebie. Kodu wygenerowanego przez AI, który wyglądał poprawnie, ale miał subtelne bugi. Wyjaśnień AI, które brzmiały autorytatywnie, ale pomijały ważny kontekst. To zrobiło warsztaty bardziej użytecznymi i bardziej uczciwymi niż warsztat pokazujący tylko technologię w jej najlepszym wydaniu.

**Powolne wejście pierwszego dnia.** Pokusa w każdym warsztacie to objęcie zbyt dużo. Pierwszy dzień był celowo powolny: jedno narzędzie, jeden workflow, wystarczająco czasu, żeby naprawdę spróbować i omówić. Szybkość przyszła w dniach drugim i trzecim, po ustanowieniu podstawowych wzorców.

## Czego nie było w programie

Kilka rzeczy, które rozważałem i zostawiłem poza programem.

**Teoria inżynierii promptów.** Są kursy poświęcone temu. Dla programistów, którzy muszą pracę zrobić, uczenie się zasad przez robienie jest bardziej użyteczne niż najpierw studiowanie teorii.

**Kompleksowe porównanie narzędzi.** Za dużo narzędzi, za szybko zmieniający się krajobraz. Dawałem opiniowane rekomendacje i tłumaczyłem rozumowanie, zamiast przeglądać wszystko.

**Strategia AI i zmiana organizacyjna.** To inna rozmowa dla innej publiczności. Ten warsztat był dla indywidualnych kontrybutorów — ludzi, którzy faktycznie piszą kod. Uczynienie ich produktywnymi jest priorytetem.

---

*Następny w tej serii: ścieżka legacy kodu w głębi — konkretne techniki, psychologiczny opór i moment, gdy opór zamienił się w entuzjazm.*
