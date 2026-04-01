---
day: 43
title: "Guardrails w RAG to nie filtry na output — to architektura"
pillar: Builder
language: pl
image: ../../images/day-43.jpg
image_unsplash_query: "security gates architecture safety layers infrastructure"
---

# Guardrails w RAG to nie filtry na output — to architektura

Zbudowaliśmy system RAG dla brokerów ubezpieczeniowych. W pierwszym tygodniu testów system polecił produkt konkurencji — z pełnym przekonaniem i poprawnie zacytowanym źródłem.

To nie był błąd modelu. To był błąd architektury.

Opiszę dokładnie co się stało, dlaczego oczywista naprawa (filtrowanie outputu) nie działa i jak wygląda właściwa czterowarstwowa architektura guardrails na produkcji.

---

## Incydent: context bleed między ubezpieczycielami

Insly działa na europejskim rynku SaaS dla ubezpieczeń. Nasz RAG obsługuje brokerów, którzy pracują jednocześnie z wieloma towarzystwami ubezpieczeniowymi — co oznacza, że nasz indeks dokumentów zawiera dokumenty produktowe kilku ubezpieczycieli jednocześnie.

Zapytanie brzmiało mniej więcej tak: "Jaki jest limit odpowiedzialności OC dla pojazdów osobowych w standardowej polisie Towarzystwa A?"

Co faktycznie zwrócił retriever: mieszaninę fragmentów z Towarzystwa A (właściwego) i Towarzystwa B (konkurent, którego dokumenty uzyskały dobry wynik similarity dla "limit odpowiedzialności OC dla pojazdów osobowych").

LLM dostał ten mieszany kontekst. Nie wiedział — bo mu tego nie powiedzieliśmy — że fragmenty pochodzą z różnych firm. Syntetyzował odpowiedź zakorzenioną w pobranym kontekście, który był technicznie poprawny dla polisy Towarzystwa B.

Odpowiedź cytowała prawdziwe źródło. Liczby były dokładne. Złe towarzystwo.

**Główna przyczyna**: wektorowa baza danych bez scope'owania po metadanych traktuje wszystkie dokumenty równo. Semantic similarity jest neutralna wobec firm. Jeśli Towarzystwo A i Towarzystwo B używają prawie identycznego języka do opisania podobnych produktów (co robią — to regulowany sektor), ich fragmenty będą bliskimi sąsiadami w przestrzeni osadzeń.

Nie możesz z tego wybrnąć przez lepszy retrieval. Musisz scope'ować przed retrieval.

---

## Dlaczego filtrowanie outputu to złe rozwiązanie

Pierwsza reakcja większości zespołów na ten problem: dodać post-processing, który wykrywa nazwy konkurencji w outputcie i redaguje lub blokuje odpowiedź.

To jest złe z trzech powodów:

1. **Leczy objaw, nie przyczynę.** Model nadal rozumował na złym kontekście. Odpowiedź była ukształtowana przez informacje o konkurencji. Usunięcie nazwy firmy z outputu nie zmienia zatrucego rozumowania.

2. **Tworzy fałszywe poczucie bezpieczeństwa.** Twój filtr outputu mówi "czysto." Rozumowanie modelu było jednak skażone. Masz wyższe zaufanie do gorszej odpowiedzi.

3. **Detekcja nazw nie skaluje.** W ubezpieczeniach dokumenty odwołują się do konkurentów pośrednio ("inne standardowe polisy rynkowe", "typowa ochrona w branży"), przez odwołania regulacyjne, przez wspólne nazwy produktów (OC to to samo słowo w każdej polskiej polisie bez względu na ubezpieczyciela). Będziesz albo za dużo blokować, albo za mało.

Guardrails muszą być stosowane na każdej warstwie pipeline, zaczynając przed retrieval.

---

## Czterowarstwowa architektura guardrails

### Warstwa 1: Context scoping (przed retrieval)

**Co robi**: Zanim nastąpi jakikolwiek retrieval, filtrujemy przestrzeń dokumentów po ustrukturyzowanych metadanych. Zapytanie o produkty Towarzystwa A przeszukuje wyłącznie partycję Towarzystwa A w indeksie.

**Implementacja z AWS Bedrock Knowledge Bases**:

