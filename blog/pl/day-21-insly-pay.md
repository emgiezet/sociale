---
day: 21
title: "Budowanie InslyPay: Czego nauczył mnie FinTech compliance o budowaniu AI"
pillar: Builder
language: pl
image: ../../images/day-21.jpg
image_unsplash_query: "mobile payment app fintech"
---

# Budowanie InslyPay: Czego nauczył mnie FinTech compliance o budowaniu AI

Płatności wyglądają prosto z zewnątrz. Przenosisz pieniądze z jednego miejsca do drugiego. Technologia jest dojrzała, dobrze udokumentowana i dostępna przez API. Co może być trudnego?

Trudna część — jak w niemal każdym projekcie dotykającym wyspecjalizowanej domeny — to nie technologia. To domena. A potem, w domenie regulowanej, to warstwa compliance nałożona na złożoność domeny.

Zbudowaliśmy InslyPay: mobilną aplikację płatniczą dla ubezpieczających. Umożliwia płacenie składek ubezpieczeniowych bezpośrednio z telefonu. W tamtym czasie poruszanie się po wymogach compliance wydawało się brutalne. Z perspektywy czasu — to było najlepsze możliwe przygotowanie do pracy nad systemami AI, którą wykonuję teraz.

Oto czego naprawdę mnie to nauczyło.

## Co sprawia, że płatności ubezpieczeniowe są wyjątkowo trudne

Składki ubezpieczeniowe nie działają jak płatności e-commerce. Kiedy kupujesz coś online, model płatności jest czysty: jesteś winien cenę, płacisz cenę, otrzymujesz produkt.

Płatność składki jest powiązana z konkretną polisą, konkretnym okresem ubezpieczenia i często konkretnym harmonogramem rat. "Płacenie za ubezpieczenie" może oznaczać płacenie trzeciej raty rocznej składki za polisę obejmującą dwa budynki i pojazd komercyjny, wystawioną firmie z czterema wskazanymi kierowcami, przez brokera, który zarządza relacją z klientem i pobiera prowizję od transakcji.

Pieniądze nie trafiają po prostu gdzieś — trafiają do konkretnego wpisu księgowego w systemie ubezpieczyciela, po odjęciu prowizji, która przepływa na konkretne konto brokera, ze statusem płatności aktualizującym stan polisy w systemie zarządzania polisami. To wszystko musi być odzwierciedlone dokładnie i w czasie rzeczywistym.

### Rozliczenia wielostronne

W większości scenariuszy płatniczych są dwie strony: płatnik i odbiorca. Na rynkach brokerów ubezpieczeniowych są typowo trzy: ubezpieczający który płaci, broker który obsłużył sprzedaż i pobiera prowizję, oraz ubezpieczyciel który zapewnia ochronę i otrzymuje składkę netto.

Pojedyncze zdarzenie płatnicze w InslyPay musi zarejestrować otrzymaną składkę brutto, wyliczyć i podzielić prowizję brokera, zaksięgować w systemie ubezpieczyciela, zaktualizować status płatności polisy i uruchomić potwierdzenia dla wszystkich stron.

To jest księgowość. Ale to księgowość, która musi odbywać się automatycznie, w odpowiedzi na zdarzenie płatnicze, z gwarancjami poprawności wymaganymi przez transakcje finansowe.

### Problem nieudanej płatności

E-commerce ma standardowy plan dla nieudanych płatności: ponowna próba z wykładniczym opóźnieniem, powiadomienie użytkownika, zaoferowanie alternatywnych metod płatności, anulowanie zamówienia jeśli płatność ostatecznie nie przechodzi.

Ubezpieczenia mają materialnie inną logikę biznesową dla nieudanych płatności. Konsekwencją nie jest anulowane zamówienie — to wygaśnięcie polisy. Wygaśnięcie polisy oznacza, że ubezpieczający nie jest objęty ochroną, co jest poważne zarówno dla niego, jak i dla relacji brokera z klientem.

Nasza logika nieudanej płatności musiała rozumieć ile dni okresu prolongaty ma dana polisa (to różni się w zależności od rodzaju polisy i ubezpieczyciela), czy polisa powinna wejść w stan "okresu prolongaty" czy być natychmiast zawieszona, jakie powiadomienia muszą trafić do których stron, i jak wygląda ścieżka przywrócenia polisy.

Żadna z tych odpowiedzi nie przyszła z ogólnej wiedzy o infrastrukturze płatniczej. Przyszła z głębokiej wiedzy domenowej o tym, jak działa zarządzanie cyklem życia polisy ubezpieczeniowej.

## Krajobraz compliance: PSD2, RODO i regulacje ubezpieczeniowe

Budowanie aplikacji płatniczej w Europie w obecnym środowisku regulacyjnym oznacza zarządzanie wieloma nakładającymi się ramami compliance jednocześnie.

**PSD2** reguluje usługi płatnicze w UE. Wymaga silnego uwierzytelniania klienta, nakazuje otwarty dostęp bankowy dla zewnętrznych dostawców usług płatniczych i wymaga ścieżek audytu dla każdej transakcji płatniczej. Każdy przepływ płatności w InslyPay musiał być zaprojektowany z wbudowanymi wymogami PSD2 — nie dodanymi afterward.

