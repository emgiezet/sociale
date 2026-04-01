---
day: 5
title: "Trzy prototypy RAG, trzy lekcje, jeden system, który działa"
pillar: Builder
language: pl
image: ../../images/day-05.jpg
image_unsplash_query: "prototype testing laboratory"
---

# Trzy prototypy RAG, trzy lekcje, jeden system, który działa

Budowanie produkcyjnego systemu RAG to nie jedna decyzja. To sekwencja eksperymentów, z których każdy ujawnia problem, którego poprzedni prototyp nie mógł rozwiązać.

W Insly spędziliśmy dwanaście miesięcy iterując przez wiele zasadniczo różnych architektur RAG, zanim mieliśmy system wystarczająco godny zaufania, żeby pokazać go prawdziwym użytkownikom. Oto czego nauczył nas każdy prototyp — i najważniejsza lekcja, która je wszystkie łączy.

## Pytanie, na które próbowaliśmy odpowiedzieć

Wszystkie nasze prototypy były budowane, żeby odpowiedzieć na to samo pytanie: czy brokerzy ubezpieczeniowi mogą odpytywać naszą bazę wiedzy w naturalnym języku i otrzymywać dokładne, audytowalne odpowiedzi?

Użytkownik to licencjonowany broker. Pytanie może brzmieć „co ta polisa obejmuje w przypadku szkody powodziowej?" lub „które wyłączenia stosują się do odpowiedzialności cywilnej pojazdów komercyjnych dla tego klienta?" Odpowiedź musi być precyzyjna — w ubezpieczeniach przybliżona odpowiedź dostarczona z pewnością siebie jest gorsza niż powiedzenie „nie wiem."

Mamy też ścisłe wymaganie compliance: każda odpowiedź musi być identyfikowalna z konkretnym dokumentem źródłowym. „AI tak powiedziała" nie jest akceptowalną odpowiedzią dla regulatora ani dla brokera broniącego decyzji o roszczeniu.

Mając ten kontekst, oto czego nauczyliśmy się od każdego prototypu.

## Prototyp 1: Standardowe wyszukiwanie wektorowe na AWS Bedrock

Kanoniczny tutorial RAG sugeruje prostą architekturę: zembedduj dokumenty do vector store, zembedduj zapytanie użytkownika, pobierz top-k najbardziej podobnych chunków i przekaż je do LLM do generacji.

Zbudowaliśmy to na AWS Bedrock Knowledge Bases. Konfiguracja była szybka — dni, nie tygodnie. Demo było imponujące. Brokerzy mogli zadawać pytania w naturalnym języku i otrzymywać brzmiące-istotnie odpowiedzi oparte na prawdziwych dokumentach polisowych.

Liczby produkcyjne mówiły inną historię. Na naszym zbiorze ewaluacyjnym — prawdziwych pytaniach z ticketów wsparcia brokerów — jakość retrieval wynosiła około 60%. Oznacza to, że cztery na dziesięć pytań zwracały odpowiedź opartą na złej sekcji dokumentu lub pobierały istotny tekst, ale pomijały kluczowy kontekst.

Główna przyczyna: dokumenty polisowe ubezpieczeń mają hierarchiczną strukturę i wzajemne odniesienia. Klauzula o pokryciu szkód wodnych może mówić „z zastrzeżeniem wyłączeń wymienionych w sekcji 12.3." Wyszukiwanie semantyczne pobiera klauzulę o pokryciu. Nie pobiera sekcji 12.3, chyba że ona też jest semantycznie podobna do zapytania — co często nie jest prawdą.

Embeddingi off-the-shelf trenowane na ogólnym tekście też słabo radzą sobie z wyspecjalizowaną terminologią domenową. Brokerzy używają żargonu branżowego. Model nie dopasowywał go konsekwentnie.

Lekcja: płaskie wyszukiwanie wektorowe nie rozumie struktury dokumentów. Embeddingi off-the-shelf nie rozumieją wyspecjalizowanych domen.

## Prototyp 2: Fine-tuned embeddingi i wyszukiwanie hybrydowe

Zaatakowaliśmy oba problemy z prototypu 1. Fine-tuneowaliśmy model embeddingów na dokumentach ubezpieczeniowych, żeby lepiej uchwycić terminologię domenową. Dodaliśmy wyszukiwanie słów kluczowych BM25 obok wyszukiwania wektorowego.

Jakość retrieval poprawiła się — osiągnęliśmy około 72% na naszym zbiorze ewaluacyjnym. Znaczący postęp.

Ale pojawiły się dwa nowe problemy.

Po pierwsze, dopasowanie słów kluczowych pomogło z terminologią, ale nie rozwiązało problemu strukturalnego. Nadal pobieraliśmy semantycznie istotne chunki, którym brakowało relacyjnego kontekstu potrzebnego do dokładnych odpowiedzi. Klauzula o pokryciu OC jest semantycznie podobna do zapytania o pokrycie OC. Ale jeśli rzeczywista odpowiedź zależy od aneksu dodanego sześć miesięcy później, który używa innego języka, wyszukiwanie hybrydowe ich nie łączy.

