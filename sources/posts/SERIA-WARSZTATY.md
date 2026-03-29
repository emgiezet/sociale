# Seria postów LinkedIn — Warsztaty AI dla zespołu deweloperskiego

## Context

Max przeprowadził warsztaty w Insly dla 15-osobowego zespołu programistów, żeby odblokować ich potencjał w nowych projektach produkcyjnych i projektach legacy. Teraz chce tę historię opowiedzieć na LinkedIn w serii 5-7 postów po polsku, w formie kontynuacji istniejącej serii 30-dniowej (day-31+). Cel biznesowy: przyciągnąć firmy do skorzystania z oferty przeprowadzenia takich warsztatów.

## Parametry serii

- **Język:** Polski
- **Format:** Kontynuacja serii (day-31, day-32, ...)
- **Liczba postów:** 6
- **CTA:** Stopniowo — pierwsze posty = wartość, ostatnie = wyraźne CTA sprzedażowe
- **Pillar:** Trenches / Educator

## Plan serii — 6 postów

### Post 1 — `day-31-warsztaty-dlaczego.md` — Hook: Problem

**Tytuł:** „15 programistów, 20 lat doświadczenia łącznie — i strach przed AI. Oto dlaczego zorganizowałem warsztaty."

- Postawienie problemu: zespoły deweloperskie boją się AI / nie wiedzą jak zacząć
- Osobista historia — dlaczego zdecydowałem się na warsztaty w Insly
- Format: Story post
- CTA: Pytanie angażujące — „Jak wygląda to u Was w zespole?"

### Post 2 — `day-32-warsztaty-zakres.md` — Co obejmowały warsztaty

**Tytuł:** „Oto dokładny zakres warsztatów AI, które przeprowadziłem dla 15 programistów."

- Konkretny zakres: co było na agendzie, jakie tematy, ile dni
- Podział na nowe projekty vs legacy
- Format: Breakdown / edukacyjny
- CTA: „Zapisz sobie ten post jeśli planujesz coś podobnego"

### Post 3 — `day-33-warsztaty-legacy.md` — Deep dive: Legacy

**Tytuł:** „Największy opór nie był techniczny. Był w głowach programistów pracujących z legacy kodem."

- Jak AI pomaga w pracy z legacy (refactoring, zrozumienie kodu, testy)
- Konkretne techniki / podejścia z warsztatów
- Przełomowy moment zespołu
- Format: Observation / Trenches
- CTA: „Masz legacy system? Napisz w komentarzu co jest Twoim największym wyzwaniem"

### Post 4 — `day-34-warsztaty-nowe-projekty.md` — Deep dive: Nowe projekty

**Tytuł:** „Nowe projekty z AI od dnia zero wyglądają zupełnie inaczej. Oto co pokazałem zespołowi."

- AI-first workflow w nowych projektach
- Konkretne narzędzia i podejścia
- Efekty: szybkość, jakość, pewność zespołu
- Format: How-to / Trenches
- CTA: „Które z tych podejść stosujesz? A które Cię zaskoczyło?"

### Post 5 — `day-35-warsztaty-wyniki.md` — Wyniki i transformacja

**Tytuł:** „Co się zmieniło w zespole 3 tygodnie po warsztatach? Oto twarde dane."

- Mierzalne rezultaty (jeśli dostępne z materiałów)
- Zmiana mindset'u zespołu — przed vs po
- Cytaty / feedback od uczestników
- Format: Case study / Results
- CTA: Przejście do oferty — „Jeśli chcesz takich wyników u siebie — czytaj dalej"

### Post 6 — `day-36-warsztaty-oferta.md` — Oferta / CTA sprzedażowe

**Tytuł:** „Przeprowadzam warsztaty AI dla zespołów deweloperskich. Oto dla kogo to jest — i dla kogo nie."

