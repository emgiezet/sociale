---
day: 11
title: "Vibecoding: mnożnik produktywności czy zanik osądu inżynierskiego?"
pillar: Trenches
language: pl
image: ../../images/day-11.jpg
image_unsplash_query: "developer coding laptop focus"
---

# Vibecoding: mnożnik produktywności czy zanik osądu inżynierskiego?

Niedawno wygłosiłem prezentację, którą zatytułowałem "Czy to koniec ery programistów?" Sformułowałem ją jako pytanie celowo — bo nie sądzę, żeby uczciwa odpowiedź była prosta.

Publiczność oczekiwała, że albo będę świętować narzędzia AI do kodowania jako rewolucję, albo odrzucę je jako hype. To, w co naprawdę wierzę, jest bardziej konkretne od obu tych pozycji.

Prowadzę 15-osobowy zespół inżynierów AI w Insly — od 18 miesięcy budujemy produkcyjne systemy AI w regulowanej branży. Oto czego to doświadczenie naprawdę mnie nauczyło o vibecoding.

## Czym Jest Vibecoding

"Vibecoding" to praktyka opisywania AI — w naturalnym języku lub przybliżonym pseudokodzie — co chcemy, żeby kod robił, i zlecenia AI jego wygenerowania. Termin zaczął jako ironiczny opis prawdziwego przepływu pracy, z którego coraz więcej programistów korzysta codziennie.

To naprawdę potężne narzędzie. Przy boilerplate'ach, przypadkach testowych, dobrze znanych wzorcach, refaktoryzacji powtarzalnego kodu — asystenci AI do kodowania zmienili to, co pojedynczy programista może wyprodukować w ciągu dnia. Używam ich. Mój zespół ich używa.

Ale "potężny przy wielu zadaniach" to nie to samo co "zmienia znaczenie bycia dobrym programistą."

## Czego Vibecoding Nie Robi

Vibecoding generuje kod. Nie generuje osądu inżynierskiego.

To rozróżnienie ma znaczenie w jednych kontekstach bardziej niż w innych. W projekcie pobocznym bez użytkowników, bez wymogów compliance, bez zespołu do utrzymywania kodu — swobodne vibecoding jest całkowicie rozsądne. Stawki są niskie. Szybkość jest cenna.

W systemie produkcyjnym z 150 000 dokumentów miesięcznie, złożoną architekturą wielodostępną, zobowiązaniami z zakresu compliance ubezpieczeniowego i 15-osobowym zespołem, który będzie utrzymywał ten kod przez następne pięć lat — kalkulacja jest zupełnie inna.

Widziałem vibecoded dodatki do naszego kodebase'u, które:

→ Działają poprawnie w happy path, ale zawodzą na edge case'ach specyficznych dla naszej logiki biznesowej
→ Stosują ogólne najlepsze praktyki, ale naruszają konwencje naszego zespołu
→ Rozwiązują bezpośredni problem w sposób, który tworzy trudniejszy problem w dalszej perspektywie
→ Generują technicznie poprawny SQL, który ignoruje nasze ograniczenia izolacji wielodostępności

To nie są błędy AI. To przewidywalne wyniki narzędzia, które nie zna naszego systemu. Programista używający tego narzędzia musi znać system i oceniać wynik na tle tej wiedzy.

Doświadczeni programiści robią to naturalnie. Traktują wynik AI tak, jak traktowaliby kod od kompetentnego, ale nowego członka zespołu: dokładnie przeglądają, weryfikują założenia, refaktoryzują gdzie potrzeba.

Ryzyko nie leży w seniorach używających narzędzi AI. Leży w dwóch innych grupach.

## Dwa Wzorce Niepowodzeń

**Wzorzec niepowodzenia 1: Juniorzy, którzy zastępują vibecoding nauką.**

Juniorom dostępny jest teraz niebezpieczny skrót: mogą produkować działający kod szybciej, niż są w stanie go zrozumieć. Tworzy to iluzję kompetencji, jednocześnie uniemożliwiając rozwój rzeczywistych kompetencji. Jeśli przez dwa lata generujesz kod, którego w pełni nie rozumiesz, rozwijasz bardzo małą zdolność do oceny kodu, debugowania złożonych systemów czy podejmowania decyzji architektonicznych.

Nie sądzę, żeby to oznaczało, że juniorzy nie powinni używać narzędzi AI. Sądzę, że oznacza to, że potrzebują mentorów, którzy aktywnie zmuszają ich do rozumienia tego, co wysyłają, a nie tylko tego, że przechodzi testy.

**Wzorzec niepowodzenia 2: Organizacje, które mylą wolumen wyników z jakością.**

Niektóre zespoły zaczęły mierzyć produktywność programistów liczbą wygenerowanych linii kodu lub funkcji dostarczonych w sprincie. W świecie vibecoding obydwie te metryki mogą rosnąć, podczas gdy jakość spada. Programista, który dostarcza pięć vibecoded funkcji, z których każda wprowadza dług techniczny, nie jest pięć razy bardziej produktywny niż programista, który dostarcza jedną dobrze zaprojektowaną funkcję.

Problem mierzenia jest realny i nierozwiązany. Zespoły, które mierzą wyniki zamiast efektów, uzyskają wyniki, które mierzą — a te mogą nie być systemami, które naprawdę chcą zbudować.

## Jak Wygląda Prosperujący Programista

Programiści, którzy będą prosperować w świecie rozszerzonym o AI, to ci, którzy używają AI do szybszego działania, jednocześnie utrzymując — i poprawiając — zdolność do ostrożnego działania.

→ Używają AI do generowania pierwszych szkiców, a następnie stosują osąd, aby ukształtować je w jakość produkcyjną.
→ Używają AI do szybkiego eksplorowania opcji, a następnie używają wiedzy domenowej do wyboru między nimi.
→ Używają AI do automatyzacji rutyny, a następnie skupiają uwagę na naprawdę złożonych zadaniach.
→ Rozwijają metaumiejętność wiedzy, kiedy ufać wynikowi AI, a kiedy go dokładnie weryfikować.

To nie jest zagrożenie dla programistów. To szansa — dla tych, którzy ją wykorzystają.

## Prawdziwe Zagrożenie

Zagrożenie nie polega na tym, że AI pisze kod. Zagrożenie polega na tym, że niektórzy programiści będą używać AI jako powodu do zaprzestania rozwijania osądu.

Osąd — w zakresie architektury, kompromisów, tego, co kod naprawdę musi robić w prawdziwym świecie — był zawsze tym, o co tak naprawdę chodziło w tej pracy. Programiści, którzy traktowali programowanie jako "produkowanie składni", byli już zagrożeni. Programiści, którzy traktują programowanie jako "rozwiązywanie problemów", nigdy nie byli bardziej wartościowi.

Umiejętność to nie promptowanie. To wiedza, kiedy ufać wynikowi, a kiedy napisać od zera.

Jakie są Twoje doświadczenia z narzędziami AI do kodowania w środowiskach produkcyjnych? Naprawdę jestem ciekaw, czy inni widzą te same wzorce.