Po drugie, trafiliśmy w limity kontekstu. Przy hybrydowym retrieval zwracającym więcej kandydatów, przekazywaliśmy więcej tekstu do LLM, co sprawiało że odpowiedzi były dłuższe, droższe i w niektórych przypadkach mniej skoncentrowane.

Lekcja: ilość pobranego kontekstu to nie jakość pobranego kontekstu. Fine-tuning domenowy pomaga, ale nie rozwiązuje problemów strukturalnych.

## Prototyp 3: Retrieval oparty na grafach z LightRAG

LightRAG buduje graf wiedzy z Twoich dokumentów — wyodrębniając encje i relacje między nimi, nie tylko surowy tekst. Intuicja: dokumenty odwołują się do innych dokumentów, klauzule do innych klauzul, a aneks do polisy może nadpisać warunek w polisie bazowej. Jawne modelowanie tych relacji powinno poprawić retrieval dla zapytań zależnych od połączonych informacji.

W teorii, to było dokładnie właściwe podejście.

W praktyce, trafiliśmy na problem specyficzny dla naszej domeny. Nasze dokumenty ubezpieczeniowe i pliki Ogólnych Warunków Ubezpieczenia (OWU) są strukturalnie i językowo podobne — ten sam format, ta sama terminologia, różne szczegóły dla różnych ubezpieczycieli. W tym środowisku reprezentacje wektorowe stały się równie dobre i równie złe w rozróżnianiu między dokumentami. Przechodzenie grafu LightRAG nie mogło niezawodnie ustalić, który kontekst ubezpieczyciela był istotny dla danego zapytania.

Co ważniejsze: LightRAG nie miał wbudowanego sposobu filtrowania kontekstu po nazwie firmy, linii produktów lub typie ryzyka. W ubezpieczeniach to nie jest opcja. Broker pytający o pokrycie odpowiedzialności dla jednego ubezpieczyciela nie może otrzymać kontekstu krwawiącego z dokumentów innego ubezpieczyciela. Każda odpowiedź musi być audytowalna i przypisywalna.

Nie mogliśmy sprawić, żeby LightRAG spełniał to wymaganie bez przebudowania znacznych jego części — a wtedy lepiej było zbudować od zera.

Lekcja: grafy wiedzy nie rozwiązują filtrowania. Jeśli Twoja domena wymaga ścisłego zakresu kontekstu, graph retrieval może pogorszyć problem.

## Prototyp 4: Routing oparty na intencji, budowany od zera

Wyrzuciliśmy podejścia czarnej skrzynki i zbudowaliśmy od zera w Pythonie. Wgląd, który napędził tę decyzję, przyszedł z analizy rzeczywistych zapytań brokerów.

Brokerzy nie zadają losowych pytań. Rozkład pytań jest skoncentrowany. Przeanalizowaliśmy korpus zapytań brokerów i zidentyfikowaliśmy 11 odrębnych intencji użytkownika: weryfikacja pokrycia, wyszukiwanie wyłączeń, limity odpowiedzialności, procedura roszczeń, kalkulacja składki, historia zmian i kilka innych. Każda intencja mapuje się na inną strategię retrieval — niektóre potrzebują dokładnego wyszukiwania klauzul, niektóre porównania krzyżowego dokumentów, niektóre strukturalnego wyszukiwania danych zamiast semantycznego.

Właściwa strategia retrieval stosowana per intencja. Wszystko filtrowalne po firmie, linii produktów i typie ryzyka. Wszystko audytowalne z przypisaniem źródła.

Zwalidowaliśmy system na datasecie wyodrębnionym z Egzaminu KNF dla Brokerów — oficjalnego egzaminu licencyjnego Komisji Nadzoru Finansowego dla brokerów ubezpieczeniowych. Jeśli nasz system może zdać egzamin, który zdają licencjonowani brokerzy, możemy mu ufać w produkcji. Zdał z dobrymi wynikami.

Architektura retrieval jest ważniejsza niż model. Używaliśmy AWS Bedrock Claude przez cały czas. Ten sam model, ta sama jakość generacji. To, co się zmieniło, to jakość tego, co mu dawaliśmy do pracy.

## Co powiedziałbym sobie na początku

Właściwa architektura RAG zależy całkowicie od struktury Twoich danych i wymagań compliance, nie od tego, co było modne gdy zaczynałeś projekt.

Zanim cokolwiek zbudujesz, zapytaj:
→ Jakie są relacje strukturalne w moich danych, których podobieństwo semantyczne nie uchwytuje?
→ Jakie są moje wymagania filtrowania i czy moja architektura retrieval może je egzekwować?
→ Co oznacza „poprawne" dla mojego konkretnego przypadku użycia i jak to zmierzę?
→ Jakie są moje wymagania dotyczące audytu i atrybucji?

Te pytania zaoszczędziłyby nam miesięcy. Są punktem startowym dla każdej uczciwej decyzji architektonicznej RAG.
