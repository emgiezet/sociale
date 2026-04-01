---
day: 3
title: "5 pytań, które oddzielają dobre systemy RAG od kosztownych błędów"
pillar: Educator
language: pl
image: ../../images/day-03.jpg
image_unsplash_query: "checklist planning document"
---

# 5 pytań, które oddzielają dobre systemy RAG od kosztownych błędów

Jeśli wpiszesz „jak zbudować system RAG," znajdziesz setki tutoriali. Większość z nich pozwoli Ci skonfigurować vector store, zembeddować kilka dokumentów i uruchomić pierwsze zapytanie w ciągu 30 minut.

Tutorial zadziała. Twój system produkcyjny prawdopodobnie nie — nie bez odpowiedzi na pięć pytań, które zaraz podam.

Zbudowałem trzy systemy RAG w Insly, platformie ubezpieczeniowej z 150 000+ użytkownikami. Pierwszy był budowany szybko, bez zadawania tych pytań. Drugi uwzględniał niektóre z nich. Trzeci, który teraz działa w produkcji, zaczynał od jasnej odpowiedzi na wszystkie pięć. Różnica w wynikach nie była subtelna.

## Pytanie 1: Jakie jest rzeczywiste pytanie użytkownika?

To brzmi oczywisto. Tak nie jest.

„Chcemy, żeby nasze dokumenty były przeszukiwalne przez AI" to nie jest pytanie użytkownika. To wizja produktowa. A budowanie systemu RAG dla wizji produktowej, zamiast odpowiedzi na konkretne pytanie, prowadzi do systemów, które są architektonicznie nadmiarowe dla ogólnego przypadku i praktycznie niedopasowane dla prawdziwego.

Zanim cokolwiek zbudujesz, usiądź z prawdziwym użytkownikiem — osobą, która będzie używać systemu — i poproś, żeby pokazał Ci pytanie, na które najbardziej potrzebuje odpowiedzi. Nie najbardziej interesujące pytanie. Nie najbardziej imponujące. Najczęstsze. To, na które jeśli odpowiedź byłaby niezawodna, zaoszczędziłoby mu czas każdego dnia.

Dla zespołu underwriterów Insly to pytanie było konkretne i wąskie: dla tego dokumentu polisowego, jakie pokrycie stosuje się do tego rodzaju incydentu? Wszystko, co budowaliśmy, było dostrojone do dobrego odpowiadania na to pytanie.

Zaczynaj tam. Generalizuj później.

## Pytanie 2: W jakiej formie są Twoje dane?

Jedno z najbardziej niedocenianych wyzwań przy budowaniu korporacyjnych systemów RAG to przygotowanie danych. Tutoriale używają czystych plików PDF. Rzeczywiste dane enterprise to inna historia.

W Insly mamy dokumenty w wielu formatach, wielu językach, różnych poziomach jakości (część skanowana z papieru, część generowana programistycznie) i obejmujące różne konwencje schematu wśród brokerów i krajów. Zanim mogliśmy cokolwiek użytecznego zembeddować, musieliśmy:

→ Niezawodnie wyodrębniać tekst z wielu formatów (PDF, DOCX, HTML, zeskanowane obrazy przez OCR)
→ Normalizować różnice językowe i terminologiczne
→ Obsługiwać strukturę dokumentów — nagłówki, tabele, przypisy — w sposób zachowujący semantyczne znaczenie
→ Identyfikować i tagować metadane (typ dokumentu, data, wystawca, jurysdykcja), których będziemy potrzebować do filtrowanego retrieval

Ta praca zajęła tygodnie. Nigdzie nie pojawiła się w demo. I była fundamentem, na którym opierało się wszystko inne.

Bądź szczery wobec siebie co do tego, z czym masz do czynienia, zanim napiszesz pierwszą linię kodu retrieval. W ubezpieczeniach mamy dokumenty polisowe z 15 lat wstecz w 4 różnych formatach. Problemy z jakością na wejściu stają się błędami retrieval na wyjściu — gwarantowane.

## Pytanie 3: Jak wygląda „poprawna" odpowiedź?

To pytanie oddziela systemy, które działają, od systemów, które wydają się działać.

System RAG, który zwraca płynną, pewną siebie, dobrze sformatowaną złą odpowiedź, jest gorszy od tego, który mówi „nie wiem." Płynna zła odpowiedź jest używana. Wpływa na decyzje. Buduje błędne zaufanie do systemu.

