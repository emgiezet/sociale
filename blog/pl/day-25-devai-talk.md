---
day: 25
title: "Co powiem na DevAI i dlaczego to nie jest typowa prezentacja o AI"
pillar: Educator
language: pl
image: ../../images/day-25.jpg
image_unsplash_query: "conference speaker stage technology"
---

# Co powiem na DevAI i dlaczego to nie jest typowa prezentacja o AI

Kiedy przyjmuję zaproszenie do mówienia na konferencji technicznej, zawsze zadaję sobie jedno pytanie: "Co mogę powiedzieć, czego słuchacze nie znajdą w żadnym artykule Medium?"

Prezentacje o AI są często albo zbyt akademickie — elegancka teoria bez produkcyjnego kontekstu, artykuły wyjaśniające jak rzeczy powinny działać bez uznania jak faktycznie działają — albo zbyt demo-centryczne: imponujące dema pokazujące szczęśliwą ścieżkę, zero informacji o tym, co dzieje się po wyjściu ze sceny, gdy prawdziwi użytkownicy zaczynają korzystać z systemu w nieoczekiwany sposób.

Próbuję znaleźć trzecią drogę: szczegółowy raport z terenu. To jest to, co faktycznie zbudowaliśmy. Oto co się zepsuło. Oto co zmieniliśmy i dlaczego. Oto co działa w produkcji z 150 000 dokumentów miesięcznie i pełnymi zobowiązaniami compliance, a co działało tylko w stagingu.

## Co będę omawiał na DevAI by DSS

Na DevAI by DSS, przedstawię ewolucję naszej architektury RAG w Insly — nie jako historię sukcesu, ale jako sekwencję problemów produkcyjnych i decyzji architektonicznych, które z nich wynikały.

**Etap 1: AWS Bedrock Knowledge Bases**

Zaczęliśmy od AWS Bedrock Knowledge Bases, bo to był najszybszy sposób, żeby uruchomić coś działającego. Demo wyglądało dobrze. Jakość retrieval na naszym produkcyjnym zestawie danych: około 60% na naszym zestawie testowym ewaluacyjnym.

60% brzmi OK dopóki nie pomyślisz, co to oznacza w praktyce. Czterdzieści procent czasu system pobierał fragmenty, które nie były najbardziej istotne dla pytania. Kiedy budujesz coś do pobierania dokumentów ubezpieczeniowych — gdzie różnica między właściwą a błędną klauzulą może mieć realne implikacje — 60% nie jest liczbą produkcyjną.

**Etap 2: Wyszukiwanie hybrydowe**

Dodaliśmy wyszukiwanie słów kluczowych BM25 obok wyszukiwania semantycznego. Kombinacja poprawiła jakość do około 72%. Lepiej. Nadal za mało dla naszego przypadku użycia.

Problem: retrieval nadal był płaski. Traktował każdy dokument jako niezależną jednostkę i pobierał na podstawie podobieństwa do zapytania. Ale dokumenty ubezpieczeniowe mają relacje — klauzula polisy odwołuje się do wyłączenia, które odwołuje się do definicji, która odwołuje się do standardu regulacyjnego. Płaski retrieval nie widzi tych relacji. Pobiera fragmenty bez kontekstu o tym, jak się łączą.

**Etap 3: LightRAG**

Modelowaliśmy dokumenty jako graf encji i relacji. Każda klauzula polisy, każda definicja, każde odwołanie krzyżowe stało się węzłem lub krawędzią w grafie. Retrieval stał się przechodzeniem tego grafu, a nie tylko wyszukiwaniem podobieństwa.

Jakość retrieval na pytaniach wymagających rozumienia relacji między dokumentami: około 89%. Koszt: znacznie wyższy overhead operacyjny. Budowanie grafu, utrzymanie i przetwarzanie zapytań są bardziej złożone niż wyszukiwanie podobieństwa wektorowego.

**Lekcja łącząca wszystkie trzy etapy:** Każda zmiana architektoniczna była podyktowana pomiarem. Zbudowaliśmy nasz framework ewaluacyjny najpierw, ustaliliśmy bazową linię jakości i zmienialiśmy architekturę tylko wtedy, gdy pomiary pokazywały, że osiągnęliśmy sufit jakości. To ewolucja podyktowana pomiarem, nie spekulacją — i to jest centralne przesłanie, które przekażę na DevAI.

## Dlaczego ubezpieczenia to ważny kontekst

Prezentacje o AI często traktują domenę jako wymienną lub całkowicie ją ignorują. "Oto nasz system RAG — działa dla każdego rodzaju dokumentu." To zrozumiałe w kontekście akademickim. To mylące w praktycznym.

W ubezpieczeniach domena nie jest wymienna. Kształtuje każdą decyzję architektoniczną.

