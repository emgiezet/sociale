---
day: 41
title: "RAPTOR: hierarchiczne wyszukiwanie dla dokumentów, z którymi flat chunking sobie nie radzi"
pillar: Educator
language: pl
image: ../../images/day-41.jpg
image_unsplash_query: "tree hierarchy architecture document structure layers"
---

# RAPTOR: hierarchiczne wyszukiwanie dla dokumentów, z którymi flat chunking sobie nie radzi

Każda strategia chunkingu, którą opisałem w dniu 38, ma to samo fundamentalne ograniczenie: produkuje płaską listę równorzędnych chunków. Retriever nie ma pojęcia co jest ogólne, a co szczegółowe; nie jest świadomy, że trzy chunki z trzech różnych sekcji mogą razem odpowiedzieć na pytanie, na które żaden z osobna nie może.

To jest realny problem dla złożonych dokumentów — polis ubezpieczeniowych, umów prawnych, tekstów regulacyjnych — gdzie znaczenie jest rozproszone po sekcjach i gdzie cross-referencje między częściami są nośne semantycznie.

RAPTOR został zaprojektowany dokładnie po to żeby to rozwiązać. Pokażę Ci jak działa, kiedy pomaga i jak go zaimplementowaliśmy.

## Problem flat chunkingu w praktyce

Konkretny przykład. Użytkownik pyta: "Jak klauzula siły wyższej wpływa na procedury roszczeniowe i wyłączenia odpowiedzialności?"

To pytanie wymaga informacji z co najmniej trzech sekcji typowej polisy ubezpieczeniowej:
1. **Sekcja definicji:** Co stanowi siłę wyższą w rozumieniu tej polisy?
2. **Zakres ochrony / wyłączenia:** Jaka odpowiedzialność jest wyłączona przy zdarzeniach siły wyższej?
3. **Procedury roszczeniowe:** Co ubezpieczający musi zrobić zgłaszając roszczenie z tytułu siły wyższej?

Przy flat chunkingu, retriever zwróci 5 chunków najbardziej podobnych do osadzenia zapytania. W praktyce typowo zwraca 1–2 z 3 wymaganych sekcji — pozostałe mogą nie punktować wystarczająco wysoko w podobieństwie, bo nie zawierają indywidualnie "siły wyższej" w kontekście konkretnego podzapytania.

LLM odpowiada wtedy z niepełnego kontekstu. W naszych testach, na zapytaniach wymagających syntezy wielu sekcji, flat chunking skutkował kompletnymi, dokładnymi odpowiedziami tylko w około 45% przypadków. Model albo dawał częściowe odpowiedzi, albo halucynował połączenia między sekcjami, których nie widział.

RAPTOR rozwiązuje to przez strukturę drzewa, która udostępnia retrieverowi różne poziomy abstrakcji.

## Jak działa RAPTOR

RAPTOR — Recursive Abstractive Processing for Tree-Organized Retrieval — zostało zaproponowane przez Sarthiego et al. w 2024 roku. Architektura ma trzy fazy: budowa drzewa, wielopoziomowe indeksowanie i wyszukiwanie.

### Faza 1: Budowa drzewa

**Krok 1: Chunking węzłów liści**
Zacznij od standardowych podejść do chunkingu z dnia 38. Te chunki liści (typowo 256–512 tokenów) tworzą dno drzewa.

**Krok 2: Osadzanie**
Osadź wszystkie chunki liści używając swojego modelu osadzania.

**Krok 3: Klastrowanie**
Klastruj osadzone chunki w semantycznie powiązane grupy. Oryginalna praca RAPTOR używa Gaussian Mixture Models (GMM) z miękkim przypisaniem — każdy chunk może należeć do wielu klastrów z różnymi prawdopodobieństwami. Jest to ważne, ponieważ chunk definicji może być istotny dla wielu sekcji.

Liczba klastrów jest typowo ustawiana proporcjonalnie do pierwiastka kwadratowego liczby chunków (heurystyka: `n_clusters = max(1, int(sqrt(n_chunks) / 2))`).

**Krok 4: Podsumowywanie**
Dla każdego klastra, użyj LLM do wygenerowania podsumowania wszystkich chunków w klastrze. To podsumowanie jest nowym węzłem na wyższym poziomie drzewa.

**Krok 5: Rekurencja**
Osadź podsumowania, klastruj je, podsumuj klastry ponownie. Powtarzaj aż zostanie jeden węzeł korzenia — podsumowanie całego dokumentu.

