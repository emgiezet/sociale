# Day 15 — Builder: Polish RAG with Bielik (Polish + English)
**Pillar:** Builder | **Week:** 3 | **CTA:** Follow

---

## LinkedIn Post (Polish 🇵🇱)

Zbudowaliśmy system RAG po polsku, używając modeli Bielik.
Oto co odkryliśmy.

Większość systemów RAG dla polskich firm działa tak: dokument po polsku → tłumaczenie na angielski → embedding → retrieval → odpowiedź po angielsku → tłumaczenie z powrotem. To działa. Ale traci niuanse, spowalnia pipeline i zwiększa koszty.

Postanowiliśmy to zrobić inaczej.

W Insly przetwarzamy dokumenty ubezpieczeniowe w języku polskim — polisy, klauzule, endorsementy. Przetestowaliśmy modele Bielik (polskie LLM trenowane na polskim korpusie) zarówno do embeddingów jak i do generacji.

Co zadziałało:
→ Bielik embedding znacznie lepiej odwzorowuje polskie frazy ubezpieczeniowe niż anglojęzyczne modele
→ Generacja po polsku jest bardziej naturalna i terminologicznie precyzyjna
→ Pipeline bez tłumaczenia jest szybszy i tańszy

Co było trudne:
→ Bielik jest mniejszy niż Claude — wymagał więcej prompt engineeringu dla złożonych zapytań
→ Evaluation dataset w języku polskim wymagał zaangażowania polskojęzycznych ekspertów domenowych
→ Fine-tuning na polskich dokumentach ubezpieczeniowych to osobny projekt

Wynik: na naszym zbiorze testowym pytań o polskie dokumenty ubezpieczeniowe, Bielik pipeline osiągnął lepszą jakość odpowiedzi niż pipeline tłumaczenie-angielski-tłumaczenie.

**Polska scena AI ma do zaoferowania coś, czego globalnie jest mało: native Polish LLM expertise w produkcyjnych systemach enterprise.**

Budujesz systemy AI z polskojęzyczną treścią? Napisz — chętnie podzielę się szczegółami.

#BielikLLM #RAG #PolishAI #InsurTech #AIEngineering

---

## LinkedIn Post (English)

We built a Polish-language RAG system using Bielik models.
Here's what we found.

Most RAG systems for Polish companies work like this: Polish document → translate to English → embed → retrieve → answer in English → translate back. This works. But it loses nuance, slows the pipeline, and increases cost.

We did it differently.

At Insly, we process insurance documents in Polish — policies, clauses, endorsements. We tested Bielik models (Polish LLMs trained on Polish corpus data) for both embeddings and generation.

What worked:
→ Bielik embeddings significantly better captured Polish insurance terminology than English models
→ Generation in native Polish is more natural and terminologically precise
→ Pipeline without translation layer is faster and cheaper

What was hard:
→ Bielik is smaller than Claude — required more careful prompt engineering for complex queries
→ Building a Polish evaluation dataset required Polish-speaking domain experts
→ Fine-tuning on Polish insurance documents is a separate project in itself

Result: on our test set of questions about Polish insurance documents, the Bielik-native pipeline outperformed the translate-to-English-and-back approach on answer quality metrics.

**The Polish AI ecosystem has something rare globally: native Polish LLM capability for enterprise production systems.**

Building AI systems with Polish-language content? Reach out — happy to share architecture details.

#BielikLLM #RAG #PolishAI #InsurTech #AIEngineering

---

## Blog Post (Polish 🇵🇱)

### Jak Zbudowaliśmy Polski System RAG dla Dokumentów Ubezpieczeniowych

Kiedy zaczęliśmy budować systemy RAG w Insly, stanęliśmy przed pytaniem, które większość polskich firm technologicznych ignoruje: czy naprawdę musimy tłumaczyć wszystko na angielski?

Standardowy pipeline dla polskojęzycznych dokumentów w większości firm wygląda tak: polski dokument → przekład na angielski (Amazon Translate lub DeepL) → angielski embedding → angielskie retrieval → angielska generacja → przekład odpowiedzi z powrotem na polski. To rozwiązanie funkcjonuje. Ale ma konkretne wady.

#### Dlaczego Tłumaczenie To Za Mało

Polska terminologia ubezpieczeniowa jest specyficzna. Terminy takie jak "ubezpieczenie mienia", "klauzula franszyzy redukcyjnej", "ubezpieczenie odpowiedzialności cywilnej deliktowej" mają precyzyjne znaczenia prawne, które tłumaczenia maszynowe oddają niedokładnie lub niejednolicie.

Kiedy dokument przechodzi przez tłumaczenie przed embeddingiem, tracimy część sygnału semantycznego specyficznego dla polskiego prawa ubezpieczeniowego. Retrieval działa na angielskiej wersji dokumentu, nie na oryginalnym polskim tekście. Małe przekłamania w tłumaczeniu kumulują się na każdym etapie pipeline'u.

Postanowiliśmy przetestować alternatywę: native Polish pipeline oparty na modelach Bielik.

#### Czym Jest Bielik

Bielik to rodzina polskich modeli językowych trenowanych na dużym korpusie polskojęzycznym. Projekt jest rozwijany przez polską społeczność AI, a modele są dostępne open-source. Nie jest to GPT-4 ani Claude — modele są mniejsze i mają inne charakterystyki jakościowe. Ale dla polskojęzycznych zastosowań enterprise, rozmiar i koszt nie są jedynymi parametrami, które się liczą.

Przetestowaliśmy Bielik w dwóch rolach: jako model embeddingowy (konwersja tekstu na wektory) oraz jako model generatywny (produkcja odpowiedzi).

#### Wyniki Embeddingów

