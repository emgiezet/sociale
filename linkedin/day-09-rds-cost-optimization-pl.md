---
day: 9
title_pl: "Nasz rachunek AWS RDS rósł o 40% rok do roku. Oto co z tym zrobiliśmy."
pillar: Builder
format: Technical
scheduled_date: 2026-04-02
posting_time: "07:30 CET"
hashtags: ["#AWS", "#OptymalizacjaBazDanych", "#KosztyChury", "#InżynieriaOprogramowania"]
image: ../images/day-09.jpg
cta: "Jakie jest Twoje największe zaskoczenie kosztowe AWS? Napisz w komentarzu."
blog_url: "https://mmx3.pl/blog/day-09-rds-cost-optimization"
---

Nasz rachunek AWS RDS rósł o 40% rok do roku. Oto co z tym zrobiłem.

W Insly buduję multi-tenant oprogramowanie ubezpieczeniowe na rynkach europejskich. Wolumen danych rośnie. To oczekiwane. Ale 40% roczny wzrost kosztów RDS bez proporcjonalnego wzrostu użytkowników oznaczał, że coś jest nie tak. I nie była to baza danych.

**Krok 1: Diagnoza**
Zacząłem od AWS Cost Explorer i RDS Performance Insights. W ciągu dwóch godzin zidentyfikowałem 10 najdroższych zapytań według łącznego czasu wykonania 🕵️ Trzy z nich odpowiadały za ponad 60% obciążenia CPU. Dwa z tych trzech nie miały indeksów na filtrowanych kolumnach.

Kod legacy. Dodany lata temu. Nigdy nieodwiedzony 😐

**Krok 2: Analiza zapytań**
Użyłem `pg_stat_statements` do uchwycenia wzorców zapytań przez pełny tydzień. To było bardziej użyteczne niż profilowanie punktowe. Obciążenia ubezpieczeniowe nie są jednorodne: aktywność brokerów szczytuje o określonych godzinach, raporty kwartalne tworzą skoki. Tydzień danych pokazał wzorce, które przegapiłbym w 2-godzinnym oknie.

**Krok 3: Targetowane indeksowanie**
Nie dodawałem indeksów na ślepo. Każdy kandydat przechodził przez to samo sprawdzenie:
→ Ile razy dziennie to zapytanie jest uruchamiane?
→ Jaki jest stosunek zapis do odczytu dla tej tabeli?
→ Jaka jest rzeczywista selektywność proponowanego indeksu?

Nadmierne indeksowanie tabel z wysokim zapisem może pogorszyć sytuację. Dodałem 6 indeksów, usunąłem 3 które były nieużywane i dodawały overhead zapisu.

**Krok 4: Right-sizing instancji**
Performance Insights pokazało, że szczytowe wykorzystanie CPU wynosiło 35%. Siedziałem na instancji z 70%+ headroomem w zapasie. Obniżyłem o jeden tier dla dwóch nie-krytycznych replik. Headroom zachowałem tam, gdzie miał znaczenie.

**Wynik: koszty RDS przestały rosnąć. Roczny rachunek jest stabilny, a wolumen danych nadal rośnie.**

To nie była sprytna architektura. To był pomiar, a potem działanie. W tej kolejności.

Jakie jest Twoje największe zaskoczenie kosztowe AWS? Napisz w komentarzu.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-09-rds-cost-optimization

#AWS #OptymalizacjaBazDanych #KosztyChury #InżynieriaOprogramowania
