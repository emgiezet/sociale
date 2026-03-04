# Day 8 — Trenches: Nikt nie mówi o AI w ubezpieczeniach (Polish + English)
**Pillar:** Trenches | **Week:** 2 | **CTA:** Comment (Polish)

---

## LinkedIn Post (Polish 🇵🇱)

W Polsce nikt nie mówi o AI w ubezpieczeniach.
A to jeden z najbardziej wymagających kontekstów do wdrożenia AI.

Buduję systemy AI w Insly — platformie dla brokerów ubezpieczeniowych obsługującej ponad 150 000 użytkowników w Europie. Kiedy rozmawiam z polskimi firmami technologicznymi o AI, słyszę przede wszystkim o chatbotach, generowaniu treści i automatyzacji procesów biurowych.

Ubezpieczenia to inna liga:

→ Dokumenty polisowe pisane przez różnych brokerów, w różnych formatach, często z OCR ze skanowanych papierowych arkuszy
→ Zapytania prawne, gdzie "podobna treść" to za mało — liczy się dokładna klauzula i jej kontekst
→ Regulacje RODO i lokalne przepisy finansowe, które ograniczają co możesz z danymi zrobić
→ Systemy legacy, które nie rozmawiają ze sobą nawet przed AI

Budujemy RAG-owe systemy na AWS Bedrock i testujemy modele Bielik dla polskojęzycznej treści ubezpieczeniowej. To nie jest projekt badawczy — to produkcja. Z prawdziwymi użytkownikami i prawdziwymi konsekwencjami błędów.

Polska branża tech jest świetna w budowaniu software. Nadszedł czas, żeby budowała też AI — nie tylko gadżety AI, ale systemy AI w trudnych domenach.

**Jeśli budujesz AI w regulowanej branży w Polsce — napisz. Chcę wiedzieć jak to wygląda u Ciebie.**

#AIwPolsce #InsurTech #RAG #PolskiTech #AIwProdukcji

---

## LinkedIn Post (English)

In Poland, nobody talks about AI in insurance.
And insurance is one of the hardest contexts to deploy AI in.

I build AI systems at Insly — a European insurance platform with 150,000+ users. When I talk to Polish tech companies about AI, the conversation is mostly about chatbots, content generation, and office automation.

Insurance is a different league:

→ Policy documents written by different brokers, in different formats, often OCR'd from paper
→ Legal queries where "semantically similar" isn't enough — you need the exact clause and its context
→ GDPR and local financial regulations that constrain what you can do with data
→ Legacy systems that don't talk to each other even before you add AI

We're building RAG systems on AWS Bedrock and testing Bielik models for Polish-language insurance content. This isn't a research project — it's production. Real users, real consequences for errors.

The Polish tech scene is excellent at building software. It's time to build AI — not AI gadgets, but AI systems in hard domains.

**If you're building AI in a regulated industry in Poland, reach out. I want to hear what it looks like on your end.**

#PolandTech #InsurTech #RAG #AIEngineering #ProductionAI

---

## Blog Post (Polish 🇵🇱)

### Dlaczego AI w ubezpieczeniach jest najtrudniejszym sprawdzianem dla Twojego systemu

Kiedy mówię ludziom spoza branży ubezpieczeniowej, że buduję systemy AI dla Insly, często spotykam się z podobną reakcją: "Ubezpieczenia? To nudne. Dlaczego nie coś bardziej ekscytującego?"

Mam na to prostą odpowiedź: jeśli Twój system AI działa w ubezpieczeniach, zadziała wszędzie.

To nie jest chełpliwość. To obserwacja techniczna. Ubezpieczenia to środowisko, które maksymalizuje każde wyzwanie związane z wdrożeniem AI w produkcji: złożone dane, wymagania prawne, konsekwencje błędów i legacy systemy. Jeśli potrafisz zbudować coś, co działa tutaj, masz umiejętności do pracy w każdej regulowanej domenie.

#### Problem Danych: Chaos Przed AI

Zanim zaczniesz myśleć o modelach językowych, wektorach i retrieval augmented generation, musisz zmierzyć się z rzeczywistością danych ubezpieczeniowych.

Insly obsługuje brokerów w całej Europie. Nasze dokumenty pochodzą z dziesiątek różnych źródeł: polisy generowane przez systemy zarządzające napisane przed 2010 rokiem, endorsementy skanowane z papieru i poddawane OCR, klauzule pisane w różnych językach przez różnych brokerów w różnych krajach. Każde źródło ma inną strukturę. Każde wymaga innego podejścia do ekstrakcji i normalizacji tekstu.

Zanim napisaliśmy pierwszą linię kodu RAG, spędziliśmy tygodnie na data pipeline'ach. Nie ma skrótu przez tę fazę.

#### Problem Prawny: Precyzja Ma Znaczenie

W większości zastosowań AI "w przybliżeniu poprawne" jest dopuszczalne. W ubezpieczeniach nie jest.