- Jasna oferta: co dostajesz, dla kogo, czego NIE robię
- Social proof z Insly
- Konkretny next step (DM, link, formularz)
- Format: Course tease / Offer
- CTA: Bezpośrednie — „Napisz do mnie 'WARSZTATY' jeśli chcesz porozmawiać"

---

# Seria RAG Deep Dive: Koszty, Modele, Dane

## Context

Trzy posty techniczne rozwijające wątki RAG z serii 30-dniowej. Cel: pokazać praktyczną wiedzę, której nie ma w tutorialach. Pozycjonowanie jako ekspert, który zna realne koszty i kompromisy, nie tylko architekturę.

## Strategia: LinkedIn jako zajawka bloga

Każdy post LinkedIn to skondensowana wersja pełnego artykułu na blogu. Post daje 30% wartości (hook, kluczowy insight, 1-2 konkrety), blog daje 100% (tabele, kalkulacje, kod, szczegółowe porównania). CTA kieruje na blog, co buduje ruch i pozycjonuje jako eksperta z głębią.

Struktura każdego posta:
- LinkedIn (PL): zajawka ~400 słów, najciekawszy fragment, kończy się "Pełne porównanie z tabelami i kalkulacjami na blogu: [link]"
- LinkedIn (EN): ten sam post po angielsku, linkuje do tego samego artykułu na blogu
- Blog: pełny artykuł z tabelami, kodem, szczegółowymi case studies

## Parametry

- **Język:** Dwujęzyczny (PL + EN, każdy post w obu wersjach)
- **Format:** Kontynuacja serii (day-37, day-38, day-39), każdy w wariancie -pl i -en
- **Pillar:** Educator / Builder
- **CTA:** Link do pełnego artykułu na blogu + zaproszenie do kontaktu

## Plan serii: 3 posty

### Post 7 -- `day-37-rag-llm-selection` -- Wybór modelu LLM pod RAG

**Pliki:** `day-37-rag-llm-selection-pl.md` + `day-37-rag-llm-selection-en.md`

**Tytuł PL:** „Claude, GPT-4, Mistral, Bielik. Który model wybrać do RAG pipeline?"
**Tytuł EN:** "Claude, GPT-4, Mistral, Bielik. How I choose an LLM for a RAG pipeline."

**LinkedIn (zajawka):**
- Hook: "Wybrałeś model do RAG-a na podstawie benchmarków? Ja też. A potem zobaczyłem rachunek."
- Kluczowy insight: koszt per 1M tokenów to dopiero początek. Liczy się jakość na Twoich danych, nie na MMLU
- 1 konkretny przykład: jak zmieniliśmy model w trakcie projektu i co to zmieniło w kosztach i jakości
- Teaser: "Pełną tabelę porównawczą z cenami, latencją i wynikami ewaluacji opisałem na blogu"
- CTA: link do bloga

**Blog (pełny artykuł):**
- Tabela porównawcza: Claude (Bedrock) vs GPT-4o vs Mistral vs Bielik (self-hosted). Kolumny: cena input/output per 1M tokenów, context window, latencja p95, obsługa polskiego, compliance story
- Kompromisy: managed API (prostsze, droższe) vs self-hosted (tańsze per token, ops overhead)
- Ewaluacja: jak testujemy modele na naszych danych. Golden test set, metryki faithfulness i retrieval
- Decision framework: flowchart "który model wybrać" w zależności od volume, języka, compliance
- Format: Technical / Comparison

### Post 8 -- `day-38-rag-data-chunking` -- Przygotowanie danych i chunking

**Pliki:** `day-38-rag-data-chunking-pl.md` + `day-38-rag-data-chunking-en.md`

**Tytuł PL:** „Twój RAG nie działa? Problem jest w danych, nie w modelu."
**Tytuł EN:** "Your RAG doesn't work? The problem is your data, not your model."

