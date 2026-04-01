---
day: 45
title: "Nie ma jednego universal RAG promptu"
pillar: Educator
language: pl
image: ../../images/day-45.jpg
image_unsplash_query: "programming code text editor crafting writing precision"
---

# Nie ma jednego universal RAG promptu

Widziałem "ultimate RAG prompt" w social media. 47 linii. Działa pięknie na demo z 5 starannie dobranymi dokumentami.

W produkcji z 3000 dokumentami polis ubezpieczeniowych z wielu linii produktowych, po polsku, gdzie użytkownicy pytają o wszystko — od prostych factów do porównań ochrony między dokumentami? Halucynował na mniej więcej 40% zapytań.

Prompt nie był zły. Problem polegał na wierze, że jeden prompt może obsłużyć wszystkie scenariusze retrieval z równą kompetencją.

Ten artykuł opisuje jak myślę o inżynierii promptów RAG jako o systemie — nie jednym szablonie, ale zestawie strategii dopasowanych do intencji, jakości retrieval i charakterystyki kontekstu.

---

## Dlaczego jeden prompt zawodzi na skali

Intuicja stojąca za "jednym promptem do rządzenia wszystkimi" jest słuszna w teorii: napisz jasne instrukcje, daj modelowi dobry kontekst, uzyskaj dobre odpowiedzi. Na demach to działa, bo demo używa:
- Wysokiej jakości, wyselekcjonowanych dokumentów
- Pytań specjalnie dobranych żeby działały
- Małego corpus gdzie każde zapytanie dostaje trafny retrieval

Produkcja jest inna. Produkcja oznacza:
- Dokumenty różnej jakości, struktury i długości
- Użytkowników pytających o rzeczy, których nie przewidziałeś
- Zmienną jakość retrieval w całym corpus (niektóre tematy dobrze pokryte, inne ledwo)
- Wiele języków i rejestrów w tym samym indeksie

Prompt mówiący "odpowiedz wyczerpująco używając poniższego kontekstu" działa świetnie gdy kontekst jest doskonały. Gdy kontekst jest przeciętny (retrieval score 0.64), ten sam prompt produkuje pewnie brzmiącą odpowiedź syntetyzowaną z marginalnie istotnego tekstu. To halucynacja ubrana jako pomocność.

Naprawą nie jest lepszy jeden prompt. To system wybierający właściwy prompt dla scenariusza retrieval.

---

## Cztery zmienne w inżynierii promptów RAG

Zanim mogę wybrać strategię promptu, muszę scharakteryzować zapytanie i kontekst na czterech wymiarach:

### Zmienna 1: Typ intencji użytkownika

Różne intencje wymagają fundamentalnie różnych zachowań odpowiedzi:

**Faktual retrieval** ("Jaki jest limit odpowiedzialności OC dla pojazdów osobowych?"): Odpowiedź to konkretna wartość, która pojawia się — lub nie — w pobranym kontekście. Prompt musi priorytetyzować precyzję i dosłowny cytat ponad syntezą. Długość: krótka. Format: odpowiedź + dokładny cytat + źródło.

**Porównanie** ("Czym plan A różni się od planu B w kwestii X?"): Wymaga multi-source syntezy z jawną atrybucją źródła. Jeśli dokument A i dokument B są sprzeczne w tym samym punkcie (co zdarza się w ubezpieczeniach — ten sam termin regulacyjny, różna interpretacja firmy), prompt musi instruować model żeby ujawnił sprzeczność, a nie dowolnie ją pogodził.

**Procedura** ("Jak zgłosić roszczenie od osoby trzeciej?"): Sekwencyjne kroki, format numerowany, bez skracania. Odpowiedź jest oceniana przez kompletność procedury, nie przez faktyczną precyzję w tym samym sensie co kwota ochrony.

