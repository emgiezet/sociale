---
day: 42
title_pl: "RAG miał wyeliminować halucynacje. W praktyce je maskuje."
pillar: Educator
format: Technical
scheduled_date: 2026-05-21
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#InsurTech", "#MachineLearning", "#Hallucination", "#AIProduction"]
image: ../images/day-42.jpg
cta: "Napisz w komentarzu z jakim problemem halucynacji walczysz — albo jakie checkpointy już masz u siebie."
blog_url: "https://mmx3.pl/blog/day-42-rag-hallucinations"
---

RAG miał wyeliminować halucynacje. W praktyce je maskuje.

Model odpowiada pewnie, cytuje źródło, a źródło mówi coś innego. To najgroźniejszy typ halucynacji — nie brak odpowiedzi, ale odpowiedź błędna, podana z autorytetem i bibliografią.

Przez rok pracy z RAG na dokumentach ubezpieczeniowych nauczyłem się jednego: im lepiej działa retrieval, tym bardziej ufam odpowiedziom. I tym łatwiej przeoczyć błąd, który kosztuje.

---

**Jak RAG zmienia charakter halucynacji**

W klasycznym LLM halucynacja wygląda tak: model wymyśla fakty, które nie istnieją. Łatwo to wychwycić — brak źródeł, niespójność z rzeczywistością.

W RAG halucynacja wygląda inaczej: model ma kontekst, ale go parafrazuje zbyt luźno. Albo łączy dwa fragmenty z różnych dokumentów. Albo ekstrapoluje z podobnego przypadku. Wynik — odpowiedź, która brzmi jak cytat ze źródła, ale nim nie jest.

---

**5 checkpointów, które wdrożyłem w naszym pipeline**

1. Retrieval precision gate. Jeśli top chunk ma score poniżej progu (u nas 0.72 na cosine similarity), pipeline nie odpowiada. Nie wysyłamy do LLM kontekstu, który sam retriever ocenił jako słaby.

2. LLM-as-judge faithfulness. Osobny, tańszy model (Claude Haiku) weryfikuje: "Czy ta odpowiedź wynika wyłącznie z dostarczonego kontekstu?" Tak/nie + uzasadnienie. Zajmuje ~150ms i kosztuje ułamek centa.

3. Source-answer alignment. Sprawdzamy, czy kluczowe liczby i terminy w odpowiedzi faktycznie pojawiają się w zacytowanym fragmencie. Regexem. Prosto, ale skutecznie dla danych ubezpieczeniowych.

4. Confidence scoring. Model raportuje własną pewność. Nie jako zastępstwo dla poprzednich checkpointów, ale jako sygnał do logowania. Odpowiedzi z niskim confidence trafiają do kolejki review.

5. Canary test set. Zestaw ~80 pytań ze znanych odpowiedzi, uruchamiany przy każdym deployu i co noc w produkcji. Jeśli precision spada poniżej 0.90, dostaję alert.

---

**Przykład z produkcji**

Mieliśmy zapytanie o zakres ochrony przy szkodzie komunikacyjnej. Model zwrócił odpowiedź z poprawnym numerem polisy, poprawnym źródłem i błędną kwotą franszyzy redukcyjnej. Przeszedł przez checkpointy 1, 2, 3 i 4. Dopiero canary set wychwycił to jako regresję po aktualizacji modelu.

Checkpoint 5 uratował produkcję.

---

**Gdzie halucynacje są blockerem absolutnym**

W ubezpieczeniach: kwoty, zakresy ochrony, wyłączenia. Każda halucynacja w tych polach to potencjalna szkoda prawna. Nasz system nie odpowiada, jeśli nie przejdzie wszystkich 5 checkpointów — woli powiedzieć "nie wiem" niż podać pewnie błędną informację.

To nie jest pesymizm. To jest inżynieria na dokumentach, gdzie stawka jest wysoka.

---

Na blogu opisuję pełny framework z progami, kosztami każdego checkpointu i tym jak monitorować dryfowanie jakości w czasie. Plus implementacja LLM-as-judge w Pythonie.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-42-rag-hallucinations

#RAG #AI #LLM #InsurTech #MachineLearning #Hallucination #AIProduction