**LinkedIn (zajawka):**
- Hook: "Spędziliśmy 2 tygodnie optymalizując prompty. Potem sprawdziliśmy co retriever faktycznie zwraca. Problem był w chunkingu."
- Kluczowy insight: ta sama klauzula ubezpieczeniowa, 4 strategie chunkingu, dramatycznie różne wyniki. Pokazać 1 przykład
- Teaser: "Na blogu opisałem cały nasz pipeline: od brudnego PDF-a do czystego chunka z metadanymi. Z kodem."
- CTA: link do bloga

**Blog (pełny artykuł):**
- Garbage in, garbage out: dlaczego 60% czasu w RAG to przygotowanie danych
- Chunking strategies w praktyce: fixed-size vs semantic vs section-based vs RAPTOR (z przykładami kodu)
- Pipeline krok po kroku: czyszczenie PDF-ów, ekstrakcja struktury, metadata tagging
- Zarządzanie kontekstem: overlap, parent-child chunks, sliding window
- Context window management: jak nie zmarnować 128k tokenów na śmieci
- Wizualizacja: ta sama klauzula w 4 wariantach chunkingu z wynikami retrieval
- Format: Technical / How-to

### Post 9 -- `day-39-rag-costs` -- RAG: ile to kosztuje naprawdę

**Pliki:** `day-39-rag-costs-pl.md` + `day-39-rag-costs-en.md`

**Tytuł PL:** „Ile kosztuje RAG w produkcji? Rozbijam 3 architektury na czynniki pierwsze."
**Tytuł EN:** "What does RAG actually cost in production? I break down 3 architectures."

**LinkedIn (zajawka):**
- Hook: "Wszyscy mówią o RAG. Nikt nie mówi ile to kosztuje. Oto 3 architektury i ich realne koszty."
- Kluczowy insight: 1 tabela porównawcza (uproszczona) z monthly burn per 10k zapytań
- Zaskakujący fakt: kiedy self-hosted jest droższy niż managed (i odwrotnie)
- Teaser: "Pełną kalkulację ze wzorami, break-even pointem i ukrytymi kosztami ops opisałem na blogu"
- CTA: link do bloga + "DM jeśli chcesz policzyć koszty RAG dla swojego case"

**Blog (pełny artykuł):**
- 3 case studies kosztowe:
  - **Case 1: AWS Bedrock (managed)** - Knowledge Base + Claude via Bedrock. Embedding, OpenSearch Serverless, retrieval, generation. Monthly burn dla 10k/50k/200k zapytań
  - **Case 2: Self-hosted z GPU** - A100/H100, Mistral/Bielik. GPU rental, storage, ops, engineering time. Break-even vs managed
  - **Case 3: Hybrid** - retrieval self-hosted, generation via API
- Rozliczenie per 1M tokenów: input vs output, ukryte koszty (embedding, reranking, evaluation runs)
- Tabela break-even: od jakiego volume self-hosted się opłaca
- Czego nie widać w cenniku: ops, monitoring, ewaluacja, iteracja
- Format: Technical / Cost analysis

---

# Seria RAG Masterclass: techniki zaawansowane

## Context

Deep dive'y do technik, które day-06 ("RAG breaks at 15 documents") tylko zasygnalizował. Każdy post rozwija jeden koncept w pełny artykuł. Razem z serią "Koszty, Modele, Dane" tworzą kompletny RAG knowledge hub na blogu.

**Uwaga:** Day-06 już pokrywa temat "RAG z tutoriali pada po 15 dokumentach" i wspomina RAPTOR + HyDE. Nowe posty to deep dive'y, nie powtórki. Każdy nowy post może linkować wstecz do day-06 jako wprowadzenia.

## Parametry

- **Język:** Dwujęzyczny (PL + EN)
- **Format:** Kontynuacja serii (day-40 do day-44)
- **Pillar:** Educator / Builder
- **CTA:** Link do bloga + kontakt biznesowy w ostatnich postach

## Plan serii: 5 postów

