---
day: 33
title: "Problem legacy kodu nie jest techniczny. Jest psychologiczny."
pillar: Trenches
language: pl
image: ../../images/day-33.jpg
image_unsplash_query: "legacy code old software developer debugging"
---

# Problem legacy kodu nie jest techniczny. Jest psychologiczny.

Chcę Ci opowiedzieć o jednym momencie z warsztatów.

Jeden z inżynierów — kilka lat w Insly, odpowiada za jeden z naszych starszych modułów Symfony — siedział ze skrzyżowanymi rękami na początku sesji o legacy kodzie. Zanim zaczęliśmy, powiedział: "To nie zadziała dla naszego kodu. Nasz kod jest za skomplikowany. Nikt go nie rozumie — ani ludzie, ani AI."

Poprosiłem go, żeby pokazał mi najtrudniejszy fragment jaki może znaleźć.

Wkleił klasę. Może trzysta linii, bez komentarzy, kilka warstw dziedziczenia, logika biznesowa przemieszana z kodem infrastrukturalnym. Rodzaj rzeczy, który sprawia, że nowi programiści po cichu panikują kiedy im to trafia.

Zapytałem Claude'a: "Wytłumacz co robi ta klasa, krok po kroku, jakbyś opisywał to komuś, kto widzi ją po raz pierwszy."

Odpowiedź wróciła w jakieś dziesięć sekund. Była dobra. Nie perfekcyjna — inżynier poprawił dwa konkretne szczegóły, gdzie model źle odczytał intencję. Ale szkielet był trafny. Podstawowa logika była czytelna. Wyjaśnienie nazwało odpowiedzialność klasy w terminach, które pasowały do tego, jak inżynier sam by ją opisał gdyby był przyciśnięty.

Patrzył na ekran przez chwilę. Potem powiedział: "No dobra. Nie spodziewałem się tego."

I wtedy sesja się zmieniła.

## Co tak naprawdę się działo

Dużo myślałem o tym momencie po warsztatach. Inżynier nie mylił się co do złożoności kodu. Mylił się co do tego, co ta złożoność oznaczała dla AI.

Konkretne przekonanie, które miał — i słyszałem jego wersje od programistów w kilku różnych firmach — brzmi mniej więcej tak: "Legacy kod jest szczególny. Jest tak stary, tak słabo udokumentowany, tak idiosynkratycznie ustrukturyzowany, że nowoczesne narzędzia AI, wytrenowane na czystych przykładach i sensownych wzorcach, nie będą w stanie tego ogarnąć. Nasza sytuacja jest wyjątkiem."

To przekonanie jest zrozumiałe. Czuje się ochronnie. Jeśli narzędzia nie potrafią pracować z Twoim kodem, to narzędzia nie mogą oceniać Twojego kodu, a kod, który utrzymujesz od lat i nauczyłeś się czytać, może pozostać terytorium, gdzie Twoja ekspertyza jest suwerenna.

Ale jest też błędne, w konkretny i ważny sposób. Legacy kod nie jest zbyt dziwny dla AI — jest po prostu dziwny w taki sam sposób jak każdy kod na skalę. Za dużo odpowiedzialności na klasę. Niejasne nazewnictwo. Logika biznesowa, która nagromadziła się w nieoczekiwanych miejscach. Niejawne zależności. To są wzorce, które AI widział w ogromnych ilościach w danych treningowych. Kod nie jest szczególny. Jest tylko stary.

Przełom w tej sesji nie polegał na tym, że AI zrobił coś technicznie imponującego. Polegał na tym, że obalił przekonanie, które blokowało doświadczonego inżyniera przed nawet próbowaniem.

## Psychologia programistów pracujących z legacy kodem

Programiści, którzy pracują na legacy systemach przez lata, rozwijają specyficzną relację z tym kodem. Staje się znane terytorium — nie dokładnie komfortowe, ale nawigowane. Wiedzą gdzie są zakopane miny. Wiedzą które klasy można dotknąć bezpiecznie, a które wybuchną jeśli spojrzysz na nie nie tak. Znają historię: dlaczego ta funkcja robi tę dziwną rzecz, dlaczego ten serwis wywołuje tamten inny serwis, jaki incydent z 2017 roku doprowadził do tego konkretnego hacka, który nigdy nie został wyczyszczony.

