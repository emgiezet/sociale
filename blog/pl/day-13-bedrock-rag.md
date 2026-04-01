---
day: 13
title: "Budowanie pierwszego pipeline'u RAG na AWS Bedrock: praktyczny przewodnik"
pillar: Educator
language: pl
image: ../../images/day-13.jpg
image_unsplash_query: "AWS cloud architecture diagram"
---

# Budowanie pierwszego pipeline'u RAG na AWS Bedrock: praktyczny przewodnik

To jest przewodnik, który chciałem mieć, kiedy zaczynałem budować systemy RAG w Insly. Większość tutoriali albo pomija zagadnienia produkcyjne, albo grzebie je w złożoności. Ten jest zaprojektowany, żeby być praktyczny, sekwencyjny i uczciwy w kwestii tego, gdzie są trudne miejsca.

Zbudowałem 3 systemy RAG w produkcji. Pod koniec tego przewodnika zrozumiesz pełny pipeline RAG na AWS Bedrock — od surowych dokumentów do wygenerowanych odpowiedzi — z wystarczającym kontekstem, żeby zbudować i ocenić swój pierwszy system.

## Co Budujemy

RAG — Retrieval-Augmented Generation — to dominujący wzorzec dla enterprise AI odpowiadającego na pytania na podstawie Twoich własnych dokumentów i danych. Główna idea: zamiast polegać na wyuczonej wiedzy LLM (która nie zawiera Twoich danych), pobierasz odpowiednią treść z magazynu dokumentów i dołączasz ją do kontekstu promptu.

AWS Bedrock zapewnia zarządzane środowisko zarówno dla infrastruktury retrieval (poprzez Bedrock Knowledge Bases) jak i modeli generacji (Claude, Titan, Llama i inne).

## Krok 1: Przygotowanie Dokumentów

Jakość Twojego systemu RAG jest w dużej mierze określona zanim napiszesz jedną linię kodu retrieval. Przygotowanie dokumentów — ekstrakcja, czyszczenie, chunkowanie — to miejsce, gdzie jakość jest tworzona lub tracona.

**Ekstrakcja.** Pobierz tekst z dokumentów źródłowych. Ekstrakcja PDF jest dobrze obsługiwana przez biblioteki takie jak `pypdf` lub `pdfplumber`. DOCX przez `python-docx`. HTML przez `beautifulsoup4`. Dla zeskanowanych dokumentów potrzebujesz OCR — Amazon Textract radzi sobie z tym dobrze i naturalnie integruje się z pipeline'ami Bedrock.

**Czyszczenie.** Usuń artefakty z ekstrakcji: nagłówki i stopki stron, znaki wodne, powtarzający się tekst nawigacyjny, błędy kodowania. Znormalizuj białe znaki. Identyfikuj i obsługuj tabele specjalnie — dane tabelaryczne często wymagają ekstrakcji i formatowania jako tekst.

**Chunkowanie.** Podziel dokumenty na segmenty, które będą indywidualnie embeddowane i pobierane. Kluczowe parametry:
- Rozmiar chunka: zazwyczaj 300–800 tokenów dla większości przypadków użycia
- Overlap: 50–100 tokenów nakładania między sąsiednimi chunkami, żeby kontekst nie był tracony na granicach
- Strategia podziału: stały rozmiar lub semantyczny (podział na granicach akapitu lub zdania)

Przechowuj każdy chunk z metadanymi: co najmniej identyfikator dokumentu źródłowego i sekcję/pozycję.

## Krok 2: Tworzenie Embeddingów

Embeddingi to numeryczne reprezentacje wektorowe tekstu, które chwytają semantyczne znaczenie. Podobny tekst będzie miał podobne wektory, co pozwala na retrieval oparty na podobieństwie.

W AWS Bedrock masz dwie główne opcje modelu embeddingowego:
- **Amazon Titan Embeddings G1 – Text**: własny model embeddingowy AWS, dobrze zintegrowany z Bedrock Knowledge Bases
- **Cohere Embed**: silna wydajność wielojęzyczna, jeśli pracujesz z dokumentami inny niż angielski

Aby stworzyć embedding dla chunka:

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def embed_text(text: str) -> list[float]:
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=json.dumps({'inputText': text})
    )
    body = json.loads(response['body'].read())
    return body['embedding']
```

Zrób to dla każdego chunka w swoim korpusie. Przechowuj wynikowe wektory obok tekstu chunka i metadanych w swoim vector store.

## Krok 3: Vector Store

Twój vector store to miejsce, gdzie żyją embeddingi i gdzie działa wyszukiwanie podobieństw. AWS Bedrock Knowledge Bases używa Amazon OpenSearch Serverless jako natywnego vector store.

Jeśli już korzystasz z PostgreSQL na AWS RDS, `pgvector` jest praktyczną alternatywą — dodaje wyszukiwanie podobieństwa wektorowego do Twojej istniejącej bazy danych bez wprowadzania nowego data store.

Dla pierwszego systemu Bedrock Knowledge Bases to najszybsza droga do działającego pipeline'u retrieval. Tworzysz knowledge base, łączysz go z bucketem S3 zawierającym Twoje dokumenty, a Bedrock obsługuje chunkowanie, embeddowanie i indeksowanie automatycznie.

## Krok 4: Retrieval

Kiedy użytkownik zadaje pytanie, krok retrieval znajdu je chunki najbardziej odpowiednie do tego pytania.

```python
bedrock_agent = boto3.client('bedrock-agent-runtime')

