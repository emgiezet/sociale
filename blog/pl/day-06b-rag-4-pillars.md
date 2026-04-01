---
day: 6
title: "Dlaczego Twój system RAG sypie się gdy go skalujesz: 4 problemy, o których nikt nie ostrzega"
pillar: Builder
language: pl
image: ../../images/day-06.jpg
image_unsplash_query: "library books knowledge continuous"
---

# Dlaczego Twój system RAG sypie się gdy go skalujesz: 4 problemy, o których nikt nie ostrzega

RAG działa idealnie dla 10 dokumentów. Potem dodajesz 5 więcej i się psuje.

To nie błąd. To cztery nierozwiązane problemy uderzające naraz.

To wzorzec, który widzę wielokrotnie budując systemy RAG w produkcji w Insly, gdzie przetwarzamy dokumenty ubezpieczeniowe w skali dla 150 000+ użytkowników. Tutorial YouTube doprowadza Cię do działającego. Produkcja doprowadza Cię do wszystkich czterech poniższych.

## Problem 1: Strategia chunkowania sypie się na ustrukturyzowanych dokumentach

Większość tutoriali dzieli tekst co N znaków. Dobrze dla dem. Sypie się na ustrukturyzowanych dokumentach, gdzie jedna klauzula odwołuje się do definicji z trzech innych sekcji.

Główny problem: chunkowanie według liczby tokenów traktuje tekst jako jednorodny strumień. Ale dokumenty polisowe ubezpieczeń — jak dokumenty prawne, dokumentacja medyczna, specyfikacje techniczne — mają wewnętrzną strukturę, która niesie znaczenie. Klauzula w sekcji 4 może mówić „zgodnie z definicją w sekcji 1.3" i „z zastrzeżeniem wyłączeń w sekcji 12." Chunk zawierający klauzulę sekcji 4, arbitralnie podzielony przy 512 tokenach, traci oba te odniesienia.

Fix to nie mniejsze chunki. To mądrzejsze.

Używamy kilku technik razem:

**RAPTOR (Recursive Abstractive Processing Tree Organization for Retrieval)** buduje hierarchiczne podsumowania drzew dokumentów. Zamiast tylko chunkować na poziomie liścia, tworzysz też węzły podsumowujące na wyższych poziomach hierarchii dokumentu. Zapytanie o pokrycie szkody wodnej może pobrać zarówno konkretną klauzulę, jak i podsumowanie sekcji, które daje jej kontekst.

**Tagowanie metadanych** zapewnia, że każdy chunk wie skąd pochodzi: typ dokumentu, sekcja, sekcja nadrzędna, ID dokumentu, data obowiązywania, wystawca. Te metadane stają się dostępne do filtrowania przed uruchomieniem wyszukiwania semantycznego.

**HyDE (Hypothetical Document Embeddings)** bridguje lukę językową między tym, jak pytania są zadawane a jak odpowiedzi są pisane. Broker pytający „czy to pokrywa szkodę powodziową?" brzmi zupełnie inaczej niż klauzula polisowa, która na to odpowiada. HyDE generuje hipotetyczny dokument odpowiedzi i embedduje go do retrieval, zamiast bezpośrednio embeddować pytanie.

To brzmi złożono. Jest złożone. Ale „inteligentne chunkowanie raz" jest dużo tańsze niż „pobieranie złych chunków na zawsze."

## Problem 2: Samo wyszukiwanie wektorowe sypie się na podobnych dokumentach

Gdy Twój korpus dokumentów rośnie i dokumenty stają się bardziej strukturalnie podobne, reprezentacje wektorowe przestają niezawodnie rozróżniać.

W naszym kontekście ubezpieczeniowym: nasze pliki OWU (Ogólne Warunki Ubezpieczenia) dla różnych ubezpieczycieli współdzielą tę samą ogólną strukturę, te same szablony prawne, te same nagłówki sekcji. Dokumenty różnią się w szczegółach, które mają znaczenie — konkretnych limitach pokrycia, konkretnych listach wyłączeń, konkretnych zasadach kalkulacji składki. Ale ich wektory są blisko siebie, co oznacza, że wyszukiwanie semantyczne zwraca mieszankę dokumentów od różnych ubezpieczycieli zamiast niezawodnie zwracać właściwy.

Czyszte wyszukiwanie wektorowe też przeoczy dokładne dopasowania terminologii. Broker pytający o „OC komunikacyjne" może nie dopasować dokumentu używającego pełnej frazy „ubezpieczenie odpowiedzialności cywilnej posiadaczy pojazdów mechanicznych" nawet jeśli odnoszą się do tego samego.

Odpowiedzią jest hybrid retrieval:

→ Gęste wyszukiwanie wektorowe dla podobieństwa semantycznego i dopasowania parafraz
→ Rzadkie wyszukiwanie słów kluczowych (BM25) dla dokładnego dopasowania terminów i terminologii domenowej
→ Warstwa rerankingu, która ocenia kandydatów z obu ścieżek retrieval dla rzeczywistej trafności do konkretnego zapytania przed przekazaniem ich do modelu