**Sprawdzenie wyłączenia** ("Czy szkody powodziowe są wykluczone?"): Binarna odpowiedź (tak/nie/niejasne) z cytatem wspierającym. Fałszywie negatywne (powiedzenie "nie wykluczone" gdy jest) to najgroźniejszy tryb błędu. Prompt musi być skalibrowany żeby erować w stronę "niejasne" zamiast "nie wykluczone."

### Zmienna 2: Jakość kontekstu

Mierzę jakość kontekstu przez retrieval quality score — wynik similarity top-k fragmentów.

Trzy strefy:
- **Wysoki confidence** (≥ 0.78): Kontekst jest wysoce trafny. Model może odpowiadać swobodnie używając pobranego materiału.
- **Średni confidence** (0.62–0.78): Kontekst jest trafny ale może nie adresować bezpośrednio konkretnego pytania. Model musi być ostrożniejszy z wnioskowaniem.
- **Niski confidence** (< 0.62): To powinno być zablokowane przez retrieval gate. Jeśli dotarło do etapu promptu, prompt musi być prawie w pełni defensywny.

Retrieval quality score to pojedynczy najważniejszy input do wyboru strategii promptu.

### Zmienna 3: Język i rejestr domeny

Nasze dokumenty ubezpieczeniowe są po polsku. Polski tekst w rejestrze prawnym ma cechy strukturalne wpływające na to jak prompty powinny instruować model:

- Struktury zdań są dłuższe i bardziej złożone, z więcej zagnieżdżonymi podklauzulami
- Terminy techniczne często nie mają bezpośredniego angielskiego odpowiednika i muszą być zachowane dosłownie
- Odwołania regulacyjne (do konkretnych artykułów polskiego prawa ubezpieczeniowego) nie powinny być parafrazowane

Instrukcja promptu "streszcz zwięźle" stosowana do języka polskiej umowy ubezpieczenia ma tendencję do produkowania skondensowanych parafraz, które tracą precyzję regulacyjną. Nauczyliśmy się tego w trudny sposób. Instrukcja stała się "zachowaj dosłownie wszystkie wartości liczbowe, nazwy terminów prawnych i odwołania regulacyjne."

Angielska dokumentacja techniczna jest traktowana inaczej — te same instrukcje streszczania, które zawodzą na polskich kontraktach, działają dobrze na angielskiej dokumentacji API.

### Zmienna 4: Format outputu

Ta sama treść odpowiedzi potrzebuje różnego formatowania w zależności od:
- Gdzie jest wyświetlana (interfejs portalu brokera → krótkie; szkic emaila → dłuższe + kontekst)
- Kto to czyta (broker szybko sprawdzający fakt → minimalne formatowanie; wyjaśnienie dla klienta końcowego → czytelna struktura z nagłówkami)
- Dalsze przetwarzanie (czytelnik ludzki → język naturalny; ekstrakcja danych ustrukturyzowanych → JSON)

---

## Cztery strategie promptów

### Strategia 1: High-confidence bezpośrednia odpowiedź

**Kiedy używać**: Retrieval score ≥ 0.78, intencja to faktual retrieval lub sprawdzenie wyłączenia.

**Logika głównej instrukcji**:
```
Jesteś asystentem dokumentacji ubezpieczeniowej. Odpowiedz na poniższe pytanie 
używając WYŁĄCZNIE informacji w kontekście poniżej.

Zasady:
- Cytuj dosłownie odpowiedni tekst polisy, umieszczając go w "cudzysłowach"
- Podaj dokument źródłowy i sekcję
- Jeśli odpowiedź obejmuje konkretną liczbę (kwota, data, procent), 
  uwzględnij ją dokładnie tak jak pojawia się w źródle
- Nie dodawaj informacji nieobecnych w kontekście

Pytanie: {pytanie}

Kontekst:
{pobrane_fragmenty}
```

**Co ten prompt optymalizuje**: Precyzję. Dosłowne cytowanie. Atrybucję źródła. Nie próbuje być pomocny poza tym co zawiera kontekst.

