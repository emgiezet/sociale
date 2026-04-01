---
day: 42
title: "RAG nie eliminuje halucynacji — zmienia ich charakter"
pillar: Educator
language: pl
image: ../../images/day-42.jpg
image_unsplash_query: "AI safety checkpoint inspection quality control"
---

# RAG nie eliminuje halucynacji — zmienia ich charakter

Krąży przekonanie, powtarzane w demach i prezentacjach sprzedażowych, że RAG rozwiązuje problem halucynacji. Model nie wymyśla — czyta z twoich dokumentów i odpowiada na podstawie źródeł. Sprawa zamknięta.

Zbudowałem trzy systemy RAG na produkcji. Dwa z nich nauczyły mnie kosztownych lekcji. To przekonanie jest błędne — i błędne w konkretny, niebezpieczny sposób: RAG nie eliminuje halucynacji, tylko sprawia, że trudniej je wykryć.

Halucynujący system RAG odpowiada pewnie, cytuje źródło i myli się subtelnie. W ubezpieczeniach, gdzie pracuję, "subtelnie" oznacza podanie błędnej kwoty franszyzy, błędną interpretację zakresu ochrony albo połączenie dwóch polis w fikcyjną trzecią. Każdy taki błąd ma konsekwencje prawne i finansowe.

Ten artykuł opisuje pipeline pięciu checkpointów antyhalucynacyjnych, który zbudowałem — co każdy kosztuje i gdzie jest granica między "ostrożnym systemem" a "systemem, który nic nie odpowiada."

---

## Dlaczego RAG zmienia (ale nie naprawia) halucynacji

Klasyczny LLM halucynujący jest relatywnie łatwy do wykrycia: wymyśla encje, produkuje fakty bez zakorzenienia. Sygnałem jest brak — żadne prawdziwe źródło nie stoi za twierdzeniem.

System RAG halucynujący jest trudniejszy. Model pobrał prawdziwe dokumenty. Ma prawdziwy kontekst. Błąd pojawia się na warstwie syntezy:

- **Luźna parafraza**: model streszcza fragment, ale dryfuje od jego precyzyjnego znaczenia. "Ochrona obejmuje szkody przypadkowe" staje się "ochrona obejmuje wszystkie szkody."
- **Łączenie dokumentów**: dwa fragmenty z różnych polis trafiają razem. Żaden z osobna nie jest błędny, ale połączona odpowiedź jest fikcją.
- **Ekstrapolacja z podobnych przypadków**: pobrany dokument nie odpowiada bezpośrednio na pytanie, model wnioskuje z analogicznego przypadku — bez zaznaczenia, że to wniosek, nie cytat.
- **Pewność przy słabym retrieval**: retriever zwraca fragment z wynikiem 0.61, ale LLM traktuje go jak autorytatywne źródło.

Wspólny mianownik: model działa z pewnością, na którą nie zasłużył. Halucynacja jest ubrana w autorytet cytatu.

---

## Pipeline pięciu checkpointów

Zbudowałem ten pipeline iteracyjnie przez około osiem miesięcy produkcyjnego działania RAG na dokumentach ubezpieczeniowych. Każdy checkpoint był odpowiedzią na realny przypadek błędu, nie na teoretyczną ostrożność.

### Checkpoint 1: Retrieval precision gate

**Co robi**: Zanim pobrany kontekst trafia do LLM, oceniam wyniki relevance score dla top-k fragmentów. Jeśli najlepszy fragment jest poniżej progu, pipeline odmawia kontynuacji.

**Nasz próg**: 0.72 cosine similarity na osadzeniach z Amazon Titan Embed v2. Ta wartość była kalibrowana ręcznie na 500 zapytaniach otagowanych jako "retrievable" lub "not retrievable" i znalezieniu granicy dającej <5% false positives.

**Implementacja**:
```python
def retrieval_gate(chunks: list[ScoredChunk], threshold: float = 0.72) -> bool:
    if not chunks:
        return False
    top_score = chunks[0].score
    if top_score < threshold:
        logger.info(f"Retrieval gate zablokował: score {top_score:.3f} < {threshold}")
        return False
    return True
```

**Co wychwytuje**: Zapytania o tematyce nieznanej systemowi, które zwracają słabo powiązane fragmenty. Zmusza system do odpowiedzi "Nie mam informacji na ten temat" zamiast generowania odpowiedzi z nieistotnego kontekstu.

**Koszt**: Praktycznie zerowy — wyniki score i tak pochodzą z kroku retrieval.

### Checkpoint 2: LLM-as-judge — weryfikacja wiarygodności

**Co robi**: Osobny, mniejszy model (Claude Haiku w naszym przypadku) ocenia, czy wygenerowana odpowiedź jest zakorzeniona w dostarczonym kontekście. Otrzymuje pytanie, pobrane fragmenty i roboczą odpowiedź, zwraca werdykt: wiarygodna, częściowo wiarygodna, lub niewiarygodna.

