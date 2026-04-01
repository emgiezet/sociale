---
day: 18
title: "LightRAG vs. AWS Bedrock Knowledge Bases: uczciwe porównanie produkcyjne"
pillar: Builder
language: pl
image: ../../images/day-18.jpg
image_unsplash_query: "software architecture decision comparison"
---

# LightRAG vs. AWS Bedrock Knowledge Bases: uczciwe porównanie produkcyjne

Większość porównań narzędzi AI jest pisana przez ludzi, którzy czytali dokumentację. To jest napisane przez kogoś, kto uruchamiał oba w produkcji w środowisku ubezpieczeniowym, z prawdziwymi użytkownikami i prawdziwymi wymaganiami jakościowymi.

Krótka wersja: oba narzędzia są wartościowe, są zoptymalizowane dla różnych przypadków użycia, a wybór między nimi (lub zdecydowanie o używaniu obu) zależy od zrozumienia, jaki problem naprawdę próbujesz rozwiązać.

## Kontekst

W Insly przetwarzamy dokumenty ubezpieczeniowe — polisy, endorsementy, biblioteki klauzul — i musimy odpowiadać na pytania underwriterów dotyczące ich treści. Wyzwanie: dokumenty ubezpieczeniowe są mocno cross-referencyjne. Klauzula pokrycia może mieć sens tylko w kontekście wyłączenia w innej sekcji tego samego dokumentu lub w kontekście dokumentu ogólnych warunków ubezpieczenia, który stosuje się do wszystkich polis.

To jest konkretny problem, który napędził naszą ewaluację LightRAG obok Bedrock Knowledge Bases. Przeprowadziliśmy to porównanie przez cztery miesiące, z zestawem testowym 200 pytań walidowanych przez ekspertów domenowych z branży ubezpieczeniowej.

## AWS Bedrock Knowledge Bases: Gdzie Wygrywa

Bedrock Knowledge Bases to najszybsza droga od dokumentów do działającego retrieval. Wskazujesz na bucket S3, obsługuje chunkowanie, embeddowanie (przez Titan Embeddings) i indeksowanie do OpenSearch Serverless. Masz API retrieval w ciągu godzin.

Dla zespołów bez dedykowanych inżynierów infrastruktury ML, to jest naprawdę wartościowe. Zarządzana infrastruktura oznacza, że nie zarządzasz operacjami vector store, skalowaniem ani utrzymaniem. Aktualizacje korpusu dokumentów są obsługiwane przez re-synchronizację knowledge base.

Jakość retrieval przy prostych zadaniach Q&A — pytaniach, gdzie odpowiedź istnieje w jednej sekcji dokumentu — jest solidna. AWS dodał opcje wyszukiwania hybrydowego (łączące semantyczne i leksykalne retrieval), które poprawiają recall na technicznej terminologii.

Gdzie wyróżnia się:
- Q&A dokumentacji produktu
- Wyszukiwanie w bazie wiedzy dla zespołów wsparcia
- Analiza pojedynczych dokumentów
- Przypadki użycia, gdzie dokumenty są w dużej mierze niezależne

Co zawodzi: złożone relacje między dokumentami. Jeśli Twoje dokumenty odwołują się do siebie nawzajem — jeśli zrozumienie klauzuli A wymaga znajomości klauzuli B w innym dokumencie — Bedrock Knowledge Bases nie modeluje tych relacji. Pobiera podobny tekst. Nie rozumuje o połączeniach.

## LightRAG: Gdzie Wygrywa

LightRAG buduje graf wiedzy z Twoich dokumentów zamiast tylko indeksu wektorowego. Ekstraktuje encje (osoby, organizacje, koncepty, daty, klauzule) i relacje między nimi. Kiedy odpytujesz system, retrieval przechodzi przez ten graf — znajdując nie tylko podobny tekst, ale połączone informacje.

Dla dokumentów ubezpieczeniowych, to jest transformacyjne. Zapytanie o to, jak konkretna klauzula wchodzi w interakcję z inną klauzulą w dwóch dokumentach, to problem przechodzenia grafu, a nie wyszukiwania podobieństwa. LightRAG może podążać za relacjami. Bedrock Knowledge Bases pobiera tekst najbardziej podobny do zapytania, co może być właściwą klauzulą bez jej kontekstu.

