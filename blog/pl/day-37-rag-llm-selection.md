---
day: 37
title: "Wybór LLM do RAG-a: jak wybrać model na podstawie swoich danych, nie benchmarków"
pillar: Educator
language: pl
image: ../../images/day-37.jpg
image_unsplash_query: "comparison chart decision making technology models"
---

# Wybór LLM do RAG-a: jak wybrać model na podstawie swoich danych, nie benchmarków

Kiedy zaczęliśmy budować systemy RAG w Insly — europejskim InsurTech SaaS — nasze rozwiązania AI przetwarzają ponad 150 000 dokumentów miesięcznie — nasz proces wyboru LLM wyglądał jak u większości zespołów: wchodzimy na leaderboard, sortujemy po MMLU, bierzemy top 3, testujemy na demo pytaniach. GPT-4o wygrał. Decyzja podjęta.

Trzy miesiące później zaczęliśmy zadawać właściwe pytania.

Nie "który model jest globalnie najlepszy?" — tylko "który model jest najlepszy na naszych danych, w naszym języku, przy naszym wolumenie zapytań, w ramach naszych wymogów compliance?" Ta zmiana perspektywy brzmi banalnie. Ale zmienia każdą decyzję downstream.

Ten artykuł to porównanie, które chciałbym mieć zanim zaczęliśmy.

## Dlaczego benchmarki kłamią

MMLU, HellaSwag, HumanEval, MATH — to są dobre benchmarki. Mierzą realne rzeczy. Czego nie mierzą, to jak model poradzi sobie z paragrafem z polskiej polisy ubezpieczeniowej napisanej w 2009 roku, wyekstrahowanej niedoskonale z dziesięcioletniego pliku Word, po podziale na chunki przez tokenizer, który nie uwzględnił polskich wyrazów złożonych.

Przepaść między warunkami benchmarkowania a warunkami produkcyjnymi jest ogromna. A przepaść językowa jest jeszcze większa, gdy Twoje dokumenty nie są po angielsku.

Budujemy systemy przetwarzające dokumenty ubezpieczeniowe z wielu europejskich rynków. Model, który osiąga 85% na MMLU, ale produkuje płynne halucynacje przy rozumowaniu o klauzulach regresowych w języku polskim — nie jest dobrym modelem dla naszego przypadku użycia.

Jedynym benchmarkiem, który ma znaczenie, jest Twój własny zestaw ewaluacyjny.

## Cztery modele, które przetestowałem

Przeprowadziłem ustrukturyzowane porównanie na zbiorze testowym 80 realnych zapytań ubezpieczeniowych — pytań, które nasi użytkownicy faktycznie zadają lub będą zadawać, z odpowiedziami referencyjnymi zaczerpniętymi z naszych dokumentów polis. Oto co znalazłem.

### Claude Sonnet 3.5 / Claude Sonnet (przez AWS Bedrock)

**Cena:** ~$3/1M tokenów wejściowych, ~$15/1M tokenów wyjściowych (opublikowane ceny Bedrock)

**Okno kontekstu:** 200k tokenów

**Latencja p95:** ~2.1s dla typowych odpowiedzi RAG (~300 tokenów na wyjściu)

**Wsparcie języka polskiego:** Dobre. Nie idealne — sporadycznie niezgrabne sformułowania przy bardzo formalnym tekście prawniczym — ale konsekwentnie rozumiał kontekst i produkował spójne polskie odpowiedzi.

**Historia compliance:** Natywny deployment AWS. Dane pozostają w Twoim VPC. Dla europejskich klientów ubezpieczeniowych znacząco upraszcza to rozmowę o RODO. Dla nas był to istotny wyróżnik.

**Nasza ewaluacja:** Wynik faithfulness 0.87, answer relevance 0.84. Nieznacznie poniżej GPT-4o pod względem surowej jakości, ale kombinacja compliance i ceny sprawiła, że jest naszym podstawowym wyborem dla pipeline'u opartego na AWS Bedrock.

### GPT-4o (OpenAI API)

**Cena:** ~$5/1M tokenów wejściowych, ~$15/1M tokenów wyjściowych (opublikowane ceny OpenAI)

**Okno kontekstu:** 128k tokenów

**Latencja p95:** ~1.8s dla podobnych odpowiedzi

**Wsparcie języka polskiego:** Doskonałe. Najlepsze ze wszystkich zarządzanych API, które testowaliśmy na polskich tekstach prawnych i ubezpieczeniowych.

**Historia compliance:** Bardziej skomplikowana dla europejskich klientów enterprise. Tier enterprise OpenAI i umowy o przetwarzaniu danych pomagają, ale pytanie "czy dane opuszczają UE?" pojawia się w każdej rozmowie sprzedażowej z enterprise. Nie jest to bloker, ale generuje overhead.

