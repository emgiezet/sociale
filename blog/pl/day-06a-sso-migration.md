---
day: 6
title: "Migracja SSO bez przestojów w skali: to czego analizy post-mortem nie mówią"
pillar: Builder
language: pl
image: ../../images/day-06.jpg
image_unsplash_query: "security authentication enterprise"
---

# Migracja SSO bez przestojów w skali: to czego analizy post-mortem nie mówią

Kiedy ludzie pytają o naszą migrację Microsoft SSO w Insly, chcą wiedzieć o przepływach OAuth, architekturze multi-tenancy, obsłudze tokenów. Te rzeczy mają znaczenie. Ale migracja nie powiodła się dlatego, że dobrze poradziliśmy sobie ze szczegółami technicznymi. Powiodła się, bo dobrze poradziliśmy sobie z koordynacją.

Ten artykuł dotyczy części, którą techniczne analizy przypadków zwykle pomijają.

## Punkt startowy

Insly przetwarza ponad 150 000 dokumentów miesięcznie — brokerów ubezpieczeniowych, underwriterów i personel administracyjny na europejskich rynkach. Wielu naszych klientów enterprise działa na Microsoft 365, co oznacza, że ich pracownicy są już uwierzytelnieni przez platformę tożsamości Microsoft do wszystkiego innego w pracy.

Żądanie przyszło od wielu dużych klientów jednocześnie: pozwólcie naszym pracownikom używać poświadczeń Microsoft do logowania do Insly. Nie zmuszajcie ich do utrzymywania oddzielnego hasła. Zintegrujcie się z naszym istniejącym tenant Microsoft.

To standardowe żądanie funkcji enterprise. „Po prostu dodaj SSO."

## Dlaczego to jest naprawdę trudne

Złożoność techniczna była realna. Nasza architektura jest multi-tenant, z każdą organizacją brokera działającą w ścisłej izolacji. Dodanie SSO wymagało mapowania tożsamości tenant Microsoft na przynależność do organizacji Insly bez ich mieszania. Różne konfiguracje tenant Microsoft mają różne zachowania OAuth 2.0. Klienci enterprise często mają polityki bezpieczeństwa ograniczające, które zewnętrzne aplikacje mogą uczestniczyć w przepływach SSO.

Ale problemy techniczne miały rozwiązania techniczne. Wsparcie biblioteczne dla Microsoft MSAL jest dojrzałe. AWS Cognito, którego używamy do zarządzania tożsamością, integruje się czysto z zewnętrznymi dostawcami tożsamości.

Trudniejszymi problemami były problemy koordynacji.

## Problemy koordynacji

**Problem 1: Przegląd bezpieczeństwa IT enterprise.** Każdy duży klient, którego migrowaliśmy, potrzebował zatwierdzenia od swojego zespołu IT security przed włączeniem SSO. Oznaczało to dostarczenie dokumentacji naszej implementacji OAuth, obsługi tokenów, zarządzania sesjami i procedur reagowania na incydenty. Niektóre zespoły IT miały cykle przeglądów od czterech do sześciu tygodni. Niektóre miały wymagania, których nie przewidzieliśmy — określone czasy życia tokenów, określone zachowanie wylogowania, określone logowanie audytu.

Zaczęliśmy zbierać te wymagania trzy miesiące przed pierwszą migracją. I tak napotkaliśmy niespodzianki.

**Problem 2: Dopasowywanie kont.** Kiedy konto Microsoft użytkownika jest po raz pierwszy łączone z jego kontem Insly, musimy je dopasować. To brzmi prosto, dopóki nie napotkasz: wielu kont Insly z tym samym adresem email (dzieje się to częściej niż myślisz), adresów email, które się zmieniły od czasu założenia konta Insly, współdzielonych kont, z których korzystało wiele osób pod jednym emailem.

Każda anomalia wymagała ręcznego przeglądu i decyzji. Opracowaliśmy protokół dopasowywania i przeprowadziliśmy pełne dopasowanie dla każdego klienta przed jego oknem migracji, flagując wyjątki do ręcznego przeglądu.