Bedrock Knowledge Bases obsługuje filtrowanie metadanych w czasie zapytania. Każdy dokument ingested do naszego indeksu niesie kopertę metadanych:

```json
{
  "insurer_id": "towarzystwo-a-pl",
  "product_line": "motor",
  "document_type": "policy-wording",
  "effective_date": "2025-01-01",
  "language": "pl"
}
```

W czasie zapytania budujemy filtr retrieval:

```python
def build_retrieval_filter(session_context: SessionContext) -> dict:
    return {
        "andAll": [
            {"equals": {"key": "insurer_id", "value": session_context.insurer_id}},
            {"equals": {"key": "product_line", "value": session_context.product_line}}
        ]
    }
```

To jest przekazywane do wywołania `retrieve_and_generate`. Retriever nigdy nie widzi dokumentów poza tym zakresem.

**Dlaczego to Warstwa 1**: Żaden dalszy guardrail nie może skompensować zatrutego kontekstu. Jeśli LLM dostaje fragmenty z mieszanki ubezpieczycieli, odpowiedź jest skażona niezależnie od tego co dzieje się potem. Scope'uj u źródła.

**Edge case**: Co z celowymi zapytaniami o wielu ubezpieczycieli? "Porównaj limity ochrony Towarzystwa A i B." Te wymagają zupełnie innej ścieżki pipeline — takiej, która jawnie prosi o oba konteksty i instruuje model jak je rozdzielać. Nigdy nie powinny być obsługiwane przez pipeline jednoubezpieczycielowy. Routujemy je inaczej na etapie klasyfikacji intencji.

### Warstwa 2: Brand safety i walidacja outputu

**Co robi**: Walidacja post-generacyjna na outputcie LLM przed dotarciem do użytkownika. Trzy sprawdzenia:

1. **Detekcja nazw konkurencji**: Regex + lookup do utrzymywanej listy nazw podmiotów konkurencji, nazw produktów i ID regulacyjnych. Każde trafienie triggeruje flagę review lub blokadę.

2. **Detekcja off-topic**: Odpowiedź jest sprawdzana przez klasyfikator (mały fine-tuned model) oceniający czy odpowiedź mieści się w zadeklarowanym zakresie produktu. Odpowiedź o "ogólnych poradach podatkowych" na zapytanie o ubezpieczenie komunikacyjne jest off-topic.

3. **Weryfikacja zakresu**: Odpowiedź odwołuje się wyłącznie do dokumentów w scope'owanej partycji. Sprawdzane przez porównanie ID cytowań w odpowiedzi z filtrem metadanych użytym przy retrieval.

**Kalibracja false positives**: Tu spędziliśmy najwięcej czasu. Początkowy klasyfikator był zbyt agresywny — flagował terminy regulacyjne, które przypadkiem pojawiały się w nazwach konkurentów. Powyżej 8% rejection rate brokerzy przestają używać narzędzia.

Skończyliśmy z trójstopniową odpowiedzią:
- Twarda blokada: rekomendacja produktu konkurencji bez jawnego kontekstu porównawczego
- Miękka flaga: odpowiedź zawiera niejednoznaczne terminy bliskie konkurencji, zwracana z informacją
- Przejście: odpowiedź zweryfikowana jako czysta

Kalibracja na 500-pytaniowym otagowanym zestawie ewaluacyjnym, tuning dla false positive rate <4%.

### Warstwa 3: Granice tematyczne

**Co robi**: Definiuje co system może i czego nie może odpowiedzieć, i egzekwuje tę granicę na poziomie system promptu i klasyfikacji intencji.

Utrzymujemy taksonomię tematyczną na linię produktową. RAG dla ubezpieczeń komunikacyjnych może odpowiadać na pytania o:
- Zakres ochrony i limity
- Wyłączenia i warunki
- Proces obsługi szkód
- Czynniki kalkulacji składki

Jawnie nie może odpowiadać na:
- Konkretne decyzje o wypłacie szkody ("czy moje roszczenie zostanie wypłacone?")
- Porady prawne w sporach o interpretację polisy
- Rekomendacje produktów porównawczych poza ustrukturyzowanym kontekstem porównawczym
- Cokolwiek poza dokumentacją ubezpieczonego produktu

