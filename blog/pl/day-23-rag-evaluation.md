---
day: 23
title: "Ewaluacja jakości RAG dla zespołów bez inżynierów ML"
pillar: Educator
language: pl
image: ../../images/day-23.jpg
image_unsplash_query: "data quality metrics dashboard"
---

# Ewaluacja jakości RAG dla zespołów bez inżynierów ML

Najczęstszy tryb awarii, który widzę w zespołach developerskich RAG, które nie radzą sobie dobrze: wdrożyły system, "wydaje się działać", i nie mają pojęcia, czy naprawdę działa.

To nie jest problem z wyrafinowaniem technicznym. To problem z dyscypliną ewaluacji. I w przeciwieństwie do wielu aspektów machine learning, budowanie dobrej infrastruktury ewaluacyjnej dla systemów RAG nie wymaga wykształcenia ML.

Po zbudowaniu 3 systemów RAG w produkcji — dwa z których były kosztownymi doświadczeniami edukacyjnymi — to jest framework ewaluacyjny, który chciałbym mieć od pierwszego dnia.

## Dlaczego ewaluacja jest niezbywalna

System RAG, który "wydaje się działać", generuje brzmiące pewnie odpowiedzi o nieznanej jakości. Bez ewaluacji nie masz możliwości:

- Wiedzieć, kiedy zmiana kodu poprawiła lub pogorszyła jakość
- Identyfikować, które typy pytań Twój system obsługuje słabo
- Odróżniać błędy retrieval (pobrano złe dokumenty) od błędów generowania (właściwe dokumenty, błędna odpowiedź)
- Budować uzasadnienie dla dalszych inwestycji lub korekty kursu

Zespoły, które pomijają ewaluację, kończą w miejscu, które widziałem zbyt wiele razy: miesiące w projekt, pewne że system jest dobry, a potem użytkownik demonstruje systematyczny błąd, który istniał od wdrożenia. Zmarnowaliśmy dwa tygodnie optymalizując prompty w naszym pierwszym systemie RAG, zanim przeprowadziliśmy właściwą ewaluację retrieval i odkryliśmy, że retriever był wąskim gardłem przez cały czas.

Buduj infrastrukturę ewaluacyjną zanim zbudujesz swoją pierwszą funkcję produkcyjną. Jeśli już wdrożyłeś bez niej, buduj ją teraz.

## Krok 1: Zbuduj swój zestaw testowy

Twój framework ewaluacyjny jest tak dobry jak Twój zestaw testowy. Zestaw testowy dla RAG składa się z trzech rzeczy:

**Pytania**: Realistyczne zapytania, które zadają prawdziwi użytkownicy. Wyciągnij je ze swoich ticketów wsparcia, wywiadów z użytkownikami lub logów użytkowania. Jeśli jesteś przed uruchomieniem, stwórz je z ekspertem domenowym.

**Oczekiwane fragmenty źródłowe**: Konkretne fragmenty z Twojego korpusu dokumentów, które powinny być pobrane, by odpowiedzieć na każde pytanie. To wymaga wiedzy domenowej — kogoś, kto naprawdę rozumie temat wystarczająco dobrze, by wiedzieć, które sekcje których dokumentów są istotne.

**Oczekiwane odpowiedzi**: Jak wygląda poprawna, wysokiej jakości odpowiedź na każde pytanie.

Praca walidacyjna jest pracochłonna. Planuj 30-60 minut na pytanie dla dokładnej walidacji. Dla zestawu 50 pytań to 25-50 godzin czasu eksperta. Zaplanuj to jawnie w budżecie. To najbardziej dźwigniowa inwestycja, jaką dokonasz w projekcie.

W ubezpieczeniach w Insly, nasze pytania do zestawu testowego pochodzą od prawdziwych underwriterów i brokerów. Oczekiwane odpowiedzi są walidowane przez ludzi, którzy zawodowo obsługują zapytania ubezpieczeniowe. Nie możemy fałszować tego kroku. Jakość naszej ewaluacji jest ograniczona przez jakość naszego dostępu do wiedzy domenowej.

