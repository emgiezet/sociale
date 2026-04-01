---
day: 46
title: "Ile naprawdę kosztuje RAG? Model TCO dla trzech architektur"
pillar: Educator
language: pl
image: ../../images/day-46.jpg
image_unsplash_query: "financial model spreadsheet cost analysis infrastructure budget"
---

# Ile naprawdę kosztuje RAG? Model TCO dla trzech architektur

"Ile kosztuje RAG?" to złe pytanie. To jak pytanie "ile kosztuje samochód" — odpowiedź to od 35 000 zł do 400 000 zł zależnie od tego co kupujesz, po co kupujesz i ile kosztuje eksploatacja przez trzy lata.

Byłem pytany o to wystarczająco dużo razy i widziałem wystarczająco dużo projektów niedoszacowujących swoich kosztów, żeby zbudować właściwy model TCO. Ten artykuł dzieli się tym modelem z realistycznymi (jawnie oznaczonymi jako szacunki) liczbami dla trzech popularnych architektur w ramach stałego scenariusza.

---

## Sześć zmiennych decydujących o wycenie RAG

Zanim możemy mówić o liczbach, musimy omówić zmienne wejściowe modelu. Te sześć zmiennych wyjaśnia większość wariancji cenowej, którą widziałem w realnych projektach.

### Zmienna 1: Wolumen dokumentów i zapytań

Liczba dokumentów determinuje koszt indeksowania (jednorazowy per partię + cykliczny przy aktualizacjach) i koszt hostowania indeksu (przechowywanie wektorów). Wolumen zapytań determinuje koszt inferencji (osadzenia per zapytanie + tokeny LLM per generacja).

Zależność nie jest liniowa. Przejście z 1 000 do 10 000 dokumentów to głównie koszt przechowywania. Przejście z 1 000 do 10 000 zapytań/dzień to przede wszystkim koszt inferencji — który się kumuluje, bo zarówno model osadzeń jak i LLM działają na każdym zapytaniu.

### Zmienna 2: Język i domena

Dokumenty angielskie: masz dostęp do pełnego zakresu wysokiej jakości, opłacalnych modeli. Amazon Titan Embed, Cohere Embed, Claude Haiku/Sonnet — rynek jest konkurencyjny i ceny to odzwierciedlają.

Dokumenty polskie (i wiele innych nieangielskich języków europejskich): opcje zwężają się znacząco:

- Możesz używać wielojęzycznych modeli osadzeń (E5-multilingual, Cohere multilingual) przy wyższym koszcie per token niż modele zoptymalizowane pod angielski
- Możesz używać modeli klasy Claude lub GPT-4, które obsługują polski wystarczająco, ale w cenie premium
- Możesz self-hostować polskie natywne modele jak Bielik (12 miliardów parametrów, otwarte wagi) po koszcie infrastruktury zamiast kosztu per token

W Insly znaleźliśmy 12 punktów procentowych poprawy precision przechodząc z wielojęzycznych osadzeń na Bielika dla polskich dokumentów ubezpieczeniowych. Koszt self-hostowania był uzasadniony zarówno jakością jak i wymogami data residency.

### Zmienna 3: SLA jakości

To zmienna, której klienci najbardziej niedoszacowują przy scope'owaniu. Różnica między celowaniem w 80% dokładności odpowiedzi a 95% dokładności to nie 15% wzrost nakładu inżynieryjnego. To mniej więcej 3x całkowity koszt pętli zapewnienia jakości i iteracji.

Dlaczego? Bo:
- Każdy punkt procentowy powyżej ~85% wymaga znacznie więcej otagowanych danych ewaluacyjnych żeby wiarygodnie zmierzyć
- Techniki poprawy, które wynoszą cię z 80% do 90% (lepszy chunking, lepsze prompty) są tanie. Przejście z 90% do 95% wymaga wyspecjalizowanych strategii retrieval, rozbudowanego fine-tuningu i ciągłej ewaluacji ludzkiej — wszystko drogie
- Narzut monitoringowy skaluje się z celem jakości: system 95% precision wymaga ciągłej ewaluacji; system 80% toleruje cotygodniowe sprawdzanie

