---
day: 15
title: "Zbudowaliśmy system RAG po polsku, używając modeli Bielik. Oto czego się nauczyliśmy."
pillar: Builder
format: Architecture
language: Polish
scheduled_date: 2026-04-10
posting_time: "08:00 CET"
hashtags: ["#AI", "#RAG", "#BielikAI", "#RODO", "#Technologia"]
image: ./images/day-15.jpg
image_unsplash_query: "Polish technology innovation architecture"
cta: Udostępnij, jeśli zależy ci na polskim AI
---

Zbudowaliśmy system RAG po polsku, używając modeli Bielik. Oto czego się nauczyliśmy.

Pracuję jako Tech Lead w Insly. Budujemy oprogramowanie dla ubezpieczycieli i brokerów w całej Europie. Kiedy zaczęliśmy wdrażać AI, szybko trafiliśmy na problem, który rzadko pojawia się w anglojęzycznych tutorialach: nasze dane są po polsku.

Polisowe dokumenty, klauzule, regulaminy, wszystko w języku polskim. Modele wytrenowane głównie na angielskim tekście radzą sobie z tym znacznie gorzej, niż można by oczekiwać 😅

Dlatego zaczęliśmy testować Bielik, polski model językowy rozwijany przez AI71 i społeczność, zoptymalizowany pod kątem języka polskiego.

Co zyskaliśmy:

→ Lepsze rozumienie polskiej składni i terminologii ubezpieczeniowej bez specjalnego promptowania.
→ Możliwość hostowania modelu lokalnie, co w kontekście RODO i przetwarzania danych klientów ma ogromne znaczenie.
→ Niższe ryzyko wycieku danych wrażliwych do zewnętrznych API.

Co nas zaskoczyło:

→ Jakość embeddingów dla polskiego tekstu jest wciąż słabsza niż dla angielskiego. To obszar, który wymaga dodatkowej pracy przy budowie pipeline'u RAG.
→ Ewaluacja wyników jest trudniejsza. Nie ma tylu gotowych benchmarków dla polskiego jak dla angielskiego.
→ Społeczność rośnie, ale dokumentacja bywa nieaktualna. Trzeba eksperymentować 🤷‍♂️

Dlaczego to ważne poza Insly? Polska ma tysiące firm przetwarzających wrażliwe dane w języku polskim: prawo, medycyna, finanse, ubezpieczenia. Modele anglojęzyczne działają tutaj na pół gwizdka. Bielik to krok w dobrym kierunku.

**Polski AI to nie jest ciekawostka. To infrastruktura, którą będziemy potrzebować, jeśli chcemy realnie wdrażać AI w regulowanych sektorach polskiej gospodarki.**

Udostępnij, jeśli zależy ci na polskim AI.

#AI #RAG #BielikAI #RODO #Technologia