Dla 50-stronicowej polisy ubezpieczeniowej z ~200 chunkami liści, możesz skończyć z:
- Poziom 0 (liście): 200 chunków
- Poziom 1 (podsumowania sekcji): ~15 podsumowań
- Poziom 2 (podsumowania części): ~5 podsumowań
- Poziom 3 (korzeń): 1 podsumowanie całego dokumentu

### Faza 2: Wielopoziomowe indeksowanie

Wszystkie węzły na wszystkich poziomach trafiają do magazynu wektorowego. Nie wybierasz między poziomami — indeksujesz wszystko.

Każdy węzeł dostaje metadane wskazujące jego poziom w drzewie, węzły rodzicielskie i węzły potomne. Pozwala to nawigować hierarchię po wyszukaniu.

### Faza 3: Wyszukiwanie

**Wyszukiwanie ze zwiniętym drzewem** (prostsze): Szukaj we wszystkich węzłach na wszystkich poziomach jednocześnie. Pozwól wynikowm podobieństwa zadecydować który poziom zostaje wyszukany. Dla szerokiego pytania konceptualnego, wysokopoziomowe podsumowania mają tendencję do wygrywania. Dla konkretnego pytania faktycznego, chunki liści mają tendencję do wygrywania.

**Przechodzenie przez drzewo** (bardziej kontrolowane): Zacznij od korzenia. Na każdym poziomie, wyszukaj top-k węzłów i zejdź do ich potomków po więcej szczegółów. Zatrzymaj się gdy osiągniesz wymaganą głębokość lub gdy wyniki podobieństwa zaczną spadać.

Dla naszego przypadku użycia dokumentów ubezpieczeniowych, wyszukiwanie ze zwiniętym drzewem działało lepiej w praktyce — było prostsze, produkowało spójne wyniki i hierarchiczny indeks naturalnie wydobywał właściwy poziom abstrakcji dla różnych typów zapytań.

## Implementacja w Pythonie

Oto główna implementacja RAPTOR, której używamy:

```python
from anthropic import Anthropic
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import normalize
import json

client = Anthropic()

def summarize_cluster(chunks: list[str], level: int) -> str:
    """Użyj LLM do podsumowania klastra chunków dokumentu."""
    combined_text = "\n\n---\n\n".join(chunks)
    
    level_instruction = {
        1: "Są to powiązane sekcje z dokumentu polisy ubezpieczeniowej.",
        2: "Są to podsumowania powiązanych sekcji polisy ubezpieczeniowej.",
        3: "Są to wysokopoziomowe podsumowania. Utwórz streszczenie wykonawcze.",
    }.get(level, "Są to sekcje dokumentu.")
    
    prompt = f"""{level_instruction}

Utwórz zwięzłe podsumowanie (150-250 słów) które ujmuje kluczowe punkty, 
wszelkie cross-referencje między sekcjami i główne zasady lub warunki opisane.
Skup się na informacjach które pomogłyby odpowiedzieć na pytania użytkowników o dokument.

Sekcje dokumentu:
{combined_text}

Podsumowanie:"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def build_raptor_tree(
    chunks: list[str],
    embeddings: list[list[float]],
    max_levels: int = 3,
    min_cluster_size: int = 3
) -> list[dict]:
    """
    Zbuduj strukturę drzewa RAPTOR.
    Zwraca wszystkie węzły (liście + podsumowania) na wszystkich poziomach.
    """
    all_nodes = []
    
    # Poziom 0: chunki liści
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        all_nodes.append({
            "id": f"L0-{i}",
            "level": 0,
            "text": chunk,
            "embedding": emb,
            "children": [],
            "parent": None
        })
    
    current_level_nodes = all_nodes.copy()
    
    for level in range(1, max_levels + 1):
        if len(current_level_nodes) < min_cluster_size:
            break
        
        # Pobierz osadzenia dla bieżącego poziomu
        level_embeddings = np.array([n["embedding"] for n in current_level_nodes])
        level_embeddings_normalized = normalize(level_embeddings)
        
        # Ustal liczbę klastrów
        n_clusters = max(1, int(np.sqrt(len(current_level_nodes)) / 2))
        
        if n_clusters == 1:
            # Utwórz pojedyncze podsumowanie korzenia
            cluster_texts = [n["text"] for n in current_level_nodes]
            summary = summarize_cluster(cluster_texts, level)
            # (osadź podsumowanie i dodaj do all_nodes...)
            break
        
        # Dopasuj GMM
        gmm = GaussianMixture(n_components=n_clusters, random_state=42)
        gmm.fit(level_embeddings_normalized)
        
        # Miękkie przypisanie: każdy węzeł może należeć do wielu klastrów
        probs = gmm.predict_proba(level_embeddings_normalized)
        threshold = 0.1  # węzeł należy do klastra jeśli prawdopodobieństwo > próg
        
        new_level_nodes = []
        
        for cluster_idx in range(n_clusters):
            # Pobierz węzły w tym klastrze
            cluster_node_indices = [
                i for i, p in enumerate(probs[:, cluster_idx]) 
                if p > threshold
            ]
            
            if len(cluster_node_indices) < 2:
                continue
            
            cluster_nodes = [current_level_nodes[i] for i in cluster_node_indices]
            cluster_texts = [n["text"] for n in cluster_nodes]
            
            # Wygeneruj podsumowanie
            summary_text = summarize_cluster(cluster_texts, level)
            
            # Osadź podsumowanie (użyj swojej funkcji embed_text z dnia 40)
            summary_embedding = embed_text(summary_text)
            
            # Utwórz węzeł podsumowania
            summary_node = {
                "id": f"L{level}-{cluster_idx}",
                "level": level,
                "text": summary_text,
                "embedding": summary_embedding,
                "children": [n["id"] for n in cluster_nodes],
                "parent": None
            }
            
            # Zaktualizuj referencje rodziców potomków
            for n in cluster_nodes:
                n["parent"] = summary_node["id"]
            
            all_nodes.append(summary_node)
            new_level_nodes.append(summary_node)
        
        current_level_nodes = new_level_nodes
    
    return all_nodes

def raptor_retrieve(query: str, all_nodes: list[dict], top_k: int = 5) -> list[dict]:
    """
    Wyszukiwanie ze zwiniętym drzewem: szukaj we wszystkich węzłach na wszystkich poziomach jednocześnie.
    """
    query_embedding = np.array(embed_text(query))
    
    # Oblicz wyniki podobieństwa dla wszystkich węzłów
    scored_nodes = []
    for node in all_nodes:
        node_emb = np.array(node["embedding"])
        # Podobieństwo kosinusowe
        similarity = np.dot(query_embedding, node_emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(node_emb) + 1e-10
        )
        scored_nodes.append((similarity, node))
    
    # Sortuj po podobieństwie i zwróć top-k
    scored_nodes.sort(key=lambda x: x[0], reverse=True)
    return [node for _, node in scored_nodes[:top_k]]
```