W ubezpieczeniach, gdzie potrzebujemy > 92% precision dla faktualnych zapytań o kwoty ochrony i wyłączenia, ta zmienna sama determinuje czy system kosztuje 1 200$/mies czy 3 500$/mies.

### Zmienna 4: Wymogi compliance

Każdy wymóg compliance przekłada się bezpośrednio na koszt architektoniczny:

**RODO / data residency**: Dane nie mogą opuścić UE. Wyklucza to niektóre komercyjne opcje API lub wymaga konkretnej konfiguracji. W praktyce oznacza uruchamianie na AWS EU-region (Frankfurt, Irlandia) i weryfikację że żadne dane zapytań nie przechodzą przez endpointy US-region.

**Obsługa PII**: Wymaga detekcji i redakcji danych osobowych zarówno w inputach jak i outputach. Albo Bedrock Guardrails (dodaje ~$0.75/1k tokenów wejściowych) albo custom pipeline PII (koszt inżynieryjny).

**Audit trail**: Każde zapytanie i odpowiedź muszą być logowane z wystarczającymi metadanymi do przeglądu compliance. Wymaga dedykowanej infrastruktury logowania — nie tylko CloudWatch, ale ustrukturyzowane logi z niezmienną retencją.

**Specyficzne dla ubezpieczeń**: W Polsce regulacje dystrybucji ubezpieczeń wymagają że każdy system podający informacje produktowe brokerom utrzymuje audit trail możliwy do przedstawienia w przeglądzie regulacyjnym. Ten wymóg architektoniczny nie jest opcjonalny.

Wpływ na koszt: w pełni zgodny RAG ubezpieczeniowy kosztuje około 40-60% więcej całkowicie w developmencie i rocznym utrzymaniu niż nieregulowane wewnętrzne narzędzie o równoważnym wolumenie zapytań.

### Zmienna 5: Złożoność integracji

Standalone chatbot (osobny URL, użytkownicy nawigują do niego) to najprostsza integracja: web frontend wywołujący API. Czas developmentu: 2-4 tygodnie.

Wbudowanie w istniejący portal brokerski (inline w workflow wyszukiwania produktów, uwierzytelniony, uwzględniający kontekst): 3-5x więcej czasu developmentu. Budujesz integrację z istniejącym systemem, obsługujesz kontekst sesji, uwierzytelnianie, dostęp oparty na rolach i potencjalnie wyświetlasz wyniki w formacie ustrukturyzowanym natywnym dla istniejącego UI.

Koszt integracji często przekracza koszt pipeline RAG w projektach korporacyjnych. Klienci skupiający się na "koszcie AI" całkowicie to pomijają.

### Zmienna 6: Bieżące utrzymanie

To koszt najczęściej niedoszacowywany i ten, który niszczy projekty w roku 2.

Prace bieżącego utrzymania:
- **Kadencja ewaluacji**: uruchamianie canary test set, przeglądanie wyników, badanie regresji. Budżet minimum 4-8 godzin inżynieryjnych miesięcznie.
- **Aktualizacje modeli**: dostawcy chmury cicho aktualizują modele. Aktualizacje modeli Bedrock przesunęły nasze metryki precision o nawet 6 punktów. Ktoś musi to wychwycić.
- **Reindeksowanie dokumentów**: polisy ubezpieczeniowe zmieniają się corocznie. Reindeksowanie 1 000 dokumentów zajmuje mniej więcej 2-4 godziny inżynieryjne plus koszty osadzeń.
- **Iteracja promptów**: zapytania użytkowników ewoluują. Pojawiają się nowe wzorce, które twoje aktualne prompty obsługują słabo. Tuning promptów to ciągła aktywność.
- **Support użytkowników przez pierwsze 3-6 miesięcy**: "Dlaczego nie wie o X?" zajmuje nieproporcjonalnie dużo czasu inżynieryjnego po wdrożeniu.

Jeśli planujesz zerowe bieżące utrzymanie, spodziewaj się że precision zedryfuje z 92% do 78% w ciągu 18 miesięcy gdy dokumenty się zmienią, modele zaktualizują i wzorce zapytań ewoluują.

---

## Case Study: trzy architektury, jeden przypadek użycia

