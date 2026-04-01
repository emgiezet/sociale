---
day: 38
title: "Chunking w RAG: dlaczego 60% pracy jest zanim LLM cokolwiek zobaczy"
pillar: Educator
language: pl
image: ../../images/day-38.jpg
image_unsplash_query: "document parsing pipeline data engineering processing"
---

# Chunking w RAG: dlaczego 60% pracy jest zanim LLM cokolwiek zobaczy

Historia debugowania, która kosztowała nas dwa tygodnie.

Nasz system RAG produkował niespójne odpowiedzi. Czasem ostre i precyzyjne. Czasem niekompletne, czasem jawnie błędne. Model to Claude Sonnet — dobry model, dobrze skonfigurowany. Prompt był iterowany dziesiątki razy. Osadzenia (embeddings) z wysokiej jakości modelu.

A potem ktoś z zespołu spojrzał na to, co faktycznie trafiało do okna kontekstu.

Retriever zwracał środek klauzuli ubezpieczeniowej. Bez nagłówka sekcji. Bez numeru paragrafu. Bez odniesienia do definicji, którą cytował. Chunk zaczynał się od "...zgodnie z postanowieniami §4 ust. 2 niniejszej umowy..." i nie zawierał żadnego wskazania co te postanowienia mówiły ani gdzie je znaleźć.

Model nie miał szans. Nie możesz wygenerować poprawnej odpowiedzi z niekompletnego fragmentu, niezależnie jak mądry jest model.

Tego dnia zrozumieliśmy: RAG to w większości problem przygotowania danych.

## Garbage in, garbage out

Najczęstszy tryb awarii w systemach RAG, który widzę, to nie prompt engineering. Nie dobór modelu. To wyszukiwanie zwracające treść, która jest technicznie trafna, ale kontekstowo niekompletna.

Chunking jest powodem.

To jak dzielisz dokument na przeszukiwalne kawałki determinuje co model widzi gdy użytkownik zadaje pytanie. Zrób to źle i będziesz miesiącami poprawiał każdy inny komponent, podczas gdy fundamentalny problem pozostaje na miejscu.

Nasze dokumenty w Insly to trudny przypadek: polisy ubezpieczeniowe z dziesięciu europejskich rynków, część w formatach Word z 2009 i 2012 roku, część jako skany PDF z artyfaktami OCR, część z tabelami osadzonymi jako obrazy. Zanim mogliśmy myśleć o strategii chunkingu, mieliśmy poważny problem ekstrakcji danych do rozwiązania.

Omówmy oba.

## Krok 1: Czyszczenie dokumentów źródłowych

Uzyskanie czystego tekstu z realnych dokumentów jest trudniejsze niż wygląda. Oto co napotykamy na każdym etapie.

**Ekstrakcja PDF.** Standardowe biblioteki PDF (PyMuPDF, pdfminer) radzą sobie rozsądnie z dobrze ustrukturyzowanymi plikami PDF. Zawodzą na zeskanowanych dokumentach, plikach PDF z dwukolumnowym układem i plikach PDF gdzie tabele są renderowane jako obrazy. Dla naszych polis:

- PDF-y tekstowe: PyMuPDF działa dobrze, zachowuje informacje o układzie
- PDF-y zeskanowane: Używamy AWS Textract, który obsługuje OCR i zwraca strukturalne wyjście z detekcją tabel
- PDF-y wielokolumnowe: niestandardowe post-przetwarzanie do wykrywania i porządkowania kolumn

**Dokumenty Word.** Legacy pliki .doc i .docx z lat 2009–2013 są niespójnie ustrukturyzowane. Nagłówki mogą być pogrubionymi akapitami zamiast stylów nagłówkowych Word. Listy mogą być ręcznie numerowane. Używamy python-docx do ekstrakcji z niestandardowymi heurystykami do wykrywania elementów strukturalnych.

**Artefakty OCR.** Błędy podstawiania znaków, które OCR wprowadza, są specyficzne: "0" zamiast "O", "l" zamiast "1", "rn" zamiast "m". W dokumentach ubezpieczeniowych "§ 4 ust. 2" może wyjść jako "§ 4 ust 2" lub "§4ust.2". To psuje późniejsze dopasowywanie tekstu. Uruchamiamy niestandardowy przebieg czyszczenia, który normalizuje polskie wzorce cytowania prawnego.

**Ekstrakcja metadanych.** Podczas ekstrakcji przechwytujemy: tytuł dokumentu, datę, typ polisy, rynek wystawiający, język, strukturę sekcji (jeśli możliwa do odzyskania). Te metadane stają się metadanymi chunka i są krytyczne do filtrowania przy wyszukiwaniu.

## Krok 2: Cztery strategie chunkingu

