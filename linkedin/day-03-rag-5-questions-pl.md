---
day: 3
title_pl: "Zanim zbudujesz swój pierwszy system RAG, odpowiedz na te 5 pytań."
pillar: Educator
format: Checklist
scheduled_date: 2026-03-25
posting_time: "07:30 CET"
hashtags: ["#RAG", "#AI", "#InżynieriaOprogramowania", "#MachineLearning"]
image: ../images/day-03.jpg
cta: "Zapisz na swój następny projekt"
blog_url: "https://mmx3.pl/blog/day-03-rag-5-questions"
---

Zanim zbudujesz swój pierwszy system RAG, odpowiedz na te 5 pytań.

Zbudowałem 3 systemy RAG w produkcji. Pierwsze dwa miały odpowiedzi na niektóre z tych pytań. Trzeci miał odpowiedzi na wszystkie. Zgadnij, który nadal działa 😅

**1. Jaka jest rzeczywista jakość Twoich danych źródłowych?**
Nie „czy są gdzieś przechowywane," ale: czy są spójne, ustrukturyzowane, kompletne? W ubezpieczeniach mam dokumenty polisowe z 15 lat wstecz w 4 różnych formatach. Pliki PDF z zeskanowanym tekstem. Arkusze Excel skonwertowane do CSV. Problemy z jakością na wejściu stają się błędami retrieval na wyjściu — gwarantowane.

**2. Jaka jest Twoja strategia chunkowania i dlaczego?**
Większość tutoriali dzieli tekst według liczby tokenów. To działa dla ogólnego tekstu. Klauzule ubezpieczeniowe mają kontekst prawny. Podziel jedną w złym miejscu a pobrany chunk znaczy coś innego. Ja chunkuję według granic sekcji, nie liczby znaków.

**3. Jaki jest podział między precyzją retrieval a jakością generacji?**
Jeśli Twój retrieval zwraca nieistotne chunki, żaden model Cię nie uratuje. Spędziłem więcej czasu na dostrajaniu retrieval niż na promptach. Mierz oba oddzielnie.

**4. Jak ocenisz ten system, zanim użytkownicy go dotkną?**
Potrzebujesz zestawu testowego z prawdziwymi pytaniami i oczekiwanymi odpowiedziami. „Wydaje się że działa" to nie jest strategia ewaluacji 🫠 Zbudowałem 200 oznaczonych par Q&A z prawdziwych zapytań brokerów, zanim cokolwiek wdrożyłem.

**5. Jakie są Twoje ograniczenia compliance?**
RODO. Rezydencja danych. Logi audytowe. Wymagania dotyczące wytłumaczalności. W regulowanych branżach to nie są sprawy na po fakcie. Wbuduj je w architekturę w pierwszym dniu.

**Większość błędów RAG, które widziałem, można było uniknąć przez odpowiedzenie na te pytania przed napisaniem jednej linii kodu.**

Zapisz na swój następny projekt.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-03-rag-5-questions

#RAG #AI #InżynieriaOprogramowania #MachineLearning
