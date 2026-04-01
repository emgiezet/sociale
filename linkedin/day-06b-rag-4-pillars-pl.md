---
day: 6
title_pl: "RAG działa idealnie dla 10 dokumentów. Potem dodajesz 5 więcej i się psuje. Oto dlaczego."
pillar: Builder
format: Technical
scheduled_date: 2026-03-30
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#InżynieriaOprogramowania", "#InsurTech"]
image: ../images/day-06.jpg
cta: "Udostępnij, jeśli Twój zespół skaluje system RAG."
blog_url: "https://mmx3.pl/blog/day-06b-rag-4-pillars"
---

RAG działa idealnie dla 10 dokumentów. Potem dodajesz 5 więcej i się psuje.

To nie błąd. To cztery nierozwiązane problemy uderzające naraz.

**1. Chunkowanie**
Większość tutoriali dzieli tekst co N znaków. Dobrze dla dem. Sypie się na ustrukturyzowanych dokumentach, gdzie jedna klauzula odwołuje się do definicji z trzech innych sekcji 🫠

Fix to nie mniejsze chunki. To mądrzejsze. Używam RAPTOR dla hierarchicznego podsumowywania drzew dokumentów, taguję metadane, żeby każdy chunk wiedział skąd pochodzi, i stosuję HyDE (Hypothetical Document Embeddings), żeby bridgować gap między tym, jak pytania są zadawane a jak odpowiedzi są pisane. Broker pytający „czy to pokrywa szkodę powodziową?" brzmi zupełnie inaczej niż klauzula polisowa, która na to odpowiada.

**2. Zarządzanie kontekstem i wyszukiwanie**
Samo wyszukiwanie wektorowe sypie się gdy korpus rośnie. Gdy dokumenty są strukturalnie podobne — ten sam format, ta sama terminologia, różne szczegóły — wektory przestają niezawodnie rozróżniać.

Odpowiedzią jest hybrid retrieval: wyszukiwanie wektorowe dla podobieństwa semantycznego, wyszukiwanie słów kluczowych dla precyzji na konkretnych terminach i warstwa rerankingu, która ocenia kandydatów przed dotarciem do modelu.

**3. Konfiguracja retrieval**
Tu większość zespołów cicho krwawi. Top-k zbyt niskie i brakuje istotnego kontekstu. Zbyt wysokie i rozcieńczasz sygnał szumem. Progi podobieństwa ustawione zbyt permisywnie i model halucynuje pewnie. Każdy parametr — nakładanie chunków, model embeddingów, top-k, próg rerankingu, szablon promptu — musi być niezależnie sterowalny i ciągle mierzony.

**4. Benchmarking i ewaluacja**
Nie możesz poprawić tego, czego nie mierzysz. Większość zespołów nie wie, czy ich RAG jest lepszy czy gorszy po każdej zmianie.

Zbuduj dataset ewaluacyjny zanim dotkniesz produkcji. Zdefiniuj odpowiedzi ground-truth dla reprezentatywnego zestawu zapytań. Mierz recall retrieval, wierność odpowiedzi i poprawność odpowiedzi. Zautomatyzuj to w CI. Walidowałem to na formalnym datasecie Egzaminu KNF dla Brokerów — oficjalnym egzaminie licencyjnym polskiego regulatora finansowego. Jeśli RAG zda egzamin, brokerzy mogą mu ufać.

**Tutoriale YouTube o RAG uczą Cię budować pierwsze 10%. Pozostałe 90% to strategia chunkowania, hybrid retrieval, dyscyplina konfiguracyjna i nieustanna ewaluacja 🎉**

Udostępnij, jeśli Twój zespół skaluje system RAG.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-06b-rag-4-pillars

#RAG #AI #InżynieriaOprogramowania #InsurTech
