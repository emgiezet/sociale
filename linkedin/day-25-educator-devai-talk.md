# Day 25 — Educator: DevAI Talk (Polish + English)
**Pillar:** Educator | **Week:** 5 | **CTA:** Follow/Waitlist

---

## LinkedIn Post (Polish 🇵🇱)

Za kilka tygodni występuję na DevAI by DSS.
Temat: jak budujemy AI w produkcji w regulowanej branży.

Nie będę mówił o tym, jak zbudować chatbota w 30 minut. Nie będę recenzował najnowszych modeli OpenAI. Będę mówił o tym, co naprawdę dzieje się, kiedy próbujesz wdrożyć AI w środowisku, gdzie błędy mają konsekwencje prawne.

Co zaprezentuję:

→ Ewolucja naszej architektury RAG — od Bedrock Knowledge Bases do LightRAG — i dlaczego każda zmiana była wymuszona przez realne problemy produkcyjne
→ Jak budować evaluation infrastructure dla systemu AI, jeśli nie masz zespołu ML
→ Polski model językowy Bielik w ubezpieczeniowych dokumentach — co działa, co nie
→ Emocjonalna i organizacyjna strona prowadzenia zespołu przez transformację AI

DevAI by DSS to polska konferencja dla developmentu AI — jedno z niewielu miejsc, gdzie możesz usłyszeć o AI w produkcji od kogoś, kto buduje to na żywo, nie w akademickim laboratorium.

Jeśli będziesz na DevAI — napisz, chętnie pogadam.
Jeśli nie będziesz — te tematy pojawią się w kursie "Agentic AI Developer." Zostaw komentarz jeśli chcesz być na liście oczekujących.

#DevAI #DSS #AIwProdukcji #PolskiTech #AIKonferencja

---

## LinkedIn Post (English)

I'm speaking at DevAI by DSS in a few weeks.
Topic: building AI in production in a regulated industry.

I won't be talking about how to build a chatbot in 30 minutes. I won't be reviewing the latest model releases.

I'll be talking about what actually happens when you try to deploy AI in an environment where mistakes have legal consequences — and you have 150,000 users, an 11-person team, and compliance obligations you can't ignore.

What I'll cover:

→ The evolution of our RAG architecture — from Bedrock Knowledge Bases to LightRAG — and why each change was driven by real production failures
→ How to build evaluation infrastructure for an AI system without an ML team
→ Bielik (Polish LLM) for Polish insurance documents — what worked, what didn't
→ The human and organizational side of leading a team through AI transformation

DevAI by DSS is one of the leading AI developer conferences in Poland — one of the few places where you can hear about production AI from someone actively building it, not just researching it.

If you'll be at DevAI, message me. Would love to connect in person.

If you won't be there, these topics will all appear in the "Agentic AI Developer" course launching this spring. Leave a comment if you want to be on the waitlist.

#DevAI #AIEngineering #ProductionAI #InsurTech #PolandTech

---

## Blog Post (Polish 🇵🇱)

### Co Powiem na DevAI i Dlaczego To Nie Jest Typowa Prezentacja o AI

Kiedy przyjmuję zaproszenie do mówienia na konferencji technicznej, zawsze zadaję sobie jedno pytanie: "Co mogę powiedzieć, czego słuchacze nie znajdą w żadnym artykule Medium?"

Prezentacje o AI są często albo zbyt akademickie (elegancka teoria bez produkcyjnego kontekstu) albo zbyt demo-centryczne (imponujące demo, zero informacji o tym co dzieje się po wyjściu ze sceny). Próbuję znaleźć trzecią drogę: szczegółowy raport z terenu.

#### Co Będę Opowiadał

Na DevAI przedstawię ewolucję naszej architektury RAG w Insly — nie jako sukces story, ale jako serię problemów produkcyjnych i decyzji architektonicznych, które z nich wynikały.

**Etap 1: Bedrock Knowledge Bases**
Zaczęliśmy od AWS Bedrock Knowledge Bases, bo to był najszybszy sposób, żeby uruchomić coś działającego. Demo wyglądało dobrze. Jakość retrieval na produkcyjnych danych: ~60% na naszym test secie.

**Etap 2: Hybrid Search**
Dodaliśmy BM25 keyword search obok semantic search. Jakość wzrosła do ~72%. Ale retrieval nadal był płaski — nie rozumiał relacji między dokumentami.

