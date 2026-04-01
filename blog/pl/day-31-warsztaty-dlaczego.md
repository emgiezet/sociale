---
day: 31
title: "Dlaczego doświadczeni programiści boją się AI (i dlaczego zorganizowałem warsztaty)"
pillar: Trenches
language: pl
image: ../../images/day-31.jpg
image_unsplash_query: "developer team workshop coding discussion"
---

# Dlaczego doświadczeni programiści boją się AI (i dlaczego zorganizowałem warsztaty)

Piętnastu programistów. Dwadzieścia lat doświadczenia łącznie. I wyraźny, uczciwy strach przed AI.

Tego się spodziewałem. Entuzjazmu — albo przynajmniej ciekawości. Dostałem coś innego: szczerość.

Jeden z seniorów — dwanaście lat w branży, naprawdę jeden z najlepszych inżynierów w szerszym zespole — powiedział wprost: "Nie wiem od czego zacząć. I szczerze mówiąc, trochę się boję, że jak spróbuję, okaże się, że nie daję rady."

To zdanie mnie zatrzymało. Nie dlatego, że było zaskakujące. Dlatego, że było tak uczciwe. I dlatego, że wiedziałem — po osiemnastu miesiącach budowania systemów AI w produkcji — że jego strach ma realne podstawy.

To jest historia o tym, dlaczego zdecydowałem się zorganizować te warsztaty — i czego się nauczyłem o doświadczonych programistach i AI, zanim jeszcze zaczęliśmy.

## To nie jest kwestia umiejętności. To kwestia niepewności.

Jest pewien specyficzny rodzaj dyskomfortu, który pojawia się gdy pojawia się narzędzie, które zdaje się na nowo definiować Twoją wartość. Seniorzy spędzili lata budując ekspertyzę w rzemiośle — architektura, debugowanie, code review, projektowanie systemów — i nagle pojawia się technologia, która zdaje się to wszystko zagrażać.

Reakcja rzadko jest paniką. To coś cichszego i bardziej paraliżującego: brak wiedzy dokładnie gdzie leży zagrożenie, a co za tym idzie — brak wiedzy jak na nie zareagować.

Pracuję w Insly, europejskim InsurTech SaaS — nasze rozwiązania AI przetwarzają ponad 150 000 dokumentów miesięcznie. Mój zespół jedenastu inżynierów od osiemnastu miesięcy buduje systemy AI w produkcji — pipeline'y RAG, integracje z LLM, AWS Bedrock, LightRAG. Widzę na co dzień co działa, co nie i gdzie leży prawdziwa złożoność.

Ale pozostałe piętnaście osób w Insly? Inżynierowie pracujący z kodem produkcyjnym, legacy systemami, codziennymi featurami? Dla nich AI było gdzieś w tle. Coś, o czym słyszeli. Coś, czego "powinienem się nauczyć", ale bez konkretnej drogi.

Przepaść między tymi dwoma rzeczywistościami — między ludźmi aktywnie budującymi AI a ludźmi niepewnymi od czego zacząć — była przepaścią, którą warsztaty miały zamknąć.

## Konkretne obawy, które usłyszałem

Zanim zaczęliśmy, rozmawiałem z kilkoma inżynierami nieformalnie i po prostu słuchałem. Trzy rzeczy pojawiały się regularnie.

**"Nasz kod jest za stary na AI."**

Stack Insly obejmuje systemy PHP/Symfony sięgające 2012 i 2015 roku. Legacy w najbardziej realnym sensie: systemy które działają, które są krytyczne dla biznesu i których nikt już w pełni nie rozumie od początku do końca. Obawa była taka, że narzędzia AI są zaprojektowane dla nowych projektów — czystych, dobrze otypowanych, dobrze udokumentowanych — i będą bezużyteczne wobec kilkunastoletniego kodu enterprise.

Ta obawa jest zrozumiała. Jest też błędna. Ale żeby ją obalić, potrzebna jest demonstracja, nie argument.

**"Nie wiem czy bezpiecznie jest wklejać kod do ChatGPT."**

To uzasadniona obawa, i odzwierciedla coś ważnego: to są inżynierowie, którym zależy na ich obowiązkach zawodowych. Insly przetwarza wrażliwe dane ubezpieczeniowe. Instynkt ostrożności przed wysłaniem zastrzeżonego kodu do komercyjnego API AI jest właściwym instynktem. Ten strach nie wynikał z ignorancji — wynikał z odpowiedzialności.

Odpowiedź tutaj nie brzmi "po prostu zrób to." Brzmi: oto jak myśleć o tym, co można bezpiecznie udostępniać, a czego nie. Oto co oznaczają ustawienia prywatności i plany enterprise. Oto jak używać narzędzi AI bez naruszania swoich obowiązków.

**"Jeśli AI napisze PR, skąd będę wiedział, że jest dobry?"**

To był najgłębszy strach i najbardziej interesujący. Krył się pod nim pytanie o osąd: jeśli AI produkuje kod, i ja go akceptuję bez pełnego zrozumienia, czy wykonałem swoją pracę? Czy wciąż jestem inżynierem, czy stałem się recenzentem outputu AI — i co to oznacza dla mojej ekspertyzy?