Gdy masz już czysty tekst, stoisz przed decyzją o chunkingu. Oto jak każda strategia się zachowuje — na konkretnym przykładzie z naszych danych.

**Klauzula źródłowa:**
> "Ubezpieczyciel ponosi odpowiedzialność za szkody powstałe wskutek powodzi, z wyłączeniem przypadków określonych w §4 ust. 2 niniejszej umowy, o ile Ubezpieczający wyraził pisemną zgodę na rozszerzenie zakresu ochrony w trybie §8."

### Strategia 1: Chunking fixed-size

Podziel tekst na chunki N tokenów (typowo 256–512) z pewnym nakładaniem (typowo 10–20%).

**Co dzieje się z naszą klauzulą:** Przy 256 tokenach klauzula może rozpaść się w połowie zdania jeśli otaczający kontekst jest gęsty. Bardziej prawdopodobne, że ląduje w środku chunka razem z niepowiązaną treścią z sąsiednich akapitów. Fraza "pisemna zgoda na rozszerzenie zakresu ochrony" pojawia się w chunku, ale "powódź" może być w poprzednim chunku.

**Wynik wyszukiwania dla zapytania "czy polisa pokrywa szkody powodziowe":** System może zwrócić chunk zawierający definicję "powodzi" z innej sekcji, lub listę wyłączeń z §4 ust. 2, ale nie główną klauzulę odpowiedzialności.

**Kiedy używać:** Jednorodny tekst gdzie granice sekcji nie mają znaczenia. Bazy FAQ. Korpusy krótkich dokumentów. Nigdy dla ustrukturyzowanych dokumentów prawnych lub polis.

### Strategia 2: Semantic chunking

Podział na naturalnych granicach semantycznych: zdania, akapity, lub przy użyciu podejścia z przesuwanym oknem z porównaniem osadzeń na poziomie zdań do wykrywania zmian tematycznych.

**Co dzieje się z naszą klauzulą:** Klauzula typowo staje się własnym chunkiem — jest syntaktycznie kompletna. Ale jest odizolowana od definicji §4 ust. 2, do której się odnosi. Gdy model widzi "z wyłączeniem przypadków określonych w §4 ust. 2" bez treści §4 ust. 2 w kontekście, nie może odpowiedzieć na pytanie o wyłączenia.

**Wynik wyszukiwania:** Lepiej niż fixed-size, ale problem cross-referencji pozostaje. Użytkownik pytający "czy szkody powodziowe są wyłączone jeśli nie podpisałem rozszerzenia?" dostaje niekompletną odpowiedź.

**Kiedy używać:** Ogólnie ustrukturyzowany tekst z rozsądnymi granicami akapitów. Lepiej niż fixed-size w większości przypadków. Wciąż niedobry dla silnie cross-referencjonowanych dokumentów.

### Strategia 3: Chunking sekcjowy

Wyodrębnij logiczne sekcje dokumentu jako pojedyncze chunki — nagłówek sekcji i całą jej treść.

**Co dzieje się z naszą klauzulą:** Cała sekcja "Zakres ochrony" staje się jednym chunkiem, zawierającym naszą klauzulę powodziową, definicję powodzi i listę wyłączeń. To dokładnie to czego potrzebujemy — z wyjątkiem tego, że sekcja może mieć 2 000 tokenów.

**Problem rozcieńczenia:** Osadzenie (embedding) chunka o 2 000 tokenach produkuje gęstą reprezentację uśrednioną po wielu koncepcjach. Przy szukaniu "ochrona powodziowa", ten chunk konkuruje z krótszymi, bardziej skoncentrowanymi chunkami z innych dokumentów. Wynik podobieństwa jest rozcieńczony przez treść niezwiązaną z powodzią w tej samej sekcji.

**Wynik wyszukiwania:** Lepszy kontekst gdy znaleziony, ale niższy recall wyszukiwania — znajdziesz go rzadziej.

**Kiedy używać:** Dokumenty z wyraźnymi, ograniczonymi sekcjami gdzie cała sekcja jest istotna dla pytania użytkownika. Sprawdza się dobrze dla dokumentów w stylu FAQ.

### Strategia 4: Chunking parent-child z metadanymi

To podejście, którego używamy w produkcji dla dokumentów polis ubezpieczeniowych.

**Struktura:** Każda klauzula lub akapit staje się chunkiem "child" z precyzyjnymi metadanymi: nagłówek sekcji, numer paragrafu, tytuł dokumentu, typ polisy, rynek, data. Chunki parent to sekcje lub podsekcje — większe jednostki zapewniające szerszy kontekst.

**Co dzieje się z naszą klauzulą:** Klauzula odpowiedzialności za powódź staje się chunkiem child oznaczonym:
```
sekcja: "Zakres ochrony"
podsekcja: "Odpowiedzialność za konkretne zdarzenia"
paragraf: "§3.2"
odniesienia: ["§4.2", "§8"]
dokument: "Kompleksowe ubezpieczenie domu v2.3"
rynek: "PL"
```

