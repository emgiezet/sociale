---
day: 15
title_pl: "Zbudowaliśmy system RAG po polsku, używając modeli Bielik. Oto czego się nauczyliśmy."
pillar: Builder
format: Architecture
scheduled_date: 2026-04-10
posting_time: "08:00 CET"
hashtags: ["#AI", "#RAG", "#BielikAI", "#RODO", "#Technologia"]
image: ../images/day-15.jpg
cta: "Udostępnij, jeśli zależy ci na polskim AI"
blog_url: "https://mmx3.pl/blog/day-15-bielik-rag"
---

Zbudowałem system RAG po polsku, używając modeli Bielik. Oto czego się nauczyłem.

Jestem Tech Leadem w Insly — budujemy oprogramowanie dla ubezpieczycieli i brokerów w całej Europie. Kiedy zacząłem wdrażać AI, szybko trafiłem na problem, który rzadko pojawia się w anglojęzycznych tutorialach: moje dane są po polsku.

Polisowe dokumenty, klauzule, regulaminy — wszystko w języku polskim. Modele wytrenowane głównie na angielskim tekście radzą sobie z tym znacznie gorzej, niż można by oczekiwać.

Dlatego zacząłem testować Bielik, polski model językowy rozwijany przez polską społeczność AI, zoptymalizowany pod kątem języka polskiego.

Co zyskałem:

→ Lepsze rozumienie polskiej składni i terminologii ubezpieczeniowej bez specjalnego promptowania.
→ Możliwość hostowania modelu lokalnie, co w kontekście RODO i przetwarzania danych klientów ma ogromne znaczenie.
→ Niższe ryzyko wycieku danych wrażliwych do zewnętrznych API.
→ Precyzja retrieval wzrosła o 12 punktów procentowych w porównaniu z podejściem tłumaczenie-angielski-retrieval.

Co mnie zaskoczyło:

→ Jakość embeddingów dla polskiego tekstu jest wciąż słabsza niż dla angielskiego w niektórych przypadkach. To obszar wymagający dodatkowej pracy przy budowie pipeline'u RAG.
→ Ewaluacja wyników jest trudniejsza. Nie ma tylu gotowych benchmarków dla polskiego jak dla angielskiego.
→ Społeczność rośnie, ale dokumentacja bywa nieaktualna. Trzeba eksperymentować.

Przyjąłem podejście hybrydowe: Bielik do embeddingów i retrieval, Claude do złożonej generacji.

Dlaczego to ważne poza Insly? Polska ma tysiące firm przetwarzających wrażliwe dane w języku polskim: prawo, medycyna, finanse, ubezpieczenia. Modele anglojęzyczne działają tutaj na pół gwizdka.

**Polski AI to nie jest ciekawostka. To infrastruktura, którą będziemy potrzebować w regulowanych sektorach polskiej gospodarki.**

Udostępnij, jeśli zależy ci na polskim AI. Budujesz systemy AI z polskojęzyczną treścią? Napisz — chętnie podzielę się szczegółami architektury.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-15-bielik-rag

#AI #RAG #BielikAI #RODO #Technologia
