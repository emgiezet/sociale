---
day: 30
title: "30 dni, 30 postów: Czego nauczyłem się dzieląc się wszystkim co wiem o AI w produkcji"
pillar: Educator
language: pl
image: ../../images/day-30.jpg
image_unsplash_query: "online course learning developer laptop"
---

# 30 dni, 30 postów: Czego nauczyłem się dzieląc się wszystkim co wiem o AI w produkcji

Miesiąc temu podjąłem zobowiązanie: dzielić się czymś realnym o budowaniu AI w produkcji każdy dzień roboczy przez 30 dni. Nie przetworzonym komentarzem branżowym. Nie treścią tutorialową ignorującą rzeczywistą złożoność. Faktyczne relacje z pracy, którą wykonuję w Insly — decyzje architektoniczne, dynamika zespołu, porażki produkcyjne, rzeczy które naprawdę działały.

To jest retrospektywa. I ogłoszenie co będzie dalej.

## Dlaczego zacząłem

Bezpośredni powód: śledziłem praktyków w innych domenach, którzy otwarcie dzielili się swoją pracą, i uznałem to za znacznie bardziej wartościowe niż treści akademickie czy marketing dostawców. Chciałem wnieść taki rodzaj treści dla konkretnego przecięcia, w którym się poruszam: doświadczona inżynieria oprogramowania, systemy AI w produkcji, branże regulowane i polski rynek technologiczny.

Głębszy powód: naprawdę wierzę, że wiedza potrzebna do odpowiedzialnego wdrażania AI w branżach regulowanych jest skoncentrowana w zbyt niewielu miejscach. Literatura akademicka jest rygorystyczna, ale oderwana od problemów produkcyjnych. Marketing dostawców jest błyszczący i mylący. Głos praktyka — to jest to, co faktycznie zbudowaliśmy, oto co się zepsuło, oto czego się nauczyliśmy — jest niedoreprezentowany.

Jeśli znam rzeczy, które pomogłyby zespołom unikać drogich błędów, niedzielenie się nimi jest formą gromadzenia. Ten 30-dniowy projekt był moją próbą zaprzestania gromadzenia.

## Co omówiłem

Patrząc wstecz na 30 postów w trzech filarach, pojawiły się pewne tematy:

**Wątek architektury technicznej.** RAG od fundamentów do produkcji. Progresja od Bedrock Knowledge Bases (60% jakości) do wyszukiwania hybrydowego (72%) do LightRAG (89%). Frameworki ewaluacyjne. Bielik dla polskojęzycznych dokumentów — poprawa precyzji o 12 punktów procentowych w porównaniu z podejściem tłumaczeniowym. Badanie kosztów AWS RDS. Czterosystemowa architektura Insly i gdzie AI w niej pasuje.

Te posty ustanowiły wiarygodność techniczną i były najwyraźniejszym wyróżnieniem od generycznej treści o AI.

**Wątek przywództwa i zespołu.** Informacja zwrotna 360 stopni. Emocjonalny koszt prowadzenia przez transformację AI. Co tworzy wyjątkowy zespół i dlaczego to infrastruktura, a nie talent. Vibecoding i osąd dewelopera. Zarządzanie lękiem przed utratą kompetencji u doświadczonych inżynierów.

Te posty uzyskały więcej zaangażowania niż oczekiwałem. Ludzka strona technicznego przywództwa jest niedoreprezentowana w treściach technicznych.

**Wątek domeny i kariery.** Ewolucja kariery od PHP do AI. Kontrybucja open source i co 18 milionów instalacji Packagist nauczyło mnie o trwałej architekturze. Ekosystem AI w Polsce. Przyszłość AI w ubezpieczeniach i dlaczego firmy muszą zacząć budować teraz.

Te posty budowały kontekst i społeczność w sposób, którego czysto techniczna treść nie robi.

## Co zrobiłem dobrze

**Postowanie po polsku dla polskiej publiczności.** Wskaźnik zaangażowania polskich postów w polskiej społeczności technologicznej był znacznie wyższy niż angielskich. Mniejsze liczby bezwzględne, ale dokładnie ta publiczność, która ma dla mnie największe znaczenie. Polska społeczność technologiczna jest niedostatecznie obsługiwana przez treści techniczne tylko po angielsku i wypełnienie tej luki jest warte robienia celowo.

**Nastawienie na komentarze jako pierwsze.** Kilka postów było zaprojektowanych, by generować komentarze — pytając o reakcje, stawiając prawdziwe pytania, formułując sporne pozycje. Wątki komentarzy były często lepsze niż posty. Nauczyłem się więcej z odpierania ataków i uzupełnień niż z pisania oryginału.

