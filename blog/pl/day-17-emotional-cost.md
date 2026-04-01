---
day: 17
title: "Ukryty emocjonalny ciężar prowadzenia zespołu przez transformację AI"
pillar: Trenches
language: pl
image: ../../images/day-17.jpg
image_unsplash_query: "engineering team pressure work stress"
---

# Ukryty emocjonalny ciężar prowadzenia zespołu przez transformację AI

Posty na blogach o transformacji AI w zespołach inżynierskich skupiają się na architekturze, narzędziach i procesie. Mają wiele do powiedzenia o tym, jak oceniać modele, jak strukturować pipeline'y RAG, jak mierzyć jakość AI. Mają bardzo mało do powiedzenia o tym, jak wygląda prowadzenie 11 ludzi przez zmianę, która wpływa na ich zawodową tożsamość.

To jest post, którego pisania się wahałem, bo wymaga powiedzenia na głos rzeczy, które nie pasują schludnie do dyskusji technicznej. Ale po 18 miesiącach tego myślę, że te rzeczy trzeba powiedzieć.

## Lęk przed Utratą Kompetencji

Inżynierowie zarabiają na swój staż. Lata rozwiązywania trudnych problemów, budowania niezawodnych systemów, rozwijania rozpoznawania wzorców, które pozwala im szybko identyfikować właściwe rozwiązanie. Ten staż to zawodowa tożsamość, nie tylko tytuł stanowiska.

Transformacja AI zakłóca tę tożsamość w konkretny sposób: tworzy sytuacje, w których seniorzy inżynierowie znajdują się w prawdziwych stanach początkujących. Uczą się LLM API. Pracują przez nieznane architektury retrieval. Czytają artykuły, żeby zrozumieć, dlaczego podejście retrieval zawiodło. Są wyprzedzani w tych tematach przez inżynierów pięć lat młodszych, którzy wcześniej trafili w prace ML.

Widziałem wykwalifikowanych, doświadczonych programistów opisujących to językiem, którego normalnie nie słyszę: "Czuję się głupio." "Nie wiem, co robię." "Cały czas próbuję różnych rzeczy i nie wiem, dlaczego działają albo nie."

Zarządzanie tym nie polega na wyjaśnianiu, że nie są głupi. Polega na tworzeniu środowisk, w których bycie w stanie początkującego jest strukturalnie oczekiwane i wspierane, a nie niejawnie zawstydzające.

Robiliśmy to przez wyraźną normalizację ("Też nie wiem, i oto co robię, żeby się dowiedzieć"), przez uczenie się w parach (parowanie senior-na-senior w różnych obszarach wiedzy) i przez świętowanie zachowań uczenia się, a nie tylko zachowań wysyłania, w retrospektywach zespołu.

To nie jest rozwiązany problem. Ale nazywanie tego jest krokiem pierwszym.

## Permanentne Poczucie Bycia w Tyle

Krajobraz narzędzi AI zmienia się szybciej niż jakikolwiek poprzedni shift technologiczny, przez który przeszłem. Nowe modele wydawane są co miesiąc ze znaczącymi różnicami zdolności. Nowe frameworki pojawiają się i osiągają dojrzałość produkcyjną szybciej, niż zespoły deweloperskie mogą je ocenić. Najlepsze praktyki zmieniają się na podstawie zmian zachowania modeli.

W tym środowisku nawet deweloperzy, którzy naprawdę się uczą i rosną, często czują, że zostają w tyle. Czytają o nowej zdolności, zaczynają ją integrować, a zanim się z nią zapoznają, pojawia się coś nowszego. Tworzy to konkretny rodzaj niepokoju, który różni się od "jeszcze nie znam tej technologii" — to "nigdy w pełni nie poznam tej technologii, bo ciągle się zmienia."

Uznałem, że naprawdę pomocne jest bezpośrednie nazwanie tego mojemu zespołowi: poczucie bycia w tyle jest normalne i nie odzwierciedla ich tempa uczenia się. Wszyscy razem uczymy się w krajobrazie, który porusza się szybciej niż ktokolwiek z nas może w pełni śledzić. Celem nie jest opanowanie obecnego stanu — to budowanie nawyków uczenia się i podstawowych konceptów, które pozwalają nam adaptować się, gdy krajobraz nadal się zmienia.

Łatwiej to powiedzieć niż zinternalizować. Ale mówienie tego, wielokrotnie i wprost, pomogło.

