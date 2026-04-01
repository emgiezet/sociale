---
day: 19
title: "Stack AI development, którego naprawdę używamy w produkcji"
pillar: Educator
language: pl
image: ../../images/day-19.jpg
image_unsplash_query: "developer tools software workspace"
---

# Stack AI development, którego naprawdę używamy w produkcji

Co kilka tygodni ogłaszane jest nowe narzędzie AI z tekstem marketingowym, że jest "ostatnim narzędziem, którego potrzebujesz do tworzenia AI". Co kilka miesięcy narzędzie, które miało zastąpić wszystko, po cichu staje się jedną z sześciu rzeczy w złożonym stosie.

Ten post dotyczy narzędzi, których faktycznie używamy w Insly do budowania i obsługiwania systemów AI w produkcji. Podzielę się tym, dlaczego zatrzymaliśmy każde z nich, co ocenialiśmy i usunęliśmy, oraz logiką decyzji za wyborami.

## Najpierw Filozofia

Wybór stosu jest kierowany przez kilka zasad:

**AWS-natywny kiedy możliwe.** Już jesteśmy na AWS. Compliance, przegląd bezpieczeństwa, integracja IAM — to rozwiązane problemy w naszej istniejącej infrastrukturze. Dodanie nowego dostawcy oznacza dodanie nowej powierzchni compliance. Dodajemy narzędzia spoza AWS tylko gdy luka zdolności jest znacząca.

**Preferuj nudną infrastrukturę dla nowych zdolności.** Nie chcemy zarządzać dwoma nowymi złożonymi systemami, żeby wydać jedną nową funkcję. pgvector na istniejącym PostgreSQL zamiast dedykowanej bazy danych wektorów, wszędzie tam gdzie pozwala sufit wydajności.

**Oceniaj na podstawie mierzonych wyników, a nie dem.** Każde narzędzie w naszym stosie przeżyło ocenę względem naszego rzeczywistego przypadku użycia, nie syntetycznego benchmarku.

## Stos

### 1. AWS Bedrock — API Modeli Foundation i Zarządzany RAG

Bedrock jest centrum naszej infrastruktury AI. Daje nam dostęp do Claude 3.5 Sonnet (nasz główny model generacji), Amazon Titan Embeddings i Bedrock Knowledge Bases dla zarządzanego RAG.

Argument compliance dla Bedrocka jest znaczący w naszej branży: dane pozostają w naszym regionie AWS, umowa serwisowa pasuje do naszych wymagań kontekstu ubezpieczeniowego, a integracja IAM oznacza, że nie zarządzamy oddzielnymi kluczami API dla dostępu do modeli. Dla firm w regulowanych branżach, to ma takie samo znaczenie jak jakość modelu.

### 2. LightRAG — Retrieval Oparty na Grafie

LightRAG zarabia swoje miejsce w naszym stosie specjalnie dla retrieval dokumentów ubezpieczeniowych — złożonych, cross-referencyjnych dokumentów, gdzie wyszukiwanie semantyczne osiąga sufit jakości. Dla 40% naszych typów zapytań, LightRAG zapewnia o 20-30 punktów procentowych lepszą dokładność retrieval niż standardowe wyszukiwanie wektorowe.

Wiąże się ze znaczącym overhead operacyjnym, dlatego nie używamy go wszędzie. Ale dla przypadków użycia, gdzie ma znaczenie, jest niezastąpiony.

### 3. RAGAS — Framework Ewaluacji

Ewaluacja jakości RAG to nieefektowna infrastruktura, która decyduje o tym, czy Twój system naprawdę się poprawia, czy tylko czujesz, że się poprawia.

RAGAS zapewnia automatyczne metryki używające podejść LLM-as-judge: precyzja kontekstu (czy pobrana treść jest odpowiednia?), recall kontekstu (czy wszystkie odpowiednie fragmenty są pobierane?), wierność (czy odpowiedź jest wsparta przez pobraną treść?), i trafność odpowiedzi (czy odpowiedź adresuje pytanie?).

Uruchamiamy oceny RAGAS co tydzień względem naszego zestawu testowego i śledzimy metryki w naszym dashboardzie inżynierskim. Kiedy metryki degradują, badamy przed wdrożeniem zmian do produkcji. To dwukrotnie wychwytywało regresje jakości, które inaczej by trafiły do wysyłki.

### 4. LangSmith — Obserwowalność LLM

