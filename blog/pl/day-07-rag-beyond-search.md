---
day: 7
title: "Stos RAG, o którym nikt nie mówi: co oddziela dema od systemów produkcyjnych"
pillar: Educator
language: pl
image: ../../images/day-07.jpg
image_unsplash_query: "search pipeline architecture"
---

# Stos RAG, o którym nikt nie mówi: co oddziela dema od systemów produkcyjnych

Jeśli śledziłeś tutorial „zbuduj system RAG w 30 minut," znasz architekturę: zembedduj dokumenty, zapisz wektory, zapytuj przez podobieństwo, generuj z LLM. Ta architektura działa. Dla dem.

Produkcyjne systemy RAG — te obsługujące prawdziwe zapytania, od prawdziwych użytkowników, w domenach, gdzie błędne odpowiedzi mają konsekwencje — wymagają głębszego stosu. Oto komponenty, które większość tutoriali pomija, i dlaczego każdy z nich ma znaczenie.

Zbudowałem trzy z tych systemów w Insly, gdzie przetwarzamy dokumenty ubezpieczeniowe dla 150 000+ użytkowników. Każdy z nich nauczył mnie czegoś, czego tutorial nie omówił.

## Komponent 1: Strategia chunkowania

Kiedy dzielisz dokument na chunki do embeddowania, podejmujesz fundamentalną decyzję o tym, jakie informacje są możliwe do pobrania. Za małe, a poszczególne chunki tracą kontekst potrzebny do odpowiedzi na pytanie. Za duże, a sygnał semantyczny jest rozcieńczony.

Właściwa strategia chunkowania zależy od trzech rzeczy: struktury Twoich dokumentów źródłowych, natury Twoich zapytań i okna kontekstu Twojego LLM.

Dla dokumentów ubezpieczeniowych w Insly testowaliśmy rozmiary chunków od 200 do 1 200 tokenów. Testowaliśmy nakładające się chunki. Testowaliśmy semantyczne chunkowanie (dzielenie na granicach zdań lub akapitów). Testowaliśmy hierarchiczne chunkowanie (zachowywanie relacji sekcja-podsekcja w metadanych).

Czego się nauczyliśmy: nie ma powszechnej odpowiedzi. Optymalna strategia zależy od Twoich danych. Jedynym sposobem jej znalezienia jest mierzenie jakości retrieval przy różnych strategiach na rzeczywistym zbiorze ewaluacyjnym.

Dlatego strategia chunkowania i infrastruktura ewaluacji muszą być budowane razem. Nie możesz oceniać wyborów chunkowania bez sposobu mierzenia jakości retrieval, i nie możesz mierzyć jakości retrieval bez spójnego baselinowego chunkowania.

## Komponent 2: Filtrowanie metadanych

Wyszukiwanie semantyczne znajduje chunki semantycznie zbliżone do zapytania. Nie używa ustrukturyzowanych informacji, które masz o swoich dokumentach — kiedy zostały stworzone, który produkt opisują, którą jurysdykcję obejmują, którą wersję reprezentują.

Filtrowanie metadanych to możliwość ograniczenia wyszukiwania semantycznego przy użyciu tych ustrukturyzowanych informacji. Przed uruchomieniem kalkulacji podobieństwa embeddingów filtrujesz do odpowiedniego podzbioru dokumentów. Zmniejsza to przestrzeń wyszukiwania (poprawiając latencję i koszt) i zapobiega pobieraniu semantycznie podobnych, ale kontekstowo nieistotnych dokumentów.

