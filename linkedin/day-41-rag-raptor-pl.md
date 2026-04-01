---
day: 41
title_pl: "Chunking po 300 tokenów to jak czytanie książki po jednym zdaniu. Tracisz kontekst po 3 chunkach."
pillar: Educator
format: Technical
scheduled_date: 2026-05-19
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#RAPTOR", "#InsurTech", "#NLP", "#GenAI"]
image: ../images/day-41.jpg
cta: "Stosowaliście RAPTOR albo inne hierarchiczne podejście do wyszukiwania? Jestem ciekaw Waszych doświadczeń."
blog_url: "https://mmx3.pl/blog/day-41-rag-raptor"
---

Chunking po 300 tokenów to jak czytanie książki po jednym zdaniu. Tracisz kontekst po 3 chunkach.

Flat chunking ma fundamentalne ograniczenie: każdy chunk jest równorzędny. Retriever nie wie co jest bardziej ogólne, a co bardziej szczegółowe. Nie wie, że trzy chunki z trzech różnych sekcji razem odpowiadają na pytanie, na które każdy z osobna odpowiada tylko częściowo.

RAPTOR rozwiązuje ten problem. I to elegancko.

**Co robi RAPTOR**

RAPTOR — Recursive Abstractive Processing for Tree-Organized Retrieval — buduje hierarchię zamiast płaskiej listy chunków.

Krok po kroku:

→ Podziel dokumenty na chunki (leaf nodes)
→ Osadź chunki, wykonaj klastrowanie (np. Gaussian Mixture Model)
→ Dla każdego klastra: wygeneruj podsumowanie LLM-em
→ Osadź podsumowania — teraz są węzłami wyżej w hierarchii
→ Powtarzaj rekurencyjnie aż zostanie jeden korzeń (podsumowanie całego dokumentu)

Wyszukiwanie może się odbywać na każdym poziomie drzewa. Pytanie wymagające szerokiego kontekstu ("opisz ogólne podejście do regulacji ryzyka w tej polisie") trafi na poziom podsumowań. Pytanie precyzyjne ("jaki jest limit ochrony dla sprzętu elektronicznego?") trafi na poziom leaf chunków.

**Realny przykład z Insly**

Pytanie: "Jak klauzula siły wyższej wpływa na procedury roszczeniowe i wyłączenia odpowiedzialności?"

To pytanie wymaga informacji z co najmniej trzech sekcji: definicje (co to siła wyższa), zakres ochrony (co jest wyłączone), procedury (co trzeba zrobić przy roszczeniu).

→ **Flat chunking:** Retriever zwraca 1–2 z 3 potrzebnych fragmentów. Model odpowiada niekompletnie lub halucynuje połączenia między sekcjami.

→ **RAPTOR:** Wyszukiwanie trafia na węzeł podsumowania obejmujący wszystkie trzy sekcje. Model widzi syntezę, odpowiada kompletnie.

**Kiedy RAPTOR jest wart zachodu, a kiedy nie**

Wart: długie dokumenty z wzajemnie powiązanymi sekcjami, pytania wymagające syntezy wielu fragmentów, dokumenty prawne i regulacyjne gdzie kontekst między sekcjami jest krytyczny.

Nie wart: proste FAQ, krótkie dokumenty, systemy gdzie latencja indeksowania jest krytyczna (RAPTOR indeksuje znacznie dłużej), budżety bez miejsca na dodatkowe LLM calls przy budowie indeksu.

Pełną architekturę z pseudokodem Pythona, diagramem hierarchii i porównaniem metryk przed/po opisuję na blogu.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-41-rag-raptor

#RAG #AI #LLM #RAPTOR #InsurTech #NLP #GenAI
