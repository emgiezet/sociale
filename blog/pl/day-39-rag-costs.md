---
day: 39
title: "Realne koszty RAG w produkcji: trzy architektury, trzy modele kosztowe"
pillar: Educator
language: pl
image: ../../images/day-39.jpg
image_unsplash_query: "cloud computing costs infrastructure billing dashboard"
---

# Realne koszty RAG w produkcji: trzy architektury, trzy modele kosztowe

Każdy tutorial RAG kończy się działającym demo. Żaden nie wspomina ile kosztuje uruchomienie tego demo przy 10 000 zapytań miesięcznie. Ani przy 200 000.

Zbudowałem i uruchamiam trzy systemy RAG w produkcji w Insly — europejskim InsurTech SaaS obsługującym 150 000+ użytkowników z 15-osobowym zespołem inżynierów. W tym artykule opisuję realne koszty trzech różnych architektur RAG, z prawdziwymi liczbami, ukrytymi kosztami i analizą break-even, którą większość zespołów buduje zbyt późno.

Kontrowersyjne twierdzenie na wstępie: self-hosted RAG jest często droższy niż managed. Szczególnie przez pierwszy rok.

## Składowe kosztów systemu RAG

Zanim porównamy architektury, zmapujmy co faktycznie kosztuje. System RAG ma cztery warstwy kosztów:

1. **Osadzanie (embedding):** Przekształcanie tekstu w wektory (zarówno przy indeksowaniu, jak i przy zapytaniu)
2. **Przechowywanie i wyszukiwanie wektorów:** Baza danych przechowująca i przeszukująca osadzenia
3. **Generacja:** LLM produkujący końcową odpowiedź na podstawie wyszukanego kontekstu
4. **Narzut operacyjny:** Czas inżyniera, monitorowanie, ewaluacja, iteracja

Warstwa 4 to prawdziwe pieniądze. Po prostu nie ma jej w żadnym kalkulatorze cenowym.

## Architektura 1: AWS Bedrock (w pełni zarządzana)

To opcja "najniższy narzut operacyjny". AWS Bedrock zapewnia zarządzane osadzanie (Amazon Titan Embed), zarządzane przechowywanie wektorów (OpenSearch Serverless przez Bedrock Knowledge Base) i zarządzaną inferencję LLM (Claude Sonnet, Llama, Titan).

**Koszty składowych przy 10 000 zapytań/miesiąc:**

| Składowa | Cena jednostkowa | Wolumen miesięczny | Koszt miesięczny |
|---|---|---|---|
| Titan Embed v2 (indeksowanie, jednorazowe) | $0.02/1M tokenów | Zmienny (zależy od rozmiaru korpusu) | ~$2–5 jednorazowo |
| Titan Embed v2 (zapytania) | $0.02/1M tokenów | 10k zapytań × ~50 tokenów śr. | ~$0.10 |
| OpenSearch Serverless (OCU) | ~$0.24/OCU-godz. | Minimum 2 OCU | ~$350/miesiąc |
| Generacja Claude Sonnet | $3/1M wejście + $15/1M wyjście | 10k × (500 wejście + 300 wyjście) | ~$49 |
| Żądania Bedrock Knowledge Base | $0.000004/żądanie | 10 000 żądań | ~$0.04 |

**Łącznie przy 10 000 zapytań/miesiąc: szacunkowo ~$400/miesiąc**

Chwila — $350 za OpenSearch Serverless? Tak. OpenSearch Serverless ma minimum 2 OCU (OpenSearch Compute Units) na kolekcję, po $0.24/OCU-godz. To $172.80/miesiąc za OCU, minimum $345.60/miesiąc tylko za magazyn wektorów, zanim wykonałeś choć jedno zapytanie.

To jest największy ukryty koszt w stosie AWS Bedrock. Dla małych wdrożeń płacisz za pojemność, której nie używasz.

**Łagodzenie:** Do developmentu i małoskalowych wdrożeń używaj OpenSearch Serverless tylko gdy potrzebujesz pełnej integracji Bedrock Knowledge Base. Dla mniejszych obciążeń alternatywą jest zewnętrzna baza wektorowa (Pinecone, Qdrant, pgvector) z Bedrock tylko dla osadzania i generacji.

**Poprawione szacunki używając Bedrock tylko dla LLM + osadzania, zewnętrzna baza wektorowa:**

| Składowa | Koszt miesięczny |
|---|---|
| Titan Embed v2 (zapytania, 10k zapytań) | ~$0.10 |
| Qdrant Cloud (warstwa bezpłatna lub podstawowa) | $0–$25 |
| Generacja Claude Sonnet (10k zapytań) | ~$49 |
| **Łącznie** | **~$50–75/miesiąc** |

To jest znacznie rozsądniejsza liczba dla systemów we wczesnej fazie. Skaluj do 50k zapytań: ~$200–250/miesiąc. Skaluj do 200k zapytań: ~$750–900/miesiąc.

