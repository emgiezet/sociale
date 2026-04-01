---
day: 10
title: "Framework 3 pytań, który chroni projekty AI przed cichą porażką"
pillar: Educator
language: pl
image: ../../images/day-10.jpg
image_unsplash_query: "decision framework whiteboard"
---

# Framework 3 pytań, który chroni projekty AI przed cichą porażką

Widziałem projekty AI zawodzące na dwa sposoby. Pierwszy to oczywista porażka: system nie działa, jakość jest słaba, zespół go porzuca. To bolesny wynik, ale przynajmniej jest widoczny. Wiesz, że tak się stało i możesz się z tego nauczyć.

Drugi to cicha porażka: system zostaje wdrożony, technicznie działa, jest okazjonalnie używany, ale nigdy faktycznie nie rozwiązuje problemu, dla którego został zbudowany. Ta porażka jest trudniejsza do wykrycia i droższa pod względem zmarnowanego wysiłku i źle ulokowanego zaufania.

Z mojego doświadczenia w prowadzeniu pracy AI w Insly, ciche porażki prawie zawsze wywodzą się z tej samej głównej przyczyny: problem nigdy nie był precyzyjnie zdefiniowany na początku.

Framework 3 pytań, który tutaj przedstawiam, został opracowany z obserwowania tych porażek — i z samodzielnego budowania trzech systemów RAG, z których jeden kosztownie zawiódł, zanim zmieniliśmy nasz proces. To nie jest eleganckie ani skomplikowane. Ale zespoły, które mogą odpowiedzieć na wszystkie trzy pytania zanim zaczną budować, prawie zawsze budują właściwą rzecz. Zespoły, które nie mogą na nie odpowiedzieć, potrzebują więcej pracy odkrywczej.

## Pytanie 1: Jaką konkretną decyzję ma wspierać to AI?

Słowo „konkretną" robi dużo pracy w tym pytaniu.

„Chcemy, żeby AI uczyniło nasz workflow mądrzejszym" to nie jest konkretna decyzja. Podobnie „chcemy używać AI do analizy naszych dokumentów" ani „chcemy asystenta AI dla naszego zespołu wsparcia."

Konkretna decyzja wygląda tak: „Kiedy underwriter otrzymuje powiadomienie o roszczeniu, musi w ciągu 30 sekund zidentyfikować, która klauzula pokrycia stosuje się i czy roszczenie mieści się w limitach pokrycia." To decyzja, w kierunku której możesz budować, oceniać ją i mierzyć.

W praktyce stwierdziłem, że wiele propozycji projektów AI nie przechodzi tego testu za pierwszym razem. „Chcemy, żeby AI poprawiło naszą obsługę klienta" staje się, po dziesięciu minutach pytań, „chcemy automatycznie kategoryzować przychodzące tickety wsparcia, żeby kierowały do właściwego zespołu bez ręcznej selekcji." To inny i znacznie łatwiejszy do zbudowania projekt.

Dyscyplina nazywania konkretnej decyzji ma kilka efektów. Wymusza rozmowę o tym, kto podejmuje decyzję i jakie informacje potrzebuje. Ujawnia listę jakościową — jak wygląda „poprawne" dla tej decyzji? Wyjaśnia zakres — nie budujesz systemu AI, budujesz wsparcie dla tej konkretnej decyzji.

Powiązane, ale odrębne pytanie: czy to jest problem retrieval czy problem generacji? Większość żądań AI okazuje się zamaskowanymi problemami retrieval. Broker pytający „co ta polisa obejmuje?" nie potrzebuje kreatywnej odpowiedzi. Potrzebuje dokładnego tekstu z właściwego dokumentu. To retrieval. Rozwiązanie tego z generatywnym modelem dodaje złożoność, latencję i ryzyko halucynacji bez dodawania wartości. Pomylenie tego kosztuje Cię miesiące.

## Pytanie 2: Co robi człowiek, gdy AI się myli?

To pytanie jest najbardziej niekomfortowym na spotkaniu inicjacyjnym projektu. Sugeruje, że AI będzie się mylić. We wczesnym entuzjazmie projektu AI, to brzmi jak negatywizm. To jest faktycznie dyscyplina inżynierska.

Każdy system AI myli się czasami. Pytanie brzmi, czy zaprojektowałeś dla tej rzeczywistości.