**Szkielet promptu**:
```
Jesteś ewaluatorem wiarygodności. Mając pytanie użytkownika, pobrany kontekst 
i odpowiedź asystenta, oceń czy każde twierdzenie faktyczne w odpowiedzi 
jest bezpośrednio poparte przez kontekst.

Zwróć JSON: {"verdict": "faithful|partial|unfaithful", "reason": "..."}

Nie karaj odpowiedzi za niekompletność. Karaj tylko za twierdzenia nieobecne 
lub niemożliwe do wywnioskowania z kontekstu.
```

**Nasze progi**: `faithful` → kontynuuj; `partial` → loguj i oznacz do przeglądu, zwróć odpowiedź z zastrzeżeniem; `unfaithful` → zablokuj, zwróć "Nie mogę potwierdzić tego na podstawie dostępnych dokumentów."

**Opóźnienie**: ~150ms średnio dla kontekstu 500 tokenów. Akceptowalne dla naszego przypadku (asynchroniczne zapytania o dokumenty).

**Koszt (szacunek)**: ~$0.0003 za wywołanie przy cenach Haiku. Przy 5 000 zapytań/dzień to ~45$/miesiąc.

**Co wychwytuje**: Najczęstszy tryb błędu — model parafrazuje kontekst w sposób, który subtelnie zmienia znaczenie. "Franszyza obowiązuje od trzeciej szkody" sparafrazowane jako "franszyza obowiązuje po trzeciej szkodzie."

### Checkpoint 3: Wyrównanie źródła z odpowiedzią

**Co robi**: Wyciąga kluczowe wartości liczbowe i terminy z wygenerowanej odpowiedzi, następnie sprawdza czy te konkretne wartości pojawiają się w cytowanych fragmentach źródłowych.

To jest celowo proste — nie pipeline NLP, tylko ustrukturyzowana ekstrakcja i lookup.

**Szkic implementacji**:
```python
def source_alignment_check(answer: str, chunks: list[ScoredChunk]) -> AlignmentResult:
    extracted = extract_key_terms(answer)  # regex + tabela ubezpieczeniowa
    
    chunk_text = " ".join(c.text for c in chunks)
    
    missing = []
    for term in extracted.numbers + extracted.named_terms:
        if term not in chunk_text:
            missing.append(term)
    
    if missing:
        return AlignmentResult(aligned=False, missing_terms=missing)
    return AlignmentResult(aligned=True)
```

**Co wychwytuje**: Halucynację, która mnie martwi najbardziej w ubezpieczeniach — sfabrykowane lub błędnie zacytowane liczby. Model generujący "franszyza 2 000 PLN" gdy źródło mówi "1 500 PLN" nie przejdzie tego checkpointu.

**Ograniczenie**: Nie wychwytuje halucynowanych twierdzeń jakościowych bez unikalnych terminów. Checkpoint 2 zajmuje się tymi przypadkami.

### Checkpoint 4: Scoring pewności

**Co robi**: Generujący LLM raportuje własną pewność jako pole w strukturyzowanym output obok odpowiedzi.

Nie mam złudzeń, że LLM-owa samoocena pewności jest skalibrowana. Nie jest. Ale jest użytecznym sygnałem do:
1. Routowania odpowiedzi o niskiej pewności do kolejki przeglądu ludzkiego
2. Logowania do analizy dryfu w czasie

**Implementacja**: Prompt systemowy zawiera: "Po swojej odpowiedzi podaj wynik pewności 1-5, gdzie 1 = domysł, 5 = bezpośrednio i kompletnie zaadresowane przez kontekst."

Odpowiedzi z wynikiem ≤ 2 dostają flagę UI ("Ta odpowiedź może być niekompletna") i trafiają do kolejki przeglądu.

**Czego NIE robi**: Nie zastępuje checkpointów 1-3. To sygnał uzupełniający, nie brama.

### Checkpoint 5: Canary test set

**Co robi**: Utrzymywany zestaw ~80 pytań ze znanych odpowiedzi, uruchamiany przy każdym deployu i co noc na produkcji. Precision na tym zestawie musi pozostać powyżej 0.90 — inaczej dostaję alert.

To jest ciągłe testowanie regresji dla jakości halucynacji.

**Skład zestawu testowego**:
- 30 pytań faktycznych o konkretne warunki polis (kwoty, daty, wyłączenia)
- 20 pytań porównawczych między dokumentami
- 15 przypadków brzegowych (niejednoznaczna ochrona, nakładające się polisy)
- 15 pytań "powinien odmówić" — tematy poza zakresem zestawu dokumentów

**Dlaczego canary wychwytuje to, czego inne nie wychwytują**: Canary działa na poziomie systemu, włącznie z aktualizacjami modeli, zmianami modelu osadzeń i zmianami strategii chunkowania. Aktualizacja modelu Bedrock w październiku 2025 przesunęła nasze wyniki similarity o ~0.04 średnio — niezauważalne per-zapytanie, ale canary wychwycił 6-punktowy spadek precision z dnia na noc i miałem czas na rekalibrację zanim użytkownicy to zauważyli.

---

## Realny incydent: halucynacja, która przeszła cztery checkpointy

Zapytanie o limity ochrony dla roszczenia OC z polisy komunikacyjnej pojazdu komercyjnego. Model zwrócił:

