---
day: 38
title_pl: "Spędziliśmy 2 tygodnie optymalizując prompty. Potem sprawdziliśmy co retriever faktycznie zwraca. Problem był w chunkingu."
pillar: Educator
format: Deep dive
scheduled_date: 2026-05-07
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#DataEngineering", "#InsurTech", "#NLP", "#GenAI"]
image: ../images/day-38.jpg
cta: "Jaką strategię chunkingu stosujecie? Ciekaw jestem czy mieliście podobne odkrycia."
blog_url: "https://mmx3.pl/blog/day-38-rag-data-chunking"
---

Spędziłem 2 tygodnie optymalizując prompty. Potem sprawdziłem co retriever faktycznie zwraca. Problem był w chunkingu.

Klasyczna pułapka RAG-a. Model generuje odpowiedź, która jest niespójna albo niekompletna. Zakładasz, że prompt jest zbyt ogólny. Iterujesz. Dwa tygodnie i dziesięć wersji promptu później — nadal niedobrze.

A potem loguję się do pipeline'u i patrzę na to, co faktycznie trafia do kontekstu modelu. I tam jest odpowiedź: retriever zwraca środek klauzuli. Bez nagłówka sekcji. Bez numeracji ustępu. Bez kontekstu definicji, która była dwa akapity wyżej.

Model nie ma szans. Nawet najlepszy LLM nie wygeneruje poprawnej odpowiedzi, jeśli dostanie fragment, który jest niepełny.

I tak zaczęło się prawdziwe 60% pracy w RAG-u.

To samo zdanie, cztery różne chunki

Weźmy konkretny przykład. Klauzula z polisy ubezpieczeniowej:

"Ubezpieczyciel ponosi odpowiedzialność za szkody powstałe wskutek powodzi, z wyłączeniem przypadków określonych w §4 ust. 2 niniejszej umowy, o ile Ubezpieczający wyraził pisemną zgodę na rozszerzenie zakresu ochrony w trybie §8."

Podziel to na cztery sposoby i dostaniesz cztery różne wyniki wyszukiwania:

→ Fixed-size 256 tokenów: zdanie trafia w środek chunka razem z poprzednim akapitem o definicji "powodzi". Retriever go nie znajdzie, bo wyszukiwanie po "zakres ochrony powodziowej" trafi na inny chunk.

→ Semantic chunking: zdanie jest osobnym chunkiem, ale odcięte od definicji §4 ust. 2, do której odsyła. Odpowiedź modelu będzie niekompletna.

→ Section-based: cała sekcja "Zakres ochrony" jako jeden chunk — zbyt długa, retriever ją zdepriorytetyzuje przez "dilution" rzadkich terminów.

→ Parent-child z metadanymi: zdanie jako child chunk z metadanymi sekcji, numeru paragrafu i tytułu dokumentu. Retrieval trafia w punkt. Model ma kontekst.

Różnica w wynikach: między "nie rozumiem pytania" a "oto precyzyjna odpowiedź z numerem paragrafu."

Dlaczego to jest 60% pracy

Brzmi trywialnie dopóki nie zobaczysz realnych danych: polisy z dziesięciu europejskich rynków, część w Word sprzed 2010 roku, część jako skany OCR z artyfaktami, część jako PDF z tabelami i nagłówkami wbudowanymi w obraz.

Zanim cokolwiek podzielisz na chunki — musisz mieć czysty tekst. A żeby mieć czysty tekst z legacy dokumentów — to jest projekt sam w sobie.

Pełny pipeline opisuję na blogu: od brudnego PDF do czystego chunka z metadanymi. Krok po kroku. Z przykładami z dokumentów polis z wielu rynków.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-38-rag-data-chunking

#RAG #AI #LLM #DataEngineering #InsurTech #NLP #GenAI
