---
day: 44
title: "RAG to produkt, nie chatbot na dokumentach"
pillar: Educator
language: pl
image: ../../images/day-44.jpg
image_unsplash_query: "product design blueprint planning framework user journey"
---

# RAG to produkt, nie chatbot na dokumentach

"Chcemy dodać chatbota do naszych dokumentów." Słyszałem to zdanie na początku każdego projektu RAG, który potem miał problemy. Nie dlatego, że pomysł jest zły — ale dlatego, że to nie jest specyfikacja produktowa. To sugestia architektury ubrana w wymaganie.

Co dzieje się potem — jest przewidywalne. Trzy miesiące budowania, potem kolejne trzy miesiące "dlaczego jakość nie jest lepsza?" bez wspólnej definicji co "lepsza" znaczy i dla kogo.

Zbudowałem trzy systemy RAG. Ten, który działa dobrze na produkcji, był pierwszym, przy którym zaczęliśmy od myślenia produktowego zanim napisaliśmy linijkę kodu.

---

## Co "chatbot na dokumentach" pomija

Specyfikacja produktowa odpowiada na pięć pytań:
1. Kto tego używa?
2. O co pytają?
3. Jak wygląda "dobrze" i jak to zmierzymy?
4. Co się dzieje gdy system nie wie?
5. Jak uczymy się i poprawiamy w czasie?

"Chatbot na dokumentach" nie odpowiada na żadne z nich. Opisuje metaforę interfejsu, nie produkt.

Konsekwencja: każdy członek zespołu wypełnia luki własnymi założeniami. Inżynierowie budują pod pytania, które ich zdaniem zadają użytkownicy. Produkt ocenia według intuicji "brzmi dobrze." Użytkownicy przychodzą z zupełnie innymi modelami mentalnymi. Wszyscy są rozczarowani i nikt nie zgadza się dlaczego.

Architektura techniczna wynika ze specyfikacji produktowej. Jeśli nie masz specyfikacji produktowej, nie wiesz jakiej architektury potrzebujesz.

---

## Krok 1: Persony użytkowników i ich rzeczywiste pytania

Pierwszą rzeczą, którą zrobiliśmy dla naszego RAG-a dla brokerów ubezpieczeniowych, było spędzenie dwóch tygodni bez budowania czegokolwiek. Przeprowadziliśmy wywiady z sześcioma brokerami, przeczytaliśmy trzy miesiące logów e-mailowych do supportu i obserwowaliśmy jak brokerzy nawigują po istniejącej dokumentacji polisowej.

Z tych badań wyodrębniliśmy jedenaście odrębnych intencji zapytań:

1. **Lookup faktu**: "Co dokładnie mówi polisa o X?" — jedno źródło, kluczowa precyzja
2. **Porównanie produktów**: "Czym wariant A różni się od B?" — wiele źródeł, kluczowa kompletność
3. **Procedura krok po kroku**: "Jak krok po kroku zarejestrować szkodę?" — sekwencyjne, kluczowy format
4. **Sprawdzenie wyłączenia**: "Czy X jest wykluczone z ochrony?" — kluczowa precyzja, fałszywie negatywne niedopuszczalne
5. **Szacowanie składki**: "Ile mniej więcej kosztuje to dla klienta z profilem Y?" — bliskie kalkulacji, wymaga jawnego komunikowania niepewności
6. **Interpretacja klauzuli**: "Co konkretnie oznacza termin Z w tej polisie?" — język prawny, wymaga dosłownego cytatu
7. **Porównanie historyczne**: "Czy ten warunek zmienił się względem poprzedniej wersji polisy?" — uwzględniający wersje, wymaga metadanych dokumentu
8. **Multidokumentowa synteza**: "Porównaj ochronę A, B i C dla scenariusza X" — złożony retrieval, wysoka latencja akceptowalna
9. **Analiza edge case**: "Co się dzieje gdy Y i Z wystąpią jednocześnie?" — niski confidence retrieval oczekiwany, kluczowa ścieżka eskalacji
10. **Odmowa poza zakresem**: "Czy powinienem polecić ten produkt klientowi?" — nie pytanie o wiedzę, wymaga twardej granicy
11. **Eskalacja do człowieka**: "Muszę porozmawiać z underwriterem w tej sprawie" — routing, nie odpowiadanie

Te jedenaście intencji nie jest równoważnych. Każda ma inne wymagania dotyczące formatu odpowiedzi, akceptowalnej latencji, wymagania precyzji i akceptowalnego trybu błędu.

---

## Krok 2: Kontrakt jakości

Gdy masz intencje, musisz zdefiniować co "działanie poprawnie" oznacza dla każdej z nich. Nazywam to kontraktem jakości — jawne, uzgodnione cele, które rządzą tym co budujesz i jak to oceniasz.

Dla każdej intencji kontrakt jakości określa:

