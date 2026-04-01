---
day: 34
title: "AI-first od dnia zero: co pokazałem zespołowi podczas warsztatów"
pillar: Trenches
language: pl
image: ../../images/day-34.jpg
image_unsplash_query: "developer laptop coding workflow team"
---

# AI-first od dnia zero: co pokazałem zespołowi podczas warsztatów

"AI-first" brzmi jak zdecydowane hasło w prezentacji i nie znaczy prawie nic na retrospektywie. Kiedy prowadziłem warsztaty AI dla 15 programistów w Insly, pierwszą rzeczą, którą musiałem zrobić, było zastąpienie tego hasła konkretnym zachowaniem — konkretnymi rzeczami, które robisz, w konkretnej kolejności, inaczej niż dotychczas.

O tym właśnie jest ten wpis. Jak "AI-first" wygląda naprawdę, kiedy zaczynasz nowy projekt od zera.

## Czym "AI-first" nie jest

Nie chodzi o dodanie chatbota do produktu.

Nie chodzi o uruchomienie GitHub Copilot i ogłoszenie sukcesu.

Nie chodzi o oddawanie decyzji modelowi i liczenie na najlepsze.

To łatwe błędne odczytania, i widziałem zespoły robiące każde z tych trzech. "AI-first" w kontekście workflow deweloperskiego oznacza coś bardziej konkretnego: angażujesz AI na każdym etapie pracy — od wymagań do review — w sposób, który zmienia to, co tworzysz i jak szybko to tworzysz. Nie dekorujesz istniejącego workflow. Przebudowujesz go z AI jako pełnoprawnym uczestnikiem.

Oto jak to wygląda w praktyce, etap po etapie.

## Etap 1: Wymagania — AI jako tester odporności

Większość zespołów pisze wymagania, a potem je przekazuje dalej. Albo przegląda z innym człowiekiem. Ja teraz robię najpierw jeszcze jedną rzecz: wklejam opis problemu do Clauda i proszę o poszukanie dziur.

Nie "napisz mi specyfikację". Raczej: "Oto problem, który rozwiązuję. Czego nie uwzględniam? Które edge case'y pomijam? Co jest na tyle niejednoznaczne, że dwóch inżynierów zbudowałoby różne rzeczy?"

Wyniki są konsekwentnie niewygodne w użyteczny sposób. Podczas warsztatów zrobiłem live demo z fikcyjnym serwisem do przetwarzania roszczeń ubezpieczeniowych — domeny, którą zespół dobrze znał. W ciągu dwóch minut Claude wskazał trzy konflikty w wymaganiach, które spowodowałyby problemy integracyjne dalej w projekcie.

Reakcja zespołu nie była "wow, AI jest mądre". Była: "poczekaj, my robimy to z prawdziwymi specyfikacjami i łapiemy to znacznie później." Właśnie o to chodziło.

AI nie pisze Twoich wymagań. Kwestionuje je, kiedy jeszcze tanio je zmienić.

## Etap 2: Architektura — skompresowana eksploracja, nie oddane decyzje

Kiedy zaczynam nowy projekt, kiedyś spędzałem pierwsze kilka godzin w prywatnej pętli myślenia — szkicowałem opcje, odrzucałem je z powodów, które sformułowałbym dopiero później, w końcu lądowałem na czymś. Ta pętla jest wartościowa. AI jej nie zastępuje. Ale ją kompresuje.

Co pokazałem zespołowi: opisz swój kontekst (domena, ograniczenia, wielkość zespołu, istniejący stack, rzeczy niepodlegające negocjacji) i poproś o trzy różne podejścia architektoniczne z jawnie wyrażonymi kompromisami. Nie akceptujesz żadnego z nich. Używasz ich jako punktów startowych do prawdziwego myślenia.

To nie jest abdykacja. To jak praca z parą — bardzo oczytanym inżynierem, który nie ma ego przy swoich sugestiach. Sugestie są często błędne w sposób, który wyjaśnia, czego naprawdę potrzebujesz.

W Insly używamy backendu Go i Python na AWS, z Symfony wciąż w częściach systemu legacy. Kiedy projektuję coś nowego w tym kontekście, mogę przejść od "pustej strony" do "trzech realnych opcji z nazwanymi kompromisami" w 30 minut zamiast trzech godzin. Decyzja nadal należy do mnie. Eksploracja jest wspólna.

