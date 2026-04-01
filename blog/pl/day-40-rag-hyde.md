---
day: 40
title: "HyDE: wypełnianie semantycznej luki między pytaniami użytkowników a językiem dokumentów"
pillar: Educator
language: pl
image: ../../images/day-40.jpg
image_unsplash_query: "semantic search document retrieval bridge gap"
---

# HyDE: wypełnianie semantycznej luki między pytaniami użytkowników a językiem dokumentów

W dniu 7 pisałem o tym, dlaczego systemy RAG zbudowane z tutoriali sypią się po zderzeniu z realnymi dokumentami. Jednym z głównych powodów jest problem zwany semantyczną luką — a HyDE to jedno z najbardziej eleganckich rozwiązań, które znalazłem.

Pokażę Ci problem konkretnie, potem przejdę przez to jak HyDE go rozwiązuje, gdzie działa i gdzie nie.

## Problem semantycznej luki

Broker pyta: "Czy ta polisa pokrywa szkody powodziowe na nieruchomości?"

Właściwa klauzula brzmi: "Zakres ochrony obejmuje zdarzenia losowe powodujące szkody w ubezpieczonej nieruchomości zgodnie z §4 ust. 2, w tym zdarzenia sklasyfikowane jako klęski żywiołowe w rozumieniu obowiązującego prawa polskiego."

Słowo "powódź" nigdzie nie pojawia się w klauzuli. Fraza "szkody powodziowe" nie ma bezpośredniego dopasowania leksykalnego w dokumencie. Pytanie użytkownika i właściwa odpowiedź żyją w różnych sąsiedztwach przestrzeni osadzeń (embedding space).

Wyszukiwanie semantyczne po podobieństwie wektorowym działa przez znajdowanie dokumentów, których osadzenia są geometrycznie bliskie osadzeniu zapytania. Jeśli zapytanie zawiera "szkody powodziowe" a właściwy fragment zawiera "zdarzenia losowe powodujące szkody zgodnie z §4", podobieństwo kosinusowe między tymi osadzeniami może być niskie — mimo że to dokładnie właściwy dokument.

To jest semantyczna luka: język w którym użytkownicy zadają pytania i język w którym pisane są formalne dokumenty często znacząco się różnią. Problem jest najpoważniejszy w domenach z gęstym specjalistycznym żargonem: ubezpieczenia, prawo, medycyna, regulacje finansowe.

W naszym produkcyjnym doświadczeniu w Insly, naiwne wyszukiwanie semantyczne na dokumentach ubezpieczeniowych miało recall wyszukiwania szacunkowo 0.61 na naszym złotym zbiorze testowym — co oznacza, że w 39% przypadków właściwa klauzula nie pojawiała się w top-5 wyszukanych wynikach. LLM odpowiadał wtedy z niewystarczającego kontekstu, produkując niekompletne lub błędne odpowiedzi.

HyDE był jedną z interwencji, która znacząco poprawiła tę liczbę.

## Jak działa HyDE

HyDE — Hypothetical Document Embeddings — zostało zaproponowane przez Gao et al. w pracy z 2022 roku "Precise Zero-Shot Dense Retrieval without Relevance Labels." Kluczowa intuicja jest prosta i skuteczna.

**Standardowe wyszukiwanie RAG:**
1. Osadź zapytanie użytkownika: `query_embedding = embed("Czy polisa pokrywa szkody powodziowe?")`
2. Szukaj podobnych chunków: `results = vector_search(query_embedding, top_k=5)`

**Wyszukiwanie HyDE:**
1. Poproś LLM o wygenerowanie hipotetycznej odpowiedzi na zapytanie: odpowiedzi, która *wygląda jak fragment z docelowego korpusu dokumentów*
2. Osadź hipotetyczną odpowiedź: `hyde_embedding = embed(hypothetical_answer)`
3. Szukaj podobnych chunków używając osadzenia hipotetycznej odpowiedzi: `results = vector_search(hyde_embedding, top_k=5)`

Hipotetyczna odpowiedź nie musi być faktycznie poprawna — nie ma znaczenia, jeśli LLM wymyśli szczegóły. Liczy się to, że jest napisana w tym samym rejestrze, słownictwie i stylu co rzeczywiste dokumenty. Gdy LLM generuje "Polisa obejmuje szkody powodziowe jako zdarzenie losowe w myśl §4, z zastrzeżeniem wyłączeń wymienionych w §7", ten wygenerowany tekst żyje w tym samym sąsiedztwie osadzeń co rzeczywiste klauzule w dokumencie.

Nie szukasz pytania. Szukasz dokumentów, które wyglądają jak odpowiedź.

## Implementacja w Pythonie