Chunk child jest wystarczająco krótki i gęsty dla efektywnego osadzenia. Gdy zostanie wyszukany, system może opcjonalnie pobrać chunk parent dla szerszego kontekstu.

**Wynik wyszukiwania dla "czy szkody powodziowe są pokryte":** Klauzula powodziowa jest wyszukana jako chunk child. Wyłączenia §4.2 są wyszukane jako osobny chunk child, przyciągnięty ponieważ "§4.2" pojawia się w metadanych jako odniesienie. Model widzi oba, odpowiada kompletnie.

**Kiedy używać:** Złożone ustrukturyzowane dokumenty z cross-referencjami. Teksty prawne, polisy ubezpieczeniowe, dokumenty regulacyjne. Wart kosztu konfiguracji.

## Krok 3: Nakładanie, przesuwane okna i RAPTOR

Kilka dodatkowych technik uzupełniających powyższe.

**Nakładanie.** Nawet przy semantycznym lub sekcyjnym chunkingu, dodanie nakładania 50–100 tokenów między sąsiednimi chunkami zapewnia, że zdanie podzielone przez granicę chunka nie zniknie. Prosto i skutecznie.

**Przesuwane okno.** Dla narracyjnego tekstu bez silnych markerów strukturalnych, przesuwane okno (chunk 256 tokenów, przesuń o 128 tokenów) zapewnia, że każde zdanie pojawi się w co najmniej dwóch chunkach. Pomaga wyszukiwaniu, ale zwiększa rozmiar indeksu.

**RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval).** Bardziej zaawansowane podejście: osadź chunki, klastruj je, generuj podsumowania każdego klastra, osadź podsumowania i zbuduj hierarchię. Wyszukiwanie może odbywać się na każdym poziomie hierarchii. Omówię to szczegółowo w dniu 41 — rozwiązuje problemy, których powyższe strategie nie mogą.

## Pełny pipeline

Oto sekwencja, którą uruchamiamy dla każdego nowego korpusu dokumentów w Insly:

1. **Wykrycie formatu:** Czy to dobrze ustrukturyzowany PDF, zeskanowany PDF, dokument Word?
2. **Ekstrakcja:** PyMuPDF / AWS Textract / python-docx w zależności od formatu
3. **Normalizacja:** Czyszczenie artefaktów OCR, normalizacja kodowania, standaryzacja wzorców cytowania
4. **Wykrywanie struktury:** Identyfikacja nagłówków, sekcji, numerowanych klauzul używając wyrażeń regularnych dostrojonych do każdego typu dokumentu
5. **Ekstrakcja metadanych:** Przechwycenie metadanych na poziomie dokumentu i sekcji
6. **Wybór strategii chunkingu:** Na podstawie typu dokumentu i jakości struktury
7. **Generowanie chunków:** Z metadanymi dołączonymi do każdego chunka
8. **Kontrola jakości:** Próbkowanie 50 chunków ręcznie, weryfikacja dokładności i kompletności metadanych
9. **Osadzanie:** Uruchom model osadzania na chunkach
10. **Aktualizacja indeksu:** Upsert do magazynu wektorowego z filtrami metadanych

Kroki 1–8 typowo zajmują więcej czasu niż reszta systemu RAG razem wzięta, gdy robisz to porządnie. Dlatego mówię, że to 60% pracy.

## Jak to wygląda w Insly

Przetwarzamy dokumenty polis z 10+ europejskich rynków. Każdy rynek ma własne formaty dokumentów, tradycje prawne i konwencje strukturalne. Polska polisa z 2022 roku wygląda strukturalnie inaczej niż brytyjska polisa z 2015 roku.

Utrzymujemy profile ekstrakcji specyficzne dla rynku: różne heurystyki wykrywania struktury, różne schematy metadanych, różne wzorce normalizacji cytowania. Brzmi jak narzut — i jest nim. Ale alternatywą jest system działający dobrze na jednym korpusie i źle na wszystkim innym.

Wynik: nasz recall wyszukiwania na złotym zbiorze testowym poprawił się z 0.61 przy naiwnym chunkingu fixed-size do 0.87 przy chunkingu parent-child plus filtrowanie metadanych. Ta poprawa o 26 punktów procentowych nie pochodzi z ulepszeń modelu ani zmian promptów. Pochodzi z lepszego przygotowania danych.

To jest lekcja. Jeśli Twój system RAG nie działa dobrze, sprawdź co retriever faktycznie zwraca zanim dotkniesz promptu.

---

*Dzień 38 serii RAG Deep Dive. Jutro: realne koszty uruchamiania RAG w produkcji — trzy studia przypadków i analiza break-even.*
