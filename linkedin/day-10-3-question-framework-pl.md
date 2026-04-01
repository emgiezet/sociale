---
day: 10
title_pl: "Używam frameworku 3 pytań przed rozpoczęciem każdego projektu AI. Oszczędził mi miesięcy."
pillar: Educator
format: Framework
scheduled_date: 2026-04-03
posting_time: "08:00 CET"
hashtags: ["#AI", "#InżynieriaOprogramowania", "#LiderzyTechniczni", "#RAG"]
image: ../images/day-10.jpg
cta: "Napisz do mnie 'framework' po pełny szablon."
blog_url: "https://mmx3.pl/blog/day-10-3-question-framework"
---

Używam frameworku 3 pytań przed rozpoczęciem każdego projektu AI. Oszczędził mi miesięcy.

Zbudowałem 3 systemy RAG w produkcji i widziałem, jak jeden z nich kosztownie zawodzi. Od tamtej pory wymuszam na sobie odpowiedź na te trzy pytania przed napisaniem jednej linii kodu. Za każdym razem, gdy pominąłem jedno, żałowałem 🫠

**Pytanie 1: Czy to problem retrieval czy problem generacji?**

Większość żądań "AI" to zamaskowane problemy retrieval. Broker pytający "co ta polisa obejmuje?" nie potrzebuje kreatywnej odpowiedzi. Potrzebuje dokładnego tekstu z właściwego dokumentu, szybko. To retrieval. Rozwiązanie tego z generatywnym modelem dodaje złożoność, latencję i ryzyko halucynacji bez żadnej wartości dodanej.

Jeśli odpowiedź istnieje w Twoich danych i po prostu musi być znaleziona: optymalizuj retrieval.
Jeśli odpowiedź musi być syntezowana z wielu źródeł: wtedy potrzebujesz generacji.

Pomylenie tego kosztuje miesiące.

**Pytanie 2: Jaka jest granica compliance?**

W ubezpieczeniach to pytanie ma zęby. Zanim cokolwiek zacznę budować, mapuję:
→ Jakich danych dotyka ten system?
→ Gdzie te dane żyją i czy mogą opuścić tę jurysdykcję?
→ Czy automatyczne decyzje z użyciem tego systemu wymagają wytłumaczalności zgodnie z prawem UE?
→ Jakie jest wymaganie dotyczące logu audytu?

Jeśli nie możesz na to odpowiedzieć zanim zaczniesz, architektura zmieni się pod Tobą w połowie drogi. Widziałem jak to się dzieje. To nie jest dobry sprint review 😅

**Pytanie 3: Czy możemy to ocenić przed wdrożeniem?**

Nie "czy możemy to przetestować," ale czy możemy zmierzyć, czy jest wystarczająco dobry? To znaczy zdefiniować z góry, czym jest "wystarczająco dobry": progi precyzji, cele recall, budżety latencji, limity błędów.

Dla mojego produkcyjnego systemu RAG "wystarczająco dobry" oznaczało: >85% precyzji retrieval na oznaczonym zestawie testowym 200 pytań, <2 sekundy czasu odpowiedzi przy p95, zero odpowiedzi cytujących nieistniejące źródła.

Jeśli nie możesz zdefiniować kryteriów ewaluacji przed budowaniem, nie jesteś gotowy budować.

**Te trzy pytania nie gwarantują udanego projektu AI. Ale pominięcie któregokolwiek prawie gwarantuje bolesny.**

Napisz do mnie 'framework' po pełny szablon.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-10-3-question-framework

#AI #InżynieriaOprogramowania #LiderzyTechniczni #RAG