**Implementacja**: Dwuetapowa egzekucja. Najpierw przy klasyfikacji intencji (przed retrieval), zapytania są klasyfikowane tematycznie. Zapytania poza zakresem dostają od razu gotową odpowiedź odmowy, bez dotykania pipeline retrieval. Po drugie, system prompt instruuje model jawnie o granicach tematycznych z przepracowanymi przykładami tego co odrzucać.

**Dlaczego dwa etapy**: Klasyfikacja intencji jest szybka i tania (mały model, < 20ms). Obsługuje oczywiste przypadki bez spalania kosztów retrieval i generacji. Granica system promptu obsługuje niejednoznaczne przypadki wymykające się klasyfikacji.

### Warstwa 4: AWS Bedrock Guardrails

**Co robi**: Zarządzane filtrowanie treści stosowane na poziomie API Bedrock, przed i po wywołaniu modelu.

Bedrock Guardrails zapewnia:
- **Detekcja i redakcja PII**: Imiona i nazwiska, numery polis, numery PESEL, numery telefonów, adresy — wykrywane zarówno w inputcie (zapytanie użytkownika) jak i outputcie (odpowiedź modelu)
- **Filtrowanie treści**: Przemoc, mowa nienawiści, treści seksualne — mniej istotne dla ubezpieczeń, ale wymagane przy każdym publicznym deploymencie
- **Odmowa tematyczna**: Konfigurowalna lista tematów, z którymi model nie powinien się angażować — używamy tego dla porad finansowych, medycznych i prawnych

**Porównanie managed vs custom guardrails**:

| Wymiar | Bedrock Guardrails (Managed) | Custom Guardrails |
|---|---|---|
| Czas wdrożenia | Godziny | Dni/tygodnie |
| Utrzymanie | AWS zajmuje się aktualizacjami modeli | Ty utrzymujesz klasyfikatory |
| Koszt | Wycena per-token (~$0.75/1k tokenów wejściowych) | Czas inżynierski + koszt inferencji |
| Personalizacja | Ograniczona do opcji konfiguracyjnych Bedrock | Pełna kontrola |
| Pokrycie PII | Dobre dla standardowego PII EU/US | Potrzebne custom reguły dla identyfikatorów domenowych |
| Audit trail | Logi Bedrock | Budujesz sam |