> "Na podstawie dokumentu polisy X, sekcja 4.2, limit ochrony OC wynosi 500 000 PLN."

Wynik każdego checkpointu:
1. Retrieval gate: PRZESZEDŁ (score top chunka 0.81)
2. LLM faithfulness: PRZESZEDŁ (liczba pojawiała się w kontekście)
3. Source alignment: PRZESZEDŁ (500 000 PLN pojawiło się w fragmencie)
4. Confidence: PRZESZEDŁ (model ocenił się na 4/5)

Problem: sekcja 4.2 cytowanego dokumentu opisywała *inną* klasę pojazdu. Wartość 500 000 była prawdziwa, ale dotyczyła pojazdów osobowych, nie komercyjnych. Odpowiedź była technicznie obecna w pobranym tekście — ale LLM pominął warunek kwalifikujący.

Checkpoint 5, canary, wychwycił podobne pytanie w zestawie regresyjnym trzy dni po aktualizacji szablonu promptu. Test oczekiwał "ochrona dla pojazdów komercyjnych: 1 200 000 PLN" i dostał "500 000 PLN". Precision spadła do 0.87, poniżej progu. Prześledziłem to do zmiany promptu, która nieumyślnie usunęła instrukcję zachowania kontekstu klasy pojazdu.

Lekcja: checkpointy 1-4 operują na indywidualnej odpowiedzi. Tylko checkpoint 5 wychwytuje systemowe regresje dotykające całej klasy pytań.

---

## Czerwone linie w ubezpieczeniach

Trzy kategorie, gdzie każda halucynacja — bez względu na rozmiar — jest twardym blokerem:

1. **Kwoty pieniężne**: franszyzy, limity ochrony, składki. Każda rozbieżność blokuje odpowiedź.
2. **Zakres ochrony**: co jest i nie jest objęte. Przesadzone ochrony to ryzyko prawne.
3. **Wyłączenia**: co unieważnia roszczenie. Pominięcie wyłączenia to potencjalnie błędna reprezentacja.

Dla tych kategorii stosuję ostrzejsze progi: retrieval gate na 0.80 (vs 0.72 domyślnie), weryfikacja wiarygodności wymaga werdyktu "faithful" (nie "partial"), wyrównanie źródła wymaga dokładnego dopasowania liczb.

---

## Monitorowanie dryfu halucynacji w czasie

Wskaźniki halucynacji nie są stałe. Dryfują gdy:
- Dokumenty w indeksie są aktualizowane (warunki ochrony zmieniają się co roku)
- Bazowe modele LLM są aktualizowane przez dostawcę
- Rozkład zapytań się przesuwa (użytkownicy znajdują nowe sposoby pytania)

Śledzę trzy metryki w dashboardach produkcyjnych:

1. **Precision canary**: sprawdzane co noc, alerty przy 3-punktowym spadku od 30-dniowej bazy
2. **Wskaźnik odrzuceń faithfulness check**: odsetek werdyktów "unfaithful" przez 7 dni krocząco
3. **Wskaźnik odrzuceń retrieval gate**: jak często system odmawia przez słabą jakość retrieval (nagłe skoki sygnalizują problemy z indeksem dokumentów)

Te trzy liczby mówią mi czy system się pogarsza zanim użytkownicy to zauważą.

---

## Koszty i kompromisy

| Checkpoint | Dodane opóźnienie | Koszt na 1k zapytań | Co wychwytuje |
|---|---|---|---|
| Retrieval gate | ~0ms | ~0$ | Słaby kontekst |
| LLM-as-judge | ~150ms | ~0.30$ | Niewierne syntezy |
| Source alignment | ~10ms | ~0$ | Halucynacje liczb/terminów |
| Confidence scoring | ~0ms (w prompcie) | ~0$ | Sygnał routingu |
| Canary test set | Async, brak opóźnienia dla użytkownika | ~2$/uruchomienie | Systemowe regresje |

Łącznie: ~0.30$/1k zapytań za sprawdzenie wiarygodności, prawie zero za resztę. Przy 5 000 zapytań/dzień pełny pipeline kosztuje ~45$/miesiąc. Dla systemu podejmującego decyzje o ubezpieczeniach to nie jest trudny kompromis.

---

## Podsumowanie

RAG nie eliminuje halucynacji. Zmienia je z "wymyślonych faktów" w "błędnie zacytowane źródła" — które są trudniejsze do wykrycia i groźniejsze w regulowanych dziedzinach.

Pipeline pięciu checkpointów wychwytuje różne tryby błędów na różnych warstwach:
- Bramka przy jakości retrieval
- Weryfikacja wiarygodności przy syntezie
- Sprawdzenie wyrównania źródła dla kluczowych terminów
- Śledzenie pewności jako sygnał routingu
- Uruchamianie canary do wykrywania systemowego dryfu

Żaden pojedynczy checkpoint nie wystarczy. Razem obniżyły nasz wskaźnik halucynacji z ~12% (jednoetapowy RAG) do ~1.8% przez 6 miesięcy danych produkcyjnych — w domenie, gdzie pozostałe 1.8% nadal nie dają mi spać.