Debugowanie wieloetapowych pipeline'ów LLM bez obserwowalności to archeologia — wnioskujesz z artefaktów zamiast widzieć, co się stało.

LangSmith śledzi każde wywołanie LLM: wejścia, wyjścia, pośrednie kroki, latencję i koszt. Dla pipeline'u agentic z pięcioma lub sześcioma krokami rozumowania, ta widoczność jest niezbędna. Używaliśmy go do identyfikacji problemów z promptem, nieoczekiwanego zachowania modelu i skoków kosztów z nieefektywnych wzorców wywołań.

### 5. pgvector na PostgreSQL — Wyszukiwanie Wektorowe dla Prostszych Przypadków

pgvector dodaje wyszukiwanie podobieństwa wektorowego do PostgreSQL. Używamy go dla przypadków użycia, które nie uzasadniają złożoności operacyjnej OpenSearch Serverless lub dedykowanej bazy danych wektorów.

Sufit wydajności jest realny — przy milionach wektorów z wysokim obciążeniem zapytań, będziesz chciał dedykowany vector store. Ale dla wewnętrznych narzędzi, funkcji o niższym wolumenie zapytań i środowisk deweloperskich, pgvector oznacza, że odpytujemy wektory w tej samej infrastrukturze bazy danych, której używamy do wszystkiego innego.

### 6. Bielik — Polski LLM

Bielik to open-source polski LLM trenowany na polskojęzycznych danych. Używamy go głównie do embeddowania polskich dokumentów ubezpieczeniowych, gdzie przewyższa modele wielojęzyczne w precyzji terminologii — konkretnie o 12 punktów procentowych lepszą precyzję retrieval na zapytaniach specyficznych dla polskich ubezpieczeń.

To jest wąski, ale ważny przypadek użycia dla nas. Jeśli Twoje systemy są głównie anglojęzyczne, nie będziesz go potrzebować. Jeśli przetwarzasz polskie dokumenty i zależy Ci na precyzji terminologii — ubezpieczenia, prawo, finanse — warto go ocenić.

### 7. Claude Code / Cursor — Wspomagane AI Tworzenie

Oba używane do różnych celów. Claude Code dla terminalowego, świadomego codebase asystowania. Cursor dla generowania i edytowania kodu w IDE.

Argument produktywności jest realny: generowanie boilerplate'u, pisanie przypadków testowych, tworzenie dokumentacji. Argument osądu też jest realny: żadne narzędzie nie zastępuje myślenia architektonicznego, dyscypliny code review ani wiedzy domenowej, która sprawia, że kod produkcyjny jest godny zaufania.

## Co Nie Trafiło na Listę

**Pinecone**: Doskonała zarządzana baza danych wektorów z silną wydajnością. Ale koszt w naszej skali, połączony z dodatkową relacją z dostawcą i przeglądem compliance, nie uzasadniał przewagi wydajności nad pgvector przy naszym obecnym wolumenie zapytań.

**Weaviate**: Silna opcja open-source z doskonałą obsługą multi-tenancy. Ale złożoność operacyjna self-hostingu przekraczała wartość dla naszego przypadku użycia, gdy Bedrock Knowledge Bases pokrywał większość naszych potrzeb.

**LangChain jako główna orkiestracja**: Używamy komponentów LangChain (ładowarki dokumentów, dzielniki tekstu, niektóre łańcuchy), ale usunęliśmy go jako główną warstwę orkiestracji w większości naszych pipeline'ów. Abstrakcja zasłaniała to, co się dzieje w sposób, który utrudniał debugowanie.

## Podsumowanie

Najlepszy stos AI dev to ten, który pasuje do rzeczywistych ograniczeń Twojego zespołu — technicznych, operacyjnych, compliance i kosztowych. Optymalizowanie pod stos benchmarkowy lub stos z prezentacji konferencyjnych zamiast Twoich ograniczeń to sposób, w jaki zespoły kończą ze złożoną infrastrukturą, której nie mogą utrzymać.

Zacznij prosto. Dodawaj złożoność kiedy zmierzyłeś na nią potrzebę. Usuwaj rzeczy, które nie zarabiają na swoje miejsce. I przeglądaj stos co sześć miesięcy, bo krajobraz narzędzi zmienia się wystarczająco szybko, że zeszłoroczny najlepszy wybór może nie być tegorocznym.

Co masz w swoim stosie? Jestem szczególnie ciekaw narzędzi w kategorii ewaluacji i obserwowalności — to miejsce, gdzie widziałem największą wariancję w podejściach zespołów do problemu.
