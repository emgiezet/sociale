---
day: 7
title_pl: "RAG to nie tylko wyszukiwanie + LLM. Oto część, którą większość tutoriali pomija."
pillar: Educator
format: Educational
scheduled_date: 2026-03-31
posting_time: "07:30 CET"
hashtags: ["#RAG", "#AI", "#MachineLearning", "#InżynieriaOprogramowania"]
image: ../images/day-07.jpg
cta: "Zapisz i wyślij swojemu zespołowi AI."
blog_url: "https://mmx3.pl/blog/day-07-rag-beyond-search"
---

RAG to nie tylko wyszukiwanie + LLM. Oto część, którą większość tutoriali pomija.

Każdy tutorial RAG pokazuje ten sam diagram: zembedduj dokumenty, zapisz wektory, pobierz na zapytanie, przekaż do LLM, gotowe. Ten diagram jest poprawny. Jest też niebezpiecznie niekompletny.

**Warstwa ewaluacji to miejsce, gdzie systemy RAG faktycznie żyją albo umierają.**

Oto co mam na myśli, z budowania 3 systemów RAG w produkcji:

**Jakość retrieval to odrębny problem od jakości generacji.**
Trzeba je mierzyć niezależnie. Retrieval zwracający top 5 złych chunków wyprodukuje pewne siebie złe odpowiedzi niezależnie od tego, jak dobry jest model. Śledzę recall i precyzję retrieval oddzielnie od jakości odpowiedzi. Jeśli retrieval się degraduje, wiem o tym zanim zauważą użytkownicy.

**Reranking ma znaczenie większe niż większość ludzi myśli.**
Surowe podobieństwo wektorowe pobiera semantycznie podobny tekst, niekoniecznie najbardziej trafny do odpowiedzi na konkretne pytanie. Dodałem cross-encoder reranker po początkowym kroku retrieval. Dodał opóźnienie (około 200ms), ale dokładność odpowiedzi poprawiła się wystarczająco, żeby to uzasadnić. Dla zapytań ubezpieczeniowych dokładność bije szybkość.

**Strategia chunkowania jest ważniejsza niż wybór modelu.**
Widziałem zespoły spędzające tygodnie na ocenianiu GPT-4 vs Claude vs Gemini, podczas gdy ich chunkowanie dzieli klauzule polisowe w połowie zdania 🤦 Napraw chunkowanie. Model ma mniejsze znaczenie niż myślisz na tym etapie.

**Potrzebujesz oznaczonego datasetu ewaluacyjnego przed wdrożeniem.**
Nie po. Przed. Mój ma 200 pytań brokerów z oczekiwanymi odpowiedziami, wyciągniętych z prawdziwych ticketów wsparcia. Uruchamiam go przy każdej znaczącej zmianie. Jeśli dokładność spada o więcej niż 3%, nie wdrażam. Bez wyjątków 🚫

**RAG to system inżynierski, nie prompt. Traktuj go jak jeden.**

Zapisz i wyślij swojemu zespołowi AI.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-07-rag-beyond-search

#RAG #AI #MachineLearning #InżynieriaOprogramowania