**Co poświęca**: Płynność. Te odpowiedzi mogą brzmieć mechanicznie. To jest w porządku dla brokerskiego lookup faktów — chcą liczby, nie przyjaznego wyjaśnienia.

### Strategia 2: Low-confidence ostrożna odpowiedź

**Kiedy używać**: Retrieval score 0.62–0.78, lub każda intencja gdzie retrieval gate przeszedł ale confidence jest marginalne.

**Logika głównej instrukcji**:
```
Jesteś asystentem dokumentacji ubezpieczeniowej. Kontekst poniżej może, 
ale nie musi, bezpośrednio odpowiadać na pytanie.

Zasady:
- Odpowiedz TYLKO jeśli kontekst zawiera bezpośrednią, jednoznaczną odpowiedź
- Jeśli kontekst tylko częściowo adresuje pytanie, powiedz: 
  "Dostępna dokumentacja częściowo adresuje to: [co znalazłeś]. 
   W celu pełnej odpowiedzi prosimy skonsultować [ścieżka eskalacji]."
- Jeśli kontekst nie adresuje bezpośrednio pytania, powiedz:
  "Dostępna dokumentacja nie zawiera bezpośredniej odpowiedzi na to pytanie."
- NIE wnioskuj, nie ekstrapoluj, nie rozumuj poza tym co jest jawnie stwierdzone

Pytanie: {pytanie}

Kontekst:
{pobrane_fragmenty}
```

**Co ten prompt optymalizuje**: Unikanie halucynacji gdy retrieval jest słaby. Jawnie łamie domyślny drive "bądź pomocny" modelu i zastępuje go "bądź szczery co do niepewności."

**Kluczowa instrukcja**: "NIE wnioskuj ani nie ekstrapoluj." LLM-y są trenowane żeby być pomocnymi przez wypełnianie luk wnioskowaniem. W ubezpieczeniach, wnioskowanie z marginalnie istotnej klauzuli do konkluzji o ochronie to dokładnie wzorzec halucynacji, który zapobiegamy.

### Strategia 3: Multi-source synteza

**Kiedy używać**: Retrieval score ≥ 0.78, intencja to porównanie lub multi-dokumentowa synteza.

**Logika głównej instrukcji**:
```
Jesteś asystentem dokumentacji ubezpieczeniowej porównującym informacje 
z wielu dokumentów źródłowych. Kontekst poniżej zawiera fragmenty z {n} dokumentów.

Zasady:
- Przypisz każde twierdzenie faktyczne do jego dokumentu źródłowego: 
  "[Źródło: Dokument X, Sekcja Y]"
- Jeśli dwa dokumenty zawierają sprzeczne informacje w tym samym punkcie, 
  jawnie oznacz to: "Uwaga: Dokumenty X i Y różnią się w tym punkcie: [szczegóły]"
- Nie syntetyzuj sprzecznych informacji w jedną odpowiedź — zachowaj 
  sprzeczność dla użytkownika do rozstrzygnięcia
- Ustrukturyzuj odpowiedź z wyraźnymi nagłówkami dla każdego porównywanego 
  dokumentu/wymiaru

Pytanie: {pytanie}

Kontekst:
{pobrane_fragmenty_z_etykietami_źródeł}
```

**Kluczowa zasada**: Nie gódź sprzeczności. To jest kontraintutycyjne — zazwyczaj chcemy syntetyzowanych odpowiedzi. Ale w ubezpieczeniach, jeśli Polisa A mówi "szkody powodziowe wykluczone" a Polisa B mówi "szkody powodziowe objęte ochroną z warunkami," poprawna odpowiedź to ujawnienie obu, nie uśrednianie ich.

**Co poświęca**: Zwięzłość. Odpowiedzi multi-source syntezy są długie. To jest właściwe dla przypadku użycia (brokerzy robiący badania porównawcze produktów).

