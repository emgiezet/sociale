---
day: 43
title_pl: "Nasz RAG polecił produkt konkurencji. Z pełnym przekonaniem. Z poprawnym źródłem."
pillar: Builder
format: Technical
scheduled_date: 2026-05-26
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#InsurTech", "#Guardrails", "#AIArchitecture", "#ProductionAI"]
image: ../images/day-43.jpg
cta: "Jak zabezpieczasz swój RAG przed context bleed? Napisz w komentarzu."
blog_url: "https://mmx3.pl/blog/day-43-rag-guardrails"
---

Zbudowałem RAG dla brokerów ubezpieczeniowych. W pierwszym tygodniu testów system polecił produkt konkurencji. Z pełnym przekonaniem. Z poprawnym źródłem.

Nie był to błąd modelu. Był to błąd architektury.

---

**Co się stało**

Nasz RAG obsługiwał kilku ubezpieczycieli jednocześnie. Dokumenty produktowe Towarzystwa A i Towarzystwa B były w tym samym indeksie wektorowym. Zapytanie o OC komunikacyjne pobrało fragmenty z obu — bo similarity nie rozróżnia, czyj to dokument.

Model dostał kontekst z polisą Towarzystwa B, zapytanie brzmiało o ofertę Towarzystwa A i zwrócił rekomendację poprawnie ugruntowaną w pobranym kontekście. Problem: ten kontekst był z niewłaściwej firmy.

To nie jest edge case. To fundamentalna właściwość wektorowych baz danych bez scope'owania.

---

**Guardrails to nie filtr na output. To architektura.**

Pierwsza reakcja większości zespołów: "dodajmy filtr, który usuwa nazwy konkurencji z odpowiedzi." To nie rozwiązuje problemu. Model dalej będzie operował na złym kontekście — po prostu nie będzie tego pokazywał.

Poprawne podejście: guardrails na każdej warstwie pipeline.

**Warstwa 1: Context scoping** — przed retrieval filtrujemy dokumenty po atrybutach metadanych (insurer_id, product_line, document_type). LLM nigdy nie dostaje mieszanego kontekstu z różnych ubezpieczycieli, jeśli nie powinien.

**Warstwa 2: Brand safety** — post-processing output: detekcja nazw konkurencji, off-topic detection, walidacja że odpowiedź dotyczy właściwego zakresu.

**Warstwa 3: Topic boundaries** — system ma zdefiniowany zakres tematyczny. Pytania poza zakresem dostają "To pytanie wykracza poza moją wiedzę o produkcie X" — zamiast halucynacji z bliskiego tematu.

**Warstwa 4: AWS Bedrock Guardrails** — zarządzane guardrails dla compliance (RODO, PII detection), uzupełniają custom guardrails, nie zastępują.

---

**Kluczowe odkrycie z testowania**

False positives są tak samo groźne jak false negatives. Guardrail, który blokuje zbyt dużo, sprawia, że broker dzwoni do supportu zamiast korzystać z systemu. Zmierzyłem to: powyżej 8% rejection rate użytkownicy rezygnują z narzędzia.

Kalibracja guardrails to nie jednorazowe ćwiczenie. To ciągły proces z czerwonym teamem — ktoś próbuje aktywnie obejść system — i zestawem testów w CI.

Adversarial test set: 150 pytań zaprojektowanych żeby wyciągnąć błędną odpowiedź. Uruchamiam przy każdym deployu.

---

**Insly-specific: co jest wymaganiem nie opcją**

→ Żadnych produktów konkurencji w odpowiedzi bez jawnego scope'u porównawczego  
→ Żadnych porad poza zakresem polisy (to jest zadanie agenta, nie RAG-a)  
→ PII detection na wejściu i wyjściu (RODO, dane klientów)  
→ Pełny audit trail każdej odpowiedzi

Każdy z tych punktów to nie "nice to have." To wymóg regulacyjny lub biznesowy.

---

Na blogu opisuję pełną architekturę czterech warstw guardrails, porównanie managed vs custom Bedrock Guardrails i jak zbudować adversarial test set który faktycznie testuje twój system — nie tylko uspokaja sumienie.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-43-rag-guardrails

#RAG #AI #LLM #InsurTech #Guardrails #AIArchitecture #ProductionAI