**Przy 200k zapytań/miesiąc sam koszt generacji Bedrock to ~$1 000/miesiąc.** To jest moment gdy rozmowa o self-hosted zaczyna mieć sens.

## Architektura 2: Self-hosted GPU (Mistral lub Bielik)

Uruchomienie własnego LLM eliminuje koszt generacji per token. Kompromisem jest stały koszt infrastruktury i narzut inżynierski.

**Opcje infrastruktury GPU:**

| Typ instancji | GPU | On-demand $/godz. | Reserved $/godz. (szac.) | Miesięcznie (reserved) |
|---|---|---|---|---|
| p3.2xlarge | V100 16GB | $3.06 | ~$1.50 | ~$1 080 |
| p4d.24xlarge | 8× A100 40GB | $32.77 | ~$15 | ~$10 800 |
| g5.2xlarge | A10G 24GB | $1.21 | ~$0.60 | ~$432 |

Dla Mistral 7B lub Bielik 7B, A10G (g5.2xlarge) wystarczy do umiarkowanej przepustowości. Dla Mistral 13B lub Bielik 13B przy produkcyjnym obciążeniu potrzebujesz minimum V100 lub A100.

**Pełny model kosztowy dla self-hosted (g5.2xlarge, Mistral 7B):**

| Składowa | Koszt miesięczny |
|---|---|
| Instancja GPU (g5.2xlarge, reserved) | ~$432 |
| Przechowywanie modelu (EBS, 20GB) | ~$2 |
| Baza wektorowa (Qdrant, self-hosted EC2 c5.xlarge) | ~$140 |
| Osadzanie (self-hosted lub API) | ~$5–30 |
| Narzut inżynierski (0.3 FTE @ $10k/miesiąc koszt FTE) | ~$3 000 |
| **Łącznie (bez narzutu inż.)** | **~$580/miesiąc** |
| **Łącznie (z szacunkiem narzutu inż.)** | **~$3 580/miesiąc** |

Liczba narzutu inżynierskiego jest ważna. Ktoś musi wdrożyć model, skonfigurować vLLM lub TGI do serwowania, ustawić autoskalowanie, monitorować latencję inferencji, obsługiwać aktualizacje modelu i debugować awarie serwowania o 2 w nocy. Przy 0.3 FTE doświadczonego inżyniera ML — to nie jest trywialny koszt.

**Koszt per token przy skali:** Gdy GPU jest opłacone, dodatkowe tokeny są w zasadzie darmowe. Przy 200k zapytań/miesiąc z 800 tokenami generacji na zapytanie, koszt generacji to koszt GPU podzielony przez przepustowość — około $0.003–0.010 na zapytanie na reserved A10G, w zależności od efektywności batchowania.

**Break-even vs zarządzane API:**

| Zapytania miesięczne | Bedrock (tylko Claude Sonnet) | Self-hosted (g5.2xlarge + 0.3 FTE) | Self-hosted tańszy? |
|---|---|---|---|
| 10 000 | ~$50 | ~$3 580 | Nie |
| 50 000 | ~$240 | ~$3 590 | Nie |
| 200 000 | ~$960 | ~$3 620 | Nie |
| 500 000 | ~$2 400 | ~$3 650 | Na granicy |
| 1 000 000 | ~$4 800 | ~$3 700 | Tak |

Te liczby ilustrują kluczowy wniosek: **jeśli uwzględnisz realistyczny narzut inżynierski, self-hosted nie osiąga break-even dopóki nie przekroczysz 500k–1M zapytań/miesiąc.** Większość zespołów budujących swój pierwszy system RAG nie osiąga tego wolumenu w pierwszym roku.

**Kiedy self-hosted jest naprawdę właściwym wyborem:**
- Wymóg compliance: dane nie mogą opuszczać Twojej infrastruktury (typowe w europejskich regulowanych branżach)
- Wolumen powyżej 500k zapytań/miesiąc konsekwentnie
- Wymóg latencji: odpowiedź poniżej 500ms, a round-trip API plus limity przepustowości są wąskim gardłem
- Specyficzny wymóg modelu: potrzebujesz Bielika dla precyzji w języku polskim i nie ma zarządzanego API dla niego

## Architektura 3: Hybrydowa (self-hosted wyszukiwanie + zarządzana generacja)

Środkowa ścieżka: własna baza wektorowa i infrastruktura wyszukiwania (pełna kontrola nad chunkingiem, metadanymi, rerankingiem), ale zarządzane API dla generacji LLM.

**Model kosztowy:**

| Składowa | Koszt miesięczny |
|---|---|
| EC2 c5.xlarge (Qdrant self-hosted) | ~$140 |
| Titan Embed v2 lub Cohere Embed (10k zapytań) | ~$0.50–2 |
| Claude Sonnet przez Bedrock (10k zapytań) | ~$49 |
| Reranking (Cohere Rerank API, opcjonalnie) | ~$10–40 |
| Narzut inżynierski (0.1 FTE) | ~$1 000 |
| **Łącznie (bez narzutu inż.)** | **~$190–230/miesiąc** |
| **Łącznie (z szacunkiem narzutu inż.)** | **~$1 190–1 230/miesiąc** |