**Nasza ewaluacja:** Wynik faithfulness 0.91, answer relevance 0.88. Najlepsza surowa jakość w kategorii zarządzanych API.

### Mistral Medium (Mistral API)

**Cena:** szacunkowo ~$0.4/1M tokenów wejściowych, ~$1.2/1M tokenów wyjściowych (szacunek na podstawie opublikowanych progów cenowych Mistral)

**Okno kontekstu:** 32k tokenów

**Latencja p95:** ~1.2s

**Wsparcie języka polskiego:** Wystarczające dla treści technicznych, słabsze na formalnym prawniczym polskim. Sporadyczne sformułowania "tłumaczeniowe", które nie odpowiadają temu, jak Polacy faktycznie piszą dokumenty ubezpieczeniowe.

**Historia compliance:** Mistral to firma francuska z opcją rezydencji danych w UE — realna przewaga nad OpenAI dla europejskich regulowanych branż.

**Nasza ewaluacja:** Wynik faithfulness 0.78, answer relevance 0.76. Znacząca przepaść jakości vs Claude/GPT-4o na naszej domenie. Jednak stosunek jakości do ceny jest najlepszy ze wszystkich zarządzanych API, jeśli wymagania językowe są mniej rygorystyczne.

### Bielik (self-hosted)

Bielik to open-source'owy model języka polskiego rozwijany w ramach projektu SpeakLeash, specjalnie trenowany na polskich tekstach. Uruchomiliśmy go na własnej instancji GPU (A100 40GB).

**Cena za token:** Efektywnie zero gdy GPU działa. Koszt leży w infrastrukturze.

**Okno kontekstu:** 8k tokenów (wcześniejsze wersje) — to realne ograniczenie

**Latencja p95:** ~1.4s na A100 (silnie zależna od batchowania i sprzętu)

**Wsparcie języka polskiego:** Wyjątkowe na polskich tekstach ubezpieczeniowych. Do tego właśnie był budowany.

**Historia compliance:** Perfekcyjna — dane nigdy nie opuszczają Twojej infrastruktury.

**Nasza ewaluacja:** Na naszym zbiorze dokumentów ubezpieczeniowych, Bielik przewyższył Mistral Medium o **12 punktów procentowych precyzji** na pytaniach dotyczących polskich klauzul i terminologii. Był w odległości 5pp od Claude Sonnet na naszym zbiorze ewaluacyjnym. To niezwykły wynik dla modelu open-source.

Haczyk tkwi w wszystkim pozostałym.

## Ukryte koszty self-hostingu

Koszt Bielika za token wynosi zero. Koszt operacyjny — nie.

Uruchomienie modelu w produkcji wymaga:

- **Infrastruktura GPU:** Instancja A100 na AWS (p4d.24xlarge) kosztuje szacunkowo $32/godz. on-demand lub ~$15/godz. w reserved. Miesięcznie: $10 800–$23 000 w zależności od zarezerwowanej pojemności.
- **Overhead inżynierski:** Deployment modelu, optymalizacja inferencji, autoskalowanie, monitorowanie, aktualizacje. Szacujemy 0.5 FTE żeby robić to porządnie.
- **Infrastruktura przechowywania i serwowania:** Wagi modelu (~14GB dla Bielika 13B), framework serwowania (vLLM, TGI), load balancer, health checks.

Przy 10 000 zapytań miesięcznie self-hosting kosztuje dramatycznie więcej niż zarządzane API. Przy 200 000 zapytań miesięcznie z generowaniem odpowiedzi ~500 tokenów, koszty zarządzanego API zaczynają boleć.

**Punkt break-even** między self-hosted a managed zależy silnie od architektury, ale dla większości zespołów wynosi gdzieś 50 000–100 000 zapytań miesięcznie. Większość zespołów budujących swój pierwszy system RAG nie osiąga tej liczby w pierwszym roku.

## Tabela porównawcza

| Model | Wejście $/1M | Wyjście $/1M | Kontekst | Polski | Compliance |
|---|---|---|---|---|---|
| Claude Sonnet (Bedrock) | $3 | $15 | 200k | Dobry | AWS VPC, GDPR-friendly |
| GPT-4o | $5 | $15 | 128k | Doskonały | Tier enterprise wymagany |
| Mistral Medium | ~$0.4* | ~$1.2* | 32k | Wystarczający | Opcja rezydencji danych EU |
| Bielik (self-hosted) | $0/token | $0/token | 8k | Wyjątkowy | Pełna kontrola |

