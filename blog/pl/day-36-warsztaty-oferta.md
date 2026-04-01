---
day: 36
title: "Przeprowadzam warsztaty AI dla zespołów deweloperskich. Co jest w ofercie — i dla kogo to nie jest."
pillar: Trenches
language: pl
image: ../../images/day-36.jpg
image_unsplash_query: "workshop training developers team whiteboard"
---

# Przeprowadzam warsztaty AI dla zespołów deweloperskich. Co jest w ofercie — i dla kogo to nie jest.

To jest post, w którym opisuję, co faktycznie oferuję. Postaram się, żeby był użyteczny niezależnie od tego, czy mnie zatrudnisz — bo jeśli opis jest wystarczająco konkretny, żeby ocenić ofertę, jest też wystarczająco konkretny, żeby pomyśleć o tym, czego Twój zespół faktycznie potrzebuje.

## Skąd to pochodzi

Jestem Tech Leadem w Insly — europejskim InsurTech SaaS — nasze rozwiązania AI przetwarzają ponad 150 000 dokumentów miesięcznie. Mój zespół 15 inżynierów buduje systemy AI w produkcji od ponad roku — AWS Bedrock, LightRAG, Python, Go, integrując AI z codebasem obejmującym komponenty Symfony sięgające roku 2012. Nauczyliśmy się co działa i co nie działa na własnej skórze.

Kilka miesięcy temu przeprowadziłem warsztaty AI dla 15 innych programistów w Insly — ludzi pracujących na tym samym codebasie, ale nie w moim zespole AI. Inżynierów zajmujących się legacy PHP, wieloletnią architekturą, standardowymi problemami rosnącego produktu SaaS. Zrobiłem to, bo patrzyłem jak dobrzy ludzie tracą czas i pewność siebie na rzeczy, z którymi AI mogło im pomóc — jak ktoś im to pokaże.

Trzy dni praktycznych sesji. Dwa tory: nowe projekty i legacy kod. Żadnych slajdów bez kodu. Żadnej teorii bez praktyki.

Trzy tygodnie później napisałem uczciwe sprawozdanie z tego, co się zmieniło. Część się zmieniła. Część nie. Szczegóły są w poprzednim poście.

Teraz oferuję to samo innym zespołom.

## Co obejmują warsztaty

### Tor 1: AI-first w nowych projektach

To obejmuje to, jak wygląda Twój workflow deweloperski, gdy AI jest uczestnikiem od dnia zero — nie narzędziem, które dodajesz na końcu.

Konkretnie:

**Wymagania pod presją.** Jak używać AI do testowania odporności wymagań zanim zaczniesz budować — łapanie luk, niejednoznaczności i konfliktów, kiedy ich naprawa jest tania. Samo to zmienia sposób, w jaki przebiegają rozmowy planistyczne.

**Eksploracja architektury.** Jak przejść od pustej strony do trzech dobrze uzasadnionych opcji z jawnymi kompromisami w 30 minut zamiast trzech godzin. Jak pozostać za kierownicą, gdy model generuje opcje. Jak rozpoznać, kiedy sugestie AI są subtelnie błędne dla Twojej domeny.

**Pętle implementacyjne.** Konkretna dyscyplina programowania wspomaganego AI, która produkuje kod, który rozumiesz i posiadasz — nie vibecoded output, który działa dopóki nie przestaje. Jak dostrajać rozmiar pętli. Jak efektywnie używać Cursora do backend developmentu (Go, Python, PHP — zależy od Twojego stacku).

**AI code review jako podniesienie podłogi.** Konkretny szablon promptu do pre-review zanim ludzcy reviewerzy zobaczą kod. Co łapie konsekwentnie. Czego konsekwentnie nie łapie (i dlaczego ludzkie review pozostaje niezbędne).

**Generowanie testów bez żmudności.** Jak używać AI do generowania przypadków testowych, które byś pominął — szczególnie edge case'ów — i jak oceniać, które wygenerowane testy faktycznie testują właściwe rzeczy.

### Tor 2: AI w legacy kodzie

To jest trudniejszy problem, i ten, który większość warsztatów ignoruje. Większość Twoich inżynierów prawdopodobnie pracuje z kodem, który ma 5-10 lat. Techniki pracy wspomaganej AI w tym kontekście są inne niż w greenfield developmencie.

**Strategie dostarczania kontekstu.** Jak dać asystentowi AI wystarczająco dużo kontekstu o systemie legacy, żeby dostać użyteczne odpowiedzi — gdy nie możesz po prostu wkleić całego codebase'u. Architektoniczne podsumowania, ukierunkowane wstrzykiwanie kontekstu, praca z mniejszymi wycinkami.

