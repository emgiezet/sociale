---
day: 40
title_pl: "Broker pyta: 'czy to pokrywa szkody powodziowe?' Klauzula mówi: 'zakres ochrony obejmuje zdarzenia losowe zgodnie z par. 4 ust. 2'. Vector search tego nie połączy."
pillar: Educator
format: Technical
scheduled_date: 2026-05-14
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#HyDE", "#InsurTech", "#NLP", "#GenAI"]
image: ../images/day-40.jpg
cta: "Czy stosowaliście HyDE albo inne techniki poprawy wyszukiwania? Chętnie porównam wyniki."
blog_url: "https://mmx3.pl/blog/day-40-rag-hyde"
---

Broker pyta: "czy to pokrywa szkody powodziowe?" Klauzula mówi: "zakres ochrony obejmuje zdarzenia losowe zgodnie z par. 4 ust. 2". Vector search tego nie połączy.

To jest problem semantycznej luki. I jeden z głównych powodów, dla których RAG z tutoriali pada po 15 dokumentach.

W dniu 7 pisałem o tym, że naiwny RAG ma fundamentalne ograniczenia. Jednym z nich jest właśnie ta przepaść: pytania użytkowników są sformułowane w języku potocznym. Dokumenty ubezpieczeniowe są napisane w języku prawnym. Te dwa języki żyją w różnych przestrzeniach semantycznych.

"Powódź" vs "zdarzenie losowe obejmujące zalanie nieruchomości wskutek wezbrania wód". Podobieństwo kosinusowe w przestrzeni wektorowej: niskie. Fakt, że to to samo zdarzenie: tak.

**HyDE rozwiązuje ten problem elegancko**

HyDE — Hypothetical Document Embeddings — to technika zaproponowana przez Gao et al. w 2022 roku. Idea jest prosta:

Zamiast osadzać pytanie użytkownika i szukać podobnych fragmentów, prosimy LLM żeby najpierw napisał *hipotetyczną odpowiedź* na to pytanie. Taką, jak gdyby była w dokumencie ubezpieczeniowym. Potem osadzamy TĘ odpowiedź i szukamy podobnych fragmentów.

Dlaczego to działa? Bo hipotetyczna odpowiedź jest napisana w tym samym stylu i języku co rzeczywiste dokumenty. "Zdarzenie powodziowe jest zdarzeniem losowym w rozumieniu niniejszych OWU i podlega ochronie zgodnie z §4." — to jest tekst, który semantycznie leży blisko klauzuli.

**Przed i po HyDE na moich danych**

Zapytanie: "Czy polisa pokrywa szkody spowodowane zalaniem od strony rzeki?"

→ **Bez HyDE:** Retriever zwraca fragmenty ze słowem "zalanie" — głównie procedury zgłaszania szkód, nie klauzule odpowiedzialności. Recall na moim zbiorze testowym: 0.61.

→ **Z HyDE:** LLM generuje hipotezę: "Ochrona obejmuje szkody powstałe wskutek powodzi i zalania, w tym zalania od strony cieków wodnych, z zastrzeżeniem wyłączeń określonych w §7." Retriever trafia w klauzulę. Recall: 0.79.

18 punktów procentowych poprawy. Na realnym zbiorze pytań ubezpieczeniowych.

**Kiedy HyDE pomaga, a kiedy szkodzi**

Pomaga: pytania specjalistyczne w języku branżowym, gdzie pytanie użytkownika i dokument są napisane bardzo inaczej. Ubezpieczenia, prawo, medycyna.

Szkodzi (lub nie pomaga): proste pytania faktyczne ("jaki jest numer polisy?"), pytania gdzie latencja jest krytyczna (dodatkowe wywołanie LLM = 500–800ms), niskie wolumeny gdzie koszt dodatkowego wywołania nie jest uzasadniony.

Pełna implementacja w Pythonie, metryki przed/po i analiza kiedy HyDE jest warta kosztu — na blogu. Plus odniesienie do tego jak HyDE łączy się z resztą pipeline'u z poprzednich tygodni.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-40-rag-hyde

#RAG #AI #LLM #HyDE #InsurTech #NLP #GenAI
