---
day: 13
title_pl: "Jak skonfigurować swój pierwszy pipeline RAG z AWS Bedrock — po ludzku."
pillar: Educator
format: How-to
scheduled_date: 2026-04-08
posting_time: "07:30 CET"
hashtags: ["#RAG", "#AWS", "#AI", "#InżynieriaSoftware", "#CloudComputing"]
image: ../images/day-13.jpg
cta: "Zapisz to na przyszłość"
blog_url: "https://mmx3.pl/blog/day-13-bedrock-rag"
---

Jak skonfigurować swój pierwszy pipeline RAG z AWS Bedrock — po ludzku.

Zbudowałem 3 systemy RAG w produkcji. Za pierwszym razem spędziłem dni zbierając dokumentację, posty na blogach i próbując metodą prób i błędów. Ty nie musisz.

RAG to Retrieval-Augmented Generation. Idea: zamiast pytać LLM, co wie, najpierw dajesz mu odpowiednie dokumenty, a potem zadajesz pytanie. Odpowiedzi są zakorzenione w Twoich danych, nie w wagach treningowych.

Oto pipeline krok po kroku:

**1. Przechowuj dokumenty w S3.**
Wgraj PDF-y, dokumenty Word, zwykły tekst — cokolwiek wygląda jak Twoje dane. Knowledge Base Bedrocka ingestuje z S3. Trzymaj bucket zorganizowany według domeny lub typu źródła.

**2. Utwórz Knowledge Base w AWS Bedrock.**
To bierze dokumenty z S3, chunkuje je, embedduje przy użyciu modelu (Titan Embeddings dobrze działa) i przechowuje wektory w OpenSearch Serverless. AWS zarządza tym wszystkim za Ciebie.

**3. Zsynchronizuj Knowledge Base.**
To jest krok ingestion. Dokumenty są chunkowane (domyślnie: 300 tokenów z overlap), embeddowane i indeksowane. Dla dużych zbiorów dokumentów spodziewaj się, że zajmie to czas.

**4. Uruchom zapytanie retrieval.**
Wywołaj API `retrieve` z zapytaniem w języku naturalnym. Bedrock zwraca top-k najbardziej odpowiednich chunków z referencjami źródłowymi.

**5. Augmentuj i generuj.**
Weź pobrane chunki, zbuduj prompt zawierający je jako kontekst i wywołaj model foundation (Claude, Titan itp.) z tym promptem. Model odpowiada używając Twoich dokumentów.

Co Bedrock robi dobrze: zarządzana infrastruktura, wbudowane IAM i rozsądna postawa compliance dla workloadów EU z odpowiednią konfiguracją regionu.

Na co uważać: strategia chunkowania ma większe znaczenie, niż większość ludzi zakłada. Domyślne ustawienia działają dla ogólnego tekstu. Dokumenty techniczne, klauzule polisowe i dane strukturyzowane często wymagają niestandardowego chunkowania.

**Trudna część RAG to nie setup. To ewaluacja.** Zbuduj zestaw testowych pytań ze znanymi odpowiedziami zanim wyślesz cokolwiek. Nauczyłem się tego kosztownym sposobem.

Zapisz to na przyszłość. Pytania? Wpisz poniżej.

Pełny artykuł na blogu z kodem: https://mmx3.pl/blog/day-13-bedrock-rag

#RAG #AWS #AI #InżynieriaSoftware #CloudComputing