*Szacunkowo na podstawie opublikowanych poziomów cenowych z początku 2026. Zweryfikuj przed podjęciem decyzji.

## Jak faktycznie ewaluować modele na swoich danych

Oto proces ewaluacji, którego używamy. Trwa 2–3 dni żeby go skonfigurować; oszczędza tygodnie złych decyzji.

**Krok 1: Zbuduj złoty zestaw testowy.**
Weź 50–100 realnych zapytań ze swojego systemu — pytania, które użytkownicy faktycznie zadali lub zadadzą. Dla każdego napisz oczekiwaną odpowiedź i oznacz chunk źródłowy w korpusie dokumentów, który powinien zostać wyszukany.

**Krok 2: Uruchom pełny pipeline RAG dla każdego modelu.**
Nie ewaluuj samej generacji w izolacji. Uruchom pełny pipeline: zapytanie → wyszukiwanie → budowa kontekstu → generacja → odpowiedź. Izoluj modele tylko żeby osobno zrozumieć jakość generacji.

**Krok 3: Mierz to, co ważne.**

- **Faithfulness (wierność):** Czy odpowiedź pozostaje w granicach wyszukanego kontekstu, czy model wprowadza informacje spoza dokumentów? (Użyj RAGAS lub własnego setupu LLM-as-judge)
- **Answer relevance (trafność odpowiedzi):** Czy odpowiedź faktycznie adresuje zadane pytanie?
- **Recall wyszukiwania:** Czy chunki referencyjne pojawiają się w top-5 wyszukanych wynikach? (Ewaluuj wyszukiwanie osobno — często wąskim gardłem jest tam, nie w generacji)

**Krok 4: Zmierz latencję pod realistycznym obciążeniem.**
Latencja pojedynczego zapytania jest bez znaczenia. Liczy się latencja p95 gdy 10 użytkowników zapytuje jednocześnie. To często ujawnia, że najtańsze API staje się drogie po doliczeniu obsługi timeoutów i retry.

## Framework decyzyjny

Zadaj te pytania po kolei:

1. **Wolumen:** Mniej niż 50k zapytań miesięcznie? Użyj zarządzanego API. Więcej? Zacznij modelować break-even dla self-hosted.
2. **Język:** Dużo polskiego lub innego nieangielskiego europejskiego języka? Bielik lub Claude Sonnet przewyższają modele ogólne. Nie przeocz tego.
3. **Compliance:** Regulowana branża, europejscy klienci, wrażliwe dane? AWS Bedrock (Claude) lub Mistral EU uprości rozmowy z prawnikami.
4. **Długość kontekstu:** Czy Twoje dokumenty wymagają okien kontekstu >32k tokenów? GPT-4o lub Claude Sonnet. Mistral Medium i Bielik mają tu realne ograniczenia.
5. **Dolna granica jakości:** Uruchom swój zestaw ewaluacyjny. Jeśli faithfulness spada poniżej 0.80 lub answer relevance poniżej 0.75, ten model nie jest gotowy do produkcji dla Twojego przypadku użycia — niezależnie od ceny.

Model wygrywający na benchmarkach prawie nigdy nie wygrywa na wszystkich pięciu wymiarach jednocześnie. Dlatego ewaluujesz na swoich danych, nie na leaderboardach.

## Co ostatecznie wybraliśmy

Nasz główny system produkcyjny używa Claude Sonnet przez AWS Bedrock. Historia compliance, okno kontekstu i ogólny stosunek jakości do ceny przy naszym obecnym wolumenie sprawiły, że był oczywistym wyborem.

Bielika uruchamiamy w pomocniczym pipeline dla specyficznego podzbioru zapytań w języku polskim, gdzie precyzja liczy się bardziej niż koszt lub latencja. Ten wzrost precyzji o 12pp na polskich klauzulach ubezpieczeniowych jest realny i wart overhead infrastruktury dla tego przypadku użycia.

GPT-4o jest w naszym pipeline ewaluacyjnym jako wzorzec odniesienia — używamy go do generowania odpowiedzi referencyjnych przy budowaniu nowych złotych zbiorów testowych, bo jakość jego odpowiedzi na złożone rozumowanie jest wciąż najlepsza, jaką testowaliśmy.

"Właściwy" model zmienia się w miarę jak rośnie Twój wolumen i jak same modele się poprawiają. Zbuduj system ewaluacyjny, który pozwoli Ci ponownie uruchamiać porównania co kwartał. Krajobraz zmienia się zbyt szybko dla jednorazowej decyzji.

---

*Dzień 37 serii RAG Deep Dive. Jutro: strategie chunkingu — dlaczego problem wyszukiwania to w większości problem przygotowania danych.*