**Stały scenariusz**: 1 000 polskich dokumentów ubezpieczeniowych, 5 000 zapytań/miesiąc, cel > 90% precision, zgodność z RODO, standalone chatbot (bez integracji), deployment EU.

Wszystkie liczby poniżej są szacunkami opartymi na opublikowanych cennikach AWS (aktualne na początku 2026), typowych stawkach wynajmu GPU i moim doświadczeniu z podobnymi projektami. Są wyraźnie oznaczone jako szacunki gdzie jest niepewność.

### Opcja A: Full managed (AWS Bedrock)

Wszystkie komponenty to zarządzane usługi AWS. Żadnej infrastruktury do obsługi.

**Komponenty**:
- Osadzenia: Amazon Titan Embed v2 (wielojęzyczny z obsługą polskiego)
- Wektorówka: Amazon OpenSearch Serverless
- LLM: Claude Sonnet 3.5 przez Bedrock
- Guardrails: Bedrock Guardrails dla PII
- Ewaluacja: custom canary set + CloudWatch

**Koszt developmentu** (jednorazowy, szacunek):
- Setup pipeline i integracja: ~40 godzin inżynieryjnych (~16 000 zł przy stawce blended senior dev)
- Tworzenie zestawu ewaluacyjnego (80 otagowanych pytań): ~16 godzin (~6 400 zł)
- Łącznie jednorazowo: ~22 400 zł

**Miesięczny koszt cykliczny** (przy 5 000 zapytań/miesiąc):
- Titan Embed v2: ~$0.02/1k tokenów × ~200k tokenów/miesiąc = ~$4
- OpenSearch Serverless: minimum ~$175/miesiąc (ceny OCU, podłoga serverless)
- Claude Sonnet 3.5: ~$3/1k tokenów wyjściowych × ~50k tokenów/miesiąc = ~$150
- Bedrock Guardrails: ~$0.75/1k tokenów wejściowych × ~100k tokenów/miesiąc = ~$75
- CloudWatch + logowanie: ~$20
- Utrzymanie inżynieryjne: 6h/miesiąc × ~400 zł/h = ~$600 (~2 400 zł)
- **Łącznie miesięcznie: ~$1 025 (~4 100 zł)**

**TCO**:
- Rok 1: ~$17 900 (~72 000 zł)
- Rok 2: ~$12 300 (~49 000 zł)
- Rok 3: ~$12 300 (~49 000 zł)
- **Łącznie 3 lata: ~$42 500 (~170 000 zł)**

**Kompromisy**:
- Najniższy próg wejścia
- Żadnej infrastruktury do zarządzania
- Ograniczona kontrola nad zachowaniem modelu (zależność od aktualizacji modeli AWS)
- Data residency wymaga konfiguracji EU-region
- Najwyższy koszt per zapytanie na skali (koszty skalują liniowo z wolumenem zapytań)

### Opcja B: Self-hosted (Bielik + Qdrant)

Bielik 12B zarówno do osadzeń jak i generacji (natywny polski), Qdrant jako self-hosted wektorowa baza danych na EC2.

**Infrastruktura**:
- Osadzenia i generacja: g4dn.2xlarge (1x GPU T4, ~$0.752/godz) — dedykowana instancja dla pracy 24/7
- Wektorowa baza danych: m6i.large dla Qdrant (~$0.096/godz)
- Miesięczny szacunek 24/7: (~$0.752 + ~$0.096) × 730h = ~$620/miesiąc infrastruktura

**Koszt developmentu** (jednorazowy, szacunek):
- Setup Bielik, kwantyzacja, serwowanie: ~60 godzin inżynieryjnych (~24 000 zł)
- Setup Qdrant, pipeline indeksowania: ~40 godzin (~16 000 zł)
- Infrastruktura ewaluacji: ~20 godzin (~8 000 zł)
- Łącznie jednorazowo: ~48 000 zł

**Miesięczny koszt cykliczny**:
- Infrastruktura EC2: ~$620 (~2 480 zł)
- Utrzymanie inżynieryjne (wyższe niż managed — posiadasz infra): ~10h × ~400 zł/h = ~$1 000 (~4 000 zł)
- Logowanie odpowiednik CloudWatch: ~$15
- **Łącznie miesięcznie: ~$1 635 (~6 500 zł)**

