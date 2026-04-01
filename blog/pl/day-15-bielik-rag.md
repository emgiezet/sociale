---
day: 15
title: "Jak Zbudowaliśmy Polski System RAG dla Dokumentów Ubezpieczeniowych"
pillar: Builder
language: pl
image: ../../images/day-15.jpg
image_unsplash_query: "Polish technology innovation architecture"
---

# Jak Zbudowaliśmy Polski System RAG dla Dokumentów Ubezpieczeniowych

Kiedy zaczęliśmy budować systemy RAG w Insly, stanęliśmy przed pytaniem, które większość polskich firm technologicznych ignoruje: czy naprawdę musimy tłumaczyć wszystko na angielski?

Standardowy pipeline dla polskojęzycznych dokumentów w większości firm wygląda tak: polski dokument → przekład na angielski (Amazon Translate lub DeepL) → angielski embedding → angielskie retrieval → angielska generacja → przekład odpowiedzi z powrotem na polski. To rozwiązanie funkcjonuje. Ale ma konkretne wady.

## Dlaczego Tłumaczenie To Za Mało

Polska terminologia ubezpieczeniowa jest specyficzna. Terminy takie jak "ubezpieczenie mienia", "klauzula franszyzy redukcyjnej", "ubezpieczenie odpowiedzialności cywilnej deliktowej" mają precyzyjne znaczenia prawne, które tłumaczenia maszynowe oddają niedokładnie lub niejednolicie.

Kiedy dokument przechodzi przez tłumaczenie przed embeddingiem, tracimy część sygnału semantycznego specyficznego dla polskiego prawa ubezpieczeniowego. Retrieval działa na angielskiej wersji dokumentu, nie na oryginalnym polskim tekście. Małe przekłamania w tłumaczeniu kumulują się na każdym etapie pipeline'u.

Postanowiliśmy przetestować alternatywę: natywny polski pipeline oparty na modelach Bielik.

## Czym Jest Bielik

Bielik to rodzina polskich modeli językowych trenowanych na dużym korpusie polskojęzycznym. Projekt jest rozwijany przez polską społeczność AI, a modele są dostępne open-source. Nie jest to GPT-4 ani Claude — modele są mniejsze i mają inne charakterystyki jakościowe. Ale dla polskojęzycznych zastosowań enterprise, rozmiar i koszt nie są jedynymi parametrami, które się liczą.

Przetestowaliśmy Bielik w dwóch rolach: jako model embeddingowy (konwersja tekstu na wektory) oraz jako model generatywny (produkcja odpowiedzi).

## Wyniki Embeddingów: Znacząca Wygrana

To był największy pozytywny wynik naszych testów. Bielik embeddingi dla polskich dokumentów ubezpieczeniowych były wyraźnie lepiej skalibrowane niż embeddingi anglojęzycznych modeli (Titan, Cohere) aplikowane do polskich dokumentów.

Konkretnie: dla zapytań używających polskiej terminologii ubezpieczeniowej, retrieval precision wzrósł o około 12 punktów procentowych w porównaniu z podejściem tłumaczenie-angielski-retrieval. Zyski były najbardziej wyraźne dla zapytań używających terminologii specyficznej dla ubezpieczeń — dokładnie tych zapytań, gdzie błędy tłumaczenia lub przybliżenia mają największe konsekwencje.

Hipoteza: polskie modele embeddingowe lepiej odwzorowują semantyczne relacje specyficzne dla polskiego języka prawnego i biznesowego, które globalne modele anglojęzyczne uczą się tylko częściowo.

Ten wynik był solidny dla różnych typów zapytań i kategorii dokumentów. Mamy wystarczającą pewność, żeby Bielik embeddingi były teraz domyślne dla przetwarzania polskich dokumentów w naszym produkcyjnym pipeline'ie.

## Wyniki Generacji: Bardziej Mieszane

Generacja z Bielik była bardziej mieszana. Dla prostych zapytań — faktograficzne wyszukiwania, ekstrakcja konkretnych wartości, prosta identyfikacja klauzul — odpowiedzi były poprawne i naturalnie wyrażone.

Dla złożonych zapytań wieloetapowych — "jak ta klauzula wchodzi w interakcję z ogólnymi warunkami ubezpieczenia w kontekście szkody z wodociągów?" — Claude 3.5 Sonnet (przez Bedrock), nawet z przetłumaczonym kontekstem, dawał lepsze wyniki. Ma to sens biorąc pod uwagę różnicę w rozmiarze modelu i złożoność wymaganego rozumowania.