Ta wiedza jest autentyczna i wartościowa. Bywa też — sporadycznie — klatką.

Ta sama ekspertyza, która sprawia, że ktoś jest skuteczny w utrzymaniu legacy kodu, może tworzyć opór przed zmianą — bo zmiana jest tym, przez co tracisz wiarygodną mapę, którą zbudowałeś. Nowe narzędzie, nowe podejście, nowy kolega który nie zna historii: wszystko to są zagrożenia dla przewagi nawigacyjnej, którą ekspertyza zapewnia.

AI jest szczególnie interesującą wersją tego zagrożenia, bo AI może czytać kod bez żadnego z nagromadzonego kontekstu, który sprawia, że ekspertyza legacy wydaje się wartościowa. Może wyjaśnić funkcję bez znajomości incydentu z 2017 roku. Może zasugerować refaktoring bez wiedzy o zakopanych minach.

Dla niektórych programistów to jest wyzwalające. Dla innych — w tym, początkowo, dla inżyniera z tych warsztatów — to jest zagrażające. Jeśli maszyna może wyjaśnić Twój kod nowicjuszowi w dziesięć sekund, jaka jest wartość dziesięciu lat nagromadzonej ekspertyzy?

Chcę dać bezpośrednią odpowiedź na to pytanie, bo uważam że strach zasługuje na jedną: wartość tkwi w osądzie. AI może opisać co kod robi. Nie może powiedzieć Ci czy to co robi jest poprawne. Nie może powiedzieć Ci czy podejście podjęte w 2015 roku powinno być zachowane czy zastąpione w 2026. Nie może podejmować decyzji architektonicznych. Nie może ważyć ryzyka biznesowego względem długu technicznego. Te osądy wymagają kontekstu, odpowiedzialności i wiedzy domenowej, którą tylko ludzie pracujący z tym systemem na co dzień posiadają.

AI nie czyni ekspertyzy legacy przestarzałą. Sprawia, że pewne części pracy z legacy są mniej żmudne — żeby ekspertyza mogła być wydana na części, które naprawdę jej wymagają.

## Konkretne techniki, które zadziałały

Bądźmy konkretni co do tego, co faktycznie robiliśmy w ścieżce legacy, i co przyniosło efekty.

### Wyjaśnienie kodu jako pierwszy krok

Pierwsze zastosowanie jest najprostsze i najszerzej użyteczne: poproś AI o wyjaśnienie kodu, którego w pełni nie rozumiesz, zanim go dotkniesz.

Działa przy onboardingu. Działa kiedy dostajesz ticket dla modułu, którego nigdy nie widziałeś. Działa kiedy debugujesz i musisz rozumieć funkcję, której nie napisałeś.

Technika, która ma znaczenie: nie wklejaj tylko funkcji. Daj kontekst. Włącz interfejs, który implementuje. Włącz typ obiektu, który otrzymuje. Włącz typy wyjątków, które łapie lub rzuca. Wyjaśnienie modelu jest tylko tak dobre jak kontekst, który ma.

I oceniaj wyjaśnienie krytycznie. Szukaj języka hedgingowego ("wydaje się, że", "wynika z tego, że") — to są sygnały, że model wnioskuje zamiast czytać. Sprawdzaj konkretne twierdzenia względem kodu. Używaj wyjaśnienia jako hipotezy startowej, nie ostatecznej odpowiedzi.

### Testy charakteryzacyjne przed refaktoringiem

To jedno z najwartościowszych zastosowań AI w pracy z legacy, i jedno z najmniej używanych.

Jeśli masz kod bez testów i chcesz go zrefaktoryzować, mierzysz się ze standardowym problemem: skąd wiesz, że Twój refaktoring niczego nie zepsuł, gdy nie masz testów które mogłyby nie przejść?

Odpowiedzią są testy charakteryzacyjne: testy dokumentujące co kod aktualnie robi, nie co powinien robić. Uchwytują rzeczywiste zachowanie tak jak istnieje — włącznie z bugami, jeśli są bugi — i tworzą baseline, który zaalarmuje Cię jeśli refaktoring zmieni zachowanie w nieoczekiwany sposób.

Pisanie testów charakteryzacyjnych ręcznie jest żmudne. AI sprawia, że jest szybkie.