### Post 10 -- `day-40-rag-hyde` -- HyDE: Hypothetical Document Embeddings

**Pliki:** `day-40-rag-hyde-pl.md` + `day-40-rag-hyde-en.md`

**Tytuł PL:** „Twój użytkownik pyta inaczej niż Twoje dokumenty odpowiadają. HyDE to naprawia."
**Tytuł EN:** "Your users ask questions nothing like your documents answer them. HyDE fixes that."

**LinkedIn (zajawka):**
- Hook: "Broker pyta: 'czy to pokrywa szkody powodziowe?' Klauzula w polisie mówi: 'zakres ochrony obejmuje zdarzenia losowe zgodnie z par. 4 ust. 2'. Vector search tego nie połączy."
- Kluczowy insight: HyDE generuje hipotetyczny dokument-odpowiedź i szuka po nim zamiast po pytaniu. Zmienia retrieval z "znajdź podobne słowa" na "znajdź podobne odpowiedzi"
- 1 przykład before/after: to samo pytanie, retrieval bez HyDE vs z HyDE
- Teaser: "Na blogu pokazuję implementację HyDE krok po kroku z kodem i metrykami"
- CTA: link do bloga

**Blog (pełny artykuł):**
- Problem: semantic gap między pytaniem a odpowiedzią w dokumentach domenowych
- Jak działa HyDE: LLM generuje hipotetyczną odpowiedź, embedding hipotetycznej odpowiedzi, retrieval po tym embeddingu
- Implementacja w Pythonie z przykładami kodu
- Kiedy HyDE pomaga (domain-specific jargon), kiedy szkodzi (proste pytania faktograficzne)
- Metryki: retrieval recall before/after na naszym test set
- Koszty: dodatkowe wywołanie LLM per query, kiedy to się opłaca
- Format: Technical / Deep dive
- Nawiązanie: "W day-06 wspomniałem HyDE jako jedną z technik. Oto pełny obraz."

### Post 11 -- `day-41-rag-raptor` -- RAPTOR: hierarchiczne podsumowania

**Pliki:** `day-41-rag-raptor-pl.md` + `day-41-rag-raptor-en.md`

**Tytuł PL:** „Flat chunking zabija Twój RAG. RAPTOR buduje drzewo wiedzy z Twoich dokumentów."
**Tytuł EN:** "Flat chunking is killing your RAG. RAPTOR builds a knowledge tree from your documents."

**LinkedIn (zajawka):**
- Hook: "Chunking po 300 tokenów to jak czytanie książki po jednym zdaniu. Tracisz kontekst po 3 chunkach."
- Kluczowy insight: RAPTOR buduje hierarchię: chunk -> sekcja -> dokument -> podsumowanie. Retrieval może sięgnąć na właściwy poziom abstrakcji
- 1 przykład: pytanie wymagające kontekstu z 3 sekcji dokumentu, flat chunking zwraca 1 z 3, RAPTOR zwraca podsumowanie łączące wszystkie
- Teaser: "Pełną architekturę RAPTOR z diagramami i kodem opisałem na blogu"
- CTA: link do bloga

**Blog (pełny artykuł):**
- Problem: flat chunks tracą kontekst między sekcjami dokumentu
- Jak działa RAPTOR: clustering chunks, hierarchiczne podsumowania, multi-level retrieval
- Architektura: diagram pipeline'u z RAPTOR
- Implementacja: kod Pythonowy, integracja z istniejącym pipeline
- Trade-offs: czas indeksowania (znacznie dłuższy), storage (więcej embeddingów), ale lepszy recall na pytaniach wymagających kontekstu
- Kiedy RAPTOR jest overkill (proste FAQ) vs kiedy jest niezbędny (dokumenty prawne, polisy)
- Format: Technical / Architecture

### Post 12 -- `day-42-rag-hallucinations` -- Kontrolowanie halucynacji w RAG

