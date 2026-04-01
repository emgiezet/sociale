---
day: 20
title: "Dlaczego Najlepsza Konsultacja AI Często Zaczyna Się od 'Nie Budujcie AI'"
pillar: Trenches
language: pl
image: ../../images/day-20.jpg
image_unsplash_query: "consulting business strategy meeting"
---

# Dlaczego Najlepsza Konsultacja AI Często Zaczyna Się od "Nie Budujcie AI"

Paradoks pracy jako konsultant technologiczny: najcenniejsza porada, którą możesz dać klientowi, to czasem "nie budujcie tego, co planujecie."

To nie jest cyniczne stanowisko. To wynik obserwacji, że presja na wdrożenie AI — wewnętrzna, rynkowa, ze strony zarządu — często wyprzedza diagnozę prawdziwego problemu.

## Schemat, który Widzę Regularnie

Firma przychodzi z propozycją projektu. Projekt jest sformułowany w kategoriach technologii: "chcemy wdrożyć chatbota AI", "potrzebujemy systemu RAG do naszych dokumentów", "chcemy automatyzować X przez AI". Technologia jest już wybrana. Problemem jest implementacja.

Moje pierwsze pytanie: "Jaką decyzję biznesową ma wspierać ten system?"

Zwykle następuje chwila ciszy. Potem jedna z dwóch odpowiedzi.

Albo odpowiedź jest precyzyjna i świadczy o tym, że projekt jest dobrze przygotowany: "Chcemy, żeby nasi underwriterzy mogli w 30 sekund znaleźć odpowiednią klauzulę w dokumentach polisy." To projekt, który można zbudować i zmierzyć.

Albo odpowiedź jest ogólna: "Chcemy być bardziej innowacyjni", "konkurencja wdrożyła AI", "zarząd chce zobaczyć AI w naszym produkcie." To projekt, który może pochłonąć budżet bez rozwiązania konkretnego problemu.

## Przypadek z Sektora Finansowego

Niedawno pracowałem z firmą finansową w Polsce. Przyszli z planem: chatbot oparty na dokumentach, zintegrowany z istniejącym CRM. Konkretny pomysł, budżet, harmonogram. Gotowi do budowy.

Po 45 minutach rozmowy o ich rzeczywistych procesach biznesowych okazało się, że chatbot był odpowiedzią na inny problem niż ten, który naprawdę istniał. Prawdziwy problem: handlowcy spędzali 30-40% czasu na ręcznym wyszukiwaniu informacji o klientach w trzech niezintegrowanych systemach. Chatbot by tego nie rozwiązał — bo problem nie dotyczył odpowiadania na pytania w naturalnym języku. Dotyczył fragmentacji danych operacyjnych.

Rozwiązanie: dashboard agregujący dane z trzech systemów, z ujednoliconym wyszukiwaniem i podglądem historii klienta. Czas implementacji: trzy tygodnie. Koszt: 30% planowanego budżetu. Wynik: handlowcy raportują 40% redukcję czasu na przygotowanie do rozmów z klientami.

To, co mnie uderzyło: techniczna złożoność faktycznego rozwiązania była znacznie niższa niż to, co pierwotnie planowano. Dashboard z agregacją danych to prosta inżynieria. Chatbot dokumentów z wymaganiami compliance, dokładnym retrieval, zapobieganiem halucynacjom i budowaniem zaufania użytkowników to miesiące pracy.

Diagnoza zmieniła wynik. Nie wykonanie.

## Trzy Błędy, które Widzę Regularnie

### Błąd 1: Zaczynanie od narzędzi zamiast od problemu

"Chcemy wdrożyć RAG." "Chcemy agentów AI." "Chcemy integrację z GPT."

Kiedy technologia jest wybrana zanim problem jest zdefiniowany, prawdopodobnie budujesz złą rzecz. Właściwa technologia wyłania się z właściwej definicji problemu.

Co napędza ten schemat: presja zarządu, który przeczytał artykuł o AI i chce pokazać postęp przed końcem kwartału. Zespół IT, który dostał zadanie "zróbcie coś z AI" bez zdefiniowanego problemu biznesowego. Brak osoby, która mogłaby powiedzieć "sprawdźmy najpierw, czy to ma sens."

### Błąd 2: Ignorowanie RODO i compliance na etapie projektowania

Firmy budują prototyp z danymi klientów, zanim ktokolwiek zapyta: w jakim kraju leżą serwery? Kto ma dostęp do logów? Jak wygląda prawo do bycia zapomnianym w systemie z embeddingami?

Potem płacą za przeprojektowanie wszystkiego.

To jest szczególnie dotkliwe w Polsce i UE, gdzie egzekwowanie RODO ma realne skutki. Chatbot przetwarzający dane klientów przez API LLM musi odpowiedzieć na te pytania zanim napiszesz pierwszą linię kodu, a nie po tym, jak zbudujesz demo, które dział prawny będzie musiał zatrzymać.

Dla regulowanych branż — ubezpieczenia (KNF), finanse, ochrona zdrowia — pytania compliance nie są troską po uruchomieniu. Są troską przed architekturą.

### Błąd 3: Mierzenie sukcesu przez "czy działa" zamiast przez "czy działa lepiej"

System AI, który odpowiada na 80% pytań gorzej niż stara wyszukiwarka, nie jest postępem. Jest droższym problemem.

Widziałem zespoły świętujące sukces demo i wdrażające systemy, które osiągnęły wyniki poniżej linii bazowej, którą miały zastąpić. Ocena była robiona względem "czy może odpowiadać na pytania?" zamiast "czy odpowiada na pytania tak dobrze jak to, co zastępuje?"

## Jak Wyglądają Dobre Projekty AI

Dobre projekty AI mają kilka cech wspólnych:

**Konkretna decyzja do wsparcia.** Nie "chcemy być smart", ale "nasz underwriter musi w 30 sekund ocenić ryzyko dla danego klienta."

**Znana definicja sukcesu.** "Skrócimy czas obsługi zapytania z 15 minut do 3 minut i zmierzymy to w ciągu pierwszych 30 dni."

**Zdefiniowany fallback.** "Jeśli AI nie jest pewny odpowiedzi, eskaluje do człowieka." Brak fallbacku to projekt z nieokreślonym ryzykiem.

**Odpowiedź na pytanie: co gdy system się myli?** W sektorze regulowanym to pytanie prawne i regulacyjne, nie tylko UX.

Jeśli projekt spełnia te cztery kryteria, warto budować. Jeśli nie — warto się zatrzymać i zadać pytania zanim zainwestuje się budżet.

## Pytanie, które Otwiera Prawdziwą Rozmowę

Kiedy firmy zatrudniają mnie jako konsultanta, pytanie, które zawsze zadaję na początku, ich zaskakuje.

Nie pytam o stos technologiczny. Nie pytam o architekturę.

Pytam: "Jaką konkretną decyzję biznesową ma wspierać ten system?"

To pytanie — i cisza, która następuje — mówi mi prawie wszystko, co muszę wiedzieć o tym, czy projekt zakończy się sukcesem.

Projekty AI, które odnoszą sukces, to te zbudowane z tego rodzaju jasności. Te, które zawodzą, to zazwyczaj te, które zaczęły od wyboru technologii zamiast od definicji problemu.

Potrzebujesz konsultacji AI? Napisz do mnie.
