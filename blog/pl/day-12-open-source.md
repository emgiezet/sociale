---
day: 12
title: "Czego 18 milionów instalacji nauczyło mnie o inżynierii na skalę"
pillar: Builder
language: pl
image: ../../images/day-12.jpg
image_unsplash_query: "open source code collaboration github"
---

# Czego 18 milionów instalacji nauczyło mnie o inżynierii na skalę

Nie będę słynny z moich wkładów do SonataAdminBundle. Projekt ma 18 milionów instalacji na Packagist. Moje imię pojawia się na liście kontrybutorów obok dziesiątek innych inżynierów, którzy kształtowali projekt przez lata. Nikt nie napisze bloga o moich konkretnych zmianach.

Tak powinno być — i właśnie dlatego wkładanie pracy w duże projekty open-source to jedna z najlepszych dostępnych edukacji inżynierskich.

## Czym Jest SonataAdminBundle

SonataAdminBundle to framework administracyjny dla Symfony — frameworka PHP, którego używam przez większość mojej kariery. Oferuje bogaty, konfigurowalny interfejs administracyjny dla operacji CRUD na encjach Doctrine. Jest szeroko stosowany w aplikacjach enterprise PHP w Europie i poza nią.

Zacząłem wnosić wkład po rozległym używaniu go w produkcji w kilku firmach. Impuls "widzę, jak mógłbym to poprawić" przyciąga większość kontrybutorów OSS. Trafiasz na ograniczenie, rozumiesz wystarczająco codebase, żeby zobaczyć rozwiązanie, i decydujesz się wnieść poprawkę zamiast utrzymywać lokalną łatę.

## Lekcja 1: Wsteczna Kompatybilność Zmienia Sposób Myślenia

Pierwsza główna lekcja z wkładu w szeroko używany projekt: kiedy Twój kod działa w produkcji w dziesiątkach tysięcy instalacji, wsteczna kompatybilność to nie miłe mieć. To ograniczenie pierwszej klasy, które kształtuje każdą decyzję.

W moich własnych projektach, kiedy chcę zmienić nazwę metody lub zmienić sygnaturę API, po prostu to robię. Znajduję wszystkie miejsca wywołań, aktualizuję, gotowe. W SonataAdminBundle zmiana nazwy metody oznacza, że każdy użytkownik, który rozszerzył tę klasę lub wywołał tę metodę, jest dotknięty. Jego kod się psuje. Jego panel admina się psuje. Musi spędzić czas na badaniu i aktualizacji.

Dyscyplina pisania dla wstecznej kompatybilności zmienia sposób myślenia o projektowaniu API od samego początku. Myślisz ciężej o nazwach, zanim je nadasz, bo późniejsza zmiana nazwy jest kosztowna. Myślisz ciężej o powierzchni interfejsu, który eksponujesz, bo każda publiczna metoda to zobowiązanie. Myślisz ciężej o ścieżkach deprecacji — jak ewoluować API w czasie w sposób, który daje użytkownikom ścieżkę migracji zamiast przełomowej zmiany.

W Insly ta dyscyplina bezpośrednio poprawia sposób, w jaki projektujemy nasze wewnętrzne API i integracje z systemami zewnętrznymi. Kiedy 150 000 dokumentów miesięcznie polega na Twojej platformie, Twoje zmiany API to ich przełomowe zmiany.

## Lekcja 2: Code Review w Skali to Inna Dyscyplina

Jako kontrybutor, Twój pull request będzie przeglądany przez maintainerów, którzy nie znają Twojego pełnego codebase'u, nie znają szczegółów Twojego przypadku użycia i przeglądają Twoją zmianę w izolacji. To jest klarowne ograniczenie.

Dobre PR-y dla głównych projektów OSS muszą być samodzielnym argumentem. Opis wyjaśnia problem, dlaczego obecne zachowanie jest błędne lub niekompletne, i dlaczego proponowane rozwiązanie jest właściwe. Zmiany kodu są minimalne, skupione i nie wprowadzają pobocznych zmian, które zaciemniają intencję. Testy pokazują, że poprawka działa i nie niszczy istniejącego zachowania.

