---
day: 23
title_pl: "Jak oceniać jakość systemu RAG bez zespołu ML."
pillar: Educator
format: Tutorial
scheduled_date: 2026-04-24
posting_time: "08:00 CET"
hashtags: ["#RAG", "#AI", "#MachineLearning", "#InżynieriaOprogramowania", "#QualityAssurance"]
image: ../images/day-23.jpg
cta: "Zapisz to — będziesz tego potrzebować"
blog_url: "https://mmx3.pl/blog/day-23-rag-evaluation"
---

Jak oceniać jakość systemu RAG bez zespołu ML.

Zbudowałem 3 systemy RAG. Dwa kosztowały mnie drogie lekcje. To jest framework ewaluacyjny, który chciałbym mieć od pierwszego dnia. Nie potrzebujesz zespołu data science. Potrzebujesz procesu.

1. Precyzja retrieval

Czy retriever wyciąga właściwe fragmenty? Buduję zestaw testowy 50-100 par pytanie/oczekiwany-dokument. Uruchamiam retriever i sprawdzam, jaki procent właściwych dokumentów pojawia się w 5 najlepszych wynikach. Celuję w >80% zanim dotknę warstwy LLM. Zmarnowałem dwa tygodnie optymalizując prompty, zanim zdałem sobie sprawę, że retriever był faktycznym problemem 🤦

2. Wierność odpowiedzi

Czy odpowiedź jest zakorzeniona w tym, co zostało pobrane? Używam sędziego LLM (GPT-4o lub Claude), by sprawdzić, czy każda odpowiedź może być prześledzona do pobranego kontekstu. Oznaczam wszystko poniżej 90%. To wyłapuje halucynacje, które wyglądają na pewne.

3. Trafność odpowiedzi

Czy odpowiedź rzeczywiście odpowiada na pytanie? Różne od wierności: w pełni zakorzeniona odpowiedź może nadal chybić sedna. Oceniam w skali 1-5. Cokolwiek poniżej średniej 3,5 to problem promptu lub fragmentacji, nie modelu.

4. Czerwone linie halucynacji

W ubezpieczeniach niektóre typy błędów są katastrofalne: błędne kwoty pokrycia, niepoprawne warunki polisy, sfabrykowane odniesienia prawne. Utrzymuję listę ~30 "pytań kanarych", gdzie każda halucynacja jest blokadą. Uruchamiają się przy każdym wdrożeniu.

5. Ewaluacja A/B przed zmianami

Nie zmieniam strategii fragmentacji, parametrów retrieval ani promptów bez uruchomienia pełnego zestawu testowego na starym i nowym. Nawet zmiany, które wydają się poprawkami, mogą łamać przypadki brzegowe. Utrzymuję bazę regresji i wymagam poprawy netto we wszystkich czterech metrykach przed mergem.

Narzędzia, których używam: własne skrypty ewaluacyjne w Pythonie, LLM-as-judge przez AWS Bedrock, wyniki logowane do prostego arkusza kalkulacyjnego. Nie potrzebujesz RAGAS ani platformy obserwabilności za 200 tys. zł, żeby zacząć.

System RAG bez ewaluacji to demo. Z ewaluacją staje się produktem 🎓

Zapisz to. Będziesz tego potrzebować, kiedy pierwsza ewaluacja ujawni, że Twój retriever był wąskim gardłem przez cały czas.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-23-rag-evaluation

#RAG #AI #MachineLearning #InżynieriaOprogramowania #QualityAssurance