Ten strach nie jest irracjonalny. Odzwierciedla prawdziwe napięcie w programowaniu wspomaganym przez AI: narzędzia są użyteczne właśnie dlatego, że są szybsze niż myślenie od zera, i ta szybkość tworzy pokusę akceptowania outputów bez tej samej skrupulatności, którą stosowałbyś do własnej pracy.

Odpowiedź na to wymaga czasu. Chodzi o budowanie osądu do oceny outputu AI — nie ślepe akceptowanie, nie odrzucanie z zasady, ale uczenie się jasnego widzenia.

## Dlaczego ignorowanie tego nie jest już opcją

Nie będę robić wielkich twierdzeń o AI zastępującym programistów. Ta rozmowa jest nudna i w większości bezużyteczna. Powiem natomiast coś prostszego: programiści, którzy nauczą się dobrze używać tych narzędzi, będą mogli więcej zrobić, szybciej debugować, szybciej rozumieć nieznany kod i pisać testy dla systemów, których nigdy nie dotykali.

Przepaść między programistami używającymi AI dobrze a tymi, którzy nie używają, rośnie. To jeszcze nie jest kryzys — ale będzie za dwa lata, i czas na naukę jest teraz, zanim będziesz do tyłu.

Dla zespołu pracującego nad produktem obsługującym 150 000+ użytkowników w branży regulowanej, ta przepaść jest też ryzykiem biznesowym. Jeśli ludzie budujący produkt nie rozumieją narzędzi transformujących ich domenę, są mniej przygotowani do podejmowania dobrych decyzji architektonicznych i mniej przygotowani do dobrego prowadzenia pracy.

Nie chodzi o zastąpienie ludzkiego osądu przez AI. Chodzi o danie doświadczonym inżynierom lepszych narzędzi, żeby ich osąd miał większą dźwignię.

## Co warsztaty miały rozwiązać

Zaprojektowałem warsztaty wokół konkretnych obaw i luk, które zidentyfikowałem — nie wokół generycznego curriculum o AI.

**Praktycznie od pierwszej minuty.** Żadnych godzinnych slajdów. W pierwszej sesji otworzyliśmy IDE i patrzyliśmy na prawdziwy kod. Celem było jak najszybsze przejście od abstrakcyjnej niepewności ("nie wiem jak używać AI") do konkretnego doświadczenia ("właśnie widziałem jak AI wyjaśnia tę funkcję, i widzę gdzie ma rację, a gdzie jest niepewne").

**Podzielone na dwie ścieżki.** Nowe projekty i systemy legacy mają różne wyzwania. Inżynierowie pracujący nad nowymi featurami mają jedne obawy; inżynierowie utrzymujący kod Symfony z 2013 roku mają inne. Połączenie ich w jeden warsztat nie służyłoby żadnej z grup.

**Obejmujące bezpieczeństwo i osąd, nie tylko możliwości.** Pytanie "czy to jest bezpieczne?" zasługiwało na prawdziwą odpowiedź, nie na zbagatelizowanie. A pytanie "skąd wiem czy kod wygenerowany przez AI jest dobry?" zasługiwało na praktyczny framework, nie filozoficzną odpowiedź.

**Zbudowane wokół rzeczywistego stacku.** Konkretne narzędzia dla developmentu PHP/Symfony. Konkretne techniki rozumienia legacy kodu. Konkretne podejścia do ograniczeń branży regulowanej, w której działa Insly. Generyczne warsztaty o ChatGPT nie byłyby użyteczne — te musiały adresować rzeczywisty kontekst.

## Rzecz, której się nie spodziewałem

Najważniejsze odkrycie, które zrobiłem — zanim warsztaty się jeszcze zaczęły — było takie, że strach nie był oznaką słabości. Był oznaką powagi.

Doświadczeni programiści, którzy boją się AI, nie boją się dlatego, że są niekompetentni. Boją się, bo rozumieją, że ekspertyzę buduje się starannie i nie chcą skracać drogi w sposób, który będą żałować. Boją się, bo zależy im na jakości swojej pracy i są niepewni jak AI wpisuje się w tę troskę.

To właściwy instynkt. Właściwą odpowiedzią nie jest przedzieranie się przez strach bezrefleksyjnie — to danie mu właściwej odpowiedzi.

Warsztaty były moją próbą udzielenia tej odpowiedzi: oto co AI robi dobrze, oto gdzie Cię wprowadzi w błąd, oto jak go używać w sposób, który rozszerza Twoją ekspertyzę, zamiast ją skracać.

Czy ta odpowiedź trafiła tak jak miałem nadzieję — o tym traktuje reszta tej serii.

---

*To jest pierwszy post z serii o warsztatach AI, które przeprowadziłem dla piętnastu programistów w Insly. Obserwuj serię: zakres warsztatów, techniki, przełom z legacy kodem, co się zmieniło, a co nie.*