Przechowuj swój zestaw testowy w kontroli wersji. Aktualizuj go w miarę odkrywania nowych trybów awarii.

## Krok 2: Mierz jakość retrieval

Jakość retrieval mierzy, czy Twój system znajduje właściwą treść zanim LLM się angażuje. To najczęściej niedoceniany krok pomiarowy.

**Precyzja**: Spośród pobranych fragmentów, jaki ułamek jest istotny? Jeśli pobrałeś 5 fragmentów i 3 były istotne, precyzja wynosi 0,6.

**Recall**: Spośród istotnych fragmentów w Twoim korpusie, jaki ułamek został pobrany? Jeśli jest 5 istotnych fragmentów i pobrałeś 3, recall wynosi 0,6.

Możesz mierzyć je ręcznie w arkuszu kalkulacyjnym: dla każdego pytania testowego, wylistuj fragmenty, które powinny były zostać pobrane, uruchom swój retrieval i sprawdź, które oczekiwane fragmenty pojawiają się w wynikach.

W naszych systemach produkcyjnych celujemy w >80% precyzji retrieval zanim spędzimy czas optymalizując warstwę generowania. Jeśli precyzja retrieval jest poniżej tego progu, żadna inżynieria promptów nie naprawi systemu. LLM nie może wygenerować dobrej odpowiedzi, kiedy właściwe informacje nie są w jego kontekście.

## Krok 3: Mierz jakość odpowiedzi z LLM-as-Judge

Gdy masz pobrane fragmenty, krok generowania produkuje odpowiedzi. Mierzenie jakości odpowiedzi ma trzy krytyczne wymiary:

**Wierność**: Czy odpowiedź jest poparta pobrazonymi fragmentami, czy LLM wprowadza informacje nieobecne w kontekście? Niewierna odpowiedź wskazuje na halucynację.

**Trafność**: Czy odpowiedź rzeczywiście adresuje postawione pytanie? Odpowiedź, która jest technicznie dokładna, ale nie adresuje pytania, nadal jest błędem.

**Kompletność**: Czy odpowiedź obejmuje wszystkie ważne aspekty pytania, czy adresuje tylko jego część?

Dla każdego z tych wymiarów piszesz prompty ewaluacyjne, które używają LLM do oceny wygenerowanej odpowiedzi. Oto prompt ewaluacji wierności, którego używamy:

```
System: Jesteś sędzią ewaluacyjnym. Oceń, czy podana odpowiedź
jest wierna podanemu kontekstowi.

Kontekst: {pobrane_fragmenty}
Pytanie: {pytanie}
Odpowiedź: {wygenerowana_odpowiedź}

Oceń wierność w skali od 0,0 do 1,0, gdzie 1,0 oznacza, że odpowiedź
jest całkowicie poparta kontekstem i nie wprowadza żadnych informacji spoza niego.
Podaj krótkie wyjaśnienie, następnie podaj swoją numeryczną ocenę.
```

Podejście "LLM-as-judge" nie jest doskonałe. LLM może popełniać błędy ewaluacji. Ale jest wystarczająco dokładne do śledzenia trendów na dużą skalę i identyfikowania systematycznych błędów. Uruchamiamy te ewaluacje przez AWS Bedrock, co utrzymuje nasze dane ubezpieczeniowe w obrębie naszej istniejącej granicy compliance.

Dla ubezpieczeń specyficznie, utrzymujemy tzw. "czerwone linie halucynacji" — około 30 pytań kanarych, gdzie jakakolwiek halucynacja jest blokadą wdrożenia. Błędne kwoty pokrycia, niepoprawne warunki polisy, sfabrykowane odniesienia prawne. Uruchamiają się przy każdym wdrożeniu. Jeden błąd tutaj zatrzymuje wydanie.

## Krok 4: Śledź trendy w czasie

Jednorazowa ewaluacja jest minimalnie użyteczna. Czego chcesz to trend: czy jakość się poprawia, jest stabilna, czy się pogarsza?