**Etap 3: LightRAG**
Modelowanie dokumentów jako grafu encji i relacji. Jakość retrieval na pytaniach o cross-document relationships: ~89%. Koszt: znacznie wyższy overhead operacyjny.

**Kiedy każda decyzja była podejmowana?** Kiedy pomiary pokazywały, że poprzednie rozwiązanie osiągnęło swój sufit jakości. Nie wcześniej.

To jest centralna myśl prezentacji: evolution driven by measurement, not speculation.

#### Dlaczego Ubezpieczenia To Ważny Kontekst

Prezentacje o AI często ignorują domenę lub traktują ją jako wymienną. W ubezpieczeniach domena nie jest wymienna — ona kształtuje każdą decyzję architektoniczną.

Błąd w systemie rekomendacji produktów: zły UX. Błąd w systemie interpretacji klauzuli ubezpieczeniowej: potencjalnie błędna decyzja odszkodowawcza. To zmienia wszystko: poziom wymaganej dokładności, architekturę fallback, wymogi audit trail, kryteria dla human oversight.

Wierzę, że regulowane branże — ubezpieczenia, finanse, prawo, ochrona zdrowia — są najlepszym polem do nauki produkcyjnego AI. Jeśli coś działa tutaj, działa wszędzie.

#### Dla Kogo Ta Prezentacja

Dla developerów, którzy zbudowali już swoje pierwsze demo RAG i zastanawiają się co dalej. Dla tech leadów, którzy prowadzą swój zespół przez transformację AI i szukają kogoś, kto rozumie organizacyjną stronę tego procesu. Dla inżynierów w regulowanych branżach, którzy myślą, że AI u nich "nie może zadziałać" — chcę pokazać, że może.

---

## Blog Post (English)

### What I'm Presenting at DevAI and Why It's Not a Typical AI Talk

When I accept a speaking invitation at a technical conference, I ask myself one question first: "What can I say that the audience can't find in any Medium article?"

AI presentations tend to fall into two categories: too academic (elegant theory without production context) or too demo-centric (impressive demo, zero information about what happens after you leave the stage). I try to find a third path: a detailed field report.

#### What I'll Be Covering

At DevAI by DSS, I'll present the evolution of our RAG architecture at Insly — not as a success story, but as a sequence of production problems and the architectural decisions that followed from them.

**Stage 1: Bedrock Knowledge Bases**
We started with AWS Bedrock Knowledge Bases because it was the fastest path to something working. The demo looked good. Retrieval quality on production data: approximately 60% on our evaluation set.

**Stage 2: Hybrid Search**
We added BM25 keyword search alongside semantic search. Quality improved to approximately 72%. But retrieval was still flat — it didn't understand relationships between documents, which in insurance carry critical meaning.

**Stage 3: LightRAG**
We modeled documents as a graph of entities and relationships. Retrieval quality on cross-document relationship questions: approximately 89%. The cost: significantly higher operational overhead.

**When was each decision made?** When measurements showed that the previous solution had reached its quality ceiling. Not earlier. The central message: evolution driven by measurement, not speculation.

#### Why Insurance Is an Important Context

AI presentations often ignore domain or treat it as interchangeable. In insurance, domain is not interchangeable — it shapes every architectural decision.

An error in a product recommendation system: poor UX. An error in interpreting an insurance clause: potentially a wrongful claims decision. This changes everything: the required accuracy level, the fallback architecture, the audit trail requirements, the human oversight criteria.

I believe regulated industries — insurance, finance, law, healthcare — are the best training ground for production AI. If something works here, it works anywhere.

#### The Human Dimension

Technical presentations about AI rarely address the organizational and human dimensions of AI transformation. At DevAI, I'll spend time on this explicitly.

Leading an 11-person team through 18 months of AI transformation has taught me things that no paper or tutorial covers: how experienced engineers respond to being beginners again, how to build shared context in a domain that changes weekly, how to manage teams with very different starting points in AI fluency.

This is part of the story of building production AI that nobody talks about. At DevAI, I'll talk about it.

#### For Whom

This talk is for developers who've built their first RAG demo and are wondering what comes next. For tech leads guiding their teams through AI transformation and looking for someone who understands the organizational side. For engineers in regulated industries who think AI "can't work in their domain" — I want to show them it can, and what it takes.

If you'll be at DevAI, find me — I'd love to compare notes. If you won't be there, the content from this talk will be incorporated into the "Agentic AI Developer" course launching this spring. Leave a comment or reach out if you want to be on the waitlist.