**Uwaga o jakości**: Bielik daje ~12pp poprawy precision na polskich dokumentach ubezpieczeniowych w porównaniu z alternatywami wielojęzycznymi w naszych testach. Przy celu SLA 90% to jest istotne — może być różnicą między spełnieniem celu a rozbudowaną inżynierią promptów kompensującą słabsze osadzenia.

**TCO**:
- Rok 1: ~$31 600 (~126 000 zł)
- Rok 2: ~$19 600 (~78 000 zł)
- Rok 3: ~$19 600 (~78 000 zł)
- **Łącznie 3 lata: ~$70 800 (~282 000 zł)**

Czekaj — self-hosted jest droższy? Tak, przy tej skali. Self-hosted ma sens ekonomiczny gdy wolumen zapytań jest 20x wyższy (koszty infrastruktury amortyzują się) lub gdy wymogi data residency są surowsze niż zarządzane usługi mogą spełnić.

**Kompromisy**:
- Pełna kontrola nad zachowaniem i aktualizacjami modelu
- Najlepsza precision w języku polskim
- Najlepsza kontrola data residency
- Znaczny narzut infrastruktury
- Wyższy łączny koszt przy skali 5k zapytań/miesiąc

### Opcja C: Hybrid (Bedrock do generacji + self-hosted osadzenia)

Bielik do osadzeń (self-hosted, dla precision) i Claude przez Bedrock do generacji (managed, dla niezawodności i compliance).

**Komponenty**:
- Osadzenia: model osadzeń Bielik 7B na t3.xlarge (~$0.166/godz, mniejszy GPU nie jest potrzebny dla osadzeń inference-only — CPU-based z batchingiem)
- Wektorówka: Qdrant na t3.medium (~$0.042/godz)
- Generacja: Claude Haiku przez Bedrock (tańszy niż Sonnet; wystarczający gdy retrieval jest wysokiej jakości)
- Guardrails: Bedrock Guardrails

**Koszt developmentu** (jednorazowy, szacunek):
- Setup hybrydowego pipeline: ~80 godzin inżynieryjnych (~32 000 zł)
- (Bardziej złożony niż którekolwiek czyste podejście ze względu na mieszaną infrastrukturę)

**Miesięczny koszt cykliczny**:
- t3.xlarge (osadzenia): ~$120/miesiąc (~480 zł)
- Qdrant na t3.medium: ~$31/miesiąc (~124 zł)
- Claude Haiku przez Bedrock: ~$0.25/1k inputu × ~200k tokenów/miesiąc = ~$50
- Bedrock Guardrails: ~$75
- Utrzymanie inżynieryjne: ~7h × ~400 zł/h = ~$700 (~2 800 zł)
- **Łącznie miesięcznie: ~$976 (~3 900 zł)**

**TCO**:
- Rok 1: ~$19 700 (~79 000 zł)
- Rok 2: ~$11 700 (~47 000 zł)
- Rok 3: ~$11 700 (~47 000 zł)
- **Łącznie 3 lata: ~$43 100 (~172 000 zł)**

**Tabela porównawcza TCO**:

| | Opcja A (Full Managed) | Opcja B (Self-Hosted) | Opcja C (Hybrid) |
|---|---|---|---|
| Jednorazowy koszt dev | ~22 400 zł | ~48 000 zł | ~32 000 zł |
| Miesięczny cykliczny | ~4 100 zł | ~6 500 zł | ~3 900 zł |
| Rok 1 łącznie | ~72 000 zł | ~126 000 zł | ~79 000 zł |
| Rok 2 łącznie | ~49 000 zł | ~78 000 zł | ~47 000 zł |
| Rok 3 łącznie | ~49 000 zł | ~78 000 zł | ~47 000 zł |
| TCO 3 lata | ~170 000 zł | ~282 000 zł | ~172 000 zł |
| Polish precision | Średnia | Najwyższa | Wysoka |
| Narzut infra | Niski | Wysoki | Średni |
| Kontrola | Niska | Pełna | Średnia |