## Etap 3: Implementacja — krótkie pętle z Cursorem

Chcę być bezpośredni w kwestii tego, jak faktycznie używam programowania wspomaganego AI, bo naiwna wersja marnuje czas.

Wersja naiwna: wklej duży prompt, dostań duży blok kodu, spróbuj uruchomić, debuguj przez godzinę.

Wersja, którą pokazałem: ciasne pętle. Napisz sygnaturę funkcji i docstring. Poproś o implementację. Przeczytaj ją. Jeśli jest błędna, zastanów się dlaczego Twój prompt był błędny, nie dlaczego model jest błędny. Popraw. Dostań test. Sprawdź, czy test testuje to, co myślisz, że testuje. Idź dalej.

Dyscyplina jest w rozmiarze pętli. Długie prompty do AI, próbujące wygenerować całe serwisy naraz — to jest vibecoding, i produkuje kod, którego nikt w pełni nie rozumie. Krótkie pętle, częsta weryfikacja, pozostanie za kierownicą — to produkuje kod, który posiadasz.

Przeprowadziłem warsztaty przez to na prawdziwym kodzie Go: prosty handler HTTP z trochę logiki biznesowej. Pierwsza próba modelu miała subtelny błąd w obsłudze błędów. Ten błąd był momentem nauczania — nie "AI jest złe", ale "dlatego czytasz każdą linię."

Jedna rzecz, która zaskoczyła zespół: kiedy już działasz w ciasnych pętlach, prędkość developmentu dla tych części, które nie są nowatorskie — infrastruktura, scaffolding, boilerplate — dramatycznie wzrasta. Twórcze, trudne części nadal zajmują tyle samo czasu. Ale jest mniej żmudnych rzeczy na drodze.

## Etap 4: Code review — AI przed ludźmi

Zanim pull request trafi do ludzkiego reviewera, teraz przeprowadzam go przez review AI z konkretnym szablonem promptu:

- Jakie problemy bezpieczeństwa widzisz w tym kodzie, szczególnie wokół [konkretna kwestia domenowa]?
- Które z istniejących wzorców w tym codebase narusza lub ignoruje ten kod?
- Które edge case'y nie są pokryte przez obecne testy?
- O co by zapytał senior inżynier podczas review?

Celem nie jest zastąpienie ludzkiego review. Chodzi o podniesienie podłogi. Kiedy ludzki reviewer widzi PR, oczywiste rzeczy są już zaadresowane. Ludzkie review może skupić się na architekturze, logice domenowej i rzeczach, których AI naprawdę nie łapie — jak "to działa, ale będzie koszmarem w utrzymaniu za 18 miesięcy ze względu na strukturę tego modułu."

Podczas warsztatów pokazałem przed i po: ten sam kawałek kodu, dwa opisy PR — jeden bez AI pre-review, jeden po. Różnica w tym, co zostało złapane zanim ludzkie oczy to dotknęły, była znacząca. Jeden uczestnik powiedział: "Wysyłałem moim reviewerom pracę domową, którą powinienem był zrobić sam."

## Etap 5: Generowanie testów — myślenie, nie pisanie

Tu widziałem największą zmianę nastawienia podczas warsztatów.

Tradycyjny ból pisania testów jednostkowych: wiesz, co musisz przetestować, po prostu musisz to wszystko wypisać. To jest żmudne. I ponieważ jest żmudne, pomijasz edge case'y, albo piszesz testy, które technicznie przechodzą, ale nie pokrywają trybów awarii, które mają znaczenie.

AI to zmienia. Opisujesz zachowanie, które chcesz przetestować — w zwykłym języku, najlepiej z jakimś kontekstem domenowym. Dostajasz zestaw przypadków testowych. Potem je przeglądasz — nie pod kątem tego, czy są syntaktycznie poprawne, ale pod kątem tego, czy testują właściwe rzeczy. Dodajesz te, które byś pominął. Usuwasz te, które nie mają sensu.

Pisanie nie jest już wąskim gardłem. Myślenie jest. A myślenie o tym, co testujesz — co może pójść nie tak, jakie są Twoje inwarianty — to jest część, która faktycznie sprawia, że testy mają wartość.