Przyjęliśmy hybrydowe podejście: Bielik do embeddingów i retrieval, Claude do złożonej generacji. Wyeliminowaliśmy pełne tłumaczenie dokumentów, ale zachowaliśmy tłumaczenie zapytań i odpowiedzi dla warstwy generacyjnej gdzie potrzeba.

## Praktyczna Architektura

Wynikowy pipeline:

1. Dokumenty embeddowane przy użyciu Bielik — bez wymaganego tłumaczenia
2. Zapytania użytkowników embeddowane przy użyciu Bielik — w oryginalnym języku polskim
3. Retrieval względem polskiego indeksu embeddingów
4. Pobrane polskie chunki przekazane do Claude z systemowym promptem świadomym języka polskiego
5. Claude generuje odpowiedź po polsku (radzi sobie z polskim dobrze)
6. Opcjonalne tłumaczenie na angielski dla nieanglojęzycznych użytkowników

Wpływ kosztowy: wyeliminowanie wywołań API tłumaczenia dla etapu embeddingów (nasz największy wolumen dokumentów) obniżyło koszty pipeline'u o około 20%. Latencja proporcjonalnie się poprawiła.

## Aspekt RODO

Jeden wymiar, który anglojęzyczna literatura rzadko omawia: dla polskich firm enterprise, rezydencja danych i lokalizacja przetwarzania ma znaczenie pod RODO. Uruchomienie pipeline'u translate-first oznacza, że surowa treść dokumentów przechodzi przez API tłumaczenia zewnętrznej strony przed jakimkolwiek innym przetwarzaniem.

Bielik może działać na własnej infrastrukturze — on-premises lub w dedykowanym środowisku chmurowym w UE. Dla dokumentów ubezpieczeniowych zawierających wrażliwe dane ubezpieczonych, to nie jest drobna kwestia. Znacząco upraszcza wymagania dotyczące umów przetwarzania danych i historię "dane zostają tam, gdzie powinny" dla zespołów prawnych i compliance. Ma to szczególne znaczenie w regulowanych sektorach podlegających nadzorowi KNF, ochrony zdrowia i prawa.

## Wyzwania, Których Nie Spodziewaliśmy się

Eksperyment ujawnił też wyzwania, które nie były oczywiste, zanim go przeprowadziliśmy.

**Jakość zbioru ewaluacyjnego.** Budowanie polskiego zbioru ewaluacyjnego wymagało polskojęzycznych ekspertów domenowych w dziedzinie ubezpieczeń — nie tylko polskojęzycznych, ale ludzi, którzy rozumieli semantykę polis ubezpieczeniowych wystarczająco głęboko, żeby walidować odpowiedzi. Znalezienie takich zasobów było trudniejsze niż oczekiwano.

**Brakujące benchmarki.** Dla języka polskiego jest znacznie mniej standardowych benchmarków NLP niż dla angielskiego. Mierzenie "czy to jest lepsze?" wymaga budowania własnego złotego standardu zamiast polegania na opublikowanych benchmarkach.

**Opóźnienie dokumentacji.** Dokumentacja Bielika znacząco się poprawiła, ale wciąż są obszary, gdzie czytasz kod źródłowy zamiast dokumentacji. Wymagana jest eksperymentacja. Zaplanuj na to czas.

## Co To Znaczy Dla Polskiego Enterprise AI

Budowanie natywnych polskojęzycznych systemów AI bez polegania na tłumaczeniu jako obejściu to realny kierunek. Wymaga:

→ Inwestycji w polskie modele embeddingowe i generatywne
→ Budowania polskojęzycznych datasetów ewaluacyjnych
→ Ekspertów domenowych mówiących po polsku do walidacji jakości
→ Cierpliwości inżynierskiej z modelami, które są mniejsze i wymagają staranniejszego promptowania

Polska społeczność AI buduje te zdolności. Bielik to dowód, że natywna polska AI nie jest akademickim projektem — to produkcyjne narzędzie. Dla organizacji działających głównie na polskich rynkach, budowanie na natywnych polskich modelach jest warte poważnego rozważenia.

Jeśli pracujesz z polskojęzycznymi dokumentami w kontekście AI i chcesz porównać notatki na temat architektury, skontaktuj się ze mną. To jest domena, gdzie wspólne uczenie się postępuje szybciej niż niezależne eksperymenty.
