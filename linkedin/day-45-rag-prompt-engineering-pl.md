---
day: 45
title_pl: "Ultimate RAG prompt. 47 linii. Świetny na demo. W produkcji halucynuje na 40% pytań."
pillar: Educator
format: Technical
scheduled_date: 2026-06-02
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#PromptEngineering", "#LLM", "#InsurTech", "#MachineLearning", "#AIProduction"]
image: ../images/day-45.jpg
cta: "Jaką strategię promptów używasz dla niskiego confidence retrieval? Napisz w komentarzu."
blog_url: "https://mmx3.pl/blog/day-45-rag-prompt-engineering"
---

Widziałem "ultimate RAG prompt" na Twitterze. 47 linii. Działa świetnie na demo z 5 dokumentami.

W produkcji z 3000 dokumentami ubezpieczeniowymi? Halucynuje na 40% pytań.

Nie dlatego że prompt jest zły. Dlatego że jeden universal prompt nie istnieje.

---

**Co tak naprawdę wpływa na prompt w RAG-u**

Gdy piszę prompt dla mojego systemu ubezpieczeniowego, mam co najmniej cztery zmienne, które muszę uwzględnić:

**1. Typ intencji**: Pytanie faktyczne ("jaki jest limit OC?") wymaga innego zachowania niż pytanie proceduralne ("jak zgłosić szkodę?") albo porównawcze ("różnice między wariantem A a B?"). Pytanie faktyczne: krótka, precyzyjna odpowiedź z dosłownym cytatem. Porównanie: ustrukturyzowana tabela z cytowaniami per-dokument. Procedura: lista kroków, żadnych skrótów.

**2. Jakość kontekstu**: Jeśli top chunk ma score 0.83, model może odpowiadać swobodnie z kontekstu. Jeśli top chunk ma score 0.64, prompt musi zmienić zachowanie: "odpowiedz tylko jeśli kontekst bezpośrednio zawiera informację — jeśli nie, powiedz że nie masz tej informacji."

**3. Język i domena**: Polskie dokumenty prawno-ubezpieczeniowe wymagają innego traktowania niż angielskie specyfikacje techniczne. Instrukcja "cytuj dosłownie" w dokumentach polskich daje inne rezultaty niż w angielskich, bo styl jest bardziej złożony składniowo.

**4. Format outputu**: Krótka odpowiedź do interfejsu brokera vs pełne wyjaśnienie do maila klienta. To samo pytanie, dwa różne prompty.

---

**4 strategie, których używam**

**High-confidence retrieval** (score ≥ 0.78): Model odpowiada swobodnie, opierając się na kontekście. "Na podstawie poniższych fragmentów odpowiedz na pytanie. Cytuj dosłownie kluczowe warunki."

**Low-confidence retrieval** (score 0.62-0.78): Tryb ostrożny. "Odpowiedz TYLKO jeśli kontekst bezpośrednio zawiera odpowiedź. Jeśli informacja jest niejasna lub pośrednia, powiedz: 'Dokumenty nie zawierają jednoznacznej odpowiedzi na to pytanie.'"

**Multisource synthesis**: "Poniżej masz fragmenty z [N] różnych dokumentów. Syntetyzuj informacje, wyraźnie oznaczając z którego źródła pochodzi każde twierdzenie. Jeśli dokumenty są sprzeczne — zaznacz tę sprzeczność."

**Refusal prompt**: "Kontekst nie zawiera informacji wystarczających do odpowiedzi na to pytanie. Odpowiedz: 'Nie dysponuję wystarczającymi informacjami...'" — i zero hallucination, bo model dosłownie dostaje instrukcję co powiedzieć.

---

**Ten sam prompt, dwa różne tryby błędu**

Jedno zapytanie: "Czy szkody od wandalizmu są objęte ochroną?"

Z high-confidence promptem przy niskim retrieval score: model odpowie — pewnie — na podstawie słabego kontekstu. Halucynacja.

Z low-confidence promptem: model powie "dokumenty nie zawierają jednoznacznej odpowiedzi." Bezpieczna odmowa.

Różnica: jeden parametr w logice routingu promptów.

---

**Anti-pattern: zbyt długi system prompt**

47-liniowy prompt z Twittera ma jeszcze jeden problem: sprzeczne instrukcje. "Bądź zwięzły" + "podaj pełne uzasadnienie" + "cytuj wszystkie źródła" + "unikaj powtórzeń" to przepis na niespójne odpowiedzi.

Model nie wie co priorytetyzować. Wybiera losowo w zależności od treści kontekstu.

Moje prompty mają jedną główną instrukcję i maksymalnie trzy uzupełniające. Reszta idzie do logiki routingu.

---

Na blogu opisuję pełny system dynamicznego doboru promptów oparty na retrieval quality score, ze schematem kodu routingu i przykładami dla każdej z 4 strategii na danych ubezpieczeniowych.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-45-rag-prompt-engineering

#RAG #AI #PromptEngineering #LLM #InsurTech #MachineLearning #AIProduction