**Pliki:** `day-42-rag-hallucinations-pl.md` + `day-42-rag-hallucinations-en.md`

**Tytuł PL:** „Twój RAG halucynuje. Oto 5 miejsc, w których to łapiesz zanim użytkownik to zobaczy."
**Tytuł EN:** "Your RAG hallucinates. Here are 5 places to catch it before your users do."

**LinkedIn (zajawka):**
- Hook: "RAG miał wyeliminować halucynacje. W praktyce je maskuje. Model odpowiada pewnie, cytuje źródło, a źródło mówi coś innego."
- Kluczowy insight: 5 checkpointów w pipeline (retrieval quality gate, faithfulness check, source verification, confidence scoring, canary questions)
- 1 przykład: halucynacja która przeszła przez 4 z 5 checkpointów i jak ją złapał piąty
- Teaser: "Na blogu opisuję nasz pełny anti-hallucination framework z progami i metrykami"
- CTA: link do bloga

**Blog (pełny artykuł):**
- Dlaczego RAG nie eliminuje halucynacji (tylko zmienia ich charakter)
- 5 checkpointów: retrieval precision gate, LLM-as-judge faithfulness, source-answer alignment, confidence scoring, canary test set
- Implementacja każdego checkpointu z kodem
- Progi: jakie metryki ustawiamy, kiedy blokujemy odpowiedź
- Red lines: lista pytań gdzie każda halucynacja to blocker (w ubezpieczeniach: kwoty, zakresy, wyłączenia)
- Monitoring w produkcji: jak wykrywać drift halucynacji w czasie
- Format: Technical / Framework

### Post 13 -- `day-43-rag-guardrails` -- Guardrails: Twój RAG chwali konkurencję?

**Pliki:** `day-43-rag-guardrails-pl.md` + `day-43-rag-guardrails-en.md`

**Tytuł PL:** „Nasz RAG polecał produkty konkurencji. Oto jak to naprawiliśmy i czego Cię to nauczy o guardrails."
**Tytuł EN:** "Our RAG recommended competitor products. Here's how we fixed it and what it teaches about guardrails."

**LinkedIn (zajawka):**
- Hook: "Zbudowaliśmy RAG dla brokerów. W pierwszym tygodniu testów system polecił produkt konkurencji. Z pełnym przekonaniem. Z poprawnym źródłem."
- Kluczowy insight: guardrails to nie filtr na wyjściu. To architektura: context scoping, brand safety, output validation, topic boundaries
- Teaser: "Na blogu opisuję 4 warstwy guardrails które wdrożyliśmy i jak je testujesz w CI"
- CTA: link do bloga

**Blog (pełny artykuł):**
- Historia: jak RAG polecił konkurencję (context bleed między dokumentami różnych ubezpieczycieli)
- 4 warstwy guardrails:
  1. **Context scoping**: filtrowanie dokumentów po firmie/produkcie PRZED retrieval
  2. **Brand safety**: output validation, wykrywanie nazw konkurencji, off-topic detection
  3. **Topic boundaries**: system nie odpowiada na pytania spoza zdefiniowanego zakresu
  4. **AWS Bedrock Guardrails**: managed guardrails vs custom
- Testowanie guardrails w CI: adversarial test set, red teaming
- Kiedy guardrails blokują za dużo (false positives) i jak to kalibrować
- Format: Technical / Case study

### Post 14 -- `day-44-rag-product-modeling` -- Modelowanie produktu RAG

**Pliki:** `day-44-rag-product-modeling-pl.md` + `day-44-rag-product-modeling-en.md`

**Tytuł PL:** „RAG to nie feature. To produkt. Oto jak go modeluję zanim napiszę linijkę kodu."
**Tytuł EN:** "RAG is not a feature. It's a product. Here's how I model it before writing a line of code."