**Problem 3: Sekwencjonowanie rollout.** Nie mogliśmy jednocześnie migrować wszystkich klientów. Musieliśmy ich sekwencjonować — zaczynając od mniejszych klientów, którzy mogli służyć jako populacja testowa, przechodząc do większych klientów z bardziej złożonymi konfiguracjami. Każda migracja wymagała dedykowanego okna z dostępnym zespołem IT klienta, checklisty przed migracją i okresu monitorowania po migracji.

W ciągu sześciu miesięcy zmigrowaliśmy ponad 30 organizacji klientów.

## Podejście techniczne, które sprawiło to bezpiecznym

Mając złożoność koordynacji, podjęliśmy dwie decyzje architektoniczne, które były od początku nie do negocjacji:

**Feature flagi, nie migracje big-bang.** System SSO był budowany obok istniejącego systemu uwierzytelniania, nie zastępując go. Feature flag per-organizacja decydował, którą ścieżkę uwierzytelniania dany użytkownik obierze. Włączenie SSO dla klienta było zmianą konfiguracji, nie wdrożeniem.

**Zawsze dostępny fallback.** Przez co najmniej 30 dni po włączeniu SSO dla klienta, jego użytkownicy nadal mogli logować się starymi poświadczeniami jeśli SSO zawiedzie z jakiegokolwiek powodu. Nie chodziło o nieufność do naszej implementacji — chodziło o rzeczywistość, że środowiska IT enterprise mają swoją własną dynamikę. Konfiguracja tenant Microsoft może się zmienić. Polityka IT może zostać zaktualizowana. Mając fallback, nasza migracja nigdy nie była zależnością dla dostępu klienta do jego oprogramowania.

Te dwie decyzje dodały złożoności do implementacji, ale usunęły ryzyko z każdego pojedynczego zdarzenia migracji. Trade-off był oczywiście słuszny z perspektywy czasu. Nie był oczywisty zanim go podjęliśmy.

## Co naprawdę oznacza 0 przestojów

Mieliśmy 0 przestojów podczas okresu migracji. Ale „przestoje" to wąska metryka. Mieliśmy:

→ Dwa błędy uwierzytelniania SSO dla konkretnych użytkowników w pierwszym tygodniu (rozwiązane przez korekcje dopasowania tożsamości)
→ Jednego klienta, gdzie ścieżka fallback auth była używana przez trzy dni, podczas gdy ich zespół IT rozwiązywał problem konfiguracji tenant
→ Jednego klienta, który poprosił o rollback migracji po tym, jak SSO ujawniło, że ich lista użytkowników zawierała 40 nieaktywnych kont, o których nie wiedzieli

Żaden z nich nie był incydentem krytycznym. Wszystkie byłyby, gdybyśmy nie zbudowali infrastruktury koordynacji do ich szybkiego wykrywania i reagowania.

Infrastruktura koordynacji — wspólne kanały Slack z zespołami IT klientów, codzienne odprawy podczas aktywnych okien migracji, dashboard statusu migracji per-klient — była tak samo ważna jak implementacja techniczna.

## Lekcja dla każdej migracji na dużą skalę

Jeśli planujesz migrację dotykającą Twojego systemu auth, modelu danych lub jakiejkolwiek innej warstwy fundamentalnej — oto heurystyka, którą Ci dam:

Oszacuj czas inżynierski. Pomnóż przez trzy i zabudżetuj to na koordynację.

Nie dlatego, że inżynieria jest łatwa. Dlatego, że koordynacja decyduje o tym, czy wysiłek inżynierski prowadzi do bezpiecznej, udanej zmiany czy do wysokiego ryzyka zdarzenia, które naraża użytkowników.

Najlepsza migracja, jaką kiedykolwiek widziałem, to nie ta z najbardziej elegancką architekturą. To ta, w której każda osoba, która potrzebowała wiedzieć coś, wiedziała to zanim musiała to wiedzieć.

Jakie są Twoje doświadczenia z migracjami na dużą skalę — zmianami auth, transformacjami baz danych, wersjonowaniem API w skali? Jakie wyzwanie koordynacji Cię zaskoczyło?