**RODO** stosuje się do każdego elementu danych osobowych, który obsługujemy. Dane płatnicze są szczególnie wrażliwe w ramach RODO. Musieliśmy zaprojektować minimalizację danych w naszej architekturze, wdrożyć odpowiednie polityki retencji i upewnić się, że wymogi prawa do usunięcia mogą być spełnione bez naruszania ścieżek audytu wymaganych jednocześnie przez PSD2 i regulacje ubezpieczeniowe.

**Regulacja płatności specyficznych dla ubezpieczeń** dodaje trzecią warstwę. W wielu jurysdykcjach europejskich obsługa składek ubezpieczeniowych jest regulowana oddzielnie od ogólnego przetwarzania płatności — istnieją wymogi dotyczące obsługi środków klientów, mechanizmów escrow i terminowości księgowania składek do zapisów polisy.

Zarządzanie tymi trzema ramami jednocześnie, zapewnienie, że nie kolidują ze sobą, i budowanie architektury, która mogłaby ewoluować wraz ze zmianami w którejkolwiek z nich — to był rzeczywisty wyzwanie InslyPay.

## Czego compliance FinTech nauczył mnie o compliance AI

Kiedy 18 miesięcy temu zacząłem budować systemy AI w Insly, natychmiast zauważyłem coś: wzorce compliance, które poznałem budując InslyPay, mapowały się niemal bezpośrednio na wymagania dla AI w branżach regulowanych.

**Audytowalność jako zasada pierwsza.** PSD2 wymaga śladu papierowego dla każdej transakcji. AI w ubezpieczeniach wymaga śladu dla każdej decyzji. Jeśli roszczenie zostaje odrzucone lub pytanie o ubezpieczenie jest niepoprawnie odpowiedziane, muszę być w stanie wyjaśnić dokładnie jakie dokumenty zostały pobrane, jaki kontekst dostarczono modelowi i jaka była odpowiedź modelu. Ta sama dyscyplina, która zbudowała ścieżkę audytu płatności InslyPay, zbudowała naszą ścieżkę audytu decyzji AI.

**Nie możesz najpierw wdrożyć, potem naprawiać.** Błędny przepływ płatności może unieważniać transakcje i uruchamiać konsekwencje regulacyjne. Halucynujące AI może produkować niepoprawne interpretacje zakresu ubezpieczenia z realnymi implikacjami prawnymi. W środowiskach regulowanych "move fast and break things" to strategia dla innej branży. Zarówno InslyPay, jak i nasze systemy AI wymagały właściwego zaprojektowania compliance przed uruchomieniem, a nie jako ćwiczenia porządkującego po uruchomieniu.

**Integracje z podmiotami trzecimi mnożą Twoją powierzchnię ryzyka.** Każda bramka płatnicza podłączona do InslyPay była kolejną granicą compliance do zarządzania — ich obsługa danych, ich certyfikaty bezpieczeństwa, niezawodność ich API stały się naszą odpowiedzialnością do weryfikacji. Każdy dostawca LLM w naszym stosie AI niesie ten sam ciężar. Praktyki obsługi danych AWS Bedrock, ich polityki dotyczące trenowania modeli, możliwości rejestrowania audytu — to rzeczy, które musieliśmy zweryfikować i udokumentować zanim mogliśmy używać usługi z danymi ubezpieczeniowymi.

**Zasady się zmieniają, a Twoja architektura musi to obsłużyć.** PSD2 było wielokrotnie aktualizowane odkąd zbudowaliśmy InslyPay. Ustawa o AI UE jest wdrażana etapami. Regulacja ubezpieczeniowa na konkretnych rynkach zmienia się wraz z cyklami legislacyjnymi. Architektura wymagająca przepisania za każdym razem, gdy zmienia się regulacja, byłaby niemożliwa do utrzymania. Oba systemy musiały być zaprojektowane z myślą o ewolucji regulacyjnej.

## Wzorzec, który się przenosi

Najbardziej przenośna lekcja z InslyPay do pracy z AI to ta: regulowane środowiska mają specyficzne, powtarzające się wzorce — audytowalność, wymogi ludzkiego nadzoru, minimalizacja danych, wyraźna zgoda, prawo do usunięcia lub wyjaśnienia — i raz jak dogłębnie zinternalizujesz jedne ramy regulacyjne, kolejne uczysz się znacznie szybciej.

Inżynierowie, którzy wdrożyli produkcyjne oprogramowanie w jednym regulowanym środowisku, adaptują się do nowych środowisk regulowanych znacznie szybciej niż inżynierowie wywodzący się z nieuregulowalnych domen. Model mentalny — myślenie o tym, co musi być poddane audytowi, co wymaga ludzkiego zatwierdzenia, jakie dane mogą i nie mogą być przechowywane — przenosi się.

Zbudowałem InslyPay zanim zbudowałem systemy RAG. Ta kolejność nie była przypadkowym szczęściem. To był trening, z którego wciąż czerpię za każdym razem, gdy podejmujemy decyzję architektoniczną AI w Insly.

Wiedza domenowa bije techniczne spryty za każdym razem. Nie dlatego, że techniczne spryty nie mają znaczenia, ale dlatego, że najtrudniejsze problemy w oprogramowaniu domenowym to problemy domenowe — a w domenach regulowanych, problemy compliance. Ucz się domeny. Ucz się regulacji. Technologia podąży za nimi.