Oto główna implementacja, której używamy. Jest prosta gdy zrozumiesz zasadę.

```python
from anthropic import Anthropic
import boto3
import json

client = Anthropic()
bedrock = boto3.client("bedrock-runtime", region_name="eu-west-1")

def generate_hypothetical_document(query: str, domain_context: str) -> str:
    """Generuj hipotetyczny dokument odpowiedzi używając LLM."""
    prompt = f"""Generujesz hipotetyczny fragment z formalnego dokumentu {domain_context}.
    
Użytkownik zapytał: "{query}"

Napisz krótki fragment (2-4 zdania), który ODPOWIADAŁBY na to pytanie gdyby pojawiał się 
w formalnym dokumencie {domain_context}.
Użyj formalnego języka dokumentu i terminologii. Nie zaznaczaj, że to jest hipotetyczne.
Fragment powinien być napisany jakby był wyciągiem z rzeczywistego dokumentu."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def embed_text(text: str) -> list[float]:
    """Pobierz osadzenia przez AWS Bedrock Titan Embed."""
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text, "dimensions": 1024})
    )
    return json.loads(response["body"].read())["embedding"]

def hyde_retrieve(query: str, vector_store, domain_context: str = "polisa ubezpieczeniowa", top_k: int = 5):
    """Wyszukiwanie przez HyDE: generuj hipotetyczny dokument, osadź go, szukaj."""
    # Generuj hipotetyczną odpowiedź
    hypothetical_doc = generate_hypothetical_document(query, domain_context)
    
    # Osadź hipotetyczny dokument
    hyde_embedding = embed_text(hypothetical_doc)
    
    # Szukaj używając hipotetycznego osadzenia
    results = vector_store.similarity_search_by_vector(hyde_embedding, k=top_k)
    
    return results, hypothetical_doc  # Zwróć hipotetyczny dokument do debugowania

# Przykład użycia
query = "Czy polisa pokrywa szkody spowodowane zalaniem od strony rzeki?"
results, hyp_doc = hyde_retrieve(
    query, 
    vector_store, 
    domain_context="polska polisa ubezpieczeniowa"
)

print(f"Hipotetyczny dokument: {hyp_doc}")
print(f"Wyszukano {len(results)} chunków")
```

**Jak może wyglądać hipotetyczny dokument dla naszego zapytania o powódź:**

> "Ubezpieczyciel zapewnia ochronę ubezpieczeniową od szkód powstałych wskutek zdarzeń losowych w postaci klęsk żywiołowych, w tym powodzi i zalania spowodowanego wezbraniem cieków wodnych oraz opadami nawalnymi. Zdarzenia te są klasyfikowane jako zdarzenia losowe w rozumieniu §4 ust. 2, pod warunkiem zachowania ciągłości ubezpieczenia i dokumentacji zdarzenia zgodnie z §12."

Ten tekst zawiera "powódź", "wezbranie cieków wodnych", "zdarzenia losowe", "§4", "ochrona" — słownictwo rzeczywistych dokumentów polis. Osadzenie tego hipotetycznego tekstu będzie znacznie bliższe do rzeczywistej klauzuli niż osadzenie oryginalnego pytania użytkownika.

## Mierzenie wpływu

Zmierzyliśmy wydajność HyDE na naszym zbiorze testowym dokumentów ubezpieczeniowych: 80 zapytań, każde z ręcznie zweryfikowanymi chunkami źródłowymi.

**Recall wyszukiwania@5 (docelowy chunk pojawia się w top 5 wynikach):**

| Metoda | Recall@5 | Uwagi |
|---|---|---|
| Naiwne wyszukiwanie semantyczne | 0.61 | Bazowy |
| + Filtrowanie metadanych | 0.71 | Filtruje po typie dokumentu, rynku |
| + HyDE | 0.79 | Na zapytaniach z branżowym żargonem |
| + HyDE + reranking | 0.84 | Cohere Rerank na top-20, zwróć top-5 |

HyDE dodał 8 punktów procentowych recall wyszukiwania ponad filtrowanie metadanych. Na podzbiorze zapytań zawierających ciężki żargon ubezpieczeniowy (około 60% naszego zbioru testowego), poprawa wynosiła 13–15 punktów procentowych.

**Ważny niuans:** HyDE pomagał najbardziej przy zapytaniach gdzie słownictwo użytkownika znacząco różniło się od słownictwa dokumentu. Na zapytaniach gdzie sformułowanie użytkownika bezpośrednio pasowało do języka dokumentu ("klauzula wypowiedzenia", "numer polisy", "data wymagalności składki"), HyDE nie dodawał mierzalnej korzyści.