## Problem 3: Konfiguracja retrieval to ruchomy cel

Tu większość zespołów cicho krwawi. Twoja konfiguracja RAG to nie jednorazowa decyzja — to funkcja liczby dokumentów, specyfiki domeny i dystrybucji zapytań.

To, co działa przy 100 dokumentach, zawiedzie przy 10 000. To, co działa dla zapytań po angielsku, zawiedzie dla zapytań po polsku. To, co działa dla pytań o weryfikację pokrycia, zawiedzie dla złożonych pytań porównujących wiele dokumentów.

Każdy parametr musi być niezależnie sterowalny i ciągle mierzony:

→ **Nakładanie chunków**: za małe i tracisz kontekst na granicach, za duże i tworzysz redundantne retrievale marnujące okno kontekstu
→ **Model embeddingów**: właściwy model zależy od Twojej domeny i języków
→ **Top-k**: za niskie i brakuje Ci istotnego kontekstu, za wysokie i rozcieńczasz sygnał szumem
→ **Próg podobieństwa**: zbyt permisywny i model halucynuje pewnie, zbyt ścisły i zbyt często mówi „nie wiem"
→ **Próg rerankingu**: ile kandydatów przekazujesz do rerankera, ile reranker zwraca?
→ **Szablon promptu**: jak oprawiasz pobrany kontekst znacząco wpływa na jakość odpowiedzi

Żaden z tych parametrów nie ma powszechnie poprawnej wartości. Każdy ma poprawny zakres dla Twoich konkretnych danych, dystrybucji zapytań i wymagań jakościowych. Znalezienie tego zakresu wymaga mierzenia. Utrzymanie go wymaga ciągłego monitorowania.

Konfiguracja to nie ustaw-i-zapomnij.

## Problem 4: Bez infrastruktury ewaluacji latasz na ślepo

Nie możesz poprawić tego, czego nie mierzysz. Większość zespołów nie wie, czy ich RAG jest lepszy czy gorszy po każdej zmianie.

To jest najbardziej niebezpieczny tryb awarii. Dokonujesz zmiany architektonicznej — nowy model embeddingów, inny rozmiar chunka, dostosowany próg podobieństwa — i system wydaje się inny, ale nie wiesz czy faktycznie jest lepszy. Więc dokonujesz kolejnej zmiany. I kolejnej. I w pewnym momencie użytkownicy zaczynają skarżyć się na problemy z jakością, których nie możesz powiązać z konkretną decyzją.

Zbuduj dataset ewaluacyjny zanim dotkniesz produkcji. Oznacza to:

**Pary zapytanie-odpowiedź z ground-truth**: reprezentatywny zestaw prawdziwych zapytań z zwalidowanymi poprawnymi odpowiedziami. Dla naszego systemu ubezpieczeniowego oznaczało to pracę z licencjonowanymi underwriterami, żeby walidować odpowiedzi na podstawie rzeczywistych dokumentów polisowych. Walidowaliśmy na datasecie Egzaminu KNF dla Brokerów — oficjalnym egzaminie licencyjnym Komisji Nadzoru Finansowego dla brokerów ubezpieczeniowych. Jeśli RAG zda egzamin, który zdają licencjonowani brokerzy, możemy mu ufać w produkcji.

**Trzy oddzielne metryki**:
- Recall retrieval: czy wróciły właściwe dokumenty źródłowe?
- Wierność odpowiedzi: czy model trzymał się tego, co zostało pobrane?
- Poprawność odpowiedzi: czy końcowa odpowiedź była faktycznie poprawna?

Te trzy metryki mogą się rozbiegać. Możesz mieć dobry retrieval ale słabą wierność (model ignoruje to, co mu dałeś). Możesz mieć dobrą wierność ale słabą poprawność (pobrałeś złe dokumenty, ale model wiernie je opisał). Mierzenie wszystkich trzech mówi Ci, która warstwa systemu wymaga pracy.

**Zautomatyzowana integracja CI**: uruchamiaj swój dataset ewaluacyjny przy każdej znaczącej zmianie. Ustaw próg — dla nas spadek o więcej niż 3% dokładności odpowiedzi na naszym zestawie testowym oznacza, że nie wdrażamy, bez wyjątków.

## 90%, które tutoriale pomijają

Tutoriale YouTube o RAG uczą Cię budować pierwsze 10%: zembedduj dokumenty, zapisz wektory, pobieraj na zapytanie, generuj z LLM. Ta część jest naprawdę szybka i naprawdę imponująca.

Pozostałe 90% to:
→ Strategia chunkowania dostosowana do struktury Twoich dokumentów
→ Hybrid retrieval z rerankingiem dla mieszanych typów zapytań
→ Dyscyplina konfiguracyjna i ciągły monitoring
→ Infrastruktura ewaluacji z danymi ground-truth od ekspertów domenowych

Nic z tego nie jest egzotyczne. Wszystko to jest konieczne. Zespoły, które to pomijają, budują dema imponujące w prezentacjach i zawodzące w produkcji. Zespoły, które w to inwestują, budują systemy, którym użytkownicy faktycznie ufają.