To był największy pozytywny wynik naszych testów. Bielik embeddingi dla polskich dokumentów ubezpieczeniowych były wyraźnie lepiej skalibrowane niż embeddingi anglojęzycznych modeli (Titan, Cohere) aplikowane do polskich dokumentów.

Konkretnie: dla zapytań używających polskiej terminologii ubezpieczeniowej, retrieval precision wzrósł o około 12 punktów procentowych w porównaniu z podejściem tłumaczenie-angielski-retrieval.

Hipoteza: polskie modele embeddingowe lepiej odwzorowują semantyczne relacje specyficzne dla polskiego języka prawnego i biznesowego, które globalne modele anglojęzyczne uczą się tylko częściowo.

#### Wyniki Generacji

Generacja z Bielik była bardziej mieszana. Dla prostych zapytań — "jaka jest wartość sumy ubezpieczenia w tej polisie?" — odpowiedzi były poprawne i naturalne. Dla złożonych zapytań wieloetapowych — "jak ta klauzula wchodzi w interakcję z ogólnymi warunkami ubezpieczenia w kontekście szkody z wodociągów?" — Claude 3.5 Sonnet (przez Bedrock) z przetłumaczonym kontekstem dawał lepsze wyniki.

Przyjęliśmy hybrydowe podejście: Bielik embeddingi + retrieval, Claude dla złożonej generacji. Pipeline bez pełnego tłumaczenia dokumentów źródłowych, ale z tłumaczeniem zapytań i odpowiedzi dla generatywnej warstwy.

#### Co To Znaczy Dla Polskiego Ekosystemu AI

Budowanie systemów AI dla polskiego enterprise bez polegania na tłumaczeniu jako workaround to realny kierunek. Wymaga:

→ Inwestycji w polskie modele embeddingowe i generatywne
→ Budowania polskojęzycznych datasetów ewaluacyjnych
→ Ekspertów domenowych mówiących po polsku do walidacji jakości

Polska społeczność AI buduje te zdolności. Bielik to dowód, że natywna polska AI nie jest akademickim projektem — to produkcyjne narzędzie.

---

## Blog Post (English)

### Building Native Polish-Language RAG: Architecture Decisions and Results

When we started building RAG systems at Insly, we faced a question most Polish tech companies skip: do we actually need to translate everything to English first?

The standard approach for Polish-language documents follows this pipeline: Polish source document → machine translation to English → English embedding → English retrieval → English generation → translated answer back to Polish. This works. But it has concrete costs.

#### The Translation Problem

Polish insurance terminology is precise in ways that matter legally. Terms like "ubezpieczenie odpowiedzialności cywilnej" (civil liability insurance) or "franszyza redukcyjna" (deductible clause) have specific legal meanings that machine translation handles with variable accuracy.

When documents pass through translation before embedding, we lose semantic signal specific to Polish legal and insurance language. Retrieval operates on the translated version, not the original. Small translation errors compound across pipeline stages.

We ran an experiment to test whether native Polish models could outperform the translate-first approach.

#### What We Tested

We tested Bielik — an open-source family of Polish LLMs trained on large Polish-language corpora — in two roles in our RAG pipeline:

1. As the embedding model, replacing Amazon Titan Embeddings or Cohere Embed
2. As the generation model, replacing Claude for producing final answers

Our evaluation set: 150 questions about Polish insurance policy documents, with expected answers validated by Polish-speaking insurance experts. This was the most labor-intensive part of the experiment, and the most important.

#### Embedding Results: Significant Win

For the embedding step, Bielik demonstrated clear advantages for Polish insurance content.

Retrieval precision on our evaluation set increased by approximately 12 percentage points compared to the translate-to-English-then-embed approach. The gains were most pronounced for queries using insurance-specific terminology — exactly the queries where translation errors or approximations are most consequential.

The hypothesis: models trained primarily on Polish text learn the semantic relationships between Polish legal and business terms more accurately than models trained primarily on English, even when those English models perform well on general Polish text.

This result was robust across different query types and document categories. We're confident enough in it that Bielik embeddings are now the default for Polish document processing in our production pipeline.

#### Generation Results: More Nuanced

The generation results were more nuanced. For straightforward queries — factual lookups, specific value extraction, simple clause identification — Bielik-generated answers were accurate and naturally expressed.

For complex multi-step queries — "how does this clause interact with the general insurance conditions given this type of incident?" — Claude 3.5 Sonnet on Bedrock, even with translated context, outperformed Bielik. This makes sense given the model size difference and the complexity of the reasoning required.

We adopted a hybrid approach: Bielik for embedding and retrieval, Claude for complex generation. We eliminated full document translation but retained query and response translation for the generation layer where needed.

#### Practical Architecture

The resulting pipeline:
1. Documents embedded using Bielik — no translation required
2. User queries embedded using Bielik — in original Polish
3. Retrieval against Polish embedding index
4. Retrieved Polish chunks passed to Claude with Polish-aware system prompt
5. Claude generates response in Polish (it handles Polish well)
6. Optional translation to English for non-Polish-speaking users

Cost impact: elimination of translation API calls for the embedding stage (our largest document volume) reduced pipeline costs by approximately 20%. Latency improved proportionally.

#### What This Means for Polish Enterprise AI

Building native Polish-language AI systems without the translation crutch is a viable path. It requires:

→ Investment in Polish embedding and generation models
→ Polish-language evaluation datasets validated by domain experts
→ Engineering patience with models that are smaller and require more careful prompting

The Polish AI ecosystem is building these capabilities. Bielik is proof that native Polish language AI is not an academic project — it's a production tool. For organizations operating primarily in Polish markets, building on native Polish models is worth evaluating seriously.

If you're working with Polish-language documents in an AI context and want to compare notes on architecture, reach out. This is a domain where shared learning moves faster than independent experimentation.
