---
day: 37
title_pl: "Wybrałeś model do RAG-a na podstawie benchmarków? Ja też. A potem zobaczyłem rachunek."
pillar: Educator
format: Deep dive
scheduled_date: 2026-05-05
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#InsurTech", "#AWSBedrock", "#MLOps", "#GenAI"]
image: ../images/day-37.jpg
cta: "Jak Ty podchodzisz do wyboru modelu w projekcie? Daj znać w komentarzu."
blog_url: "https://mmx3.pl/blog/day-37-rag-llm-selection"
---

Wybrałeś model do RAG-a na podstawie benchmarków? Ja też. A potem zobaczyłem rachunek.

Moje pierwsze podejście do wyboru LLM wyglądało tak: wchodzę na leaderboard, sortuję po MMLU, wybieram top 3, testuję na demo pytaniach. GPT-4o wychodzi najlepiej. Decyzja podjęta.

Trzy miesiące później zacząłem zadawać właściwe pytania.

Nie "który model jest najlepszy globalnie?", tylko "który model jest najlepszy na moich danych, w moim języku, przy moim wolumenie zapytań?"

To jest fundamentalna różnica.

**Czego benchmarki nie mierzą**

MMLU, HellaSwag, HumanEval — to są testy na angielskich danych, z angielskim kontekstem. Kiedy retriever wyciągnie klauzulę z polskiej polisy ubezpieczeniowej i zapyta model o interpretację — benchmark tego nie przewiduje.

Przetestowałem cztery podejścia na realnym zestawie polis z Insly:

→ **Claude Sonnet (Bedrock)** — ~$3/1M tokenów wejściowych. Świetna jakość rozumowania, dobry polski, natywna integracja z AWS, łatwy compliance story dla klientów z Europy.

→ **GPT-4o (OpenAI API)** — ~$5/1M tokenów wejściowych. Najlepsza jakość out-of-the-box, ale droższy i bardziej skomplikowany jeśli chodzi o kwestie GDPR dla klientów enterprise.

→ **Mistral Medium (Mistral API)** — szacunkowo ~$0.4/1M tokenów wejściowych. Zaskakująco dobry stosunek jakości do ceny na tekstach technicznych. Polski: wystarczający, nie excellent.

→ **Bielik (self-hosted)** — model open-source trenowany na polskich danych. Zero kosztu za token, ale płacisz za GPU i devops. Na moim zbiorze dokumentów ubezpieczeniowych: +12pp precision vs Mistral Medium na pytaniach o polskie klauzule.

**I tu się zaczęło prawdziwe liczenie**

Przy 10 000 zapytań miesięcznie różnica między GPT-4o a Mistral to kilkaset dolarów. Przy 200 000 zapytań — to są tysiące miesięcznie. A self-hosted Bielik przy małym wolumenie jest DROŻSZY niż zarządzane API, bo płacisz za GPU niezależnie od ruchu.

Break-even między self-hosted a managed zwykle wypada gdzieś w okolicach 50-100k zapytań miesięcznie. Zależy od architektury, ale jest to liczba, której większość startupów nie osiąga w pierwszym roku.

**Jak faktycznie testować modele na swoich danych**

Nie demo pytania. Złoty zestaw testowy: 50-100 realnych pytań z mojego systemu, z oczekiwanymi odpowiedziami. Metryki: faithfulness (czy model halucynuje poza kontekstem?) i answer relevance (czy odpowiada na właściwe pytanie?).

To zajmuje 2-3 dni raz, a oszczędza tygodnie błędnych decyzji.

Pełną tabelę porównawczą — ceny, okno kontekstu, latencja p95, wsparcie polskiego, compliance — opisuję na blogu. Plus flowchart "który model wybrać" w zależności od wolumenu, języka i wymogów regulacyjnych.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-37-rag-llm-selection

#RAG #AI #LLM #InsurTech #AWSBedrock #MLOps #GenAI