**LinkedIn (zajawka):**
- Hook: "Większość RAG-ów powstaje tak: 'dodajmy chatbota do naszych dokumentów'. Potem 3 miesiące walki z jakością bez zdefiniowanych celów."
- Kluczowy insight: RAG wymaga product thinkingu: kto jest użytkownikiem, jakie pytania zadaje, jaka precyzja jest akceptowalna, co się dzieje gdy system nie wie
- 1 przykład: jak zdefiniowaliśmy 11 intencji użytkownika i dlaczego to zmieniło architekturę
- Teaser: "Na blogu opisuję pełny framework modelowania produktu RAG z templatem do pobrania"
- CTA: link do bloga + "DM 'RAG PRODUCT' jeśli chcesz template"

**Blog (pełny artykuł):**
- Dlaczego "chatbot na dokumentach" to nie product spec
- Framework modelowania RAG jako produktu:
  1. User personas i ich pytania (nasze 11 intencji)
  2. Quality contract: precision/recall/latency targets per intencja
  3. Failure modes: co system robi kiedy nie wie (refuse vs escalate vs hedge)
  4. Feedback loop: jak zbierasz sygnały od użytkowników
  5. Ewaluacja jako product metric, nie tech metric
- Jak intent-based routing zmienił naszą architekturę (z jednego pipeline na 11 ścieżek)
- Template do pobrania: RAG Product Canvas
- Format: Strategic / Framework

### Post 15 -- `day-45-rag-prompt-engineering` -- Prompt Engineering w RAG: nie ma jednego promptu

**Pliki:** `day-45-rag-prompt-engineering-pl.md` + `day-45-rag-prompt-engineering-en.md`

**Tytuł PL:** „Nie ma jednego promptu do RAG. Kto Ci to powiedział, nigdy nie wdrażał RAG w produkcji."
**Tytuł EN:** "There's no silver bullet RAG prompt. Anyone who told you otherwise never shipped RAG to production."

**LinkedIn (zajawka):**
- Hook: "Widziałem 'ultimate RAG prompt' na Twitterze. 47 linii. Działa świetnie na demo z 5 dokumentami. W produkcji z 3000 dokumentów ubezpieczeniowych? Halucynuje na 40% pytań."
- Kluczowy insight: prompt w RAG to nie jeden template. To zestaw promptów dopasowanych do intencji, typu pytania i jakości kontekstu. Inny prompt gdy retriever zwraca 5 trafnych chunków, inny gdy zwraca 2 słabe
- 1 przykład: ten sam prompt, dwa pytania, dwie katastrofy. Prompt na pytanie o zakres polisy działa, prompt na pytanie o wyłączenia halucynuje
- Teaser: "Na blogu pokazuję nasze 4 strategie promptowania per typ intencji, z metrykami before/after"
- CTA: link do bloga

**Blog (pełny artykuł):**
- Mit "universal RAG prompt": dlaczego jeden prompt nie działa na wszystkie typy pytań
- Zmienne w prompt engineeringu RAG:
  1. Typ intencji użytkownika (fakt vs porównanie vs procedura)
  2. Jakość kontekstu (ile trafnych chunków, confidence score)
  3. Język i domena (polski prawniczy vs angielski techniczny)
  4. Output format (krótka odpowiedź vs szczegółowe wyjaśnienie ze źródłami)
- 4 strategie promptów które stosujemy:
  1. **High-confidence retrieval**: prompt pozwala modelowi odpowiadać swobodnie na podstawie kontekstu
  2. **Low-confidence retrieval**: prompt wymusza ostrożność, "odpowiedz tylko jeśli kontekst zawiera bezpośrednią odpowiedź"
  3. **Multi-source synthesis**: prompt do łączenia informacji z wielu chunków z cytowaniem źródeł
  4. **Refusal prompt**: kiedy system mówi "nie mam wystarczających informacji"
- Dynamic prompt selection: jak automatycznie dobieramy prompt na podstawie retrieval quality score
- Anti-patterns: za długie system prompts, contradicting instructions, prompt stuffing
- Metryki: faithfulness i answer relevance per strategia promptu
- Format: Technical / Framework