Odpowiedź na to pytanie definiuje Twoją architekturę obsługi błędów, design UI i profil ryzyka. Jeśli odpowiedź brzmi „człowiek przejrzy wynik AI przed działaniem na nim," to Twój interfejs musi sprawić, że rozumowanie AI jest widoczne i łatwe do nadpisania. Jeśli odpowiedź brzmi „to jest narzędzie wspomagające decyzję, nie narzędzie decyzyjne — człowiek zawsze podejmuje ostateczną decyzję," to Twój system nigdy nie powinien prezentować swojego wyniku jako definitywnego.

W ubezpieczeniach myślimy o tym starannie dla każdej funkcji. System RAG, który zwraca złą klauzulę polisową, może wpłynąć na decyzję o roszczeniu. Nasza odpowiedź: system prezentuje dowody (pobrany tekst, dokument źródłowy) obok odpowiedzi, a underwriterzy są szkoleni, żeby weryfikować źródło przed działaniem na rekomendacji. Logujemy każdy przypadek, w którym człowiek nadpisuje sugestię AI — ten log jest naszym najcenniejszym sygnałem jakości.

W regulowanych branżach to pytanie ma zęby. Zanim cokolwiek AI-zasilanego zbudujesz w ubezpieczeniach, finansach, prawie lub ochronie zdrowia, musisz zmapować: jakich danych dotyka ten system? Czy może opuścić swoją jurysdykcję? Czy automatyczne decyzje z użyciem tego systemu wymagają wytłumaczalności zgodnie z prawem UE (RODO/Akt AI)? Jakie jest wymaganie dotyczące logu audytu?

Jeśli nie możesz na to odpowiedzieć zanim zaczniesz, Twoja architektura zmieni się pod Tobą w połowie drogi. To drogi sprint review.

## Pytanie 3: Skąd będziemy wiedzieć, że działa za 3 miesiące?

To pytanie dotyczy kryteriów sukcesu i pomiaru.

„Działa" to nie jest kryterium sukcesu. „Użytkownicy wydają się to lubić" to nie jest kryterium sukcesu. Kryterium sukcesu to mierzalny wynik, który można zaobserwować w określonym przyszłym punkcie czasu.

Dobre kryteria sukcesu dla projektów AI wyglądają tak:
→ Czas do wykonania decyzji X zmniejszony z Y minut do Z minut
→ Wolumen ręcznych nadpisań rekomendacji AI poniżej N%
→ Precyzja retrieval na zbiorze ewaluacyjnym powyżej progu T
→ Liczba ticketów wsparcia wymagających ręcznej eskalacji zmniejszona o X%

Dla naszego produkcyjnego systemu RAG, „wystarczająco dobry" oznaczało: >85% precyzji retrieval na naszym oznaczonym zestawie testowym 200 pytań, <2 sekundy czasu odpowiedzi przy p95, zero odpowiedzi cytujących nieistniejące źródła. Uruchamiamy tę ewaluację przy każdej znaczącej zmianie. Jeśli dokładność spada o więcej niż 3%, nie wdrażamy. Bez wyjątków.

Definiowanie kryteriów sukcesu z góry robi dwie rzeczy. Po pierwsze, wyrównuje zespół co do tego, jak wygląda „gotowe," co zapobiega dryfowaniu projektu w nieskończoność w cyklach ulepszeń. Po drugie, daje Ci uczciwe podstawy do przeglądu post-launch — to albo zadziałało, albo nie, oto dowody, oto czego się nauczyliśmy.

## Używanie frameworku

Następnym razem, gdy będziesz na spotkaniu inicjacyjnym projektu AI — czy to prowadząc je, czy w nim uczestnicząc — spróbuj zadać te trzy pytania explicite:

1. Jaką konkretną decyzję ma wspierać to AI?
2. Co robi człowiek, gdy AI się myli?
3. Skąd będziemy wiedzieć, że działa za 3 miesiące?

Jeśli sala może wyraźnie odpowiedzieć na wszystkie trzy, masz projekt wart zbudowania. Jeśli nie może, najcenniejszą rzeczą, którą możesz zrobić, jest spędzenie więcej czasu na odkrywaniu zanim ktokolwiek napisze linię kodu.

Projekty AI, które zawodzą, zazwyczaj nie zawodzą z powodu problemu technicznego. Zawodzą, bo problem nigdy nie był precyzyjnie zdefiniowany. Te trzy pytania to mechanizm wymuszający, który sprawia, że ta definicja wydarza się zanim porażka może nastąpić.

Zapisz to. Użyj na swoim następnym spotkaniu inicjacyjnym projektu AI.