**Włączanie historii o porażkach.** Posty, w których opisywałem co nie działało — 60% jakość pierwszego prototypu RAG, wyzwania zespołowe podczas transformacji AI, decyzje architektoniczne, których żałowaliśmy — uzyskały więcej zaangażowania i więcej osobistych wiadomości niż historie sukcesu. Ludzie ufają praktykom, którzy są szczerzy co do porażki.

## Co zrobiłem błędnie

**Niedocenianie jak bardzo "nudne" tematy rezonują.** Prawie nie napisałem postu o emocjonalnym koszcie transformacji AI, bo myślałem, że "nie jest wystarczająco techniczny." Stał się jednym z najczęściej udostępnianych postów przez 30 dni. Ludzki wymiar technicznego przywództwa to luka w ekosystemie treści i powinienem był wchodzić w to wcześniej.

**Niebudowanie infrastruktury społeczności wcześniej.** Do Dnia 25 prowadziłem bezpośrednie wiadomości z ludźmi z całej europejskiej społeczności InsurTech i polskiej AI. Powinienem był wcześniej wskazać na istniejące przestrzenie społeczności lub stworzyć jedną. Połączenia nawiązane przez 30 dni są warte utrwalenia w ustrukturyzowany sposób.

## Co będzie dalej

**Kurs "Agentic AI Developer"** — Dla inżynierów oprogramowania, którzy chcą przejść od "rozumiem RAG teoretycznie" do "mogę wdrożyć produkcyjne systemy AI odpowiedzialnie." To jest kurs adresujący przepaść między treścią tutorialową a inżynierią klasy produkcyjnej.

Program nauczania:

- **Produkcyjna architektura RAG**: Poza tutorialem, w ewaluację i iterację. Strategie fragmentacji, ewaluacja retrieval, wykrywanie halucynacji, błędy które kosztowały nas tygodnie. Progresja od podstawowego wyszukiwania wektorowego do hybrydowego retrieval do retrieval opartego na grafie.

- **Projekt systemu agentic**: Jak budować systemy, gdzie AI podejmuje znaczące działania bez wychodzenia poza skrypt. Wieloetapowe rozumowanie, użycie narzędzi, orkiestracja, debugowanie kiedy rzeczy idą nie tak w systemach probabilistycznych.

- **Ewaluacja i obserwowalność**: Budowanie infrastruktury, by wiedzieć czy Twój system działa. Framework, którego używam w Insly, by bramkować każde wdrożenie.

- **AI w branży regulowanej**: Projekt compliance, ścieżki audytu, ludzki nadzór, zarządzanie interesariuszami. RODO, Ustawa AI UE i wymogi specyficzne dla branży. Jak budować systemy, które przetrwają przegląd regulacyjny.

- **Praca z danymi domenowymi**: Co zmienia się gdy Twoje dokumenty są prawne, medyczne lub ubezpieczeniowe. Rozważania językowe (w tym polskojęzyczne modele jak Bielik). Partnerstwo z ekspertami domenowymi.

- **Adopcja przez zespół**: Jak wciągnąć inżynierów, gdy narzędzia zmieniają się co trzy miesiące. Zarządzanie lękiem przed utratą kompetencji. Budowanie wspólnego kontekstu w szybko zmieniającej się domenie.

Docelowa publiczność: backend developerzy z 3+ latami doświadczenia, tech liderzy oceniający projekty AI, inżynierowie w branżach regulowanych (ubezpieczenia, finanse, ochrona zdrowia, prawo), którzy chcą podejść gotowe do produkcji.

Uruchomienie: wiosna 2026. Lista oczekujących jest otwarta — napisz komentarz poniżej lub wyślij mi DM z "KURS" po wczesny dostęp i cenę fundatora.

**Dalszą obecność tutaj** — Schodzę z 5 postów/tydzień do 3 postów/tydzień. Format pozostaje: konkretny, praktyczny, bez generycznych opinii o AI. Posty Builder, Trenches, Educator. Polskie posty dla polskiej społeczności.

## Dziękuję

Trzydzieści dni rozmów z ludźmi budującymi, prowadzącymi i poważnie myślącymi o AI — w Polsce, w całej Europie i poza nią — było naprawdę wartościowe. Sekcje komentarzy, bezpośrednie wiadomości, odpieranie ataków, które wyostrzyło moje myślenie: o to chodziło w filarze "Educator" od samego początku.

Jeśli śledziłeś: dziękuję. Jeśli to jest pierwszy post, który czytasz: zacznij od Dnia 1 — jest 29 więcej postów wartych czytania.

Jeśli chcesz kontynuować rozmowę: obserwuj, komentuj, dołącz do listy oczekujących kursu. Następne 30 dni będzie inne, ale zobowiązanie do dzielenia się tym, co faktycznie wiem z produkcyjnej pracy z AI, trwa.

Do zobaczenia w Dniu 31.
