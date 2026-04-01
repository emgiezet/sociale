---
day: 35
title: "Trzy tygodnie po warsztatach: co naprawdę się zmieniło"
pillar: Trenches
language: pl
image: ../../images/day-35.jpg
image_unsplash_query: "team meeting developers collaboration office"
---

# Trzy tygodnie po warsztatach: co naprawdę się zmieniło

Trzy tygodnie po przeprowadzeniu warsztatów AI dla 15 programistów w Insly chcę napisać uczciwe sprawozdanie. Nie to nadmuchane. Nie to rozczarowujące. To, które jest naprawdę prawdziwe.

Oto uczciwa odpowiedź: wiele się zmieniło, część się nie zmieniła, a to, co się zmieniło, nie jest tym, co pojawia się na dashboardach produktywności.

## Zmiany, których szukałem — i których nie dostałem

Zacznę od tego, co miałem nadzieję zobaczyć, ale nie mogę twierdzić, że zobaczyłem: mierzalne wzrosty produktywności. Nie przeprowadzałem kontrolowanego badania. Nie mam liczb velocity przed i po. Każdy, kto mówi, że przeprowadził 3-dniowe warsztaty AI i zmierzył 40% wzrost produktywności, albo mierzy złą rzecz, albo mówi Ci to, co chcesz usłyszeć.

To, co mam, jest bardziej użyteczne: obserwacje zmiany zachowania. Konkretne rzeczy, które ludzie robią inaczej teraz niż trzy tygodnie temu. To ma większe znaczenie niż ankiety po warsztatach, które mierzą entuzjazm, nie zmianę.

## Krzywa, o której nikt nie mówi

Jest krzywa adopcji AI w zespole, którą obserwowałem zarówno w moim własnym zespole inżynierskim w Insly, jak i teraz w innej grupie programistów:

**Sceptycyzm.** Przed warsztatami dominującym trybem było unikanie z niejasnym poczuciem winy. "Powinienem tego używać." Ale narzędzia wydawały się przytłaczające, krzywa uczenia się stroma, a ryzyko wyjścia na niekompetentnego przez zrobienie tego źle — realne. Doświadczeni inżynierowie są na to szczególnie narażeni — ktoś z 10-letnimi instynktami nie chce być znowu nowicjuszem.

**Ciekawość.** Pierwszy dzień warsztatów to otworzył. Nie dlatego, że pokazałem im magię, ale dlatego, że pokazałem nudne rzeczy — konkretne, praktyczne, powtarzalne rzeczy, które mogli robić następnego ranka. Ciekawość to nie jest inspiracja. To jest "zastanawiam się, czy to działa też dla mojej rzeczy."

**Pierwsze sukcesy.** Pierwszy sukces ma nieproporcjonalne znaczenie. Jeden programista powiedział mi, mniej więcej tydzień po warsztatach: "Utknąłem na dziwnym edge case'ie w Symfony i po prostu opisałem to Claude'owi. Odblokował mnie w pięć minut. Spędziłbym na tym godzinę." To nie jest liczba produktywności. To jest punkt danych, który resetuje domyślne założenie z "prawdopodobnie nie pomoże" na "warto spróbować."

**Nawyk.** Tu jesteśmy po trzech tygodniach. Częściowe formowanie nawyku. Niektórzy są solidnie w tym. Niektórzy zanurzają się okazjonalnie. Kilka osób jest wciąż w trybie "muszę się do tego zabrać." To normalne. Nawyki nie formują się równomiernie w zespole.

## Co zaobserwowałem — konkretnie

Chcę być konkretny, bo niejasne raporty o "ludziach używających AI więcej" są bezużyteczne. Oto, co faktycznie widziałem:

**Jeden senior developer zaczął dodawać notatkę "AI review" do swoich PR.** Przed wysłaniem do ludzkiego review przepuszcza diff przez Claude z konkretnym promptem i dodaje sekcję w opisie PR: co AI oznaczyło i jak to zaadresował (lub dlaczego nie). Jego reviewerzy powiedzieli mi, że zauważyli spadek małych komentarzy review — tych rzeczy, które wcześniej zaśmiecały wątek.

**Jedna programistka, która unikała pisania testów, zaczęła pisać testy.** Jej wyjaśnienie: "Odkładałam pokrycie tego starego modułu od miesięcy. Opisałam go Claude'owi i dostałam pierwszy zestaw przypadków testowych, z którymi mogłam pracować. W zeszłym tygodniu napisałam testy do trzech modułów." Nagle nie pokochała pisania testów. Energia aktywacji spadła wystarczająco, żeby to zrobiła.

**Pytania w team chacie się zmieniły.** Przedtem: "Jak zrobić X w Go?" (pytane do innych ludzi, odpowiadane przez innych ludzi). Po, coraz częściej: "Zapytałem Claude'a o X, zasugerował Y, czy to komuś wydaje się właściwe?" To inny wzorzec — AI staje się narzędziem pierwszego przejścia, ludzie stają się walidatorami. Dla ludzi to lepsze wykorzystanie czasu.

