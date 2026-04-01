---
day: 8
title: "Dlaczego AI w ubezpieczeniach to najtrudniejszy sprawdzian dla Twojego systemu"
pillar: Trenches
language: pl
image: ../../images/day-08.jpg
image_unsplash_query: "insurance digital transformation"
---

# Dlaczego AI w ubezpieczeniach to najtrudniejszy sprawdzian dla Twojego systemu

Kiedy mówię ludziom spoza branży ubezpieczeniowej, że buduję systemy AI dla Insly, często spotykam się z podobną reakcją: „Ubezpieczenia? To nudne. Dlaczego nie coś bardziej ekscytującego?"

Mam na to prostą odpowiedź: jeśli Twój system AI działa w ubezpieczeniach, zadziała wszędzie.

To nie jest chełpliwość. To obserwacja techniczna. Ubezpieczenia to środowisko, które maksymalizuje każde wyzwanie związane z wdrożeniem AI w produkcji: złożone dane, wymagania prawne, konsekwencje błędów i systemy legacy, które ledwo ze sobą rozmawiają, zanim wprowadzisz AI do mieszanki. Budowanie czegoś, co tu działa, rozwija umiejętności transferowalne do każdej regulowanej domeny.

## Problem danych: chaos przed AI

Zanim zaczniesz myśleć o modelach językowych, embeddingach i retrieval-augmented generation, musisz zmierzyć się z rzeczywistością danych ubezpieczeniowych.

Insly obsługuje brokerów w całej Europie. Nasze dokumenty pochodzą z dziesiątek różnych źródeł: polisy generowane przez systemy zarządzania napisane przed 2010 rokiem, aneksy skanowane z papieru i poddawane OCR, biblioteki klauzul pisane w różnych językach przez różnych brokerów w różnych krajach. Każde źródło ma inną strukturę. Każde wymaga innego podejścia do ekstrakcji i normalizacji tekstu.

Zanim napisaliśmy pierwszą linię kodu RAG, spędziliśmy tygodnie na data pipeline'ach. Nie ma skrótu przez tę fazę. Ktokolwiek mówi Ci, że etap przygotowania danych jest drobnostką, nie robił produkcyjnego RAG.

Jak wyglądają dane ubezpieczeniowe w praktyce:
→ Dokumenty polisowe obejmujące 15+ lat zmian formatu od różnych brokerów
→ Zeskanowane pliki OCR, gdzie rozpoznanie znaków jest niedoskonałe — wpływając na granice klauzul i wartości liczbowe
→ Dokumenty wzajemnie się odwołujące, gdzie klauzula A w jednym dokumencie jest modyfikowana przez aneks B w innym dokumencie z dwa lata później
→ Terminologia specyficzna dla jurysdykcji, której znaczenie zmienia się przez granice krajowe

Nasza strategia chunkowania musiała uwzględniać to wszystko zanim w ogóle mogliśmy myśleć o jakości retrieval.

## Problem prawny: precyzja ma znaczenie

W większości zastosowań AI „w przybliżeniu poprawne" jest dopuszczalne. W ubezpieczeniach nie jest.

Kiedy system RAG identyfikuje klauzulę pokrycia, ta klauzula musi być dokładną klauzulą, która obowiązuje dla tej polisy, w tym momencie, z uwzględnieniem wszystkich późniejszych zmian. Błąd to nie tylko złe doświadczenie użytkownika — to potencjalnie błędna decyzja odszkodowawcza lub naruszenie umowy.

To fundamentalnie zmieniło naszą architekturę retrieval. Czyste wyszukiwanie semantyczne nie wystarczy, gdy dokładne klauzule i ich relacyjny kontekst mają wagę prawną. Musieliśmy zbudować architekturę rozumiejącą strukturę dokumentów i wzajemne odniesienia, nie tylko podobieństwo semantyczne.

RODO dodaje kolejną warstwę. Automatyczne decyzje wpływające na pokrycie ubezpieczeniowe wymagają wytłumaczalności zgodnie z prawem UE. „AI tak powiedziała" to nie jest wyjaśnienie. Musimy być w stanie pokazać dokładnie, który dokument, którą klauzulę, który tekst wspierał każdą rekomendację systemu. To jest wymaganie projektowe, którego większość tutoriali AI nie dotyczy.

## Bielik i polskojęzyczne AI

Jednym z unikalnych wyzwań, z którymi się mierzymy, jest język. Znaczna część naszych dokumentów jest w języku polskim — a polskie LLM-y nie są tak dojrzałe jak anglojęzyczne.

Testujemy modele Bielik, polskie LLM-y trenowane na polskojęzycznym korpusie. Wczesne wyniki są obiecujące. Widzimy poprawę precyzji o 12 punktów procentowych w porównaniu do podejścia opartego na tłumaczeniu — gdzie tłumaczysz polskie dokumenty na angielski, przetwarzasz angielskim modelem i tłumaczysz z powrotem.

Podejście z tłumaczeniem jest stratne. Terminologia ubezpieczeniowa ma precyzyjne znaczenia, które nie mapują się czysto przez języki. „Odpowiedzialność cywilna" nie jest w pełni uchwycona przez „civil liability" — polski kontekst prawny wokół tej frazy jest inny. Bielik rozumie ten kontekst natywnie.

To jest konkretna przewaga, którą polska inżynieria AI może rozwinąć: budowanie systemów, które naprawdę rozumieją polskie dokumenty biznesowe, a nie tylko ich przybliżone tłumaczenia.

## Co to oznacza dla polskiej sceny tech

Polski ekosystem technologiczny buduje świetne oprogramowanie. Mamy silne tradycje w software house'ach, game dev i cyberbezpieczeństwie. Ale w AI dla regulowanych branż — fintech, legaltech, insurtech — jesteśmy za zachodnioeuropejską i amerikanką konkurencją.

To jest szansa. Firmy w tych branżach potrzebują partnerów, którzy rozumieją zarówno regulacje, jak i technologię. Inżynierów, którzy mogą rozmawiać o architekturze systemu i compliance w jednym zdaniu. Twórców, którzy wiedzą, że „działające demo" i „system produkcyjny" to dwa różne byty.

Polski rynek InsurTech jest mały, ale rośnie. Firmy, które zbudują AI z głową — z wbudowanym od początku compliance, jakością danych i realnymi potrzebami brokera — będą miały przewagę, której nie da się szybko skopiować.

Cyfrowa transformacja ubezpieczeń w Polsce dopiero się zaczyna. AI będzie jej silnikiem, nie ozdobnikiem.

Jeśli budujesz AI w regulowanej branży w Polsce — ubezpieczenia, finanse, prawo, ochrona zdrowia — chcę wiedzieć jak to wygląda u Ciebie. Napisz w komentarzu lub skontaktuj się bezpośrednio.