Konkretnie: nasz zestaw ewaluacyjny zawierał 40 pytań specjalnie o relacje między dokumentami (jak klauzula w dokumencie A wchodzi w interakcję z warunkiem w dokumencie B?). Na tych pytaniach:
- Bedrock Knowledge Bases: 52% dokładności retrieval
- LightRAG: 81% dokładności retrieval

Na pytaniach z pojedynczego dokumentu, pojedynczej sekcji, różnica była znacznie mniejsza (Bedrock: 78%, LightRAG: 84%).

Gdzie LightRAG wyróżnia się:
- Dokumenty z złożonymi cross-referencjami (prawne, ubezpieczeniowe, medyczne, regulacyjne)
- Przypadki użycia, gdzie relacje między encjami niosą informacje
- Domeny, gdzie połączenie między konceptami jest równie ważne jak same koncepty

## Rzeczywiste Koszty: Czego Nie Pokazują Benchmarki

Wybór LightRAG ma koszty, które nie pojawiają się w liczbach dokładności.

**Złożoność operacyjna.** Masz bazę danych grafów i infrastrukturę vector store. Musisz uruchamiać pipeline ekstrakcji encji i budowania relacji. Kiedy dokument się zmienia, musisz ponownie uruchomić konstrukcję grafu dla dotkniętych dokumentów.

**Czas indeksowania.** Budowanie grafu wiedzy LightRAG nad dużym korpusem dokumentów zajmuje godziny. Indeksowanie Bedrock Knowledge Bases jest znacznie szybsze dla dużych korpusów.

**Złożoność debugowania.** Kiedy retrieval zawodzi z Bedrock Knowledge Bases, zazwyczaj możesz zidentyfikować problem badając pobrane chunki. Kiedy retrieval zawodzi z LightRAG, debugujesz logikę przechodzenia grafu, jakość ekstrakcji encji i modelowanie relacji.

**Koszt.** Wywołania LLM dla ekstrakcji encji i budowania relacji w LightRAG dodają koszt na zaindeksowany dokument.

**Za pierwszym razem wybraliśmy źle.** Zaczęliśmy od LightRAG, bo chcieliśmy zdolności retrieval opartego na relacjach. Spędziliśmy tygodnie na konfiguracji infrastruktury, zanim zdali sobie sprawę, że powinniśmy byli zacząć od Bedrocka, żeby najpierw zwalidować przypadek użycia. Straciliśmy czas, którego nie musieliśmy tracić.

## Jak Uruchamiamy Oba

Nasza architektura produkcyjna uruchamia oba systemy, routując zapytania na podstawie ich charakterystyk:

→ Zapytania wymagające rozumowania między dokumentami: LightRAG
→ Zapytania o konkretne dokumenty z dobrze zdefiniowanymi sekcjami: Bedrock Knowledge Bases
→ Zapytania, gdzie z góry nie możemy określić typu: LightRAG (akceptując wyższy koszt operacyjny dla wyższego sufitu dokładności)

Warstwa routowania jest prosta: mały klasyfikator, który określa typ zapytania na podstawie tego, czy zawiera nazwane relacje ("jak X odnosi się do Y"), porównania czasowe ("co się zmieniło między wersją A a B") lub syntezę wielu dokumentów.

## Framework Decyzyjny

Wybierz Bedrock Knowledge Bases jeśli:
- Twoje dokumenty są w dużej mierze niezależne (jeden dokument może odpowiedzieć na większość pytań)
- Twój zespół nie ma pojemności do operowania dodatkową infrastrukturą
- Musisz wypchnąć coś w tygodniach, a nie miesiącach
- Twoje wymagania dokładności są spełniane przez standardowe wyszukiwanie semantyczne

Wybierz LightRAG jeśli:
- Twoje dokumenty mocno odwołują się do siebie nawzajem
- Relacje między konceptami i encjami niosą krytyczne informacje
- Masz pojemność inżynierską do operowania dodatkową infrastrukturą
- Twój przypadek użycia ma wymagania dokładności, których wyszukiwanie semantyczne nie spełnia

Zacznij od Bedrocka. Kiedy osiągniesz sufit — kiedy możesz zmierzyć, że Twoje problemy jakościowe to problemy retrieval opartego na relacjach — oceń LightRAG. Nie optymalizuj przedwcześnie pod złożone rozwiązanie.

Najlepsza architektura RAG to najprostsza, która spełnia Twoje wymagania jakościowe. Czasem to Bedrock Knowledge Bases. Czasem to LightRAG. Dane ewaluacyjne mówią Ci, które.