Klient, który skłonił mnie do zbudowania tego modelu, początkowo zakładał że self-hosted jest najtańszy ("żadnych kosztów API!"). Przy 5 000 zapytań/miesiąc jest znacznie droższy ze względu na stałe koszty infrastruktury. Opcja C dostarczyła najlepszy balans przy tej skali: prawie pełną korzyść Bielika dla retrieval, niezawodność managed Bedrock dla generacji i najniższe TCO po 3 latach.

---

## Ukryte koszty, których klienci nie widzą

Powyższe liczby zakładają kompetentne bieżące utrzymanie. Oto jak "kompetentne utrzymanie" faktycznie wygląda w godzinach i kosztach:

**Ewaluacja i monitoring** (4-8h/miesiąc): Uruchamianie canary test set, przeglądanie dashboardów, badanie regresji precision. Nie można tego w pełni zautomatyzować — ktoś musi interpretować wyniki i decydować kiedy działać.

**Coroczne reindeksowanie dokumentów** (2-4h + koszty osadzeń): Polisy ubezpieczeniowe zmieniają się corocznie. Pełny reindeks corpus wymaga weryfikacji jakości względem zestawu ewaluacyjnego po zakończeniu.

**Incydenty dryfu modelu** (zmienny, ~10-20h/incydent): Dostawcy chmury cicho aktualizują modele. Gdy to się stanie, musisz to wykryć, scharakteryzować wpływ i rekalibrować progi. Budżet na 1-2 incydenty rocznie.

**Obsługa nowych wzorców zapytań** (4-8h/kwartał): Zachowanie użytkowników ewoluuje. Strategie promptów, które działały przy wdrożeniu, wymagają aktualizacji gdy wzorce zapytań się przesuwają. To inżynieria promptów, nie infrastruktura.

**Ogon supportu użytkowników rok 2**: Przez pierwsze 3-6 miesięcy po wdrożeniu narzut supportu jest wysoki (~20% czasu inżynieryjnego dotykającego systemu). Spada do ~5% w miesiącu 12 gdy użytkownicy uczą się możliwości i ograniczeń systemu.

Jeśli klient buduje Opcję A zakładając że koszt jednorazowy pokrywa wszystko: w miesiącu 18 ma niemonitorowany system z dryfującą precision i brak budżetu na naprawę. Widziałem ten wzorzec więcej niż raz.

---

## Jak prezentować wycenę klientom

Zły sposób: "RAG kosztuje X złotych miesięcznie."

Dobry sposób: "Oto trzy architektury dla twojego przypadku użycia, z kompromisami i 3-letnim TCO dla każdej. Najtańsza opcja w roku 1 nie jest najtańszą opcją w roku 3. Oto dlaczego, i oto którą polecam biorąc pod uwagę twoje ograniczenia."

Ta rozmowa robi trzy rzeczy:
1. Ustala realistyczne oczekiwania co do bieżącego kosztu (nie tylko kosztu buildu)
2. Ujawnia wymogi compliance i jakości, które zmieniają analizę
3. Pozycjonuje cię jako kogoś rozwiązującego problem biznesowy, nie sprzedającego technologię

Klienci zaskoczeni kosztami RAG w roku 2 to zazwyczaj klienci którym sprzedano "koszt buildu" bez rozmowy o TCO. Nie bądź osobą, która to robi.

---

## Podsumowanie

Wycena RAG zależy od sześciu zmiennych: wolumen dokumentów, wolumen zapytań, język, SLA jakości, wymogi compliance i złożoność integracji. Wyjaśnij wszystkie sześć zanim cokolwiek wycenicisz.

Dla 1 000 polskich dokumentów ubezpieczeniowych przy 5 000 zapytań/miesiąc z precision > 90%:
- Full managed (Bedrock): ~170 000 zł przez 3 lata, najniższe tarcie setupu
- Self-hosted (Bielik + Qdrant): ~282 000 zł przez 3 lata, najlepsza precision i kontrola
- Hybrid (osadzenia Bielik + generacja Bedrock): ~172 000 zł przez 3 lata, najlepszy balans przy tej skali

Najtańsza infrastruktura to nie najtańsze TCO. Najdroższa infrastruktura to nie zawsze najlepsza jakość. Przelicz liczby zanim zdecydujesz się na architekturę.

Napisz "RAG PRICING" w komentarzu jeśli wyceniasz projekt RAG — podeślę arkusz kalkulacyjny z tym modelem.
