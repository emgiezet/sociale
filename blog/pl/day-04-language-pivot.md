---
day: 4
title: "Co 20 lat nauki kolejnych języków nauczyło mnie o uczeniu się AI"
pillar: Trenches
language: pl
image: ../../images/day-04.jpg
image_unsplash_query: "programming code learning career"
---

# Co 20 lat nauki kolejnych języków nauczyło mnie o uczeniu się AI

Moją pierwszą produkcyjną aplikację w PHP napisałem w 2007 roku. Pierwszy produkcyjny system RAG wdrożyłem w 2024. Odległość między tymi dwoma punktami to nie prosta linia — i rzeczy, których nauczyłem się na objezdnych, to właśnie to, co umożliwiło mi dotarcie do celu.

To historia nielinearnej ścieżki od enterprise PHP do produkcyjnego AI — i tego, czego każdy przystanek mnie nauczył, czego nie mógłbym się nauczyć inaczej.

## PHP: Fundament, który faktycznie wytrzymuje

Powiedzmy to wprost. PHP jest wyśmiewany. Trochę zasługuje na to. Wczesne PHP było bałaganem. Ale dla programistów, którzy poszli wystarczająco głęboko, PHP w erze Symfony było niezwykłą edukacją z zasad inżynierii oprogramowania.

Spędziłem 15 lat pisząc aplikacje Symfony. W tym czasie nauczyłem się wstrzykiwania zależności nie jako wzorca do zapamiętania, ale jako rozwiązania problemu, na który wielokrotnie trafiałem. Nauczyłem się, że czysta architektura nie polega na przestrzeganiu reguł — chodzi o ułatwienie właściwych zmian. Kontrybuowałem do SonataAdminBundle, open-source'owego projektu Symfony, który teraz ma ponad 18 milionów instalacji. Praca przy projekcie tej skali uczy Cię rzeczy o wstecznej zgodności, projektowaniu API i utrzymaniu społeczności, których żaden kurs nie może odtworzyć.

Najważniejsza rzecz, której nauczyło mnie PHP: język nie jest istotny. Myślenie inżynierskie jest istotne. Kiedy ludzie pytają, czy żałuję lat z PHP, mówię nie. Uczyniły ze mnie inżyniera. Wszystko po tym było specjalizacją.

Nauczyłem się też, że „nudna" technologia, która niezawodnie dostarcza, bije „ekscytującą" technologię, która nie dostarcza. Symfony nie jest glamour. Ale jest przewidywalne, dobrze przetestowane i ma społeczność, która zbiorowo rozwiązała te same problemy, na które zaraz natrafisz.

## Python: Wartość szybkiej pętli feedbacku

Kiedy przeszedłem do pracy blisko ML, Python był oczywistym wyborem. Ekosystem do machine learning, przetwarzania danych i badań AI jest tam zbudowany. Ale Python nauczył mnie czegoś mniej oczywistego niż „użyj PyTorch."

Nauczył mnie o szybkości pętli feedbacku.

Kombinacja interaktywnych notebooków, dynamicznego typowania i ekosystemu pakietów obejmującego prawie wszystko oznacza, że w Pythonie możesz przejść od pomysłu do działającego eksperymentu w minutach, a nie godzinach. To zmienia sposób, w jaki myślisz o eksploracji. Prototypujesz więcej. Odrzucasz więcej. Szybciej znajdujesz właściwe podejście.

Ta zmiana mentalna — prototypuj agresywnie, oceniaj bezlitośnie, commituj tylko wtedy, gdy wiesz, co budujesz — stała się centralnym elementem mojego podejścia do pracy z AI. Architektura naszego pierwszego prototypu RAG w Insly przeszła przez trzy kompletne przeprojektowania w ciągu dwóch miesięcy. W skompilowanym języku byłoby to paraliżująco wolne. W Pythonie na Jupyter było wystarczająco szybkie, żeby naprawdę czegoś nas nauczyć.

Nie przeszedłem na Pythona, bo był lepszy w jakimś abstrakcyjnym sensie. Przeszedłem, bo biblioteki, których potrzebowałem, nie istniały gdzie indziej w użytecznej formie. Lekcja: idź za ekosystemem, który rozwiązuje Twój aktualny problem, nie tym, który wygrywa dyskusje na Twitterze.

## Go: Dyscyplina ograniczeń

