---
day: 28
title: "Wszystko czego nauczyłem się w 18 miesiącach wdrażania AI w ubezpieczeniach"
pillar: Educator
language: pl
image: ../../images/day-28.jpg
image_unsplash_query: "knowledge lessons learned checklist"
---

# Wszystko czego nauczyłem się w 18 miesiącach wdrażania AI w ubezpieczeniach

18 miesięcy temu stanąłem przed moim zespołem inżynierskim i powiedziałem, że zbudujemy produkcyjny system RAG do pobierania dokumentów ubezpieczeniowych. Miałem pewność co do kierunku technologicznego, umiarkowaną pewność co do naszego podejścia technicznego i prawie żadnego pojęcia, jak wiele jeszcze nie wiedziałem.

18 miesięcy później mamy produkcyjne systemy AI obsługujące prawdziwych użytkowników, framework ewaluacyjny śledzący jakość w czasie i zestaw lekcji zdobytych trudną drogą, które chciałbym mieć na początku.

Ten post to wszystko, co powiedziałbym sobie na początku.

## Lekcje architektoniczne

**Model nie jest zmienną.** To była najdroższa lekcja do nauczenia się i najważniejsza. Kiedy nasz pierwszy prototyp RAG dawał 60% jakości, a trzeci 89%, model był ten sam: Claude 3.5 Sonnet na AWS Bedrock. Zmienną była architektura retrieval. Ten sam LLM na różnej infrastrukturze danych produkował radykalnie różne wyniki.

Implikacja: kiedy jakość Twojego systemu AI jest słaba, odpowiedzią prawie nigdy nie jest "użyj lepszego modelu." Odpowiedzią prawie zawsze jest "popraw swoje dane lub swój retrieval." Straciliśmy tygodnie zanim to zaakceptowaliśmy.

**Ewaluacja przed optymalizacją.** Nie zbudowaliśmy naszego frameworku ewaluacyjnego aż do szóstego tygodnia naszego pierwszego prototypu. Czas spędzony przed posiadaniem infrastruktury ewaluacyjnej był w dużej mierze zmarnowany — wprowadzaliśmy zmiany architektoniczne nie wiedząc, czy pomagają.

Właściwa kolejność: zdefiniuj swój zestaw testowy z walidacją przez eksperta domenowego, zbuduj infrastrukturę pomiarową, ustal swoją linię bazową, potem optymalizuj. Jakakolwiek iteracja przed pomiarem linii bazowej to spekulacja.

**Buduj addytywnie, nie transformatywnie.** Najbezpieczniejszy wzorzec architektoniczny dla AI w systemie produkcyjnym: możliwości AI jako niezależne, opcjonalne warstwy ze ścieżkami fallback. Flagi funkcji pozwalające na włączanie i wyłączanie indywidualnych możliwości. Oddzielne serwisy dla obciążeń ML, które mogą być wdrażane i skalowane niezależnie.

To kosztuje trochę inżynieryjnego overheadu, ale kupuje ogromne bezpieczeństwo operacyjne. Nigdy nie mieliśmy incydentu produkcyjnego, w którym awaria serwisu AI wpłynęłaby na rdzeniową funkcjonalność transakcji ubezpieczeniowych.

**Retrieval oparty na grafie dla złożonych struktur dokumentów.** Wyszukiwanie podobieństwa semantycznego ma sufit w domenach, gdzie dokumenty wzajemnie się odwołują. Polisy ubezpieczeniowe, umowy prawne, wytyczne medyczne, ramy regulacyjne — to domeny, gdzie klauzula ma pełny sens tylko w kontekście innych klauzul. Retrieval oparty na grafie LightRAG przechwytuje te relacje. Standardowe wyszukiwanie wektorowe tego nie robi.

**Język ma większe znaczenie niż ludzie przyznają.** Polskojęzyczne dokumenty ubezpieczeniowe wymagają polskojęzycznych modeli. Testowaliśmy Bielika konkretnie dlatego, że generyczne modele wielojęzyczne degradowały jakość na specyficznym dla domeny tekście polskim. Nasza ewaluacja wykazała poprawę precyzji o 12 punktów procentowych w porównaniu z podejściem tłumaczeniowym. Dopasuj model do języka swoich danych.

## Lekcje compliance

**Projektuj dla ludzkiego nadzoru od pierwszego dnia.** W branżach regulowanych "AI tak powiedziało" to nieakceptowalne wyjaśnienie. Projektuj swoje systemy AI z widocznym rozumowaniem, jasnym wydobywaniem dowodów i ludzkim potwierdzeniem dla high-stakes outputs od samego początku.

Retrofitowanie ludzkiego nadzoru do systemu zaprojektowanego wokół autonomii AI jest drogie i często architektonicznie bolesne. Rozmowa o wymogach nadzoru przed projektowaniem kosztuje jedno spotkanie. Rozmowa po zbudowaniu kosztuje tygodnie.

**RODO ogranicza to, co trafia do Twojego vector store.** To brzmi oczywisto w retrospekcji. Nie było oczywiste kiedy budowaliśmy. Dane osobowe — imiona ubezpieczających, adresy, informacje finansowe — mają konkretne wymogi obsługi w ramach RODO, które stosują się gdy te dane są embeddowane i przechowywane w indeksie wektorowym. Musieliśmy przeprojektować nasze podejście do indeksowania, żeby zapewnić przestrzeganie zasad minimalizacji danych.