Kiedy system RAG wskazuje klauzulę pokrycia szkody, ta klauzula musi być dokładną klauzulą, która obowiązuje dla danej polisy, w danym momencie, z uwzględnieniem wszystkich późniejszych aneksów. Błąd nie jest tylko złym doświadczeniem użytkownika — to potencjalnie błędna decyzja odszkodowawcza lub naruszenie umowy.

To zmieniło naszą architekturę retrieval fundamentalnie. Czysty semantic search nie wystarczy, gdy dokładna klauzula i jej kontekst mają znaczenie prawne.

#### Bielik i Polskojęzyczna AI

Jednym z unikalnych wyzwań, z którymi się mierzymy, jest język. Znaczna część naszych dokumentów jest w języku polskim — a polskie modele językowe nie są tak dojrzałe jak anglojęzyczne.

Testujemy modele Bielik, polskie LLM-y trenowane na polskojęzycznym korpusie. Wczesne wyniki są obiecujące, szczególnie dla terminologii ubezpieczeniowej, która w angielskich modelach często jest tłumaczona nieprecyzyjnie.

To jest konkretna przewaga, którą może mieć polska inżynieria AI: budowanie systemów, które naprawdę rozumieją polskie dokumenty biznesowe — nie tylko tłumaczą je na angielski i z powrotem.

#### Co To Znaczy dla Polskiej Sceny Tech

Polski ekosystem technologiczny buduje świetne oprogramowanie. Mamy silne tradycje w software house'ach, game dev, cybersecurity. Ale w obszarze AI w regulowanych branżach — fintech, legaltech, insurtech — jesteśmy za daleko za zachodnioeuropejską i americką konkurencją.

To jest szansa. Firmy w tych branżach potrzebują partnerów, którzy rozumieją zarówno regulacje, jak i technologię. Inżynierów, którzy mogą rozmawiać o architekturze systemu i compliance w jednym zdaniu. Twórców, którzy wiedzą, że "działający demo" i "system produkcyjny" to dwa różne byty.

Jeśli budujesz AI w regulowanej branży w Polsce — ubezpieczenia, finanse, prawo, ochrona zdrowia — chcę wiedzieć jak to wygląda u Ciebie. Napisz w komentarzu lub na prywatną wiadomość.

---

## Blog Post (English)

### Why AI in Insurance Is the Ultimate Production Test for Your System

When I tell people outside the insurance industry that I build AI systems for Insly, I often get a version of the same reaction: "Insurance? That's boring. Why not something more exciting?"

I have a simple answer: if your AI system works in insurance, it works anywhere.

That's not bravado. It's a technical observation. Insurance is an environment that maximizes every challenge associated with deploying AI in production: complex data, legal requirements, real consequences for errors, and legacy systems that barely communicate with each other before you introduce AI into the mix. Building something that works here develops skills that transfer to any regulated domain.

#### The Data Problem: The Chaos Before AI

Before you think about language models, embeddings, and retrieval-augmented generation, you have to face the reality of insurance data.

Insly serves brokers across Europe. Our documents come from dozens of different sources: policies generated by management systems written before 2010, endorsements scanned from paper and run through OCR, clause libraries written in different languages by different brokers in different countries. Each source has different structure. Each requires different approaches to extraction and text normalization.

Before we wrote a single line of RAG code, we spent weeks on data pipelines. There's no shortcut through this phase. Anyone who tells you the data preparation step is minor hasn't done production RAG.

#### The Legal Problem: Precision Matters

In most AI applications, "approximately correct" is acceptable. In insurance, it isn't.

When a RAG system identifies a coverage clause, that clause needs to be the exact clause that applies to this policy, at this point in time, accounting for all subsequent amendments. An error isn't just a bad user experience — it's potentially a wrongful claims decision or a contractual violation.

This changed our retrieval architecture fundamentally. Pure semantic similarity search isn't enough when exact clauses and their relational context carry legal weight. We had to build architecture that understood document structure and cross-references, not just semantic similarity.

#### Bielik and Polish-Language AI

One of the unique challenges we work with is language. A significant portion of our documents are in Polish — and Polish-language LLMs aren't as mature as their English counterparts.

We're testing Bielik models, Polish LLMs trained on a Polish-language corpus. Early results are promising, particularly for insurance terminology that English models often handle imprecisely when dealing with Polish documents.

This represents a concrete advantage that Polish AI engineering can develop: building systems that genuinely understand Polish business documents, not just translate them to English and back.

#### What This Means for Polish Tech

Poland's technology ecosystem builds excellent software. We have strong traditions in software houses, game development, and cybersecurity. But in AI for regulated industries — fintech, legaltech, insurtech — we're behind western European and American competition.

This is an opportunity. Companies in these industries need partners who understand both regulations and technology. Engineers who can discuss system architecture and compliance in the same sentence. Builders who know that "working demo" and "production system" are different things.

If you're building AI in a regulated industry in Poland — insurance, finance, law, healthcare — I want to hear what it looks like for you. Share in the comments or reach out directly.