Przeprowadziłem to ćwiczenie z kawałkiem kodu Python z hipotetycznego modułu obliczeń ubezpieczeniowych. Wygenerowane testy pokryły siedem przypadków. Ja napisałbym pięć. Dwa z tych siedmiu były naprawdę użytecznymi testami, o których bym nie pomyślał. Pozostałe dwa nie były ważne dla naszej domeny. Taki stosunek — znajdź więcej, odrzuć część — to normalny tryb.

## Przed i po: sprint z tym workflow i bez

Oto przybliżone porównanie na podstawie tego, co zaobserwowałem w Insly w pracy mojego własnego zespołu przed warsztatami i tego, co widziałem u zespołów, które przyjęły podejście AI-first:

**Nowy feature, tradycyjny sprint:**
- Dzień 1–2: Dyskusja o wymaganiach, wyjaśnienia w tę i z powrotem
- Dzień 3: Szkicowanie architektury, async feedback
- Dzień 4–7: Implementacja, natykanie się na nieoczekiwane edge case'y w środku sprintu
- Dzień 8: Pisanie testów, pośpiech ze względu na deadline
- Dzień 9: Review, kilka rund komentarzy
- Dzień 10: Wdrożenie

**Nowy feature, sprint AI-first:**
- Dzień 1: Wymagania z AI stress-testem, konflikty złapane tego samego dnia
- Dzień 1 popołudnie: Eksploracja opcji architektonicznych, wybrany kierunek
- Dzień 2–5: Implementacja z ciasnym AI loopem, testy generowane równolegle
- Dzień 6: AI pre-review, PR wystawiony z już zaadresowanymi edge case'ami
- Dzień 7: Ludzkie review skupione na tym, co ważne
- Dzień 8: Wdrożenie

Różnica czasowa zależy od projektu i zespołu. Co nie zmienia się: redukcja przepychania się pod koniec sprintu. Rzeczy tworzące crunch — odkrywanie luk w wymaganiach podczas implementacji, łapanie edge case'ów podczas review — przenoszą się wcześniej, kiedy są tańsze.

## Co nie działa w greenfield

AI-first nie rozwiązuje każdego problemu w nowych projektach i wolę to powiedzieć wprost, niż pozwolić zespołom uczyć się tego na własnej skórze.

**AI nie radzi sobie dobrze z nowatorską logiką domenową.** Jeśli rozwiązujesz problem, którego nikt nie rozwiązał wcześniej w zupełnie ten sam sposób — nietypowa logika regulacyjna, złożone obliczenia wielostronnej odpowiedzialności, domenowo specyficzne problemy optymalizacyjne — AI wygeneruje plauzybilnie wyglądający kod, który jest subtelnie błędny w domenowo specyficzny sposób. Potrzebujesz głębokiej wiedzy domenowej, żeby złapać te błędy.

**Zanik kontekstu jest realny.** W długiej sesji na dużym codebase, asystenci AI tracą ślad wcześniejszego kontekstu. Dyscyplina ciasnych pętli tu pomaga — mniejsze jednostki pracy oznaczają mniej kontekstu do utrzymania — ale nie eliminuje problemu. Musisz pozostać architektem.

**Niespójność w zespole.** Jeśli połowa zespołu adoptuje AI-first, a połowa nie, dostajesz niespójną jakość kodu i sfrustrowanych reviewerów. Dyscyplina musi być wspólna — i to wymaga celowej adopcji, nie nakazów, tylko wspólnej praktyki.

## Uczciwe podsumowanie

To, co pokazałem zespołowi, to nie magia. To zestaw nawyków — konkretnych rzeczy, które robisz na każdym etapie projektu — które przyspieszają pracę i wcześniej łapią problemy. Zmiana nastawienia jest mniejsza niż brzmi: nie stajesz się "prompt engineerem". Stajesz się inżynierem, który przemyślanie używa potężnego narzędzia.

Zespół w Insly był sceptyczny na początku. Pod koniec pierwszego dnia warsztatów nie byli "wyznawcami AI" — byli użytkownikami konkretnych technik, które już przyniosły wyniki, które mogli zobaczyć. To właściwy sposób adopcji: nie przez inspirację, przez demonstrację.

Jeśli zaczynasz nowy projekt w przyszłym tygodniu, możesz zastosować jeden z tych etapów od razu. Zacznij od wymagań. Przepuść opis problemu przez Clauda przed następną sesją planowania. Sprawdź, co wróci.

Albo znajdzie coś, co przeoczyłeś, albo potwierdzi, że dobrze to przemyślałeś. Tak czy inaczej, jesteś do przodu.