| Wymiar | Przykład dla Lookup faktu | Przykład dla Multidok. syntezy |
|---|---|---|
| Cel precision | > 0.95 | > 0.82 |
| Cel recall | > 0.80 | > 0.75 |
| Latencja (p95) | < 2s | < 8s |
| Format | Krótka odpowiedź + dosłowny cytat | Ustrukturyzowana tabela + cytowania |
| Tryb błędu | Twarda blokada + "nie mam tej informacji" | Częściowa odpowiedź + "ochrona niekompletna" |
| Wymagany przegląd? | Nie (jeśli retrieval gate przeszedł) | Ludzki przegląd dla zapytań wysokiego ryzyka |

Bez tej tabeli każda dyskusja o jakości to negocjacja bez punktu odniesienia. Z nią możesz spojrzeć na metryki produkcyjne i powiedzieć: "Lookup faktu jest na 0.91 precision, poniżej kontraktu. Oto konkretny klaster błędów."

Kontrakt jakości wymusza też rozmowy, których inżynierowie unikają, a product managerowie nie wiedzą żeby zadawać:
- Jaki jest akceptowalny wskaźnik fałszywie negatywnych dla sprawdzeń wyłączeń? (Odpowiedź w ubezpieczeniach: 0. Każde przeoczone wyłączenie to potencjalna odpowiedzialność prawna.)
- Czy 6-sekundowa odpowiedź jest akceptowalna dla multidokumentowej syntezy? (Odpowiedź od brokerów: tak, poczekają jeśli porównanie jest kompletne. Nie poczekają 6 sekund na prosty fakt.)
- Co dokładnie mówi system gdy nie wie? (Nie "nie wiem" — dokładne sformułowanie ma znaczenie dla zaufania użytkowników.)

---

## Krok 3: Tryby błędu — odmowa, eskalacja czy zastrzeżenie

Każdy system RAG napotka pytania, na które nie może dobrze odpowiedzieć. Pytanie brzmi co wtedy robi.

Trzy opcje:
1. **Odmowa**: "Nie mam informacji na ten temat. Prosimy skontaktować się z [X]."
2. **Eskalacja**: "To pytanie wymaga specjalistycznego wkładu. Łączę z underwriterem."
3. **Zastrzeżenie**: "Na podstawie dostępnej dokumentacji wydaje się, że X — ale tę interpretację należy potwierdzić ze specjalistą."

Właściwa odpowiedź zależy od intencji i stawek.

Dla lookup faktu z niskim confidence retrieval: odmowa. Nie zgadujemy limitów ochrony.

Dla analizy edge case: zastrzeżenie z jawnym wskaźnikiem pewności i ścieżką eskalacji.

Dla pytań poza zakresem (nasza intencja 10): natychmiastowa odmowa, zanim w ogóle uruchomi się retrieval. To decyzje architektoniczne, które całkowicie omijają LLM.

Dla próśb o eskalację do człowieka (intencja 11): funkcja routingu, nie generacji. Wykrywamy tę intencję i routujemy do kolejki supportu brokera.

**Projekt trybu błędu jest decyzją produktową, nie inżynierską.** Inżynierowie go implementują; produkt musi go zdefiniować. To co system robi gdy nie wie jest tak samo ważne jak to co robi gdy wie.

---

## Krok 4: Jak routing oparty na intencjach zmienił architekturę

Zaczęliśmy z jednym pipeline. Wdrożyliśmy na produkcję z czterema ścieżkami pipeline obsługującymi jedenaście intencji.

**Ścieżka A: Precision retrieval** (intencje 1, 4, 6)
- Scope'owany retrieval z wysokim progiem similarity (0.78)
- Retrieval gate na 0.78 — twarda blokada jeśli nieosiągnięty
- LLM-as-judge sprawdzenie wiarygodności
- Format krótkiej odpowiedzi z dosłownym cytatem

**Ścieżka B: Synteza** (intencje 2, 5, 8)
- Multi-chunk retrieval z jawnym rozdzielaniem źródeł
- Sprawdzenie spójności między dokumentami
- Ustrukturyzowany output z cytowaniami per-źródło
- Wyższy budżet latencji (do 8s)

**Ścieżka C: Procedura sekwencyjna** (intencja 3)
- Retrieval z filtrem metadanych specyficznie dla dokumentów proceduralnych
- Wymuszony format listy numerowanej
- Brak sprawdzenia wiarygodności (format jest głównym sygnałem jakości)

**Ścieżka D: Routing i odmowa** (intencje 7, 9, 10, 11)
- Brak generacji LLM (lub minimalna)
- Klasyfikacja intencji → szablon gotowej odpowiedzi lub zewnętrzny routing
- Intencja 7 (porównanie historyczne): specjalizowany pipeline z retrieval uwzględniającym wersje
- Intencja 9 (edge case): zastrzeżenie z jawnym poziomem pewności

