---
day: 46
title_pl: "RAG kosztuje 500 albo 15 000 miesięcznie. Zależy od sześciu zmiennych."
pillar: Educator
format: Cost analysis
scheduled_date: 2026-06-04
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#LLM", "#InsurTech", "#AIArchitecture", "#TechLead", "#CloudCosts"]
image: ../images/day-46.jpg
cta: "Napisz 'RAG PRICING' jeśli wyceniasz RAG dla swojej organizacji — odezwę się."
blog_url: "https://mmx3.pl/blog/day-46-rag-pricing-model"
---

Klient mówi: "chcemy RAG-a."

Ja pytam: "na ilu dokumentach, w jakim języku, z jakim SLA jakości, i ile zapytań dziennie?"

Bo od tego zależy czy to kosztuje 500 czy 15 000 miesięcznie. I to zanim uwzględnimy compliance, utrzymanie i ewaluację.

---

**Dlaczego "ile kosztuje RAG" to złe pytanie**

To jak pytanie "ile kosztuje samochód." Zależy czy kupujesz Dacię Logan czy BMW M5. Oba to samochody. Oba dojeżdżają do celu. Ale to inne produkty, inne koszty eksploatacji, różni właściwi nabywcy.

RAG z 200 dokumentami w języku angielskim dla wewnętrznego HR i RAG z 20 000 dokumentami po polsku dla brokerów ubezpieczeniowych z wymogiem RODO i audit trail — oba to RAG. Ale to zupełnie inne wyceny.

Sześć zmiennych decyduje o cenie:

1. Wolumen. Liczba dokumentów i zapytań miesięcznie. 1 000 zapytań/dzień to inny świat niż 100 000.

2. Język. Angielski = tańsze modele, lepsza dostępność, niższe koszty embeddingów. Polski = droższe modele lub self-hosted (Bielik), wyższe koszty inferencji.

3. SLA jakości. 80% accuracy vs 95% to nie 15% różnicy w koszcie. To 2-3x różnica w koszcie ewaluacji, iteracji i utrzymania.

4. Compliance. RODO, data residency, audit trail. Każdy wymóg to koszt architektoniczny. Dane ubezpieczeniowe nie mogą opuścić UE. To wyklucza część opcji i wymaga konkretnych konfiguracji.

5. Integracje. Standalone chatbot vs embedded w CRM/ERP/systemie brokerskim. Ten drugi kosztuje 3-5x więcej w developmencie.

6. Utrzymanie. Kto ewaluuje, iteruje, re-indeksuje gdy dokumenty się zmienią? To ukryty koszt, który zabija projekty rok po wdrożeniu.

---

**Trzy architektury, ten sam case — trzy różne ceny**

Case: 1 000 dokumentów polskich, 5 000 zapytań/miesiąc, SLA 90% precision.

Opcja A, full managed (AWS Bedrock): niski koszt dev (~40h setup), wysoki koszt recurring (~1 200$/mies w tej skali). Pełna kontrola nad niczym. Najłatwiejsza na start, najdroższa w roku 3.

Opcja B, self-hosted (Bielik + Qdrant na EC2): wysoki koszt dev (~200h setup), niski recurring po break-even (~300$/mies po amortyzacji sprzętu). Pełna kontrola. Najtrudniejszy start, najtańszy rok 3.

Opcja C, hybrid (Bedrock dla generacji + self-hosted wektorówka): umiarkowany dev (~100h), umiarkowany recurring (~600$/mies). Dobry balans.

Klient myślał że Opcja B jest najtańsza. Spojrzeliśmy na TCO rok 3: Opcja A 43 000$, Opcja B 28 000$, Opcja C 24 000$. Opcja C wygrała — najlepsza proporcja przy jego skali.

---

**Ukryte koszty, których klienci nie widzą**

→ Ongoing ewaluacja. Ktoś musi uruchamiać i interpretować canary test set. 4-8h/miesiąc inżynierskiego czasu.  
→ Model drift. Modele Bedrock są cicho aktualizowane. Precision może spaść z dnia na noc. Ktoś musi to monitorować.  
→ Re-indeksowanie. Dokumenty ubezpieczeniowe zmieniają się co roku. Re-indeksowanie 1 000 dokumentów to koszt embeddingów + weryfikacja jakości.  
→ Support użytkowników. Pierwsze 3 miesiące po wdrożeniu to 40% czasu na pytania "dlaczego nie wie o X?"

---

Na blogu opisuję pełny model TCO z tabelą rok 1/rok 2/rok 3 dla każdej architektury i szacunkami opartymi na opublikowanych cennikach. Nic nie jest zmyślone, wszystkie szacunki są jawnie oznaczone.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-46-rag-pricing-model

#RAG #AI #LLM #InsurTech #AIArchitecture #TechLead #CloudCosts
