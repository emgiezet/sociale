---
day: 2
title: "\"Po prostu dodaj AI\" to najgorsze zdanie w technologii"
pillar: Trenches
language: pl
image: ../../images/day-02.jpg
image_unsplash_query: "warning sign database technology"
---

# „Po prostu dodaj AI" to najgorsze zdanie w technologii

Słyszałem to na spotkaniach produktowych, w wiadomościach na Slacku od zarządu, podczas Q&A na konferencjach. Zdanie, które stało się odpowiednikiem roku 2026 dla „musimy to po prostu wrzucić na blockchain."

„Czy nie możemy po prostu dodać AI do tego?"

Powiem wprost: to podejście wyrządza realną szkodę realnym projektom. A budując systemy AI w produkcji w Insly — platformie ubezpieczeniowej z 150 000+ użytkownikami i poważnymi zobowiązaniami compliance — widziałem, jak to myślenie zderzą się z rzeczywistością.

## Historyczny wzorzec

„Po prostu dodaj AI" ma swoich poprzedników. We wczesnej erze baz danych, nietech­niczne zainteresowane strony wierzyły, że raz gdy masz bazę danych, wgląd pojawi się automatycznie. Dane były trudną częścią. Przechowywanie je odblokowałoby wartość.

Czego się nauczyliśmy: baza danych była łatwą częścią. Projektowanie schematu, optymalizacja zapytań, warstwy raportowania, jakość danych — to była praca.

Ten sam wzorzec powtórzył się z mikroserwisami („po prostu podziel na serwisy"), z NoSQL („po prostu użyj MongoDB") i migracją do chmury („po prostu przenieś na AWS"). Za każdym razem naprawdę potężna technologia była sprzedawana jako proste uzupełnienie, gdy w rzeczywistości była głębokim zobowiązaniem architektonicznym.

AI podąża tą samą ścieżką, ale szybciej. Cykl hype'u skrócił się. Oczekiwania są jeszcze dalej od rzeczywistości. A ludzie z obozu „po prostu dodaj" są głośniejsi niż kiedykolwiek, bo dema są naprawdę imponujące.

## Co naprawdę oznacza „dodanie AI"

Kiedy ktoś pyta mnie „jak długo zajmie dodanie AI do X," oto prawdziwa odpowiedź, którą muszą usłyszeć:

**Przygotowanie danych zajmuje dłużej, niż myślisz.** LLM-y są potężne, ale są tak dobre jak to, co im dajesz. Jeśli Twoje dane są nieustrukturyzowane, niejednorodnie sformatowane, wielojęzyczne lub rozproszone po starszych systemach — co opisuje większość danych enterprise — przygotowanie może zajmować tygodnie, zanim napiszesz pierwszą linię kodu AI.

W Insly nasze dokumenty ubezpieczeniowe są przechowywane w wielu formatach, pisane w wielu językach, z różną strukturą w zależności od brokera i kraju. Zanim mogliśmy cokolwiek użytecznego zbudować, spędziliśmy tygodnie tylko na strategiach chunkowania i normalizacji. Trzy miesiące przygotowania danych, zanim nasz pierwszy system RAG dotknął produkcji. Nie budowania. Nie treningu. Czyszczenia, klasyfikowania i audytowania tego, co już mieliśmy.

**Jakość retrieval wymaga własnej dyscypliny inżynierskiej.** RAG to dominujący wzorzec dla AI w przedsiębiorstwie teraz, i ma zwodniczą powierzchowną prostotę: embeddingujesz dokumenty, embeddingujesz zapytanie i szukasz najbliższego dopasowania. W praktyce jakość retrieval w skali produkcyjnej wymaga starannej uwagi na modele embeddingów, strategie nakładania chunków, filtrowanie metadanych, hybrydowe podejścia do wyszukiwania i logikę rerankingu.

**Infrastruktura ewaluacji nie jest opcjonalna.** To ta, która najczęściej zabija projekty. Tradycyjne oprogramowanie ma deterministyczne testy: dla wejścia X, oczekuj wyjścia Y. Systemy AI generują probabilistyczne wyniki. Potrzebujesz frameworków ewaluacji zdolnych mierzyć, czy wyniki są zakorzenione, dokładne, pomocne i spójne.

**Integracja to prawdziwa złożoność.** Wrzucenie wywołania API do LLM do Twojej bazy kodu to nie to samo co integracja AI z Twoim produktem. Prawdziwa praca leży w integracji workflow.

## W regulowanych branżach stawka jest wyższa

W ubezpieczeniach broker pyta nasz system AI: „Czy ten klient jest objęty ochroną na powódź?" Błędna odpowiedź, dostarczona pewnym siebie tonem, nie frustruje tylko użytkownika. Tworzy odpowiedzialność prawną. Może wpłynąć na realne roszczenie. Regulatorzy w UE nie są pod wrażeniem argumentu „tak powiedział model."

Oto co „po prostu dodaj AI" ignoruje w regulowanych branżach:

→ Twoje dane odzwierciedlają historyczne decyzje, w tym błędne
→ RODO wymaga wyjaśnienia automatycznych decyzji, a LLM-y nie są z natury wytłumaczalne
→ Systemy legacy nie były projektowane z myślą o formatach czytelnych dla AI
→ Produkty ubezpieczeniowe są specyficzne dla jurysdykcji — generyczny model nie zna polskiego prawa ubezpieczeniowego
→ Ewaluacja nie jest opcjonalna. Potrzebujesz metryk przed wdrożeniem, nie po

## Właściwe pytanie

„Po prostu dodaj AI" to zły sposób myślenia. Właściwe pytanie brzmi: „Jaki konkretny problem chcemy, żeby AI rozwiązało, dla których użytkowników, przy jakim pasku jakości i skąd będziemy wiedzieć, że działa?"

To pytanie jest trudniejsze do zadania na spotkaniu produktowym. Ale to jedyne, które prowadzi do systemu wartego zbudowania.

Zespoły, które widziałem, że odnoszą sukces z AI, traktują go dokładnie tak samo jak każdy inny trudny problem inżynierski: zaczynają małą, mierzą obsesyjnie, iterują na podstawie prawdziwego feedbacku od użytkowników i opierają się pokusie przebudowania wszystkiego przed udowodnieniem wartości na czymś wąskim.

Tryb awarii polega na starcie na wielką skalę, pominięciu ewaluacji i wdrożeniu czegoś, co wygląda imponująco w demo i rozpada się w produkcji.

## Co to oznacza dla Ciebie

Jeśli jesteś programistą, od którego proszą o „dodanie AI": zakwestionuj to podejście. Zapytaj o jasność co do konkretnego przypadku użycia. Zapytaj, kto zdefiniuje, jak wygląda „dobry" wynik. Zbuduj infrastrukturę ewaluacji zanim zbudujesz funkcję.

Jeśli jesteś liderem proszącym swój zespół o „dodanie AI": zrozum, że prosisz ich o nawigowanie w nowej dyscyplinie inżynierskiej z produkcyjnymi stawkami. Daj im czas na niewidoczną pracę — przygotowanie danych, ewaluacja, iteracja — która nie pokaże się w demo, ale zadecyduje o tym, czy system faktycznie działa.

Technologia jest naprawdę potężna. Ale nie dodaje się sama. A udawanie inaczej to sposób, w jaki dobre zespoły kończą na budowaniu imponujących dem, które zawodzą użytkowników.

Jakie są Twoje doświadczenia z tym? Czy byłeś po stronie odbierającej żądania „po prostu dodaj AI"? Chciałbym szczerze wiedzieć, jak zespoły sobie z tym radzą.