### Strategia 4: Refusal prompt

**Kiedy używać**: Retrieval gate zablokował (score < 0.62), intencja zaklasyfikowana jako poza zakresem, lub wymagana jawna odmowa.

**Logika głównej instrukcji**:
```
Dostępna dokumentacja nie zawiera wystarczających informacji do wiarygodnego 
odpowiedzenia na to pytanie.

Proszę [ścieżka eskalacji zależna od typu zapytania]:
- Dla pytań o ochronę: zapoznaj się z pełną dokumentacją polisy na [link]
- Dla pytań o szkody: skontaktuj się z zespołem szkód pod [kontakt]
- Dla doradztwa produktowego: porozmawiaj ze specjalistą brokerskim

ID referencji: {query_id} (dla referencji do supportu)
```

**Uwaga**: To nie jest prompt wysyłany do LLM. To gotowa odpowiedź zwracana bezpośrednio przez pipeline gdy warunek odmowy jest spełniony. Brak wywołania LLM, brak kosztu generacji, brak ryzyka halucynacji.

Dlaczego nie pozwolić LLM powiedzieć "nie wiem"? Bo "nie wiem" w outputcie LLM jest niespójnie sformułowane, czasem wypełniane hedgingiem który nadal brzmi jak częściowa informacja, i okazjonalnie przesłaniane przez trening modelu żeby być pomocnym. Gotowa odmowa jest deterministyczna, kontrolowana i audytowalna.

---

## Dynamiczny wybór promptu: logika routingu

System wyboru promptu działa tak:

```python
def select_prompt_strategy(
    intent: QueryIntent,
    retrieval_score: float,
    source_count: int,
    language: str
) -> PromptStrategy:
    
    # Poza zakresem lub poniżej minimum: zawsze odmowa
    if intent == QueryIntent.OUT_OF_SCOPE:
        return PromptStrategy.REFUSAL
    if retrieval_score < 0.62:
        return PromptStrategy.REFUSAL
    
    # Multi-source: strategia syntezy
    if intent == QueryIntent.COMPARISON and source_count > 1:
        return PromptStrategy.MULTI_SOURCE_SYNTHESIS
    
    # Wysoki confidence: bezpośrednia odpowiedź
    if retrieval_score >= 0.78:
        return PromptStrategy.HIGH_CONFIDENCE_DIRECT
    
    # Średni confidence: ostrożna
    return PromptStrategy.LOW_CONFIDENCE_CAUTIOUS


def build_prompt(
    strategy: PromptStrategy,
    question: str,
    chunks: list[ScoredChunk],
    language: str,
    output_format: OutputFormat
) -> str:
    template = PROMPT_TEMPLATES[strategy][language]
    return template.format(
        question=question,
        retrieved_chunks=format_chunks(chunks, strategy),
        output_instructions=OUTPUT_FORMAT_INSTRUCTIONS[output_format]
    )
```

Logika routingu jest prosta. Złożoność żyje w samych szablonach promptów, które są utrzymywane per-język i per-strategia — 4 strategie × 2 języki = 8 bazowych szablonów, z wariacyjami formatu outputu na wierzchu.

---

## Anti-patterny, które zaobserwowałem i naprawiłem

### Anti-pattern 1: Zbyt długi system prompt

47-liniowy prompt, do którego nawiązałem na początku, zawierał instrukcje wzajemnie sprzeczne:
- "Bądź zwięzły" i "podaj pełny kontekst dla swojej odpowiedzi"
- "Zawsze cytuj źródła" i "utrzymaj odpowiedź czytelną"
- "Odmawiaj jeśli niepewny" i "rób co możesz żeby pomóc"

LLM-y rozwiązują sprzeczności niespójnie — różne wybory przy różnych uruchomieniach. Rezultat to wariancja odpowiedzi trudna do debugowania, bo wariancja nie jest w retrieval, jest w interpretacji promptu.