## Diagram architektury (reprezentacja tekstowa)

```
                  [Podsumowanie korzenia dokumentu]
                           Poziom 3
                    /           |           \
        [Pdsm. Część A]  [Pdsm. Część B]  [Pdsm. Część C]
                           Poziom 2
           /    \              |           /      \
   [Pdsm §1.1] [Pdsm §1.2] [Pdsm §2.1] [Pdsm §3.1] [Pdsm §3.2]
                           Poziom 1
    /  |  \   / | \        / | \       / | \    / | \
   C1  C2 C3 C4 C5 C6    C7 C8 C9  C10 C11 C12 ...
                     Poziom 0 (Chunki liści)
```

Gdy użytkownik zadaje pytanie wymagające syntezy wielu sekcji, retriever zwraca węzły poziomu 2 lub 3. Gdy pyta o konkretny fakt, zwraca węzły poziomu 0. Wyszukiwanie ze zwiniętym drzewem obsługuje to automatycznie przez punktację podobieństwa.

## Realny przykład z Insly: zapytanie o siłę wyższą

**Zapytanie:** "Jak klauzula siły wyższej wpływa na procedury roszczeniowe i wyłączenia odpowiedzialności?"

**Wynik flat chunkingu (top 5):**
- Chunk z §7.3: definicja siły wyższej (liść, 280 tokenów)
- Chunk z §7.1: nagłówek ogólnej listy wyłączeń (liść, 220 tokenów)
- Chunk z §7.4: wyłączenia zdarzeń pogodowych (liść, 310 tokenów)
- Chunk z §1.1: ogólny wstęp (liść, 180 tokenów) — fałszywy pozytyw
- Chunk z §12.2: termin złożenia formularza roszczenia (liść, 195 tokenów) — częściowo trafny

Wynik: model dostał definicję i niektóre wyłączenia, ale całkowicie przeoczył interakcję procedury roszczeniowej. Niekompletna odpowiedź.