Go było dodatkową edukacją z ograniczeń. Język celowo usuwa opcje. Żadnych generyków (przez długi czas), żadnego dziedziczenia opartego na klasach, ograniczona obsługa wyjątków. Kiedy pierwszy raz pisałem Go, czułem się ograniczony. Dwa lata później rozumiałem, co projektanci mieli na myśli.

Ograniczenia wymuszają przemyślany design. Kiedy nie możesz sięgnąć po framework do rozwiązania każdego problemu, myślisz głębiej o problemie. Serwisy Go, które zbudowałem, są mniejsze, prostsze i bardziej utrzymywalne niż ich odpowiedniki w Pythonie — nie dlatego, że Go jest lepsze, ale dlatego, że ograniczenia Go nie pozwoliły mi dodać złożoności, której nie potrzebowałem.

Go zmieniło też sposób, w jaki myślę o obsłudze błędów. W Go błędy są jawnymi wartościami zwracanymi. Nie możesz ich zignorować bez celowego pisania kodu, żeby to zrobić. Ta dyscyplina — potwierdź każdą ścieżkę błędu, obsłuż ją jawnie lub świadomie zdecyduj się nie — to dokładnie model mentalny potrzebny dla produkcyjnych systemów AI, gdzie awarie są probabilistyczne i często ciche.

Ten sposób myślenia przeniósł się bezpośrednio do projektowania systemów AI. Pokusa w projektach AI polega na dodawaniu złożoności — więcej agentów, więcej vector store'ów, więcej strategii retrieval — bo narzędzia to ułatwiają. Dyscyplina polega na pytaniu, czy złożoność rozwiązuje prawdziwy problem, czy tylko sprawia, że demo wygląda bardziej imponująco.

## AI: Zmiana paradygmatu, nie kolejny język

Kiedy na poważnie zacząłem budować systemy AI, szybko zrozumiałem, że przejście nie dotyczyło przede wszystkim nauki nowych narzędzi. Chodziło o naukę nowych trybów awarii.

Tradycyjne oprogramowanie zawodzi w sposób, który możesz przetestować. Dla wejścia X, oczekuj wyjścia Y. Jeśli Y jest błędne, Twoja suita testów Ci o tym powie. Jeśli system się rozsypie, masz log błędów.

Systemy AI zawodzą inaczej. Zawodzą probabilistycznie. Zawodzą w sposób, który na pierwszy rzut oka wygląda jak sukces — pewna siebie, płynna, syntaktycznie perfekcyjna odpowiedź, która akurat jest błędna. Te awarie nie pojawiają się w Twoich logach błędów. Pojawiają się w skargach użytkowników, w przeglądach jakości, w powoli narastającym uświadomieniu, że Twój system ma ślepe pole, o którym nie wiedziałeś.

Wszystko, czego nauczyłem się o budowaniu solidnego oprogramowania — defensywny design, infrastruktura ewaluacji, obserwowalność, pętle feedbacku — stało się w pracy z AI ważniejsze, nie mniej. Programiści, którzy najbardziej zmagają się z przejściem, to ci, którzy myśleli „muszę tylko nauczyć się nowych API." Ci, którzy odnoszą sukces, to ci, którzy przynieśli swoje pełne doświadczenie inżynierskie i zastosowali je do nowego paradygmatu.

Inżynierowie, którzy pozostają relewatnymi, to nie ci, którzy wybrali właściwy język. To ci, którzy poruszali się dalej, gdy problem się zmienił.

## Lekcja kariery

Twoja ścieżka nie musi być liniowa. Objazdy są programem nauczania.

Jeśli jesteś programistą PHP zastanawiającym się, czy Twoje doświadczenie wystarczy do pracy z AI: tak. Zasady Symfony — wstrzykiwanie zależności, design SOLID, testowalne interfejsy — mapują się czysto na budowanie produkcyjnych systemów AI. Dyscyplina inżynierska, którą zbudowałeś, to dokładnie to, czego AI development potrzebuje więcej.

Jeśli jesteś wcześniej w karierze i optymalizujesz pod „właściwy" język lub „właściwy" stos: przestań. Naucz się fundamentów. Buduj rzeczy. Wdrażaj je. Konkretne technologie zmienią się co pięć lat. Myślenie inżynierskie przenosi się na zawsze.

Nadal się uczę. Każdego dnia w pracy z AI spotykam coś, czego nie wiem. Ale mam 20 lat kontekstu dla tego, jak się tego nauczyć — i to, bardziej niż jakakolwiek konkretna umiejętność, jest prawdziwym zwrotem z nielinearnej ścieżki kariery.