### Post 16 -- `day-46-rag-pricing-model` -- Wycena produktu RAG: model kosztów per architektura

**Pliki:** `day-46-rag-pricing-model-pl.md` + `day-46-rag-pricing-model-en.md`

**Tytuł PL:** „Klient pyta: ile będzie kosztował RAG? Oto jak to liczę zanim podam cenę."
**Tytuł EN:** "The client asks: how much will RAG cost? Here's how I calculate before quoting a price."

**Nawiązania:** Day-39 opisuje koszty infrastruktury. Day-44 opisuje modelowanie produktu. Ten post łączy oba: jak z kosztów infra i scope'u produktu zbudować wycenę dla klienta.

**LinkedIn (zajawka):**
- Hook: "Klient mówi: 'chcemy RAG-a'. Ja pytam: 'na ilu dokumentach, w jakim języku, z jakim SLA, i ile zapytań dziennie?' Bo od tego zależy czy to kosztuje 500 czy 15 000 miesięcznie."
- Kluczowy insight: wycena RAG to nie "cena za chatbota". To model kosztów zbudowany z 4 warstw: infra, development, maintenance, ewaluacja. Każda architektura (managed/self-hosted/hybrid) zmienia proporcje
- 1 przykład: ten sam use case, 3 architektury, 3 zupełnie różne ceny. Klient myślał że najtańsza opcja jest najlepsza. Okazało się że najdroższa w infra jest najtańsza w total cost of ownership
- Teaser: "Na blogu pokazuję pełny model wyceny z arkuszem kalkulacyjnym do pobrania"
- CTA: link do bloga + "DM 'RAG PRICING' jeśli wyceniasz RAG dla swojej organizacji"

**Blog (pełny artykuł):**
- Dlaczego "ile kosztuje RAG" to złe pytanie (odpowiedź: zależy od 6 zmiennych)
- 6 zmiennych wyceny:
  1. **Volume**: ilość dokumentów w bazie, ilość zapytań dziennie/miesięcznie
  2. **Język i domena**: angielski = tańsze modele, polski = droższe lub self-hosted
  3. **SLA jakości**: 80% accuracy vs 95% accuracy to 3x różnica w kosztach ewaluacji i iteracji
  4. **Compliance**: RODO, data residency, audit trail. Każde wymuszenie = koszt architektoniczny
  5. **Integracje**: standalone chatbot vs embedded w istniejący system
  6. **Maintenance**: kto utrzymuje, kto ewaluuje, kto iteruje
- 3 case studies wyceny (ten sam use case: 1000 dokumentów, 5000 zapytań/miesiąc, polski):
  - **Opcja A: Full managed (Bedrock)** - niski dev cost, wysoki recurring, ograniczona kontrola
  - **Opcja B: Self-hosted** - wysoki dev cost, niski recurring po break-even, pełna kontrola
  - **Opcja C: Hybrid** - umiarkowany dev cost, umiarkowany recurring, dobry balans
- Tabela TCO: Year 1 vs Year 2 vs Year 3 per architektura
- Ukryte koszty których klienci nie widzą: ewaluacja ongoing, model drift, reindeksacja, support
- Arkusz kalkulacyjny do pobrania: RAG Cost Calculator
- Jak prezentować wycenę klientowi: nie "cena za RAG", tylko "TCO per architektura z trade-offs"
- Format: Strategic / Business

---

## Kolejne kroki (wszystkie serie)

1. Dodać materiały z warsztatów do repo (seria warsztatowa)
2. Wypełnić szkielety postów konkretnymi danymi, przykładami i cytatami
3. Przygotować dane kosztowe do postów RAG (pricing Bedrock, GPU rental, szacunki)
4. Review całości jako spójnej narracji
5. Ustalić URL bloga i format linków w CTA
