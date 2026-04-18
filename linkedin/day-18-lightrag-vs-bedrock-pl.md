---
day: 18
title_pl: "LightRAG vs. AWS Bedrock Knowledge Bases: używałem obu w produkcji. Oto kiedy wybrać każdy z nich."
pillar: Builder
format: Technical
scheduled_date: 2026-04-15
posting_time: "07:30 CET"
hashtags: ["#RAG", "#AWS", "#AI", "#ArchitekturaSoftware", "#InsurTech"]
image: ../images/day-18.jpg
cta: "Zapisz to na swoją następną decyzję architektoniczną"
blog_url: "https://mmx3.pl/blog/day-18-lightrag-vs-bedrock"
---

LightRAG vs. AWS Bedrock Knowledge Bases: używałem obu w produkcji. Oto kiedy wybrać każdy z nich.

Zbudowałem systemy RAG używając obu. Nie benchmarki — rzeczywiste produkty ubezpieczeniowe, z prawdziwymi danymi polis, ograniczeniami GDPR i użytkownikami, którzy nie tolerują błędnych odpowiedzi.

Oto uczciwe porównanie.

AWS Bedrock Knowledge Bases:

→ Zarządzana ingestion: S3 → chunkowanie → embedding → OpenSearch Serverless. Konfiguruję, AWS uruchamia.
→ Natywne IAM. Logi audytu. Dostępny region EU. Historia compliance jest prosta.
→ Koszt przewidywalny, ale szybko się sumuje przy skali. Płacę za storage, wywołania retrieval i bazowy vector DB.
→ Elastyczność ograniczona. Pracuję w ramach abstrakcji Bedrocka. Niestandardowe strategie chunkowania i logika retrieval wymagają obejść.

LightRAG:

→ Retrieval oparty na grafie. Dokumenty stają się grafem wiedzy, nie tylko indeksem wektorowym. Zmienia to, na jakie typy pytań mogę odpowiadać.
→ Pełna kontrola. Mam pipeline od końca do końca: chunkowanie, model embeddingowy, logika retrieval, reranking.
→ Działa lokalnie lub na własnej infrastrukturze. Dla wrażliwych danych to często lepsze rozwiązanie domyślne.
→ Więcej pracy inżynierskiej. Nie ma przycisku "synchronizuj Knowledge Base". Sam buduję i utrzymuję pipeline.

Kiedy wybieram Bedrock: nowe projekty wymagające szybkiego uruchomienia, zespoły bez dedykowanej pojemności MLOps lub workloady, gdzie historia compliance dla AWS jest już ustalona.

Kiedy wybieram LightRAG: złożone dokumenty, gdzie relacje między encjami mają znaczenie, dane w języku innym niż angielski, gdzie potrzebuję kontroli nad embeddingami, lub gdy potrzebuję wzorców retrieval, których abstrakcja Bedrocka nie wspiera.

Na 40 pytaniach specyficznie o relacje między dokumentami: Bedrock: 52% dokładności retrieval, LightRAG: 81%.

**Właściwa odpowiedź zależy od tego, co optymalizujesz: szybkość do produkcji czy elastyczność w produkcji. Wybierz świadomie.** Za pierwszym razem wybrałem źle i straciłem tygodnie, zanim to przyznałem.

Zapisz to na swoją następną decyzję architektoniczną i oznacz kogoś, kto aktualnie stoi przed tym wyborem.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-18-lightrag-vs-bedrock

#RAG #AWS #AI #ArchitekturaSoftware #InsurTech