W Insly tagujemy każdy chunk dokumentu metadanymi: typ dokumentu, linia produktów, jurysdykcja wystawiania, zakres dat obowiązywania, status zmian. Kiedy zapytanie użytkownika ma wyraźne sygnały metadanych („polska polisa mieszkaniowa z 2023 roku"), filtrujemy przed wyszukiwaniem. To samo poprawiło precyzję retrieval o około 15 punktów procentowych na naszym zbiorze ewaluacyjnym.

To wydaje się oczywiste z perspektywy czasu. Na początku nie było oczywiste.

## Komponent 3: Infrastruktura ewaluacji retrieval

To komponent, który większość tutoriali całkowicie pomija — i ten, który ma największe znaczenie dla wdrożenia produkcyjnego.

Nie możesz poprawić tego, czego nie mierzysz. A w systemie RAG „poprawa" nie jest oczywista. Czy ten wynik retrieval jest lepszy od tamtego? Potrzebujesz standardu do mierzenia.

Zestaw ewaluacyjny dla RAG składa się z: kolekcji realistycznych pytań, oczekiwanych pobranych fragmentów dla każdego pytania i oczekiwanych odpowiedzi dla każdego pytania. Pytania i oczekiwane fragmenty powinny być zwalidowane przez eksperta domenowego — kogoś, kto faktycznie wie, jak wygląda właściwa odpowiedź.

Mając zestaw ewaluacyjny, możesz mierzyć:
→ Precyzja retrieval: z pobranych fragmentów, jaka frakcja jest istotna?
→ Recall retrieval: z istotnych fragmentów w Twoim korpusie, jaka frakcja jest pobierana?
→ Wierność odpowiedzi: czy wygenerowana odpowiedź jest poparta pobranymi fragmentami?
→ Trafność odpowiedzi: czy odpowiedź dotyczy zadanego pytania?

Każda z tych metryk może być śledzona niezależnie i może kierować konkretnymi optymalizacjami. Bez nich zgadujesz o jakości i dokonujesz zmian architektonicznych w ciemności.

Zbuduj swój zestaw ewaluacyjny zanim cokolwiek optymalizujesz. Nasz zestaw ewaluacyjny ma 200 pytań brokerów z oczekiwanymi odpowiedziami, wyciągniętych z prawdziwych ticketów wsparcia. Uruchamiamy go przy każdej znaczącej zmianie. Jeśli dokładność spada o więcej niż 3%, nie wdrażamy. Bez wyjątków.

## Komponent 4: Reranking

Dwu-encoderowy system retrieval — standardowe wyszukiwanie podobieństwa wektorowego — jest szybki, ale nieprecyzyjny. Koduje zapytania i fragmenty niezależnie, co oznacza, że nie może bezpośrednio modelować interakcji między konkretnym zapytaniem a konkretnym fragmentem.

Cross-encoder reranker to naprawia. Bierze każdy pobrany fragment i zapytanie razem, i produkuje ocenę trafności, która jawnie modeluje ich relację. Jest dużo wolniejszy niż retrieval dwu-encoderowy, dlatego jest używany jako drugi etap: pobierz większy zestaw kandydatów za pomocą szybkiego retrieval dwu-encoderowego, następnie przerankuj za pomocą cross-encodera i zwróć tylko najlepsze wyniki.

Poprawa jakości z dodania rerankingu do bazowego systemu retrieval wynosi zazwyczaj 10–20 punktów procentowych. To jedna z interwencji o najwyższej dźwigni w stosie RAG i nie wymaga żadnych zmian w modelu embeddingów ani vector store.

Dla naszego systemu dokumentów ubezpieczeniowych, dodanie kroku rerankingu cross-encodera było pojedynczą zmianą, która przeniosła jakość retrieval z 72% do 85%. Dodatkowe ~200ms latencji było warte tego za jakość. W ubezpieczeniach dokładność bije szybkość.

## Komponent 5: Zakorzenienie vs. halucynacja

To powiązane, ale odrębne problemy, a ich mylenie prowadzi do rozwiązań, które dotyczą złej rzeczy.

**Halucynacja** to gdy LLM generuje treść, która nie jest nigdzie obecna w jego kontekście. Model wymyśla klauzulę polisową, statystykę, nazwę firmy. To jest problem generacji.

**Zakorzenienie** to czy wygenerowana odpowiedź jest poparta pobranymi fragmentami. Odpowiedź może być zakorzeniona, ale błędna (jeśli retrieval zwrócił złe fragmenty). Odpowiedź może być niezakorzeniona, ale przypadkowo poprawna (jeśli parametryczna wiedza modelu akurat jest dokładna).

Mierzenie zakorzenienia niezależnie od faktycznej dokładności pomaga rozróżnić błędy retrieval od błędów generacji. Jeśli odpowiedź jest niezakorzeniona, problem leży w konfiguracji generacji. Jeśli odpowiedź jest zakorzeniona, ale błędna, problem leży w retrieval.

## Składanie w całość

Te pięć komponentów to nie zaawansowane optymalizacje dla dojrzałych systemów. To wymagania wstępne dla systemu, któremu możesz ufać w produkcji.

Zespoły, które widziałem, że odnoszą sukces z RAG, budowały infrastrukturę ewaluacji jako pierwsze, optymalizowały retrieval jako drugie i traktowały generację jako ostatnią rzecz do dostrajania.

Zespoły, które widziałem, że zawodzą, budowały najładniejsze demo jako pierwsze i odkrywały problemy z jakością, gdy prawdziwi użytkownicy je znaleźli.

Zachowaj to jako checklistę na swój następny projekt RAG. Jeśli pracujesz przez któreś z tych konkretnych wyzwań — strategia chunkowania, projektowanie ewaluacji, implementacja rerankingu — napisz w komentarzu. Napotkałem każdy z tych problemów w produkcji i chętnie podzielę się tym, co zadziałało.
