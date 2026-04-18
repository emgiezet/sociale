---
day: 12
title_pl: "Miałem wkład w projekt z 18 milionami instalacji. Oto czego open source nauczył mnie o kodzie produkcyjnym."
pillar: Builder
format: Open source
scheduled_date: 2026-04-07
posting_time: "07:30 CET"
hashtags: ["#OpenSource", "#InżynieriaSoftware", "#PHP", "#Symfony"]
image: ../images/day-12.jpg
cta: "Obserwuj, jeśli wierzysz w open source"
blog_url: "https://mmx3.pl/blog/day-12-open-source"
---

Miałem wkład w projekt z 18 milionami instalacji. Nikt nie zna mojego imienia. To jest w porządku.

SonataAdminBundle to framework administracyjny open-source dla aplikacji Symfony/PHP. Wnosiłem do niego wkład przez lata. Ponad 18 milionów instalacji na Packagist.

Większość moich wkładów nigdy nie pojawi się w niczyim wystąpieniu konferencyjnym. Część to drobne poprawki błędów. Część to doprecyzowania dokumentacji. Część to ulepszenia API, które wymagały godzin przemyśleń i pięciu linii do zaimplementowania.

Oto czego praca przy dużym projekcie OSS nauczyła mnie o oprogramowaniu na skalę:

→ Wsteczna kompatybilność zmienia sposób myślenia. Kiedy 18 milionów ludzi może polegać na Twoim kodzie, nie możesz refaktoryzować tylko dlatego, że refaktoryzacja jest elegancka. Każde publiczne API to obietnica.
→ Code review w tej skali to inna dyscyplina. Nauczyłem się oceniać PR w izolacji: czy rozwiązuje podany problem? Czy wprowadza edge case'y? Czy jest spójny z istniejącym projektem API?
→ Dokumentacja to kod. Nieudokumentowana funkcja dla większości użytkowników nie istnieje. Praca nad czytelnym oprogramowaniem, przez dokumenty, przykłady, komunikaty błędów, nazewnictwo, to praca inżynierska. Nie myśl doklejona na końcu.
→ Społeczność to produkt. Zdrowe społeczności się kumulują.

Przynoszę to wszystko do swojej pracy w Insly — szczególnie dyscyplinę wstecznej kompatybilności. Kiedy 150 000 dokumentów miesięcznie polega na mojej platformie, każda zmiana API to problem wstecznej kompatybilności.

**Najlepsza edukacja inżynierska, za którą nigdy nie zapłaciłem, to wkład w open source.**

Za co cenisz projekty OSS? Co ukształtowało Twoje myślenie o oprogramowaniu?

Pełny artykuł na blogu: https://mmx3.pl/blog/day-12-open-source

#OpenSource #InżynieriaSoftware #PHP #Symfony