**Jeden programista na poziomie mid zaczął używać AI do debugowania.** Opisując mylący stack trace Claude'owi i pytając "co może to powodować?" jako pierwszy krok przed napisaniem do zespołu. To dokładnie ten rodzaj rzeczy, który redukuje "koszty przerwań" u senior developerów — ciągłe stukanie w ramię, które fragmentuje skupiony czas.

## Co się nie zmieniło

Chcę być w tym uczciwy, bo historia "po warsztatach" jest zwykle zbyt wypolerowana.

**Adopcja kodu legacy jest wolniejsza.** Było to przewidywalne, ale wciąż warto to nazwać. Programiści pracujący głównie ze starszym codebasem Symfony zgłaszali więcej tarcia. "Nie wiem jak dać Claude'owi wystarczająco dużo kontekstu o systemie, żeby dostać użyteczne odpowiedzi." To realny problem. Praca z legacy kodem z AI wymaga innych technik — architektoniczne podsumowania, ukierunkowane dostarczanie kontekstu, praca z mniejszymi wycinkami — i to jest bardziej zaawansowane niż to, co omówiliśmy przez trzy dni. To temat na osobne warsztaty.

**Sceptycy są nadal sceptyczni.** Nie wrogo, ale dwie lub trzy osoby w grupie są w trybie "uwierzę, kiedy zobaczę wyniki konsekwentnie." To uprawnione stanowisko. Nie blokują nikogo innego. Po prostu jeszcze nie wierzą. Nauczyłem się nie traktować sceptycyzmu jako problemu do natychmiastowego rozwiązania — daj mu czas, pozwól pierwszym sukcesom kolegów być perswazją.

**Nawyki review kodu są niespójne.** Workflow AI pre-review, który pokazałem podczas warsztatów, wymaga dyscypliny do utrzymania. Dodaje kilka minut do procesu przygotowania PR. Niektórzy robią to konsekwentnie. Niektórzy robią to kiedy pamiętają. To normalny wzorzec adopcji czegokolwiek, co dodaje małe koszty z góry na rzecz późniejszych korzyści.

## Czynnik psychologicznego bezpieczeństwa

To jest rzecz, której nie w pełni przewidziałem, i teraz myślę, że to jest najważniejsza zmienna w adopcji AI przez zespół.

Bariera do wypróbowania AI przed kolegami nie jest techniczna. Jest społeczna. Jest strach przed wyglądaniem naiwnie — przed zadaniem głupiego pytania, wygenerowaniem czegoś złego, przed tym, żeby koledzy widzieli, że nie wiesz jak używać narzędzia, które "powinieneś" znać.

Warsztaty pomogły w tym przez uczynienie eksploracji zbiorową. Wszyscy uczyli się razem, włącznie z najbardziej doświadczonymi osobami. Kiedy developer na poziomie dyrektora publicznie miał trudności z promptem podczas warsztatów i śmiał się z tego, coś się zmieniło. Otworzyła się przestrzeń na "jeszcze-nie-wiedzenie."

Trzy tygodnie później, programiści, którzy zrobili największy postęp, to ci, którzy użyli warsztatów, żeby "dostać pozwolenie" na wypróbowanie AI przed swoim zespołem. Nie sam, prywatnie, bez świadków. W normalnym kontekście pracy, gdzie ich koledzy mogli widzieć, jak eksperymentują.

To pozwolenie — społeczna normalizacja "próbuję czegoś i nie wiem czy zadziała" — to nie jest coś, co można dostać z tutorialu na YouTube. Wymaga wspólnego doświadczenia.

## Co bym zrobił inaczej

Gdybym prowadził te warsztaty ponownie — a będę — dodałbym dwutygodniową strukturę check-in. Nie spotkanie. Lekki format asynchroniczny: jedna wiadomość na osobę tygodniowo, dzieląca jedną rzecz, którą próbowali, jedną rzecz, która zadziałała, jedną rzecz, która nie zadziałała. Celem nie jest odpowiedzialność. To ciągła społeczna normalizacja eksperymentowania.

Warsztaty tworzą moment wspólnego słownictwa i wspólnego doświadczenia. Check-iny przedłużyłyby to okno zanim momentum nie rozpłynie się w normalnych wzorcach pracy.

Spędziłbym też więcej czasu na workflow z legacy kodem. Pojawiało się zbyt często przez trzy tygodnie po, żebym nadal traktował to jako edge case. To jest centralne dla tego, z czym większość pracujących inżynierów faktycznie się zmaga.

## Uczciwe podsumowanie

Trzy tygodnie po: częściowa adopcja, znacząca zmiana zachowania u części programistów, wolniejsza zmiana u innych, uczciwe luki, które następnym razem zaadresowałbym inaczej.

Czy to wystarczy, żeby nazwać warsztaty sukcesem? Myślę, że tak — nie dlatego, że liczby są dobre, ale dlatego, że zmiana jest realna i trwała. Programiści, którzy zmienili swoje nawyki, nie zrobili tego z entuzjazmu, który zblednie. Zrobili to, bo wypróbowali coś konkretnego, zadziałało i kontynuowali.

W ten sposób dzieje się trwała zmiana. Nie z inspiracji. Z dowodów.

Jeśli myślisz o przeprowadzeniu czegoś podobnego dla swojego zespołu — lub o zleceniu tego komuś — jutrzejszy post jest praktyczną odpowiedzią na to pytanie.