Jeden pipeline byłby kompromisem dla wszystkich jedenastu intencji. Surowy próg precision Ścieżki A zabiłby użyteczność dla intencji 8 (multidokumentowa synteza regularnie schodzi poniżej 0.78, bo zapytania między dokumentami są z natury trudniejsze). Podejście syntezy Ścieżki B wprowadziłoby niepotrzebną złożoność i latencję dla prostych lookup faktów.

Architektura wynikła z wymagań produktowych. Bez taksonomii intencji i kontraktu jakości zbudowalibyśmy ogólny pipeline i tunili go dopóki wszyscy nie byliby równo niezadowoleni.

---

## Krok 5: Pętla feedback — zbieranie sygnałów od użytkowników

Zestawy ewaluacyjne mówią ci co się działo w przeszłości. Sygnały użytkowników mówią ci co dzieje się teraz.

Zbieramy trzy typy sygnałów:

**Jawny feedback**: Po każdej odpowiedzi kciuk w górę/dół. Niskie tarcie, niska jakość sygnału — ale wolumen kompensuje. Śledzmy wskaźnik kciuka w dół per intencja jako wiodący wskaźnik dryfu jakości.

**Niejawny feedback**: Czy użytkownik zadał pytanie uzupełniające od razu? Czy skopiował odpowiedź czy porzucił rozmowę? Te behawioralne sygnały korelują z jakością odpowiedzi bez wymagania aktywnego inputu użytkownika.

**Wskaźnik eskalacji per intencja**: Jeśli brokerzy coraz częściej eskalują zapytania o edge case (intencja 9) do ludzkiego supportu, to mówi nam że kalibracja pewności systemu dla tej intencji jest zepsuta — albo za dużo odmawia (i użytkownicy eskalują jako obejście) albo odpowiada gdy nie powinien i użytkownicy eskalują żeby zweryfikować.

Dane feedback zasilają kwartalne rekalibracje kontraktów jakości i coroczną ponowną ocenę taksonomii intencji.

---

## Krok 6: Ewaluacja jako metryka produktowa

Ostatnia zmiana myślenia: ewaluacja RAG to nie metryka techniczna. To KPI produktowe.

Precision na canary test set to nie "liczba, którą śledzi twój zespół ML." To odpowiednik uptime — metryka mówiąca ci czy produkt realizuje swój cel.

Cele kontraktu jakości z Kroku 2 to twoje SLA. Narusz je, a masz incydent produktowy, nie problem inżynierski.

To framingowanie zmienia rozmowy. Gdy precision dla lookup faktu spada z 0.95 do 0.91, to nie "model nie domaga." To "jesteśmy poniżej SLA dla najbardziej krytycznego przypadku użycia i musimy zrozumieć przyczynę i naprawić to w [terminie]."

Produkt to posiada. Inżyniering to implementuje. Liczby istnieją we wspólnych dashboardach, nie tylko w logach eksperymentów ML.

---

## RAG Product Canvas

Szablon, którego używam na początku każdego projektu RAG:

**Sekcja 1: Użytkownicy**
- Persona primarna, persona wtórna
- Top 10 pytań każdej osoby (z rzeczywistych badań, nie założeń)
- Rozkład częstotliwości między intencjami

**Sekcja 2: Kontrakt jakości**
- Tabela: intencja × (precision, recall, latencja, format, tryb błędu)
- Jawna lista "tego nigdy nie może się zdarzyć" (dla ubezpieczeń: błędne kwoty ochrony, przeoczone wyłączenia)

**Sekcja 3: Ograniczenia architektoniczne**
- Wymagania compliance (data residency, PII, audit trail)
- Punkty integracji z istniejącymi systemami
- Ograniczenia operacyjne (rozmiar zespołu do utrzymania, obwiednia budżetu)

**Sekcja 4: Plan ewaluacji**
- Skład canary test set i kadencja aktualizacji
- Mechanizm zbierania sygnałów użytkowników
- Harmonogram przeglądu i rekalibracji

**Sekcja 5: Otwarte pytania**
- Rzeczy, które specyfikacja pozostawia niejednoznaczne, z właścicielem i terminem

Napisz "RAG CANVAS" w komentarzu jeśli chcesz szablon.

---

## Podsumowanie

"Chatbot na dokumentach" to nie specyfikacja produktowa. To życzenie na start.

Droga od życzenia do działającego produktu prowadzi przez:
1. Rzeczywiste badania użytkowników → taksonomia intencji
2. Taksonomia intencji → kontrakt jakości
3. Kontrakt jakości → decyzje architektoniczne
4. Architektura + deployment → pętle feedback
5. Pętle feedback → ciągła rekalibracja

Jeden system RAG, który zbudowaliśmy tą metodą, działa na produkcji od ośmiu miesięcy z mierzalnymi celami jakości i wspólnym rozumieniem w zespole co oznacza sukces. Pozostałe były przebudowywane więcej niż raz, bo nikt nie zgadzał się co budujemy.

Zacznij od canvas produktowego. Architekturę buduj na drugim miejscu.