Daj modelowi funkcję, którą chcesz scharakteryzować. Daj mu przykładowe inputy jeśli masz. Poproś o testy uchwytujące aktualne zachowanie, włącznie z przypadkami brzegowymi. Potem przejrzyj testy względem kodu — nie żeby zwalidować, że zachowanie jest poprawne, ale żeby zwalidować, że testy dokładnie odzwierciedlają co kod faktycznie robi.

Na warsztatach zastosowaliśmy to do legacy modułu obliczania opłat, który nigdy nie miał testów. Wygenerowaliśmy testy charakteryzacyjne w około dwadzieścia minut. Przed AI zajęłoby to większość dnia. Testy nie były piękne. Nie były architektonicznie idealne. Ale istniały, co oznaczało, że mogliśmy zacząć refaktoryzować z siatką bezpieczeństwa, której wcześniej nie mieliśmy.

### Bezpieczny inkrementalny refaktoring

Z testami charakteryzacyjnymi na miejscu, refaktoring z AI staje się znacznie bardziej praktyczny.

Technika: refaktoryzuj w małych krokach. Rób jedną zmianę na raz. Uruchamiaj testy charakteryzacyjne po każdej zmianie. Jeśli test nie przejdzie, wiesz dokładnie jakie zachowanie się zmieniło i możesz zdecydować, czy ta zmiana była zamierzona.

AI jest tu użyteczny jako partner refaktoringu, nie agent refaktoringu. Opisz zmianę, którą chcesz zrobić. Poproś model, żeby pokazał jak ją zrobić. Przejrzyj proponowaną zmianę zanim ją zastosujesz. Uruchom testy. Powtórz.

Ważna dyscyplina: nigdy nie aplikuj refaktoringu sugerowanego przez AI bez uważnego przeczytania. Legacy kod ma subtelne zależności, o których AI nie wie. Refaktoring wyglądający bezpiecznie z samego kodu może złamać coś, czego testy nie obejmują. Tu kontekstualna wiedza inżyniera pozostaje niezbędna — AI proponuje, inżynier decyduje.

### Polowanie na bugi przez ustrukturyzowany dialog

Najbardziej użyteczne zastosowanie AI przy szukaniu bugów to nie "powiedz mi co jest nie tak z tym kodem." To ustrukturyzowany dialog.

Format, który zadziałał: opisz symptom w precyzyjnych terminach. Opisz ścieżkę kodu, którą prześledzałeś. Wymień hipotezy, które już wykluczyłeś i dlaczego. Potem zapytaj model: mając ten symptom i te dowody, czego mi brakuje?

To jest użyteczne z dwóch powodów. Po pierwsze, jasne artykułowanie problemu AI wymusza rodzaj systematycznego myślenia, które często naprowadza na odpowiedź zanim AI cokolwiek powie. Po drugie, AI czasem widzi coś, co przeoczyłeś — nazwę zmiennej, która nie pasuje do jej użycia, błąd o jeden, który staje się widoczny gdy wzorzec jest sformułowany wprost.

Jeden z inżynierów na warsztatach spędził czterdzieści minut na bugu przed sesją. Podczas sesji opisał go Claude'owi w ustrukturyzowanych terminach i dostał odpowiedź w pierwszej odpowiedzi. Bug był niepoprawnym sprawdzeniem null w konkretnym warunku — czymś, co widział kilka razy i nie zobaczył. Model to zobaczył, bo inżynier opisał symptom wystarczająco precyzyjnie, że sprawdzenie było jedynym sensownym wyjaśnieniem.

### Nazewnictwo i komentarze jako tani sposób na czytelność

To najtańsza poprawa, jaką możesz zrobić w legacy codebasie, i jedna z najwartościowszych.

Daj AI funkcję lub zmienną ze złą nazwą i poproś o lepsze alternatywy. Daj nieudokumentowaną funkcję i poproś o komentarz wyjaśniający jej cel i parametry. To są operacje zajmujące sekundy, które sprawiają, że kolejna osoba otwierająca plik jest mierzalnie szybsza.

To jest też bezpieczne: zmiana nazw i dodawanie komentarzy nie zmienia zachowania. To najniżej ryzykowna kategoria ulepszeń, i AI może to robić szybciej i spójniej niż programista ręcznie piszący dokumentację.

## Moment przełomu

Moment, który zmienił ścieżkę legacy, nie był przełomem technicznym. Był obserwowaniem inżyniera, który powiedział "to nie zadziała", jak zaczyna używać AI systematycznie, bez podpowiedzi, przy tickecie, który odkładał od dwóch tygodni.

