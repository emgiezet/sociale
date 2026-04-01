---
day: 6
title_pl: "150 000 dokumentów miesięcznie. 1 integracja Microsoft SSO. 0 przestojów podczas migracji."
pillar: Builder
format: Technical story
scheduled_date: 2026-03-28
posting_time: "08:00 CET"
hashtags: ["#InżynieriaOprogramowania", "#MicrosoftSSO", "#EnterpriseEngineering", "#LiderzyTechniczni", "#InsurTech"]
image: ../images/day-06.jpg
cta: "Jakie są Twoje doświadczenia z dużymi migracjami auth? Napisz w komentarzu."
blog_url: "https://mmx3.pl/blog/day-06a-sso-migration"
---

150 000 dokumentów miesięcznie. 1 integracja Microsoft SSO. 0 przestojów podczas migracji.

Ludzie zawsze pytają o część techniczną. Część techniczna była łatwą częścią.

Oto historia migracji Microsoft SSO w Insly — i czego naprawdę mnie nauczyła o inżynierii w skali.

**Kontekst:**
Insly to oprogramowanie do zarządzania ubezpieczeniami używane przez brokerów w całej Europie. Wielu klientów enterprise korzysta z Microsoft 365. Żądanie: pozwólcie ich zespołom logować się swoimi poświadczeniami Microsoft zamiast utrzymywać oddzielne hasło do Insly.

Prosta funkcja. Prawda?

**Co sprawiło że było trudne:**
→ 150 000+ aktywnych użytkowników, z różnymi typami kont i różnymi przepływami auth
→ Klienci enterprise z zespołami IT security, które musiały zatwierdzić każdą zmianę
→ Niektórzy klienci na starszych konfiguracjach tenant Microsoft z różnym zachowaniem OAuth
→ Architektura multi-tenant, gdzie każdy broker działa w izolacji

**Podejście, które utrzymało nas na 0 przestojów:**
→ Feature flag dla całej migracji — stary auth i nowy auth działające jednocześnie
→ Rollout per-klient: włączałem SSO dla jednej organizacji naraz, z ich zespołem IT na telefonie
→ Fallback zawsze dostępny: jeśli SSO zawiedzie, stara ścieżka auth nadal działa
→ 30-dniowy okres monitorowania po migracji każdej organizacji przed usunięciem fallbacku

Rzecz, którą powiedziałbym każdemu inżynierowi planującemu migrację auth na dużą skalę: **Twoja migracja to nie problem techniczny. To problem koordynacji.**

Spędziłem 20% czasu projektu na kodzie integracji. 80% spędziłem na koordynacji: komunikacja z klientem, sekwencjonowanie rollout, testowanie fallbacku, odkrywanie edge case'ów.

Inżynieria była solidna. Koordynacja sprawiła że była bezpieczna.

Jakie są Twoje doświadczenia z dużymi migracjami auth? Chciałbym usłyszeć, jak inni radzą sobie z nie-techniczną złożonością.

Pełny artykuł na blogu: https://mmx3.pl/blog/day-06a-sso-migration

#InżynieriaOprogramowania #MicrosoftSSO #EnterpriseEngineering #LiderzyTechniczni #InsurTech