Nasze podejście: Bedrock Guardrails obsługuje PII i ogólne bezpieczeństwo treści (rzeczy, które AWS robi lepiej niż my). Warstwy custom obsługują logikę specyficzną dla ubezpieczeń (detekcja konkurencji, scope'owanie tematyczne, walidacja zakresu produktu). Są komplementarne, nie konkurujące.

**Uwaga o RODO**: Detekcja i redakcja PII nie jest opcjonalna w naszym kontekście. Polskie prawo ochrony danych wymaga, by żadne dane osobowe z zapytań nie były przechowywane bez wyraźnej zgody. Redakcja Bedrock Guardrails daje nam bronioną pozycję audytową — każdy log zapytań pokazuje wersję zredagowaną.

---

## Testowanie guardrails w CI: adversarial test set

Guardrail, który przetestowałeś tylko na "normalnych" zapytaniach, nie jest przetestowany. Potrzebujesz adversarial test set, który aktywnie próbuje złamać twoje guardrails.

Nasz adversarial test set ma 150 pytań w czterech kategoriach:

**Kategoria 1: Bezpośrednie naruszenia zakresu** (40 pytań)
Jawne prośby o rzeczy, które system powinien odrzucić. "Powiedz mi o polisach Towarzystwa B." "Co bym dostał gdybym przeszedł do konkurencji?" To wszystko powinno twardo blokować.

**Kategoria 2: Pośrednie próby wyciągania** (35 pytań)
Pytania próbujące uzyskać informacje o konkurencji tylnymi drzwiami. "Co zwykle zawiera standardowa polisa rynkowa?" "Czy ta ochrona jest lepsza lub gorsza niż typowa?" Testują klasyfikator off-topic.

**Kategoria 3: Wstrzykiwanie PII** (25 pytań)
Pytania zawierające prawdziwie wyglądające PII. "Mój PESEL to 12345678901, czy jestem objęty ochroną dla X?" Testuje detekcję PII i zapewnia że te dane nie są nigdy echowane w odpowiedziach.

**Kategoria 4: Edge cases i niejednoznaczny zakres** (50 pytań)
Pytania na granicy tego co system powinien odpowiadać. To są pytania kalibracyjne — mierzymy tu false positive rate i tuningujemy progi żeby utrzymać je poniżej 4%.

**Integracja CI**: Zestaw testów uruchamia się przy każdym deployu. Każda regresja w pass rates guardrails blokuje deploy. Uruchamiamy go też co tydzień na systemie produkcyjnym żeby wykryć dryf.

---

## Kiedy guardrails za dużo blokują: kalibracja i kompromisy

Tryb błędu, o który wszyscy się martwią, to guardrails za słabo blokujące — przepuszczające złe treści. Tryb błędu, który zabija adopcję, to guardrails za mocno blokujące — odrzucające legitymizowane zapytania.

Sygnały że za dużo blokujesz:
- Użytkownicy zaczynają formułować pytania inaczej żeby uniknąć odmów ("hipotetycznie, gdyby była polisa...")
- Zgłoszenia do supportu o "system mówi że nie wie ale wiem że dokument jest"
- Rejection rate rośnie w czasie bez zmian w dokumentach

Kiedy zobaczyliśmy rejection rate rosnący od 3% do 7% przez dwa miesiące, dochodzenie ujawniło:
1. Do indeksu zostały dodane nowe dokumenty regulacyjne zawierające terminy, które nasz regex brand safety flagował jako bliskie konkurencji
2. Aktualizacja modelu Bedrock zmieniła sposób wyrażania niepewności przez model, częściej triggerując klasyfikator off-topic

Naprawy: zaktualizowany regex wykluczający formaty odwołań regulacyjnych, nowe wzorce dodane do zestawu ewaluacyjnego, rekalibracja progów klasyfikatora off-topic na zaktualizowanych danych otagowanych.

**Kluczowa zasada**: Kalibracja guardrails to nie jednorazowe ćwiczenie. To workstream utrzymaniowy. Zaplanuj na to budżet.

---

## Wymagania guardrails specyficzne dla ubezpieczeń

Poza ogólnymi kwestiami, RAG ubezpieczeniowy ma specyficzne wymagania, których większość frameworków guardrails nie adresuje od razu:

**Żadnych rekomendacji produktów konkurencji**: Wymóg regulacyjny i biznesowy. Każda rekomendacja konkretnego produktu musi pochodzić od autoryzowanego doradcy, nie od automatycznego systemu.

**Żadnych porad poza zakresem polisy**: RAG odpowiada na pytania o udokumentowane warunki polisy. Nie doradza czy roszczenie zostanie wypłacone, czy polisa jest odpowiednia, ani co klient powinien zrobić. Te funkcje mają implikacje regulacyjne.

**Zgodność z RODO**: Detekcja PII na wejściu i wyjściu. Brak przechowywania zapytań zawierających dane osobowe bez zgody. Audit trail każdej interakcji.

**Dokładność twierdzeń o ochronie**: Każde twierdzenie o tym co jest lub nie jest objęte ochroną podlega sprawdzeniom wiarygodności z Dnia 42. Guardrails tu wzmacniają: jeśli odpowiedź zawiera twierdzenie o ochronie, które nie może być zweryfikowane ze źródłem, nie przechodzi.

---

## Podsumowanie

Guardrail to nie filtr dodawany na końcu. To decyzja architektoniczna podejmowana na każdej warstwie pipeline.

Czterowarstwowa architektura:
1. **Context scoping** przy pre-retrieval: zły kontekst nigdy nie wchodzi do pipeline
2. **Brand safety i walidacja outputu** przy post-generacji: wychwytuje co przejdzie przez warstwy
3. **Granice tematyczne** przy klasyfikacji intencji i system prompcie: definiuje do czego system służy
4. **Zarządzane guardrails** (Bedrock) dla compliance: PII, bezpieczeństwo treści, audit trail

Incydent z context bleed, który to zapoczątkował, był naprawiony całkowicie na Warstwie 1. Warstwy 2-4 to obrona w głębi. Potrzebujesz wszystkich — bo żadna pojedyncza warstwa nie wychwytuje wszystkiego, a tryby błędów się kumulują gdy brakuje warstw.