Podejście hybrydowe daje Ci kontrolę nad warstwą wyszukiwania — możesz używać niestandardowego chunkingu, filtrowania metadanych, wyszukiwania hybrydowego (wektor + BM25) i zaawansowanego rerankingu — bez kosztu self-hostowania LLM.

To nasza preferowana architektura dla wdrożeń średniej skali, gdzie jakość wyszukiwania liczy się bardziej niż koszt generacji, i gdzie compliance pozwala na użycie zarządzanego API LLM.

## Koszty, które nie pojawiają się na stronach cenowych

Koszty tokenów są widoczne. Te koszty są realne, ale niewidoczne:

**Koszty ewaluacji.** Uruchomienie złotego zestawu testowego do pomiaru faithfulness i recall kosztuje pieniądze. Przy 100 zapytaniach testowych, z 2 wywołaniami LLM na ewaluację (generacja + LLM-as-judge), przy 1 000 tokenach na wywołanie, przy $18/1M tokenów łącznie: każde uruchomienie ewaluacji kosztuje ~$3.60. Uruchamiasz to przy każdej istotnej zmianie. Przy 3–5 uruchomieniach tygodniowo podczas aktywnego developmentu — $50–90/miesiąc.

**Koszty reindeksowania.** Gdy zmienisz strategię chunkingu (a zmienisz), re-osadzasz i reindeksujesz cały korpus. Dla korpusu 100k dokumentów przy 500 tokenach na chunk, 2 chunkach na dokument: 100M tokenów × $0.02/1M = $2. Brzmi niewiele dopóki nie reindeksujesz co tydzień.

**Reranking.** Dodanie rerankera (Cohere Rerank, lub cross-encoder na małym GPU) dodaje latencję i koszt do każdego zapytania. Cohere Rerank API: $1/1k zapytań = $10 przy 10k zapytań. Tanio, ale dodaje 100–200ms latencji p50.

**Monitorowanie i logowanie.** Przechowywanie logów zapytań, wyszukanych chunków i wygenerowanych odpowiedzi do debugowania i compliance: koszty S3, CloudWatch lub ekwiwalentne. Małe indywidualnie, nietrywialnie przy skali.

**Cykl iteracji.** Większość zespołów znacząco zmienia swój pipeline RAG 3–5 razy w pierwszych sześciu miesiącach. Każda zmiana wymaga ewaluacji, reindeksowania i redeploymentu. Osoba robiąca to jest inżynierem. Jej czas jest największym kosztem.

## Co uruchamiamy w Insly

Nasz główny pipeline to architektura hybrydowa: Qdrant (self-hosted na EC2) do wyszukiwania, Claude Sonnet przez AWS Bedrock do generacji. Daje nam to kontrolę nad chunkingiem i logiką wyszukiwania przy zachowaniu zarządzanego LLM.

Przy naszym obecnym wolumenie kosztuje to szacunkowo $400–600/miesiąc w kosztach infrastruktury i API. Realny koszt, gdy uwzględnisz czas inżyniera do jego utrzymania, jest wyższy — ale ten koszt jest rozłożony na trzy systemy RAG, nie tylko jeden.

Decyzja o pozostaniu przy zarządzanym LLM (nie self-hostowaniu modelu generacji) była podyktowana compliance i prostotą, nie kosztem. Przy naszym wolumenie koszt API jest do opanowania. Gdy przestanie być — mamy Bielika gotowego do ewaluacji.

## Tabela podsumowująca

| Architektura | 10k zapytań/mies. | 50k zapytań/mies. | 200k zapytań/mies. | Narzut ops |
|---|---|---|---|---|
| AWS Bedrock (pełny) | ~$400 | ~$800 | ~$2 000 | Bardzo niski |
| AWS Bedrock (LLM + osadzania, zewn. baza wekt.) | ~$75 | ~$250 | ~$950 | Niski |
| Self-hosted (A10G, 0.3 FTE) | ~$3 600 | ~$3 620 | ~$3 650 | Wysoki |
| Hybrydowy (zewn. baza wekt. + zarządzany LLM) | ~$200 | ~$450 | ~$1 200 | Średni |

Wszystkie koszty szacunkowe. Zweryfikuj aktualne ceny przed decyzjami architektonicznymi. Narzut inżynierski szacowany przy $10k/miesiąc koszt FTE — dostosuj do swojego rynku.

---

*Dzień 39 serii RAG Deep Dive. W przyszłym tygodniu: RAG Masterclass — zaawansowane techniki wyszukiwania. Zaczynamy od HyDE: wypełnianie semantycznej luki między pytaniami użytkowników a językiem dokumentów.*