Aby zbudować dobry system RAG, musisz zdefiniować ground truth. Jak wygląda poprawna odpowiedź? Kto w biznesie ma wiedzę domenową, żeby ocenić jakość odpowiedzi? Jaki procent odpowiedzi musi być poprawny, zanim trafi to do produkcji?

To nie są pytania, na które odpowie Ci Twój framework ML. Wymagają zaangażowania ekspertów domenowych — w naszym przypadku doświadczonych underwriterów, którzy mogli przeglądać wyniki systemu i mówić nam, kiedy odpowiedź była technicznie obecna w pobranym dokumencie, ale kontekstowo myląca.

Zbuduj infrastrukturę ewaluacji zanim zbudujesz pipeline retrieval. Dane ewaluacyjne, które tworzysz w tym kroku, będą najcenniejszym artefaktem całego projektu. Zbudowaliśmy 200 oznaczonych par Q&A z prawdziwych zapytań brokerów przed wdrożeniem czegokolwiek.

## Pytanie 4: Co się dzieje, gdy system się myli?

Każdy system będzie się mylił czasami. Istotne pytanie projektowe to: jaki jest zasięg szkód?

W aplikacji rekomendacji przepisów zła odpowiedź jest lekko irytująca. W ubezpieczeniach zła odpowiedź może wpłynąć na decyzję o roszczeniu, narazić firmę na ryzyko regulacyjne i zniszczyć relację z klientem.

Zaprojektuj obsługę błędów zanim wejdziesz w produkcję. Oznacza to:

→ Wyraźne decydowanie, które przypadki użycia system powinien odmawiać odpowiedzieć (i zwracanie uprzejmego „nie wiem" zamiast pewnej siebie złej odpowiedzi)
→ Budowanie pętli przeglądu przez człowieka dla odpowiedzi powyżej określonego progu ryzyka
→ Logowanie nie tylko błędów systemu, ale sygnałów jakości odpowiedzi, żeby móc identyfikować degradację w czasie
→ Definiowanie strategii rollbacku, jeśli jakość systemu spadnie poniżej Twojego progu

To nie są zaawansowane funkcje. To podstawowe wymagania dla wdrożenia produkcyjnego w każdej domenie, gdzie błędy mają konsekwencje.

## Pytanie 5: Jaką metrykę naprawdę optymalizujesz?

Systemy RAG mają wiele wymiarów jakości, które nie poruszają się w tym samym kierunku:

→ Precyzja retrieval (czy pobierane są właściwe dokumenty?)
→ Wierność odpowiedzi (czy odpowiedź jest zakorzeniona w tym, co pobrano?)
→ Trafność odpowiedzi (czy odpowiedź dotyczy zadanego pytania?)
→ Latencja (jak długo to trwa?)
→ Koszt (ile kosztuje każde zapytanie w skali?)
→ Ograniczenia compliance (RODO, rezydencja danych, logi audytowe, wytłumaczalność)

Nie możesz optymalizować wszystkiego jednocześnie, zwłaszcza w pierwszej iteracji. Wybierz jedno. Zazwyczaj jest to wierność odpowiedzi — najważniejszy sygnał, że Twój system jest zakorzeniony i nie halucynuje.

Bądź explicit co do tego, co optymalizujesz i jakie trade-offy akceptujesz. Zapisz to. Umieść w briefie projektu. Wracaj do tego, kiedy masz pokusę dodania złożoności.

W regulowanych branżach compliance nie jest opcjonalne. Wymagania dotyczące rezydencji danych, wytłumaczalności zgodnie z RODO i logi audytowe muszą być wbudowane w architekturę od pierwszego dnia — nie dodane z powrotem, gdy regulator zapyta.

## Meta-lekcja

Te pięć pytań Cię nie spowalnia. Zmienia to, co budujesz. Zespoły, które je pomijają, budują szybko i potem przebudowują powoli — bo to, co wdrożyły, nie rozwiązuje właściwego problemu lub nie jest wystarczająco godne zaufania, żeby go używać.

Zespoły, które zaczynają od tych pytań, budują coś węższego, prostszego i bardziej użytecznego przy pierwszej próbie. Potem stamtąd się rozszerzają.

Zapisz to. Podziel się z osobą, która podaje Ci stos dokumentów i mówi „po prostu zrób to przeszukiwalne." Te pytania to początek uczciwej rozmowy o tym, co naprawdę budujesz — i co będzie potrzebne, żeby zbudować to dobrze.