## Zespół Nie Jest Jednorodny

Jedna rzecz, która mnie zaskoczyła przy prowadzeniu przez tę transformację: wariancja odpowiedzi mojego zespołu na transformację AI jest ogromna.

Niektórzy inżynierowie przyszli do tego okresu z energią. Śledzili na własną rękę rozwój AI, mieli osobiste projekty używające LLM i czekali na pozwolenie, żeby wprowadzić te narzędzia do swojej pracy. Dla nich transformacja jest ekscytująca.

Inni przyszli sceptycznie — zastanawiając się, czy to kolejny cykl hype'u technologicznego, obserwując uważnie, czy praca AI produkuje realną wartość i utrzymując profesjonalny dystans do nowych narzędzi, dopóki nie są przekonani, że warto w nie inwestować.

Obie odpowiedzi są rozsądne. Obie wymagają innego zarządzania.

Energetyczni inżynierowie potrzebują kanalizowania — ich entuzjazm jest cenny, ale może tworzyć rozrost zakresu, i muszą się nauczyć dyscypliny produkcyjnego AI, tak samo jak uczą się jego możliwości. Sceptyczni inżynierowie potrzebują dowodów, a nie entuzjazmu — pokazywania im realnej wartości produkcyjnej, konkretnych metryk i uczciwego przyznawania się do ograniczeń.

Najgorsza rzecz, którą lider może zrobić, to założyć, że cały zespół jest w tym samym miejscu w transformacji. Większość tarcia, które widziałem w transformacji AI, pochodzi z traktowania zróżnicowanego zestawu odpowiedzi jako jednolitej, zarządzalnej reakcji grupowej.

## Cienka Linia Między Krzywą Uczenia się a Wypaleniem

Ciągłe uczenie się jest wymagające. Kiedy oczekiwaniem jest uczenie się nowych narzędzi, nowych architektur i nowych konceptów, jednocześnie wysyłając funkcje produkcyjne i utrzymując istniejące systemy — to znaczące obciążenie poznawcze i emocjonalne.

Linia między produktywną krzywą uczenia się a niezrównoważonym wypaleniem jest cieńsza, niż większość managerów inżynierskich przyznaje. Sygnały, na które zwracam uwagę: malejące zaangażowanie w code review, zmniejszony wkład w dyskusje techniczne, inżynierowie, którzy wcześniej byli ciekawi, milkną.

Kiedy widzę te sygnały, rozmowa nie jest "czy nadążasz z AI?" To jest "co sprawiłoby, że Twoja praca czuła się teraz bardziej zrównoważona?" Czasem odpowiedź to chroniony czas na uczenie się bez presji dostarczenia. Czasem tymczasowe zmniejszenie zakresu. Czasem po prostu przyznanie, że tempo jest trudne i nie są w tym sami.

Nie mam tego idealnie rozgryzioniętego. Mam zaangażowanie do prowadzenia wyraźnych, bieżących rozmów o tym — zamiast traktowania tego jako problemu, który techniczne rozwiązania ostatecznie rozwiążą.

## Zadanie Domowe Lidera

Jeśli prowadzisz zespół, który jest w jakiejś wersji tej transformacji, oto co sugerowałbym:

**Wyraźnie nazwij emocjonalne wymiary.** Stwórz przestrzeń dla inżynierów do mówienia o tym, co jest trudne poza wyzwaniami technicznymi.

**Chroń czas na uczenie się niezwiązane z dostarczaniem.** Uczenie się pod ciągłą presją dostarczania jest mniej efektywne i bardziej wyczerpujące niż uczenie się z pewną chronioną przestrzenią.

**Doceniaj zachowania wzrostu, nie tylko zachowania wysyłania.** "Nauczyłeś się nowego narzędzia w tym sprincie i udokumentowałeś co odkryłeś" jest warte docenienia, nawet jeśli nic nie zostało wysłane.

**Zarządzaj jednostkami, a nie zespołem jako jedną całością.** Wariancja w tym, gdzie ludzie są w tej transformacji, jest realna i wymaga indywidualnych podejść.

**Bądź szczery w kwestii tego, czego nie wiesz.** Twój zespół obserwuje, czy modelujesz mentalność uczenia się, której od nich oczekujesz. "Jeszcze nie wiem, i oto jak to odkryję" jest bardziej użytecznym sygnałem niż fałszywa pewność.

To jest naprawdę trudne. I warte tej trudności.
