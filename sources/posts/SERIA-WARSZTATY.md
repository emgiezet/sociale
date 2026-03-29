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

## Kolejne kroki (wszystkie serie)

1. Dodać materiały z warsztatów do repo (seria warsztatowa)
2. Wypełnić szkielety postów konkretnymi danymi, przykładami i cytatami
3. Przygotować dane kosztowe do postów RAG (pricing Bedrock, GPU rental, szacunki)
4. Review całości jako spójnej narracji