Skonfiguruj cotygodniowe uruchomienie ewaluacji, które:

1. Uruchamia cały Twój pipeline retrieval i generowania przeciw zestawowi testowemu
2. Automatycznie oblicza wszystkie metryki
3. Rejestruje wyniki w dashboardzie lub arkuszu kalkulacyjnym
4. Alarmuje Cię, kiedy jakakolwiek metryka spada poniżej progu

Wymagamy poprawy netto we wszystkich czterech metrykach przed mergem istotnych zmian retrieval lub generowania. Nie tylko poprawa na metryce, którą optymalizowałeś — poprawa netto w całości. Zmiany, które poprawiają wierność, ale pogarszają recall retrieval, są blokowane do czasu, gdy oba zostaną zaadresowane.

Uczyń dashboard ewaluacji widocznym dla całego Twojego zespołu. Metryki jakości widoczne tylko dla inżynierów są optymalizowane pod kątem problemów inżynierskich. Metryki jakości widoczne dla menedżerów produktu traktowane są jako funkcja produktu, którą są.

## Krok 5: Systematycznie diagnozuj awarie

Gdy ewaluacja ujawnia słabą jakość na konkretnych pytaniach, następnym krokiem jest systematyczna diagnoza. Krytyczne rozróżnienie:

**Błąd retrieval**: System pobrał fragmenty, które nie zawierały istotnej treści. Model generowania nie miał możliwości wyprodukowania dobrej odpowiedzi, bo właściwe informacje nie były w jego kontekście. Naprawa: popraw fragmentację, indeksowanie, architekturę retrieval.

**Błąd generowania**: System pobrał istotne fragmenty, ale wygenerowana odpowiedź była nadal błędna lub niewierna. Model miał właściwe informacje, ale nie użył ich poprawnie. Naprawa: popraw prompty, formatowanie kontekstu lub wybór modelu.

Te wymagają różnych interwencji. Mylenie ich prowadzi do prób naprawiania problemów generowania za pomocą zmian retrieval, lub odwrotnie — co jest dokładnie błędem, który popełniliśmy z naszym pierwszym prototypem RAG przed zbudowaniem właściwej ewaluacji.

## Narzędzia, których faktycznie używamy

Nasz stos ewaluacyjny w Insly jest celowo prosty:

- **Własne skrypty Python** do uruchamiania zestawu testowego i obliczania metryk
- **LLM-as-judge przez AWS Bedrock** do automatycznego oceniania wierności i trafności
- **Wersjonowany zestaw testowy** przechowywany w naszym repozytorium kodu obok kodu aplikacji
- **Prosty arkusz kalkulacyjny** do śledzenia trendów metryk w czasie

Nie potrzebujesz RAGAS ani platformy obserwabilności za 200 tys. zł, żeby zacząć. Prosta, własna ewaluacja uruchamiana regularnie jest nieskończenie lepsza niż żadna ewaluacja.

## Zacznij dziś

Jeśli masz system RAG w produkcji bez infrastruktury ewaluacyjnej, oto minimalny żywotny punkt startowy:

1. Zidentyfikuj 20 reprezentatywnych pytań z Twojego rzeczywistego przypadku użycia
2. Poproś eksperta domenowego o walidację oczekiwanych odpowiedzi dla każdego
3. Uruchom swój system na wszystkich 20 pytaniach
4. Ręcznie oceń każdą odpowiedź: poprawna, częściowo poprawna lub niepoprawna
5. Oblicz swój ogólny wynik jakości

Prymitywna linia bazowa jest nieskończenie lepsza niż żadna linia bazowa. Od tam buduj automatyzację do śledzenia trendu.

Systemy RAG, które przetrwają do prawdziwej użyteczności produkcyjnej, to te, które były ewaluowane od początku. Te, które nie były, zostają po cichu wycofane, gdy użytkownicy tracą do nich zaufanie.

Twój system RAG zasługuje na ewaluację, nie tylko na nadzieję.
