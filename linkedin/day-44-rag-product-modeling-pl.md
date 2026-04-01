---
day: 44
title_pl: "Większość RAG-ów powstaje tak: 'dodajmy chatbota do naszych dokumentów'."
pillar: Educator
format: Framework
scheduled_date: 2026-05-28
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#ProductManagement", "#LLM", "#InsurTech", "#AIArchitecture", "#TechLead"]
image: ../images/day-44.jpg
cta: "Masz zdefiniowane intencje użytkownika dla swojego RAG-a? Napisz ile ich jest i jak je wyodrębniłeś."
blog_url: "https://mmx3.pl/blog/day-44-rag-product-modeling"
---

Większość RAG-ów powstaje tak: "dodajmy chatbota do naszych dokumentów."

Potem 3 miesiące walki z jakością bez zdefiniowanych celów. Bez wiedzy co ma działać świetnie, a co może zawieść. Bez metryk sukcesu. Bez konsensusu co system w ogóle ma robić.

To nie jest problem techniczny. To jest brak myślenia produktowego.

---

**Co się dzieje bez specyfikacji produktowej**

Budujesz RAG. Testujesz "na oko." Coś działa, coś nie działa. Idziesz z tym do użytkowników. Pierwsze pytanie: "Dlaczego system nie wie o X?" Drugie pytanie: "Dlaczego odpowiada tak długo?" Trzecie pytanie: "Czy mogę go zapytać o Y?"

Nie masz odpowiedzi, bo nie masz kontraktu. Nie wiesz co miało działać, bo nigdy tego nie zdefiniowałeś.

Zacząłem od pytania: kto będzie używał systemu i co konkretnie będzie pytał?

---

**11 intencji, które zmieniły architekturę**

Pracując nad RAG-iem dla brokerów ubezpieczeniowych, przeprowadziłem sesje z brokerami, przejrzałem logi email do supportu i wyodrębniłem 11 typów zapytań:

1. Lookup faktu (co dokładnie mówi polisa o X?)
2. Porównanie produktów (czym różnią się wariant A i B?)
3. Procedura (jak krok po kroku zarejestrować szkodę?)
4. Sprawdzenie wyłączenia (czy X jest wykluczone z ochrony?)
5. Kalkulacja (ile będzie kosztować składka dla parametrów Y?)
6. Interpretacja klauzuli (co konkretnie oznacza termin Z?)
7. Kontekst historyczny (czy polisa zmieniła warunki względem poprzedniej?)
8. Multidokumentowe porównanie (jak porównuje się ochrona A do B do C?)
9. Przypadek edge (co gdy Y i Z wystąpią jednocześnie?)
10. Odmowa obsługi (pytanie poza zakresem polisy)
11. Eskalacja (pytanie wymagające agenta ludzkiego)

Każda intencja ma inne wymagania: inne progi precision, inną akceptowalną latency, inny format odpowiedzi, inne zachowanie przy braku wiedzy.

---

**Jak to zmieniło architekturę**

Zacząłem z 1 pipeline. Skończyłem z 11 ścieżkami — lub dokładniej: 4 ścieżkami obsługującymi 11 intencji przez routing.

Lookup faktu: prosty retrieval + generacja z rygorystyczną weryfikacją. Cel: precision > 0.95.

Porównanie multidokumentowe: inny chunking, inny prompt, LLM-as-judge na spójność między dokumentami. Cel: kompletność > 0.85.

Procedura krok-po-kroku: structured output, format listy, niższe wymagania na precision bo chodzi o przebieg, nie liczby.

Odmowa i eskalacja: brak retrieval w ogóle, natychmiastowa odpowiedź z canned response.

Jedna architektura dla wszystkich 11 przypadków byłaby kompromisem dla każdego z nich.

---

**RAG Product Canvas**

Zdefiniowałem szablon, z którym zaczynam każdy nowy projekt RAG:

→ Persony użytkowników i ich 10 najczęstszych pytań  
→ Kontrakt jakości: precision/recall/latency per intencja  
→ Tryby błędu: odmowa / eskalacja / odpowiedź z zastrzeżeniem  
→ Pętla feedback: jak zbieramy sygnały od użytkowników  
→ Metryki ewaluacji jako KPI produktowe, nie techniczne

Jeśli chcesz szablon — wpadnij w komentarzu, podeślę.

---

Na blogu piszę o pełnym frameworku z przykładami dla każdej intencji, jak routing architektoniczny wyniknął z definicji produktu i dlaczego ewaluacja RAG to KPI produktowy, nie metryka techniczna.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-44-rag-product-modeling

#RAG #AI #ProductManagement #LLM #InsurTech #AIArchitecture #TechLead