Pisanie PR-ów według tego standardu uczyniło mnie lepszym w code review własnej pracy mojego zespołu. Zastosowałem ten sam standard do kultury code review mojego zespołu w Insly: każdy PR powinien być kompletnym argumentem za konkretną zmianą, z wystarczającym kontekstem, żeby recenzent, który nie zna funkcji, mógł go poprawnie ocenić.

## Lekcja 3: Dokumentacja to Kod

Funkcja, która istnieje w kodzie, ale nie w dokumentacji, praktycznie nie istnieje dla większości użytkowników. Brzmi to oczywi ście. Nie było oczywiste dla mnie na początku kariery.

W SonataAdminBundle wnosiłem wkłady specjalnie do dokumentacji — wyjaśniając funkcje, które istniały, ale nie były jasno udokumentowane, dodając przykłady dla opcji konfiguracyjnych opisanych tylko w abstrakcyjnych terminach. Te wkłady mają wysoką dźwignię: pomagają każdemu użytkownikowi, który napotka udokumentowaną funkcję, nie tylko tym wystarczająco zaawansowanym, żeby czytać kod źródłowy.

Ta lekcja przenosi się na sposób, w jaki zarządzam inżynierią w Insly. Wewnętrzna dokumentacja — ADR (Architecture Decision Records), runbooki, dokumentacja API — jest traktowana jako praca inżynierska, planowana w sprintach i przeglądana tak rygorystycznie jak kod. Nieudokumentowana decyzja to przyszła sesja debugowania czekająca na swój moment.

## Lekcja 4: Społeczność to Produkt

Ostatnia i najbardziej kontrw intuicyjna lekcja: dla projektu OSS społeczność jest równie ważna jak kod.

Wartość SonataAdminBundle pochodzi nie tylko z tego, co robi kod, ale z ekosystemu wokół niego: odpowiedzi na Stack Overflow, blogi tutorialowe, społeczność Discord, rozszerzenia firm trzecich, firmy, które przyjęły go jako standard. Biblioteka z identycznymi funkcjami, ale bez społeczności, byłaby znacznie mniej użyteczna.

Mapuje się to na każdą platformę techniczną. W Insly mamy ekosystem partnerów integracyjnych, resellerów i zaawansowanych użytkowników, którzy rozszerzają i dystrybuują naszą platformę. Zdrowie tego ekosystemu — dokumentacja, doświadczenie deweloperskie, responsywność na pytania — jest równie ważne dla naszego biznesu jak funkcje, które wysyłamy.

Codebase to to, co działa. Społeczność to to, co się kumuluje.

## Bezwzględność w Zakresie

Jest piąta lekcja, którą wchłonąłem obserwując dobrych maintainerów OSS: mówienie nie to funkcja.

Dobry maintainer open source mówi nie częściej niż tak. Każda funkcja, którą ktoś chce, to funkcja, którą ktoś inny będzie musiał debugować, dokumentować i wspierać przez dekadę. Rozrost zakresu w projekcie OSS jest szczególnie niebezpieczny, bo osoby proponujące funkcje często nie są tymi, które poniosą ciężar utrzymania.

Przenoszę to do decyzji produktowych w Insly. Funkcje, których nie budujemy, są równie ważne jak te, które budujemy. Prostota to przewaga konkurencyjna, kiedy masz 150 000 dokumentów miesięcznie i 15-osobowy zespół.

## Dlaczego Powinieneś Wnosić Wkład

Jeśli myślisz o wkładzie w open source, ale jeszcze nie zacząłeś: zacznij od małych rzeczy. Znajdź projekt, którego używasz. Znajdź issue oznaczone "good first issue." Napraw błąd dokumentacji. Meta-umiejętności — pisanie jasnych opisów PR, rozumienie ograniczeń projektowania API, praca z nieznajomymi nad wspólnym codebasem — są warte rozwijania niezależnie od tego, czy Twój wkład jest słynny.

Najlepsza edukacja inżynierska, za którą nigdy nie zapłaciłem, to wkład w open source. Umiejętności przełożyły się bezpośrednio na moją pracę produkcyjną. I od czasu do czasu wiedza, że kod, który napisałeś, działa w 18 milionach środowisk produkcyjnych, jest swoją własną cichą satysfakcją.

Jakie projekty OSS ukształtowały Twoje myślenie o oprogramowaniu?