**Refaktoryzacja z AI.** Jak używać AI do proponowania podejść refaktoryzacyjnych i identyfikowania ryzyk w każdym — bez tracenia wiedzy instytucjonalnej wbudowanej w istniejący kod.

**Debugowanie z AI.** Opisywanie wzorców błędów, stack trace'ów i nieoczekiwanego zachowania AI jako pierwszy krok diagnostyczny. Jak uzyskać użyteczny sygnał nawet gdy model nie zna Twojego systemu. Jak zmniejszyć koszt przerwań u senior inżynierów od pytań debugowania juniora.

**Bezpieczne stopniowe usprawnianie.** Jak dodawać pokrycie testowe do nieprzetestowanego legacy kodu używając AI do generowania testów, a następnie używać tych testów do bezpiecznej refaktoryzacji.

**Gdzie AI gubi się w legacy kodzie.** Konkretne tryby awarii — przestarzałe wzorce, zachowanie specyficzne dla frameworka, niejawne założenia domenowe — i jak je obchodzić.

## Czego nie obejmują warsztaty

Chcę być w tym wyraźny, bo jasność zakresu unika rozczarowania.

Warsztaty nie obejmują funkcji produktowych AI — budowania chatbotów, wdrażania RAG, deployowania modeli AI. To inny zestaw umiejętności. To, co omawiam, to używanie AI w samym procesie tworzenia oprogramowania.

Warsztaty nie obejmują strategii AI ani analizy ROI. Nie jestem konsultantem zarządczym. Jeśli potrzebujesz zbudowanego business case'u dla inwestycji w AI, to inne zaangażowanie.

Warsztaty nie dają Ci narzędzia, które instalujesz i zapominasz. Dają Twojemu zespołowi zestaw praktyk, które wie jak stosować. Ciągła dyscyplina należy do Ciebie.

## Kto korzysta najbardziej

Programiści, którzy czerpią z takich warsztatów najwięcej, mają kilka wspólnych cech:

**Doświadczeni inżynierowie, którzy unikali AI.** Inżynierowie z 5-10 latami doświadczenia, którzy mają silne instynkty, ale nie uczynili AI nawykiem. Najtrudniej do nich dotrzeć przez samodzielne uczenie się, bo są zajęci, bo krzywa uczenia wydaje się regresem i bo początkowe wyniki z przypadkowego używania AI są często wystarczająco rozczarowujące, by potwierdzić ich sceptycyzm. Ustrukturyzowane, hands-on środowisko z praktykiem rozumiejącym ich kontekst to zmienia.

**Zespoły z mieszanymi projektami.** Dwutorowa struktura warsztatów jest specjalnie zaprojektowana dla zespołów pracujących zarówno nad nowymi funkcjami, jak i utrzymaniem legacy. Większość zespołów robi obie te rzeczy. Generyczne treści AI w ogóle nie adresują problemu legacy.

**Zespoły potrzebujące wspólnego słownictwa.** Jeden niedoceniany benefit warsztatów vs. indywidualne samouczenie: wszyscy uczą się tych samych rzeczy. Rozmowy code review zmieniają się, gdy zarówno reviewer, jak i reviewee wiedzą, co oznacza "AI pre-review" i używali tych samych szablonów. Wspólna praktyka jest cenniejsza niż indywidualna.

## Dla kogo to nie jest

Bycie jasnym w kwestii tego, kto nie powinien mnie zatrudniać, jest bardziej użyteczne niż przekonywanie wszystkich.

**Zespoły bez istniejącego zaplecza inżynierii oprogramowania.** To nie jest intro do programowania z AI. Twoi programiści muszą być w stanie oceniać wygenerowany kod. Jeśli jeszcze nie mogą, będą używać AI w sposób tworzący dług techniczny, którego nie widzą.

**Zespoły szukające jednogodzinnego keynote'u.** To, co robię, to trzy dni hands-on pracy. Jeśli chcesz inspiracyjnego wystąpienia o przyszłości AI, są doskonałe osoby do tego. To, co oferuję, jest inne.

**Zespoły, które chcą, żeby decyzje AI były podjęte za nie.** Warsztaty transferują wiedzę i praktykę — nie przynoszą mandatu dotyczącego narzędzi ani roadmapy do wdrożenia. Twój zespół podejmuje własne decyzje po. Jeśli potrzebujesz kogoś, kto przeprowadzi Twoją implementację AI, to jest zaangażowanie consultingowe, nie warsztaty.

**Zespoły, gdzie decydenci nie wierzą w relevantność AI.** Jeśli warsztaty dzieją się dlatego, że ktoś wyżej nalegał i zespół jest "wysyłany", warunki psychologicznego bezpieczeństwa do prawdziwego uczenia się nie będą istniały. Najlepsze wyniki pojawiają się, gdy przynajmniej tech leadzi są naprawdę ciekawi.