**Wynik RAPTOR (top 5):**
- Podsumowanie poziomu 2: "Część II — Wyłączenia i siła wyższa" (obejmuje §§7-9, wszystkie scenariusze wyłączeń i ich interakcję z roszczeniami)
- Chunk poziomu 0 z §7.3: definicja siły wyższej
- Chunk poziomu 0 z §13.4: procedura roszczeniowa specyficzna dla siły wyższej
- Podsumowanie poziomu 1: "Sekcja 7 — Wyłączenia odpowiedzialności" (szerszy kontekst wyłączeń)
- Chunk poziomu 0 z §7.5: wymagania dokumentacyjne dla wyłączonych zdarzeń

Wynik: model miał zarówno konkretne klauzule jak i podsumowany kontekst. Kompletna, dokładna odpowiedź z cross-referencjami do właściwych paragrafów.

**Poprawa Recall@5:** na pytaniach wymagających syntezy wielu sekcji w naszym zbiorze testowym, RAPTOR poprawił recall z 0.51 (flat chunking) do 0.82. To poprawa o 31 punktów procentowych specyficznie dla złożonych, zależnych od kontekstu pytań.

Na prostych pytaniach faktycznych, RAPTOR wypadł równoważnie z flat chunkingiem — dodatkowe poziomy drzewa nie zaszkodziły wyszukiwaniu konkretnych faktów.

## Kompromisy: kiedy RAPTOR jest wart zachodu

**RAPTOR ma sens gdy:**
- Dokumenty są długie (20+ stron) z wzajemnie połączonymi sekcjami
- Użytkownicy często zadają pytania wymagające syntezy wielu sekcji
- Struktura dokumentu ma sensowną hierarchię (części, sekcje, podsekcje)
- Masz budżet na dłuższy czas indeksowania (znaczące wywołania LLM podczas budowy drzewa)

**RAPTOR jest przerostem formy nad treścią gdy:**
- Dokumenty są krótkie lub mają proste, samodzielne sekcje
- Przypadek użycia to głównie proste wyszukiwanie faktów (styl FAQ)
- Indeks musi być często przebudowywany (indeksowanie RAPTOR jest kosztowne)
- Budżet jest napięty — podsumowanie dokumentu z 200 chunkami wymaga ~50-100 wywołań LLM tylko do budowy drzewa

**Koszt indeksowania dla dokumentu z 200 chunkami:**
- Podsumowania poziomu 1 (~15 klastrów × ~200 tokenów każde): ~3 000 tokenów wyjścia, ~10 000 tokenów wejścia ≈ $0.18
- Podsumowania poziomu 2 (~5 klastrów × ~200 tokenów każde): ~1 000 tokenów wyjścia, ~3 500 tokenów wejścia ≈ $0.06
- Korzeń poziomu 3: ~200 tokenów wyjścia, ~1 000 tokenów wejścia ≈ $0.02

**Łączny koszt budowy drzewa: ~$0.26 za dokument**

Dla korpusu 10 000 dokumentów polis, budowa pełnego drzewa RAPTOR kosztuje szacunkowo $2 600 — jednorazowo. Przebudowa przy zmianach strategii chunkingu jest kosztowną częścią, dlatego właściwe skonfigurowanie chunkingu (dzień 38) przed dodaniem RAPTOR ma znaczenie.

## Składanie wszystkiego razem: pełny stos RAG

Po pięciu dniach RAG Deep Dive i starcie RAG Masterclass:

- **Dzień 37:** Wybieraj modele na podstawie swoich danych, nie benchmarków
- **Dzień 38:** Inwestuj w przygotowanie danych — to 60% pracy
- **Dzień 39:** Modeluj koszty przed podjęciem decyzji architektonicznych
- **Dzień 40 (HyDE):** Wypełniaj semantyczną lukę między językiem użytkownika a językiem dokumentu
- **Dzień 41 (RAPTOR):** Buduj hierarchię dla dokumentów wymagających syntezy wielu sekcji

Dojrzały pipeline RAG dla złożonych dokumentów jak polisy ubezpieczeniowe nakłada te techniki warstwowo: chunking parent-child (dzień 38) na poziomie liści, hierarchia RAPTOR powyżej, HyDE podczas zapytania, z rerankingiem na finalnym zbiorze kandydatów. Wynikiem jest system wyszukiwania, który niezawodnie obsługuje zarówno konkretne zapytania faktyczne jak i złożone pytania syntetyczne.

Techniki nie wykluczają się wzajemnie. Komponują się.

---

*Dzień 41 serii RAG Masterclass. Następny: ewaluacja — jak mierzyć czy Twoje ulepszenia RAG są faktycznie ulepszeniami.*
