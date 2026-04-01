---
day: 1
title: "Czego żałuję, że mi nikt nie powiedział, zanim zacząłem prowadzić zespół AI w ubezpieczeniach"
pillar: Builder
language: pl
image: ../../images/day-01.jpg
image_unsplash_query: "insurance technology team"
---

# Czego żałuję, że mi nikt nie powiedział, zanim zacząłem prowadzić zespół AI w ubezpieczeniach

Osiemnaście miesięcy temu stanąłem przed moim 15-osobowym zespołem inżynierskim i powiedziałem coś, czego nigdy wcześniej nie mówiłem: „Nie do końca wiem jeszcze, co budujemy."

Byliśmy sześć miesięcy od początku eksperymentów z AI w Insly — europejskiej platformie InsurTech SaaS której rozwiązania AI przetwarzają ponad 150 000 dokumentów miesięcznie — i zaczynałem rozumieć, że wyzwania, które nas czekają, nie były techniczne w taki sposób, jak się spodziewałem. Były inne. Dziwniejsze. Trudniejsze do skwantyfikowania.

Buduję oprogramowanie od 20 lat. Prowadziłem zespoły przez migracje Symfony, przejścia na mikroserwisy i migrację SSO bez przestojów dla 150 000 użytkowników. Wiem, jak wygląda trudność w tradycyjnej inżynierii. AI w produkcji jest trudne w inny sposób.

Ten artykuł to to, co chciałbym, żeby ktoś mi powiedział na początku.

## Problem z danymi, o którym nikt nie ostrzega

Kiedy czytasz tutoriale RAG, dostajesz czyste pliki PDF. Dobrze ustrukturyzowane dokumenty. Rozsądne rozmiary chunków. Wszystko ładnie się wyszukuje.

Dane ubezpieczeniowe nie są takie.

W Insly przetwarzamy dokumenty od dziesiątek brokerów na wielu europejskich rynkach. Dokumenty polisowe sformatowane w Wordzie 2003. Aneksy skanowane z papieru i poddawane OCR przez system działający od 2011 roku. Biblioteki klauzul używające różnej terminologii w zależności od kraju, w którym zostały napisane.

Nasz pierwszy prototyp RAG działał pięknie na zbiorze testowym. Rozpadł się natychmiast na danych produkcyjnych. Nie katastrofalnie — po prostu zaczął zwracać złą klauzulę, z pełnym przekonaniem, dla przypadków brzegowych, które pojawiały się stale w prawdziwym użytkowaniu.

Spędziliśmy dwa miesiące na przebudowie strategii chunkowania i retrieval. Czego się nauczyliśmy: przygotowanie danych to 60% pracy. Model jest łatwą częścią.

## Asymetria compliance

W większości oprogramowania błąd generuje wyjątek. System zawodzi widocznie. Naprawiasz go.

W systemie RAG wdrożonym w ubezpieczeniach, tryb awarii jest inny: system generuje pewną siebie, płynną, syntaktycznie perfekcyjną złą odpowiedź. Bez logu błędu. Bez wyjątku. Tylko underwriter ufający rekomendacji zbudowanej na błędzie retrieval.

Ta asymetria kształtuje wszystko w sposobie budowania. Nie możesz po prostu mierzyć „czy zwraca odpowiedź." Musisz mierzyć „czy odpowiedź jest zakorzeniona w tym, co mu faktycznie daliśmy." Wymaga to infrastruktury ewaluacji, pętli przeglądu przez człowieka i mechanizmu feedbacku, którego większość tutoriali nie omawia.

Nasze rozwiązanie zbudowaliśmy na AWS Bedrock, łącząc Bedrock Knowledge Bases dla podstawowego retrieval z niestandardową integracją LightRAG dla bardziej złożonych relacji między dokumentami. Warstwa ewaluacji zajęła więcej czasu do zbudowania niż warstwa retrieval.

To właściwa kolejność priorytetów. Na początku jednak tak to nie wygląda.

## Czego biznes naprawdę potrzebuje

Na początku naszej pracy z AI spędzałem dużo czasu rozmawiając o modelach embeddingów, precyzji retrieval, rozmiarach okien kontekstu. Product managerowie, z którymi pracowałem, mieli bardzo proste pytanie: „Czy underwriter może szybciej znaleźć właściwą klauzulę?"

To wszystko. To jest metryka.

Wszystko inne — architektura, wybory modeli, strategia chunkowania — to niewidoczna infrastruktura. Biznes widzi wyniki. Mierzysz wyniki. Budujesz w kierunku wyników.

To brzmi oczywisto. Tak nie jest. Kiedy jesteś głęboko w pracy technicznej, łatwo optymalizować złą rzecz. Przyłapałem się na spędzeniu tygodnia na dostrajaniu precyzji retrieval, gdy prawdziwa skarga użytkownika dotyczyła UI — jak wynik był prezentowany, nie co było pobrane.

Pętla feedbacku między „co zbudowaliśmy" a „co użytkownik doświadcza" musi być krótka, explicitna i regularna. Prowadzimy cotygodniowe demo z prawdziwymi underwriterami. Nie product managerami interpretującymi to, czego underwriterzy chcą — prawdziwymi underwriterami, klikającymi przez system, opisującymi swoje doświadczenie.

Zmieniło to sposób, w jaki budowaliśmy, szybciej niż cokolwiek innego.

## Wymiar zespołowy

Jest wyzwanie liderskie specyficzne dla projektów AI, o którym nie czytałem zbyt wiele: twój zespół uczy się technologii w tym samym czasie, w którym z niej buduje.

W tradycyjnej inżynierii, kiedy przydzielam zadanie starszemu programiście, mam dobry model mentalny tego, ile czasu zajmie i jakie są ryzyka. W pracy z AI istnieje warstwa badawcza, która jest naprawdę nieprzewidywalna. „Jak LightRAG radzi sobie z tą strukturą dokumentu?" to nie pytanie z poznaną odpowiedzią. Musisz to wypróbować.

To zmienia sposób planowania sprintów, ustalania oczekiwań z interesariuszami i ochrony zespołu przed presją deadline'ów na pracę eksploracyjną.

Zespoły, które wygrywają z AI, to nie te, które poruszają się najszybciej. To te, które budują właściwe pętle feedbacku — między inżynierami a użytkownikami, między eksperymentami a decyzjami, między tym, co model potrafi, a tym, czego biznes naprawdę potrzebuje.

## Od czego zaczynam

Przez następne 30 dni dzielę się tym, czego się uczę — decyzjami architektonicznymi, dynamiką zespołu, konkretnymi narzędziami, historiami produkcyjnymi z okopów. Prawdziwe relacje z wdrażania AI w regulowanej branży.

Jeśli jesteś programistą próbującym dowiedzieć się, gdzie AI pasuje do Twojej kariery, tech leadem próbującym przeprowadzić swój zespół w tym kierunku, lub budowniczym w wysoce regulowanej branży zastanawiającym się, czy to w ogóle możliwe: śledź dalej. To treści, które chciałbym mieć 18 miesięcy temu.

Rozmowa w komentarzach jest często lepsza niż sam post. Przynieś swoje pytania.