## Business case

Zrobię to konkretnym, bo abstrakcyjne twierdzenia o ROI są bezużyteczne.

Senior developer kosztuje gdzieś między 150 000 a 250 000 EUR rocznie w całkowitym koszcie, w zależności od lokalizacji i stażu. Jeśli workflow wspomaganego AI oszczędzają dwie godziny tygodniowo — ostrożne szacowanie, oparte na tym, co obserwuję w moim własnym zespole — to około 100 godzin rocznie na developera. Po pełnym koszcie to 7 000-12 000 EUR na developera rocznie w odzyskanym czasie.

Dla 10-osobowego zespołu to 70 000-120 000 EUR rocznie, jeśli nawyki się utrzymają.

Warsztaty nie gwarantują tych liczb. Żaden odpowiedzialny praktyk nie gwarantowałby. Co robią, to dają Twojemu zespołowi konkretną wiedzę i wspólną praktykę, by te nawyki były osiągalne — zamiast zostawiać to każdemu developerowi do samodzielnego odkrycia, a niektórzy nigdy tam nie dochodzą.

Inwestycja w warsztaty to ułamek rocznego kosztu jednego developera.

## Co dzieje się przed i po

**Przed:** Godzinna rozmowa rozpoznawcza. Chcę zrozumieć Twój stack, aktualną relację Twojego zespołu z narzędziami AI, mix projektów (greenfield vs. legacy) i to, co najbardziej chcesz zaadresować. Zawartość warsztatów jest dostosowywana na tej podstawie — nie uruchamiam tych samych trzech dni dla każdego klienta.

**Podczas:** Trzy pełne dni, on-site lub zdalnie (Twój wybór). Hands-on od początku. Uczestnicy pracują w swoich własnych środowiskach deweloperskich, z własnym kodem gdzie to możliwe. Ćwiczenia w małych grupach, live demo, Q&A wbudowane przez cały czas.

**Po:** Opcjonalny check-in po dwóch tygodniach. Asynchroniczna struktura, gdzie uczestnicy dzielą się tym, co próbowali, co działa, co utknęło. Na podstawie tego, co zaobserwowałem po warsztatach w Insly, okres check-in jest momentem, gdy pojawia się druga fala pytań — te, które pojawiają się dopiero po tym, jak ludzie próbowali rzeczy w swoim realnym kontekście pracy.

## FAQ

**Czy to można zrobić zdalnie?** Tak. Przeprowadzałem pełne warsztaty zdalnie. Praca hands-on dobrze się na to przekłada. Wymiar społeczny/psychologiczny — normalizacja eksperymentowania przed kolegami — wymaga bardziej celowego prowadzenia zdalnie i dostosowałem się do tego.

**Jaki jest minimalny rozmiar zespołu?** Optymalne jest 8-20 osób. Mniej niż 8 i grupowa dynamika, która sprawia, że wspólne uczenie jest wartościowe, nie w pełni się pojawia. Więcej niż 20 i zdolność do zwracania indywidualnej uwagi na to, z czym ludzie się zmagają, spada.

**Czy pracujesz z firmami spoza Polski?** Tak. Jestem z Polski i czuję się najbardziej komfortowo w polskojęzycznym środowisku, ale prowadzę warsztaty po angielsku i robiłem to na rynkach europejskich.

**Nasz codebase jest stary i bałaganiarski — czy to problem?** To jest faktycznie bardziej interesujący przypadek, i ten, nad którym myślałem najdłużej. Zawartość Toru 2 jest specjalnie zaprojektowana na tę sytuację. "Nasz kod jest za stary na AI" to stwierdzenie, które słyszałem wiele razy i w większości przypadków okazało się błędne.

**Jakich narzędzi zakładasz?** Cursor do developmentu, Claude do ogólnej pomocy AI, specyficzne narzędzia różnią się stackiem. Nie jestem tool-agnostic w stylu "cokolwiek u Was działa" — mam opinie i dzielę się nimi. Ale będę pracować z tym, co Twój zespół już ma, gdzie to ma sens.

## Jak się skontaktować

Jeśli to brzmi relevantnie dla Twojego zespołu, właściwym pierwszym krokiem jest 30-minutowa rozmowa — bez pitch decku, bez propozycji, tylko rozmowa o tym, czy to ma sens dla Twojej sytuacji.

Napisz do mnie bezpośrednio jedno słowo:

**WARSZTATY**

Odpiszę i umówimy rozmowę. Bez presji.

Jeśli chcesz porozmawiać przed podjęciem tego kroku, zostaw komentarz tutaj lub pod postem na LinkedIn. Czytam wszystko.
