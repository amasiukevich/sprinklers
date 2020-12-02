# Projekt "Tryskacze"

**Autorzy**: Anton Masiukevich, Konrad Lechowski

## Cel
Zaimplementować algorytm dokonujący optymalnego rozkładu tryskaczy na danym obszarze zamkniętym w przestrzeni dyskretnej. Tryskacz zapewnia pokrycie obszaru ‘kołowego’ o średnicy D i jego zasięg może być ograniczony przez ściany. Przedmiotem minimalizacji jest liczba tryskaczy


### Dane wejściowe
* wymiary planszy (width, height)
* średnica D
* minimalne pokrycie w % do zakończenia działania algorytmu
* liczność populacji w danym pokoleniu (mu)
* liczność produkowanego potomstwa
* prawdopodobieństwo mutacji

### Dane wyjściowe
* położenie tryskaczy
* uzyskany % pokrycia

### Założenia
* Tryskacze mogą być umieszczane tylko w punktach wewnętrznych obszaru.
* Plansza jest w kształcie prostokąta


### Idea rozwiązania
Algorytm na początku znajduje minimalną wartość n, przy której teoretycznie da się pokryć wymagany procent powierzchni ("naiwne założenie"). Przeszukujemy przestrzeń (**N**, **1.5N**), gdzie n jest liczbą tryskaczy. W tym celu w pętli (iterator **k**) schodząc od **1.5N** do **N** przeprowadzamy optymalizację dla każdego naturalnego **k**. Jeśli nam się udaje przekroczyć % pokrywanej powierzchni - zatem dekrementujemy **k**, zapisujemy **k**, oraz minimalny uzyskany procent pokrycia oraz zaczynamy od nowa optymalizację dla **k - 1**. W danym kroku optymalizacji, jeśli liczba pokoleń jest większa od 100, a jeszcze nie osiągnęliśmy sukcesu lub wartość fitnesu się nie poprawiała przez 60 pokoleń - zatrzymujemy algorytm i zwracamy ostatnie **k**, dla którego poszukiwanie zakończyło się sukcesem .


## Implementacja

Językiem programowania, który został użyty jest Python.
Implementacja części optymalizacyjnej algorytmu polegała na wykorzystaniu strategii ewolucyjnej (w danym przypadku najbardziej zbliżonej do **(mi + lambda)**). 

Podstawowe klasy:
* Population (plik population.py) (**autor: Anton Masiukevich**)
    + Implementacja podstawowych atrybutów algorytmu ewolucyjnego:
        - Selekcji (turniejowa, zarówno w doborze osobników do reprodukcji, jak i w wyborze osobników do następnego pokolenia)
        - Krzyżowania (krzyżowanie dwupunktowe)
        - Mutacji (przez permutację wartości genotypu jednego z wymiarów osobnika i dodania losowej wartości {-1, 1} do jednej z wartości drugiego wymiaru danego osobnika)
* Solution (plik possible_solution.py) (**autor: Anton Masiukevich**)
    + Jako osobnika przyjęliśmy rozmieszczenie **k** tryskaczy na płaszczyźnie
* Area (plik area.py) (**autor: Anton Masiukevich**)
    + Klasa do wyliczania funkcji celu dla danego rozwiązania

Dodatkowo:
* w pliku main.py istnieje funkcja do wizualizacji otrzymanej wartości za pomocą biblioteki _matplotlib_. (**autor: Anton Masiukevich**)

### Złożoność obliczeniowa
Zaproponowany przez nas algorytm ma złożoność obliczeniową O(nmin * 60 * lambda * k ** 3), gdzie k jest w przedziałach od (nmin, 2nmin)


### Uruchomienie
Program wyposażony jest w interfejs wiersza poleceń.
Przykład uruchomienia
```
python3 main.py -wd 20 -ht 20 -ra 3 -cov 50 -mu 100 -ld 40 -mtp 0.01
```
Znaczenie parametrów można znaleźć wprowadzając
```
python3 main.py --help
```

## Testowanie
Testowanie polega na przeprowadzeniu optymalizacji 25 razy dla każdego z przypadków:
* Prosty (plansza 3x3, promień 2)
* Złożony (plansza 20x20, promień 2, p-stwo mutacji 0.1)
* Złożony z mało prawdopodobną mutacją (plansza 20x20, promień 2, p-stwo mutacji 0.001)
W każdym z wypadków liczba osobników w danym pokoleniu wyniosła 70, liczba "nowo narodzonych" osobników - 20 i procent pokrycia - 75%. 
Powyższe testy zostały wygenerowane dla pokazania, że algorytm dość dobrze sobie radzi z trywialnym przypadkiem, natomiast eksploatuje w przypadku małego prawdopodobieństwa mutacji.

W poniższej modeli przedstawiono wyniki średniej wartości uzyskanej liczby tryskaczy oraz procentu od teoretycznego minimum (dla 25 uruchomień dla każdego z przypadków).
| Przypadek | Średnie najlepsze | % teoretycznego |
|-|-|-|
| Prosty | 1 | 100 |
| Złożony | 34.76 | 144.8 |
| Złożony mała mutacja | 35.6 | 148.3 | 

### Wnioski, spostrzeżenia

Podczas testowania algorytmu (wbrew zwykłego założenia o tym, że mutacja powinna być możliwie mało prawdopodobna), ustawiłem prawdopodobieństwo mutacji na 0.1 - tylko dla takich rzędów wielkości algorytm zaczął eksplorować.