## Kiedy HyDE pomaga, a kiedy nie

**HyDE jest wartościowe gdy:**
- Zapytania użytkowników używają języka potocznego; dokumenty używają formalnego/prawniczego/technicznego języka
- Słownictwo domenowe jest wyspecjalizowane i nieczęsto używane w danych treningowych modeli językowych
- Dokumenty zawierają gęsty, referencyjny tekst gdzie jeden koncept ma wiele synonimów
- Jakość wyszukiwania jest wąskim gardłem (nie jakość generacji)

**HyDE dodaje koszt i latencję z ograniczoną korzyścią gdy:**
- Zapytania to proste wyszukiwania faktów ("jaki jest numer polisy?")
- Słownictwo użytkownika i dokumentu są już podobne
- Korpus jest wystarczająco mały żeby pełne hybrydowe wyszukiwanie (BM25 + wektor) osiągało już wysoki recall
- Budżet latencji jest ograniczony — HyDE dodaje jedno wywołanie LLM na zapytanie, typowo 300–600ms

**HyDE może zaszkodzić gdy:**
- LLM generuje hipotetyczny dokument który pewnie opisuje coś błędnego, ciągnąc wyszukiwanie od właściwych dokumentów
- Domena jest wysoce wyspecjalizowana a LLM nie ma dobrych priorów dla języka dokumentu (np. bardzo niszowe specyfikacje techniczne)

Przeprowadziliśmy test ablacyjny gdzie celowo użyliśmy słabej jakości generacji hipotetycznej (zbyt krótka, nie domenowo specyficzna). Recall wyszukiwania spadł poniżej bazy — zła hipoteza aktywnie wprowadzała wyszukiwanie w błąd.

Jakość generacji hipotetycznej ma znaczenie. Używaj zdolnego modelu i starannie skonstruowanego promptu.

## Analiza kosztów

HyDE dodaje jedno wywołanie LLM na zapytanie użytkownika. Przy cenach Claude Sonnet (~$3/1M wejście + $15/1M wyjście):

- Prompt generacji hipotezy: ~150 tokenów
- Wyjście hipotezy: ~100–150 tokenów
- Koszt na zapytanie: ~$0.00045 + ~$0.0015 ≈ **$0.002 na zapytanie**

Przy 10 000 zapytań/miesiąc: ~$20/miesiąc dodatkowy koszt za HyDE.
Przy 50 000 zapytań/miesiąc: ~$100/miesiąc dodatkowy.
Przy 200 000 zapytań/miesiąc: ~$400/miesiąc dodatkowy.

Porównaj to z wartością 8–15 punktów procentowych poprawy recall wyszukiwania. Dla systemu produkcyjnego gdzie błędne wyszukiwanie oznacza złe odpowiedzi na pytania ubezpieczeniowe, wartość jest oczywista. Dla demo lub wewnętrznego narzędzia o niskiej stawce — może nie być warta dodatkowej latencji i kosztu.

**Wpływ na latencję:** Dodatkowe wywołanie LLM dodaje ~300–800ms do latencji p50. Dla interaktywnych aplikacji jest to odczuwalne. Możesz temu zaradzić przez:
- Asynchroniczną generację (zacznij wyszukiwanie z oryginalnym zapytaniem podczas gdy hipoteza się generuje, scal wyniki)
- Cachowanie hipotetycznych dokumentów dla częstych wzorców zapytań
- Użycie szybszego/tańszego modelu do generacji hipotezy (np. Claude Haiku)

## Połączenie z szerszym pipeline'em

To jest dzień 40 — start RAG Masterclass — ale HyDE nie żyje w izolacji. Łączy się bezpośrednio ze wszystkim omówionym w poprzednim tygodniu:

- **Dzień 38 (chunking):** Lepsze chunki → lepsze wyszukiwanie nawet bez HyDE. HyDE nie naprawia złego chunkingu; dodaje się na wierzch dobrego chunkingu.
- **Dzień 37 (dobór modelu):** Model używany do generacji HyDE wpływa na jakość hipotetycznego dokumentu. Model bez silnej wiedzy domenowej generuje słabsze hipotezy.
- **Dzień 39 (koszty):** Każde wywołanie HyDE dodaje do Twoich kosztów API. Uwzględnij to w modelu kosztowym przed globalnym włączeniem.

HyDE to jedna technika w warstwowym stosie wyszukiwania. Jutro: RAPTOR — co robić gdy nawet dobry chunking traci kontekst między sekcjami długiego dokumentu.

---

*Dzień 40 serii RAG Masterclass. Seria ta jest rozwinięciem RAG Deep Dive (dni 37–39). Jeśli nie widziałeś tamtych postów, zacznij od nich.*