Błąd w systemie rekomendacji produktów daje złe UX. Błąd w interpretacji klauzuli ubezpieczeniowej może dać błędną decyzję odszkodowawczą. To zmienia wszystko: wymagany poziom dokładności, architekturę fallback, wymogi audit trail i kryteria dla ludzkiego nadzoru.

Wierzę, że regulowane branże — ubezpieczenia, finanse, prawo, ochrona zdrowia — są najlepszym polem do nauki produkcyjnego AI. Jeśli coś działa tutaj, działa wszędzie. Jeśli działa tylko w środowisku bez zobowiązań compliance, to nie jest produkcyjne AI. To demo.

## Ludzki wymiar, o którym nikt nie mówi

Techniczne prezentacje o AI rzadko adresują organizacyjne i ludzkie wymiary transformacji AI. Na DevAI poświęcę na to jawnie czas.

Prowadzenie 15-osobowego zespołu przez 18 miesięcy transformacji AI nauczyło mnie rzeczy, których nie obejmuje żaden artykuł ani tutorial.

Jak doświadczeni inżynierowie reagują na ponowne bycie początkującymi. Starsi developerzy, którzy przez lata byli ekspertami w swojej domenie, nie lubią nagle być najmniej wiedzącą osobą w pokoju. Transformacja AI wielokrotnie tworzy taką sytuację. Inżynierowie z największym doświadczeniem w Symfony i PHP nagle byli w trybie nauki obok inżynierów, którzy byli nowsi w zespole, ale bardziej komfortowi z Pythonem i narzędziami ML. Zarządzanie tą dynamiką — budowanie bezpieczeństwa psychologicznego dla "jeszcze nie wiem", nagradzanie zachowań uczenia się tak samo jak zachowań dostarczania — było tak samo ważną częścią pracy jak jakakolwiek decyzja architektoniczna.

Jak budować wspólny kontekst w domenie, która zmienia się co tydzień. Krajobraz narzędzi AI zmienia się szybko. LightRAG nie był naszym początkowym planem — pojawił się jako właściwa odpowiedź po tym, jak nauczyliśmy się wystarczająco dużo z poprzednich etapów.

To jest część historii budowania produkcyjnego AI, o której nikt nie mówi. Na DevAI będę o tym mówić.

## Trzy pytania, które zagram publiczności

Zanim przedstawię ewolucję naszej architektury, zadam publiczności trzy pytania. Chcę wiedzieć, gdzie ludzie faktycznie są, nie gdzie myślą, że powinni być.

**Pytanie 1: Czy vibecoding to narzędzie czy substytut rozumienia?**

Moja pozycja: kodowanie wspomagane AI jest potężne i niebezpieczne dokładnie wtedy, kiedy wygenerowany kod wygląda poprawnie, a ty nie wiesz dlaczego działa. W branżach regulowanych "wygląda poprawnie" to za mało. Chcę usłyszeć od inżynierów, którzy już przez to przeszli.

**Pytanie 2: Ile systemów RAG w Twojej organizacji jest naprawdę w produkcji, a ile to PoC przemianowany na produkcję?**

Zbudowałem 3 systemy RAG. Dwa były drogimi lekcjami. Jeden działa dziś z prawdziwymi użytkownikami. Różnica między PoC a produkcją jest większa niż większość zespołów przyznaje publicznie.

**Pytanie 3: Kiedy ostatnio Twój zespół powiedział "nie wdrażamy tego, bo jeszcze nie umiemy tego ocenić"?**

Ewaluacja to najczęściej pomijany krok w projektach AI. Pytam wprost, bo chcę wiedzieć, czy to tylko mój problem, czy branżowy standard.

## Dla kogo

Ta prezentacja jest dla developerów, którzy zbudowali swoje pierwsze demo RAG i zastanawiają się co dalej — jaka jest przepaść między demem, które działa, a systemem gotowym do produkcji dla prawdziwych użytkowników z prawdziwymi konsekwencjami.

Dla tech leadów, którzy prowadzą swoje zespoły przez transformację AI i szukają kogoś, kto rozumie organizacyjną stronę, nie tylko architekturę techniczną.

Dla inżynierów w branżach regulowanych — bankowości, ochronie zdrowia, prawie, ubezpieczeniach — którzy myślą, że AI "nie może zadziałać w ich domenie". Chcę im pokazać, że może, i co faktycznie to wymaga.

Jeśli będziesz na DevAI, znajdź mnie przed lub po prelekcji. Chętnie wymienię notatki i usłyszę, co budujesz.

Jeśli nie będziesz — treść z tej prezentacji zostanie włączona do kursu "Agentic AI Developer" uruchamianego tej wiosny. Zostaw komentarz poniżej lub napisz do mnie, jeśli chcesz być na liście oczekujących.
