---
day: 5
title_pl: "Zbudowaliśmy 4 prototypy RAG w 12 miesięcy. Oto co naprawdę zadziałało (i co nie)."
pillar: Builder
format: Technical
scheduled_date: 2026-03-27
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AWS", "#AI", "#InsurTech", "#InżynieriaOprogramowania"]
image: ../images/day-05.jpg
cta: "Udostępnij, jeśli Twój zespół ocenia podejścia RAG."
blog_url: "https://mmx3.pl/blog/day-05-rag-prototypes"
---

Zbudowałem z zespołem 4 prototypy RAG w 12 miesięcy. Oto co naprawdę zadziałało (i co nie).

Wszystkie cztery budowałem, żeby odpowiedzieć na to samo pytanie: czy brokerzy mogą odpytywać bazę wiedzy ubezpieczeniowej w naturalnym języku i otrzymywać dokładne, audytowalne odpowiedzi?

**Prototyp 1: Naiwny RAG na AWS Bedrock**
Proste embedding + wyszukiwanie wektorowe + Claude. Dwa tygodnie budowania, dwa miesiące żeby zrozumieć, że to nie wystarczy 😅 Problem: recall retrieval był zbyt niski na domenowej terminologii ubezpieczeniowej. Brokerzy używają żargonu. Model nie dopasowywał go konsekwentnie. Dostawałem pewne siebie błędne odpowiedzi — a w ubezpieczeniach to gorsze niż brak odpowiedzi.

Lekcja: embeddingi off-the-shelf trenowane na ogólnym tekście słabo radzą sobie w wyspecjalizowanych domenach.

**Prototyp 2: Fine-tuned embeddingi + AWS Bedrock**
Fine-tuneowałem model embeddingów na dokumentach ubezpieczeniowych. Jakość retrieval znacząco wzrosła. Ale trafiłem w inną ścianę: graf wiedzy między dokumentami polisowymi, endorsementami i warunkami był niejawny. Standardowy chunk retrieval nie mógł go podążać. Klauzula w jednym dokumencie zależy od definicji z innego. Płaskie wyszukiwanie wektorowe tego nie wie.

Lekcja: jeśli Twoja domena ma głęboki kontekst relacyjny, samo wyszukiwanie wektorowe nie wystarczy.

**Prototyp 3: LightRAG**
LightRAG buduje graf wiedzy na bazie korpusu dokumentów. Jawnie modeluje relacje między encjami. Obiecujący w teorii, ale nigdy nie trafił do produkcji.

Problem: dokumenty branżowe i pliki GTC są strukturalnie i językowo podobne. Wektory stały się równie dobre i równie złe w ich rozróżnianiu. Co ważniejsze, LightRAG nie miał sposobu filtrowania kontekstu po nazwie firmy, linii produktów lub typie ryzyka. W ubezpieczeniach to nie opcja. Broker pytający o pokrycie OC jednego ubezpieczyciela nie może dostać kontekstu innego. Nie mogłem tego uczynić audytowalnym.

Lekcja: grafy wiedzy nie rozwiązują filtrowania. Jeśli Twoja domena wymaga ścisłego zakresu kontekstu, graph retrieval może pogorszyć problem.

**Prototyp 4: 100% własny Python, routing oparty na intencji**
Wyrzuciłem podejścia czarnej skrzynki i zbudowałem od zera w Pythonie. Kluczowy wgląd: brokerzy nie zadają losowych pytań. Zidentyfikowałem 11 odrębnych intencji użytkownika i zbudowałem jawne wykrywanie dla każdej. Właściwa strategia retrieval stosowana per intencja. Wszystko filtrowalne po firmie, linii produktów i typie ryzyka. Wszystko audytowalne.

Dowód: wyodrębniliśmy duży dataset Egzaminu KNF dla Brokerów — oficjalnego egzaminu licencyjnego polskiego regulatora finansowego — i system zdał go z wyróżnieniem 🎓

**Właściwa architektura RAG zależy całkowicie od struktury Twoich danych i wymagań compliance, nie od tego, co było modne gdy zaczynałeś projekt.**

Udostępnij, jeśli Twój zespół ocenia podejścia RAG.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-05-rag-prototypes

#RAG #AWS #AI #InsurTech #InżynieriaOprogramowania