Miał złożoną funkcję filtrującą, która łączyła kilka reguł biznesowych w sposób, który z czasem stał się niejasny. Unikał jej dotykania, bo nie był pewien, że rozumie ją wystarczająco dobrze, żeby bezpiecznie modyfikować.

Poprosił Claude'a o wyjaśnienie funkcji. Dostał jasne wyjaśnienie. Poprosił Claude'a o sugestię gdzie mógłby dodać nowy warunek filtrowania bez łamania istniejącej logiki. Dostał konkretną propozycję. Przejrzał propozycję uważnie, zmodyfikował ją na podstawie swojej wiedzy o regułach biznesowych i zastosował.

Ticket, który leżał dwa tygodnie, był zrobiony w jakieś czterdzieści minut.

Co się zmieniło, to nie był kod. Co się zmieniło, to to, że miał sposób podejścia do niepewności, która go blokowała. AI nie zastąpił jego ekspertyzy — dał mu punkt startowy, żeby ekspertyza nie musiała wykonywać całej pracy orientacji od zera.

## Praktyczny framework: jak używać AI z legacy bez psucia rzeczy

Na podstawie tego co zadziałało i co nie zadziałało, oto framework, który dałbym każdemu zespołowi zaczynającemu używać AI z legacy codebasem:

**1. Zacznij od czytania, nie pisania.** Używaj AI do rozumienia istniejącego kodu zanim do jego modyfikowania. Buduj pewność w jakość wyjaśnień zanim zaufasz sugestiom zmian.

**2. Generuj testy charakteryzacyjne przed refaktoryzowaniem czegokolwiek.** To nie podlega negocjacji. Bez siatki bezpieczeństwa, refaktoring wspomagany przez AI jest zbyt ryzykowny w systemach, których w pełni nie rozumiesz.

**3. Refaktoryzuj w jak najmniejszych krokach.** AI sprawia, że kuszące jest robienie dużych zmian, bo duże zmiany są łatwe do wygenerowania. Opieraj się temu. Małe kroki są bezpieczniejsze i łatwiejsze do weryfikacji.

**4. Zachowaj dyscyplinę czytania każdej zmiany.** Nie aplikuj kodu wygenerowanego przez AI bez czytania go. Legacy codebasy mają niejawne kontrakty i zależności, o których AI nie wie.

**5. Używaj AI do żmudnych części, ludzkiego osądu do konsekwentnych części.** AI generuje testy charakteryzacyjne, wyjaśnia nieznany kod i sugeruje nazwy. Ludzie decydują które zachowanie jest poprawne, który refaktoring jest bezpieczny mając kontekst biznesowy, i który dług techniczny spłacić w jakiej kolejności.

## Co się faktycznie zmieniło, a co nie

Po warsztatach coś się przesunęło w tym, jak programiści ze ścieżki legacy pracowali. Zmiana była realna, ale konkretna.

**Co się zmieniło:** Tendencja do unikania nieznanego kodu zmniejszyła się. Programiści, którzy spędzaliby godziny zdezorientowani modułem, teraz zaczynali od wyjaśnienia AI, szybko się orientowali i spędzali te godziny na rzeczywistym problemie. Zaległość "muszę to rozumieć zanim to dotknę" zaczęła się ruszać.

**Co się nie zmieniło:** Potrzeba inżynierskiego osądu. AI nie może zdecydować, czy architektura legacy powinna być zachowana czy migrowana. Nie może ustalać priorytetów. Nie może podejmować decyzji, który dług techniczny jest wystarczająco ważny, żeby go teraz adresować. Te decyzje wciąż wymagają tej samej ekspertyzy, co zawsze.

Najbardziej uczciwe podsumowanie: AI sprawił, że żmudne części pracy z legacy są szybsze, co uwolniło czas i energię poznawczą na części, które naprawdę wymagają doświadczonego inżyniera. Nie sprawił, że praca z legacy jest łatwa. Sprawił, że jej części są mniej trudne.

Dla zespołu utrzymującego system, który działa w produkcji od ponad dekady — to nie jest mała rzecz.

---

*Następny w tej serii: co uczestnicy warsztatów mówili dwa tygodnie później — uczciwa retrospektywa tego, co zostało, a co nie.*
