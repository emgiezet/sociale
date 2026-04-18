---
day: 34
title_pl: "Nowe projekty z AI od dnia zero wyglądają zupełnie inaczej. Oto co pokazałem zespołowi."
pillar: Trenches
format: How-to
scheduled_date: 2026-04-23
posting_time: "08:00 CET"
hashtags: ["#AI", "#WarsztatyAI", "#ZespółDeweloperski", "#TechLead", "#AIFirst"]
image: ../images/day-34.jpg
cta: "Które z tych podejść stosujesz? A które Cię zaskoczyło?"
blog_url: "https://mmx3.pl/blog/day-34-warsztaty-nowe-projekty"
---

Nowe projekty z AI od dnia zero wyglądają zupełnie inaczej. Oto co pokazałem zespołowi.

Nie chodzi o to, żeby wrzucić Copilota do repo i czekać na cud.

Podczas warsztatów jeden z uczestników zapytał: "Dobra, ale od czego właściwie zacząć?" I to jest właśnie to pytanie, na które większość tutoriali nie odpowiada. Bo "AI-first" brzmi jak buzzword, a pod spodem jest bardzo konkretny workflow.

Oto co pokazałem — w takiej kolejności, w jakiej to stosuję w praktyce:

→ Wymagania razem z AI, nie po AI. Zanim napiszesz pierwszą linię kodu, otwórz Clauda i opisz problem domenowy. Nie po to, żeby dostać gotowe rozwiązanie — po to, żeby zadać sobie pytania, których sam byś nie zadał. AI widzi luki w wymaganiach szybciej niż większość review.

→ Projektowanie z asystentem, nie z białą kartką. Opisz kontekst, ograniczenia, stack. Poproś o warianty. Potem dyskutuj, odrzucaj, wybieraj. To nie jest oddanie decyzji. To skompresowanie pierwszych 3 godzin myślenia do 30 minut.

→ Implementacja: Cursor jako pair programmer. Nie "wygeneruj mi cały serwis". Krótkie pętle: napisz — sprawdź — zmodyfikuj prompt — wygeneruj test — sprawdź ponownie. Pokazałem jak to wygląda na realnym kodzie Go i Python.

→ Review kodu przez AI zanim trafi do ludzi. Przed każdym PR — daj go AI z konkretnym promptem: "Sprawdź czy to jest bezpieczne pod kątem X, czy naruszam zasadę Y, jakie edge case'y pominąłem." Na warsztatach inżynierowie zaczęli łapać rzeczy, których wcześniej nie widzieli.

→ Testy generowane, nie wymyślane. Opisujesz zachowanie, AI generuje przypadki testowe — włącznie z tymi nieprzyjemnymi. Potem weryfikujesz, czy to ma sens. Czas pisania testów skrócił się wyraźnie, ale co ważniejsze — testy stają się myśleniem, nie klepaniem.

Efekt po pierwszym dniu warsztatów?

Jeden z seniorów powiedział: "Kurczę, ja przez ostatnie trzy lata traciłem czas na rzeczy, które AI robi w 5 minut." Nie powiedział tego z frustracją. Powiedział to z ulgą.

Bo to nie jest rewolucja. To odciążenie od żmudnych fragmentów pracy.

Które z tych podejść stosujesz już na co dzień? A które Cię zaskoczyło?

Pełny artykuł na blogu: https://mmx3.pl/blog/day-34-warsztaty-nowe-projekty

#AI #WarsztatyAI #ZespółDeweloperski #TechLead #AIFirst
