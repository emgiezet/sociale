---
day: 39
title_pl: "Wszyscy mówią o RAG. Nikt nie mówi ile to kosztuje. Oto 3 architektury i ich realne koszty."
pillar: Educator
format: Cost analysis
scheduled_date: 2026-05-12
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#AWSBedrock", "#CloudCosts", "#MLOps", "#InsurTech"]
image: ../images/day-39.jpg
cta: "Jakie macie doświadczenia z kosztami RAG? Managed vs self-hosted — co wybraliście?"
blog_url: "https://mmx3.pl/blog/day-39-rag-costs"
---

Wszyscy mówią o RAG. Nikt nie mówi ile to kosztuje. Oto 3 architektury i ich realne koszty.

Zacznę od twierdzenia, które zaskakuje większość ludzi: self-hosted RAG może być droższy niż managed. I często jest. Szczególnie poniżej 50 000 zapytań miesięcznie.

Trzy architektury, które przetestowałem lub wdrożyłem, z realnymi liczbami.

Architektura 1: AWS Bedrock (w pełni zarządzana)

Składowe kosztów przy 10 000 zapytań miesięcznie:
→ Osadzenia (embeddings, Titan Embed): ~$2/miesiąc
→ OpenSearch Serverless (wyszukiwanie wektorowe): ~$60–90/miesiąc (minimum nawet przy małym ruchu)
→ Claude Sonnet — generacja: ~$45/miesiąc (zakładając avg. 500 tokenów wejścia + kontekst, 300 tokenów wyjścia)
→ AWS Bedrock Knowledge Base: request fee ~$2/miesiąc

Łącznie: ~$110–140/miesiąc przy 10k zapytań

Przy 50k zapytaniach: ~$450–600/miesiąc. Przy 200k: ~$1800–2400/miesiąc.

Ukryty koszt: OpenSearch Serverless ma minimalną opłatę OCU niezależnie od ruchu. Przy małym projekcie płacisz "podatek od bezczynności".

Architektura 2: Self-hosted GPU (Mistral/Bielik)

Przy dzierżawionym A100:
→ GPU (szacunkowo): $10–15/godz. reserved = $7 200–10 800/miesiąc
→ Inżynier DevOps (0.3 FTE do zarządzania): kolejne kilka tysięcy dolarów

Łącznie: $8 000–13 000/miesiąc niezależnie od wolumenu

Break-even vs Bedrock: gdzieś przy 200 000–500 000 zapytań miesięcznie w zależności od modelu i architektury. Większość startupów tego nie osiąga w roku 1.

Kiedy self-hosted JEST tańszy: gdy masz >500k zapytań miesięcznie, gdy latencja per query musi być poniżej 500ms i API jest zbyt wolne, lub gdy compliance wymaga braku wyjścia danych.

Architektura 3: Hybryda

Wyszukiwanie self-hosted (np. Qdrant na EC2) + generacja przez API.

→ EC2 c5.2xlarge dla Qdrant: ~$140/miesiąc
→ Osadzenia (API): ~$5–20/miesiąc przy 10k zapytań
→ Generacja (Claude Sonnet via Bedrock): ~$45–60/miesiąc

Łącznie: ~$190–220/miesiąc przy 10k zapytań

Drożej niż czyste Bedrock, ale daje kontrolę nad retrieverem i indeksem bez kosztu GPU dla modelu.

Co nie jest w żadnym cenniku

Liczby powyżej to koszty tokenów i infry. Nie ma tu:
→ Czasu inżyniera na budowę i utrzymanie pipeline'u
→ Monitorowania i ewaluacji (uruchamiam golden set testowy regularnie — to kosztuje)
→ Iteracji: każda zmiana strategii chunkingu to przeindeksowanie całego korpusu
→ Rerankingu: dodatkowy model = dodatkowe koszty i latencja

Pełna tabela break-even i szczegółowy breakdown per komponent — na blogu. Łącznie z tym kiedy warto (i kiedy nie warto) inwestować w self-hosted.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-39-rag-costs

#RAG #AI #LLM #AWSBedrock #CloudCosts #MLOps #InsurTech