Naprawka: Jedna główna instrukcja per prompt. Nie więcej niż trzy ograniczenia wspierające. Sprzeczności w prompcie przekładają się bezpośrednio na niespójność w produkcji.

### Anti-pattern 2: Prompt stuffing

"Chain of thought, few-shot przykłady, definicja persony, format outputu, wytyczne treści, instrukcje bezpieczeństwa, instrukcje językowe, format cytowań, instrukcje fallback — wszystko w jednym prompcie."

Każdy dodatek jest indywidualnie rozsądny. Razem konkurują o uwagę modelu i zwiększają prawdopodobieństwo błędów w następowaniu instrukcji na którymkolwiek wymiarze.

Naprawka: Few-shot przykłady żyją w systemie szablonów, nie w system prompcie. Persona jest utrzymywana w jednym zdaniu. Instrukcje bezpieczeństwa są obsługiwane na warstwie architektonicznej (guardrails), nie warstwie promptu.

### Anti-pattern 3: Promptowanie dla odwagi zamiast kalibracji

"Odpowiedz nawet jeśli niepewny. Rób co możesz. Użytkownik na tobie polega."

To zachęca do halucynacji. "Rób co możesz" ze słabym retrieval oznacza pewną syntezę marginalnie istotnego kontekstu. W ubezpieczeniach to błędna reprezentacja ochrony.

Naprawka: Zamień motywacyjny język na ograniczenia behawioralne. "Odpowiedz tylko jeśli kontekst bezpośrednio to wspiera" jest bardziej niezawodne niż "bądź pomocny ale bądź szczery."

### Anti-pattern 4: Ignorowanie jakości retrieval w projektowaniu promptu

Traktowanie wszystkich zapytań tak samo bez względu na retrieval score. Ten sam prompt dla retrieval 0.87 i 0.65.

Naprawka: Retrieval score jest inputem do systemu wyboru promptu, nie tylko polem logowania.

---

## Metryki produkcyjne skuteczności strategii promptu

Śledzę wydajność na poziomie promptu w produkcji:

- **Precision per-strategia** na canary test set: czy Strategia 1 (bezpośrednia) utrzymuje ≥ 0.95?
- **Wskaźnik odmów per strategia**: czy Strategia 2 (ostrożna) za dużo odmawia? Za mało?
- **Feedback użytkowników per strategia**: wskaźniki kciuka w dół skorelowane z użytą strategią promptu
- **Wyzwalacze eskalacji**: jak często każda strategia routuje do ludzkiego przeglądu?

Gdy ostrożna strategia zaczęła generować odmowy na 22% (w górę od 14% bazy), dochodzenie ujawniło że aktualizacja corpus wprowadziła nowe formaty dokumentów z krótszymi, mniej bogatymi w kontekst fragmentami — powodując że więcej zapytań trafiało do strefy średniego confidence. Naprawą było re-tuning rozmiaru chunka dla nowego formatu dokumentu, nie zmiana promptu.

---

## Podsumowanie

Universal RAG prompt zawodzi, bo zakłada jednorodną jakość retrieval i jednorodne wymagania odpowiedzi. Produkcja nie jest ani jednym, ani drugim.

Strategia promptu w RAG powinna być funkcją:
1. Typu intencji użytkownika (jakiej odpowiedzi potrzeba?)
2. Retrieval quality score (jak pewni możemy być kontekstu?)
3. Domeny i języka (co znaczy "cytuj dokładnie" dla tego corpus?)
4. Formatu outputu (kto to czyta i gdzie?)

Cztery strategie pokrywają przestrzeń: high-confidence bezpośrednia, low-confidence ostrożna, multi-source synteza i gotowa odmowa. Dynamiczny routing wybiera między nimi na podstawie retrieval score i intencji.

47-liniowy universal prompt nie zawodzi dlatego że jest długi. Zawodzi dlatego że próbuje być jednocześnie wszystkimi czterema strategiami.