Zaangażuj swojego Inspektora Ochrony Danych lub prawnika compliance przed zbudowaniem pipeline'u do wchłaniania dokumentów i tworzenia embeddingów. W Polsce, praca w ramach wymogów KNF (Komisja Nadzoru Finansowego) dodaje kolejną warstwę — te muszą być rozumiane przed podjęciem decyzji architektonicznych, nie po.

**Zaangażuj compliance wcześnie.** Każde "to nie jest zgodne z regulacjami" zgłoszone po wdrożeniu wymaga zmian projektowych, możliwie remediacji danych i potencjalnie komunikacji z użytkownikami. Ta sama rozmowa zgłoszona przed projektowaniem kosztuje spotkanie.

**LLM nie powinny podejmować deterministycznych decyzji.** Obliczenia składek, ustalenia zakresu ubezpieczenia, interpretacje prawne: zostają w systemach deterministycznych. AI asystuje ludziom. Nie zastępuje audytowalnej logiki. Ta granica to nie ograniczenie techniczne — to wymóg compliance i wymóg zaufania.

## Lekcje dotyczące zespołu

**Lęk przed utratą kompetencji to realna siła.** Doświadczeni inżynierowie, którzy przez lata byli ekspertami w swoich domenach, nie lubią być ponownie początkującymi. Transformacja AI tworzy sytuacje, gdzie staż nie pomaga — gdzie developer z 15-letnim doświadczeniem w PHP uczy się obok developerów z 3-letnim całkowitym doświadczeniem.

Jawne nazywanie tego, tworzenie bezpieczeństwa psychologicznego dla "jeszcze nie wiem" i nagradzanie zachowań uczenia się tak samo jak zachowań dostarczania to rzeczy, które chciałbym robić bardziej jawnie od początku.

**Eksperci domenowi to Twój najcenniejszy zasób ewaluacyjny.** Inżynierowie w moim zespole to doskonali inżynierowie oprogramowania. Nie są ekspertami ubezpieczeniowymi. Różnica między poprawną odpowiedzią o klauzuli ubezpieczeniowej a brzmiącą wiarygodnie błędną odpowiedzią to rozróżnienie, które underwriterzy robią natychmiast, a inżynierowie dopiero po wyszkoleniu.

Dla każdej aplikacji AI specyficznej dla domeny, jakość ewaluacji jest ograniczona przez dostęp do wiedzy domenowej. Budowanie relacji z underwriterami, brokerami i likwidatorami szkód, którzy uczestniczyli w sesjach ewaluacyjnych, było jedną z inwestycji o najwyższej dźwigni.

## Lekcje procesowe

**Zacznij od wąskiego zakresu.** Zespoły, które próbują budować kompleksowe systemy AI, zawodzą częściej niż zespoły, które zaczynają od jednego wąskiego, dobrze zdefiniowanego przypadku użycia, udowadniają że działa i rozszerzają się z tej bazy.

**Cotygodniowe dema z prawdziwymi użytkownikami.** Miesięczne przeglądy interesariuszy są zbyt wolne dla cykli informacji zwrotnej development AI. Przestawiliśmy się na cotygodniowe dema z rzeczywistymi underwriterami używającymi systemu dla prawdziwych zapytań. Informacje zwrotne z tych sesji kształtowały nasz development bardziej niż jakakolwiek metryka.

**Najpierw projektuj ścieżkę błędu.** Dla każdej funkcji AI: co się dzieje gdy jest błędna? Co się dzieje gdy jest niepewna? Co się dzieje gdy jest całkowicie niedostępna? Te pytania powinny być odpowiedziane przed projektowaniem szczęśliwej ścieżki. W branżach regulowanych obsługa błędów często podlega tym samym wymogom compliance co pomyślne wyniki.

**Vibecoding to narzędzie, nie strategia.** Asystenci kodowania AI przyspieszają development w znanych domenach. W systemach regulowanych wygenerowany kod musi być rozumiany zanim będzie zaufany. Szybkość bez zrozumienia to dług techniczny na dużą skalę.

## Lekcje dotyczące oczekiwań

**AI to nie skrót.** To inny rodzaj trudności. Złożoność ewaluacji, wymogi przygotowania danych i overhead operacyjny są realne. Ludzie przychodzący do pracy z AI spodziewając się, że będzie trudna — tylko trudna w inny sposób — adaptują się szybciej.

**Pierwszy prototyp to curriculum.** Budżetuj go. Planuj to, czego się z niego nauczysz, nie to, co wyślesz. Prototyp, który uczy Cię jaki jest prawdziwy problem, wykonał swoją pracę.

**Największą konkurencją jest zmiana procesu, nie technologia.** Adopcja AI w organizacji to przede wszystkim wyzwanie zmiany sposobu podejmowania decyzji przez organizację. Klarowność co do tych pytań wymaga zarządzania zmianą, nie inżynierii.

**Wzorce compliance przenoszą się między domenami.** PSD2, RODO, regulacje ubezpieczeniowe, Ustawa AI UE — te ramy dzielą strukturę: audytowalność, minimalizacja danych, wyraźna zgoda, prawo do usunięcia. Naucz się jednych dogłębnie, a reszta staje się znacznie szybsza do zrozumienia.

Zacznij od technologii na drugim miejscu. Zacznij od architektury decyzji na pierwszym. Technologia podąży.