response = bedrock_agent.retrieve(
    knowledgeBaseId='YOUR_KB_ID',
    retrievalQuery={'text': query},
    retrievalConfiguration={
        'vectorSearchConfiguration': {'numberOfResults': 5}
    }
)
chunks = response['retrievalResults']
```

Dodaj filtrowanie metadanych, żeby ograniczyć retrieval do odpowiednich dokumentów. To szczególnie ważne dla aplikacji wielodostępnych — nie chcesz pobierać dokumentów tenanta A dla zapytań tenanta B.

## Krok 5: Generacja

Z pobranymi chunkami w rękach, zbuduj prompt dla swojego modelu generacji i wywołaj go:

```python
def generate_answer(query: str, chunks: list[dict]) -> str:
    context = '\n\n'.join([c['content']['text'] for c in chunks])

    prompt = f"""Jesteś pomocnym asystentem. Odpowiedz na pytanie wyłącznie na podstawie dostarczonego kontekstu.
Jeśli kontekst nie zawiera wystarczających informacji do odpowiedzi na pytanie, powiedz to wprost.

Kontekst:
{context}

Pytanie: {query}

Odpowiedź:"""

    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1024
        })
    )
    body = json.loads(response['body'].read())
    return body['content'][0]['text']
```

Systemowy prompt ma większe znaczenie niż większość tutoriali przyznaje. Bądź wyraźny co do tego, co model powinien robić, kiedy kontekst nie ma odpowiedzi. "Powiedz to wprost" jest lepsze niż halucynowanie wiarygodnie brzmiącej odpowiedzi.

## Krok 6: Ewaluacja (Krok, który Większość Ludzi Pomija)

Budowanie pipeline'u retrieval i generacji to może 40% pracy. Pozostałe 60% to uczynienie go godnym zaufania — co wymaga ewaluacji.

Tu nauczyliśmy się kosztownym sposobem w Insly. Wyslaliśmy system, z którego byliśmy dumni. Potem zbudowaliśmy właściwy zestaw ewaluacyjny i odkryliśmy, że odpowiadał nieprawidłowo na znaczący procent pytań w sposób, który nie był oczywisty z przypadkowego testowania.

Zbuduj zestaw testowy 50–100 par pytanie/odpowiedź. Poproś eksperta domenowego o walidację oczekiwanych odpowiedzi. Mierz:

- **Recall retrieval**: czy odpowiednie chunki są pobierane dla każdego testowego pytania?
- **Wierność odpowiedzi**: czy wygenerowana odpowiedź jest wsparta przez pobrany kontekst, czy halucynuje?
- **Trafność odpowiedzi**: czy odpowiedź adresuje postawione pytanie?

Frameworki takie jak RAGAS mogą automatyzować niektóre z tych pomiarów używając podejść LLM-as-judge. Są niedoskonałe, ale przydatne do śledzenia trendów.

Bez ewaluacji masz system, który masz nadzieję, że działa. Z ewaluacją masz system, o którym wiesz, że działa — i wiesz, w jakich aspektach nie działa, więc możesz je poprawić.

## Co Bedrock Robi Dobrze (i Na Co Uważać)

**Robi dobrze:** Zarządzana infrastruktura, wbudowane IAM, rozsądna postawa compliance dla workloadów EU z odpowiednią konfiguracją regionu. W regulowanych branżach takich jak ubezpieczenia i finanse (gdzie obowiązuje KNF i RODO), możliwość trzymania danych w Twoim koncie i regionie AWS ma duże znaczenie.

**Uważaj:** Strategia chunkowania ma większe znaczenie niż ludzie myślą. Domyślne ustawienia działają dla ogólnego tekstu. Dokumenty techniczne, klauzule polisowe i dane strukturyzowane często wymagają niestandardowego chunkowania.

**Uważaj:** Złożone relacje między dokumentami. Jeśli Twoje dokumenty odwołują się do siebie nawzajem, Bedrock Knowledge Bases nie modeluje tych relacji. Pobiera podobny tekst. Nie rozumuje o połączeniach. Do tego potrzebujesz czegoś takiego jak LightRAG.

## Kolejne Kroki Po Pierwszym Systemie

Ten pipeline daje Ci funkcjonalny system RAG. Od tego momentu ulepszenia z największym wpływem:

→ Dodaj re-ranker cross-encoder między retrieval a generacją
→ Popraw strategię chunkowania na podstawie wyników ewaluacji
→ Dodaj wyszukiwanie hybrydowe (wektorowe + BM25) dla lepszego recall na dokładnej terminologii
→ Zaimplementuj dekompozycję zapytań dla złożonych wieloczęściowych pytań

Zacznij od Kroku 1. Ewaluuj przy Kroku 6. Iteruj na podstawie tego, co mierzysz. To jest droga od demo do produkcji.
